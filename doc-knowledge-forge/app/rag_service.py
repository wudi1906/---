"""RAG 服务：负责分块、嵌入、向量检索"""
from __future__ import annotations

import re
from functools import lru_cache
from typing import List, Sequence

import numpy as np
from sqlalchemy.orm import Session

from app.models import Document, DocumentChunk, SearchResult, DocumentChunkResponse
from app.settings import settings

try:  # 可选 FAISS，加速相似度检索
    import faiss  # type: ignore

    FAISS_AVAILABLE = True
except ImportError:  # pragma: no cover - 环境未安装时走回退策略
    faiss = None
    FAISS_AVAILABLE = False


@lru_cache(maxsize=1)
def _load_embedding_model(model_name: str):
    """延迟加载 SentenceTransformer 模型"""
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(model_name)


class RagService:
    """封装文档分块、嵌入与检索逻辑"""

    def __init__(self) -> None:
        self.model_name = settings.EMBEDDING_MODEL_NAME
        self.chunk_size = settings.RAG_CHUNK_SIZE
        self.chunk_overlap = settings.RAG_CHUNK_OVERLAP

    # ---------- 分块 ----------
    def chunk_text(self, text: str) -> List[str]:
        """按照设定长度切分文本，包含重叠提高召回"""
        normalized = re.sub(r"\s+", " ", text or "").strip()
        if not normalized:
            return []

        chunks: List[str] = []
        length = len(normalized)
        start = 0
        while start < length:
            end = min(length, start + self.chunk_size)
            chunk = normalized[start:end]

            # 避免截断句子，尝试向后补充到最近的句号/换行
            if end < length:
                extra = self._find_sentence_boundary(normalized, end, window=40)
                if extra:
                    end = min(length, end + extra)
                    chunk = normalized[start:end]

            chunks.append(chunk.strip())

            if end >= length:
                break
            start = max(0, end - self.chunk_overlap)

        return [c for c in chunks if c]

    @staticmethod
    def _find_sentence_boundary(text: str, start: int, window: int = 40) -> int:
        """在窗口范围内向后搜索句子边界"""
        boundary_regex = re.compile(r"[。！？!?\.]")
        fragment = text[start : min(len(text), start + window)]
        match = boundary_regex.search(fragment)
        if not match:
            return 0
        return match.end()

    # ---------- 嵌入 ----------
    def _embed(self, texts: Sequence[str]) -> np.ndarray:
        """获取文本嵌入向量 (float32)"""
        if not texts:
            return np.empty((0, 0), dtype="float32")

        model = _load_embedding_model(self.model_name)
        vectors = model.encode(
            list(texts),
            convert_to_numpy=True,
            normalize_embeddings=False,
            show_progress_bar=False,
        )
        if vectors.dtype != np.float32:
            vectors = vectors.astype("float32")
        return vectors

    # ---------- 索引 ----------
    def index_document(self, db: Session, document: Document, text: str) -> int:
        """为文档创建分块与向量索引"""
        # 清理旧分块
        db.query(DocumentChunk).filter(DocumentChunk.document_id == document.id).delete()

        chunks = self.chunk_text(text)
        if not chunks:
            db.commit()
            return 0

        vectors = self._embed(chunks)
        if vectors.size == 0:
            db.commit()
            return 0

        chunk_entities: List[DocumentChunk] = []
        for index, chunk_text in enumerate(chunks):
            vector = vectors[index]
            chunk_entities.append(
                DocumentChunk(
                    document_id=document.id,
                    chunk_index=index,
                    content=chunk_text,
                    token_count=self._estimate_tokens(chunk_text),
                    embedding=vector.tobytes(),
                    embedding_dim=vector.shape[0],
                    embedding_model=self.model_name,
                )
            )

        db.add_all(chunk_entities)
        db.commit()
        return len(chunk_entities)

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        if not text:
            return 0
        # 近似：英文按空格、中文按字符
        return max(len(text.split()), len(text))

    # ---------- 检索 ----------
    def search(self, db: Session, query: str, top_k: int) -> List[SearchResult]:
        chunks = (
            db.query(DocumentChunk)
            .join(Document, DocumentChunk.document_id == Document.id)
            .all()
        )
        if not chunks:
            return []

        embeddings: List[np.ndarray] = []
        valid_chunks: List[DocumentChunk] = []

        for chunk in chunks:
            if not chunk.embedding:
                continue
            vector = np.frombuffer(chunk.embedding, dtype=np.float32)
            if vector.size == 0:
                continue
            embeddings.append(vector)
            valid_chunks.append(chunk)

        if not embeddings:
            return []

        matrix = np.vstack(embeddings)
        matrix = self._normalize(matrix)

        query_vec = self._embed([query])
        if query_vec.size == 0:
            return []
        query_vec = self._normalize(query_vec)[0]

        scores, indices = self._similarity_search(matrix, query_vec, min(top_k, matrix.shape[0]))

        results: List[SearchResult] = []
        highlights = self._extract_keywords(query)
        for score, idx in zip(scores, indices):
            if idx < 0 or idx >= len(valid_chunks):
                continue
            chunk = valid_chunks[idx]
            doc = chunk.document
            snippet = self._build_snippet(chunk.content, query)
            results.append(
                SearchResult(
                    document_id=doc.id,
                    chunk_id=chunk.id,
                    chunk_index=chunk.chunk_index,
                    filename=doc.original_name,
                    title=doc.title or doc.original_name,
                    snippet=snippet,
                    highlights=highlights,
                    relevance_score=float(score),
                )
            )

        return results

    @staticmethod
    def _normalize(vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1e-8
        return vectors / norms

    def _similarity_search(self, matrix: np.ndarray, query_vec: np.ndarray, top_k: int):
        if FAISS_AVAILABLE:
            index = faiss.IndexFlatIP(matrix.shape[1])
            index.add(matrix)
            scores, idx = index.search(query_vec.reshape(1, -1), top_k)
            return scores[0], idx[0]

        scores = matrix @ query_vec
        ranked = np.argsort(scores)[::-1][:top_k]
        return scores[ranked], ranked

    @staticmethod
    def _build_snippet(content: str, query: str, window: int = 180) -> str:
        if not content:
            return ""

        lowered = content.lower()
        target = query.lower().strip()
        idx = lowered.find(target)
        if idx == -1:
            snippet = content[:window]
            return snippet + ("..." if len(content) > window else "")

        start = max(0, idx - window // 2)
        end = min(len(content), idx + len(target) + window // 2)
        snippet = content[start:end]
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."
        return snippet

    @staticmethod
    def _extract_keywords(query: str) -> List[str]:
        keywords = re.split(r"[\s,;，。]+", query.strip())
        return [kw for kw in keywords if len(kw) > 1]

    # ---------- 分块读取 ----------
    def get_chunk(self, db: Session, chunk_id: int) -> DocumentChunkResponse | None:
        chunk = db.query(DocumentChunk).filter(DocumentChunk.id == chunk_id).first()
        if not chunk:
            return None
        return DocumentChunkResponse.from_orm(chunk)


rag_service = RagService()


