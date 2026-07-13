class RagError(Exception):
    """Lỗi nghiệp vụ RAG có thể hiển thị cho client."""


class RagServiceUnavailable(RagError):
    """Ollama hoặc vector store không sẵn sàng."""


class DocumentParseError(RagError):
    """Không thể trích xuất nội dung tài liệu."""
