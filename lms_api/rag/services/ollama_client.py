from functools import lru_cache

from ollama import Client

from .config import rag_setting
from .exceptions import RagServiceUnavailable


class OllamaService:
    def __init__(self):
        self.base_url = rag_setting(
            "RAG_OLLAMA_BASE_URL",
            "http://127.0.0.1:11434",
        )
        self.embed_model = rag_setting("RAG_EMBED_MODEL", "bge-m3:latest")
        self.llm_model = rag_setting("RAG_LLM_MODEL", "qwen2.5:3b")
        timeout = float(rag_setting("RAG_OLLAMA_TIMEOUT", 180))
        self.client = Client(host=self.base_url, timeout=timeout)

    @staticmethod
    def _read(response, key, default=None):
        if isinstance(response, dict):
            return response.get(key, default)
        return getattr(response, key, default)

    def embed(self, texts):
        if not texts:
            return []
        try:
            response = self.client.embed(
                model=self.embed_model,
                input=texts,
            )
            embeddings = self._read(response, "embeddings")
            if not embeddings or len(embeddings) != len(texts):
                raise RagServiceUnavailable(
                    "Ollama không trả về đủ embedding cho tài liệu."
                )
            return embeddings
        except RagServiceUnavailable:
            raise
        except Exception as exc:
            raise RagServiceUnavailable(
                "Không kết nối được Ollama embedding. "
                "Hãy kiểm tra `ollama serve` và model bge-m3."
            ) from exc

    def chat(self, messages):
        try:
            response = self.client.chat(
                model=self.llm_model,
                messages=messages,
                options={"temperature": 0},
            )
            message = self._read(response, "message")
            if isinstance(message, dict):
                content = message.get("content")
            else:
                content = getattr(message, "content", None)
            if not content:
                raise RagServiceUnavailable(
                    "Ollama không trả về nội dung câu trả lời."
                )
            return content.strip()
        except RagServiceUnavailable:
            raise
        except Exception as exc:
            raise RagServiceUnavailable(
                "Không kết nối được Ollama LLM. "
                "Hãy kiểm tra server và model đã pull."
            ) from exc

    def health(self):
        try:
            return self.client.list()
        except Exception as exc:
            raise RagServiceUnavailable(
                f"Ollama không sẵn sàng tại {self.base_url}."
            ) from exc


@lru_cache(maxsize=1)
def get_ollama_service():
    return OllamaService()
