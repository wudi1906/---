"""Doc Knowledge Forge RAG 流程测试"""
from pathlib import Path

import numpy as np
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import rag_service
from app.main import app
from app.models import Base, get_db
from app.settings import settings


@pytest.fixture(scope="session")
def db_path(tmp_path_factory):
    return tmp_path_factory.mktemp("forge") / "tests.db"


@pytest.fixture(scope="session", autouse=True)
def _configure_settings(db_path):
    # 使用隔离的数据库与目录
    settings.DATABASE_URL = f"sqlite:///{db_path}"
    settings.UPLOAD_DIR = Path(db_path).parent / "uploads"
    settings.OUTPUT_DIR = Path(db_path).parent / "outputs"
    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@pytest.fixture()
def db_session(db_path):
    engine = create_engine(
        f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestingSessionLocal
    app.dependency_overrides.clear()
    engine.dispose()


@pytest.fixture(autouse=True)
def mock_embeddings(monkeypatch):
    def fake_embed(self, texts):
        if not texts:
            return np.empty((0, 4), dtype=np.float32)
        base_vector = np.array([0.1, 0.2, 0.3, 0.4], dtype=np.float32)
        return np.vstack([base_vector + idx for idx, _ in enumerate(texts)])

    monkeypatch.setattr(
        rag_service.rag_service,
        "_embed",
        fake_embed.__get__(rag_service.rag_service, type(rag_service.rag_service)),
    )
    monkeypatch.setattr(rag_service, "FAISS_AVAILABLE", False, raising=False)


@pytest.fixture()
def client(db_session):
    return TestClient(app)


def test_chunk_text_overlap():
    text = "这是一个测试文档，用于验证分块逻辑。" * 30
    service = rag_service.rag_service
    original_size, original_overlap = service.chunk_size, service.chunk_overlap
    service.chunk_size = 80
    service.chunk_overlap = 20
    try:
        chunks = service.chunk_text(text)
        assert len(chunks) >= 2
        assert all(len(chunk) > 0 for chunk in chunks)
    finally:
        service.chunk_size = original_size
        service.chunk_overlap = original_overlap


def test_upload_and_search_flow(client):
    payload = """Analytics drives better decisions.\n\nKey metrics: revenue, churn, engagement."""
    files = [("files", ("analytics.txt", payload.encode("utf-8"), "text/plain"))]

    resp = client.post("/api/docs/upload", files=files)
    assert resp.status_code == 200
    data = resp.json()
    assert data["uploaded"] == 1
    assert data["details"][0]["chunked"] > 0
    assert data["details"][0]["status"] in {"success", "partial"}

    search_resp = client.get("/api/search", params={"q": "analytics", "top_k": 5})
    assert search_resp.status_code == 200
    search_results = search_resp.json()
    assert len(search_results) >= 1
    hit = search_results[0]
    assert "snippet" in hit and "analytics".lower() in hit["snippet"].lower()

    chunk_id = hit["chunk_id"]
    chunk_resp = client.get(f"/api/chunks/{chunk_id}")
    assert chunk_resp.status_code == 200
    chunk_data = chunk_resp.json()
    assert "chunk" in chunk_data
    assert "Analytics" in chunk_data["chunk"]["content"]

