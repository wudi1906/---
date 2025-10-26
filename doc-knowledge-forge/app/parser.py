"""
文档解析器
"""
import re
from pathlib import Path
from typing import Optional, Dict, Any, List
import fitz  # pymupdf
from docx import Document as DocxDocument
from markdownify import markdownify


class DocumentParser:
    """文档解析器"""
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> Dict[str, Any]:
        """从PDF提取文本"""
        result = {
            "text": "",
            "title": None,
            "page_count": 0,
            "metadata": {}
        }
        
        try:
            doc = fitz.open(file_path)
            result["page_count"] = len(doc)
            
            # 提取元数据
            result["metadata"] = doc.metadata
            result["title"] = doc.metadata.get("title", "")
            
            # 提取文本
            text_parts = []
            for page in doc:
                text_parts.append(page.get_text())
            
            result["text"] = "\n\n".join(text_parts)
            doc.close()
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> Dict[str, Any]:
        """从DOCX提取文本"""
        result = {
            "text": "",
            "title": None,
            "page_count": 0,
            "metadata": {}
        }
        
        try:
            doc = DocxDocument(file_path)
            
            # 提取段落
            paragraphs = []
            for para in doc.paragraphs:
                if para.text.strip():
                    paragraphs.append(para.text)
            
            result["text"] = "\n\n".join(paragraphs)
            
            # 尝试从第一段提取标题
            if paragraphs:
                result["title"] = paragraphs[0][:100]
            
            # 估算页数（假设每页500字）
            result["page_count"] = max(1, len(result["text"]) // 500)
            
            # 提取元数据
            core_props = doc.core_properties
            result["metadata"] = {
                "title": core_props.title or "",
                "author": core_props.author or "",
                "subject": core_props.subject or "",
            }
            
            if core_props.title:
                result["title"] = core_props.title
                
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    @staticmethod
    def extract_text_from_txt(file_path: str) -> Dict[str, Any]:
        """从TXT提取文本"""
        result = {
            "text": "",
            "title": None,
            "page_count": 1,
            "metadata": {}
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            result["text"] = text
            
            # 从第一行提取标题
            lines = text.split('\n')
            if lines:
                result["title"] = lines[0][:100]
            
            result["page_count"] = max(1, len(text) // 500)
            
        except UnicodeDecodeError:
            # 尝试其他编码
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    text = f.read()
                result["text"] = text
                lines = text.split('\n')
                if lines:
                    result["title"] = lines[0][:100]
            except Exception as e:
                result["error"] = str(e)
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    @staticmethod
    def text_to_markdown(text: str, title: Optional[str] = None) -> str:
        """将文本转换为Markdown格式"""
        lines = []
        
        # 添加标题
        if title:
            lines.append(f"# {title}\n")
        
        # 分段处理
        paragraphs = text.split('\n\n')
        for para in paragraphs:
            para = para.strip()
            if para:
                # 检测是否为列表项
                if re.match(r'^[\d\-\*•]\s+', para):
                    lines.append(para)
                else:
                    lines.append(para + "\n")
        
        return "\n".join(lines)
    
    @staticmethod
    def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
        """提取关键词（简单实现）"""
        # 移除标点
        clean_text = re.sub(r'[^\w\s]', ' ', text.lower())
        
        # 分词
        words = clean_text.split()
        
        # 过滤停用词和短词
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                      'of', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
                      'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may',
                      'might', 'can', 'this', 'that', 'these', 'those', '的', '了', '在',
                      '是', '和', '与', '或', '等', '及'}
        
        words = [w for w in words if len(w) > 2 and w not in stop_words]
        
        # 统计词频
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # 排序并返回前N个
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        keywords = [word for word, freq in sorted_words[:max_keywords]]
        
        return keywords


def parse_document(file_path: str, file_type: str) -> Dict[str, Any]:
    """
    解析文档并提取内容
    
    Args:
        file_path: 文件路径
        file_type: 文件类型 (.pdf, .docx, .txt)
    
    Returns:
        包含文本、标题、标签等信息的字典
    """
    if file_type.lower() == '.pdf':
        return DocumentParser.extract_text_from_pdf(file_path)
    elif file_type.lower() in ['.docx', '.doc']:
        return DocumentParser.extract_text_from_docx(file_path)
    elif file_type.lower() in ['.txt', '.md']:
        return DocumentParser.extract_text_from_txt(file_path)
    else:
        return {"error": f"Unsupported file type: {file_type}"}

