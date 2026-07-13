from django.core.management.base import BaseCommand, CommandError

from rag.services.ollama_client import get_ollama_service
from rag.services.vector_store import get_vector_store


class Command(BaseCommand):
    help = "Kiểm tra kết nối Ollama và ChromaDB cho module RAG."

    def handle(self, *args, **options):
        try:
            get_vector_store().heartbeat()
            self.stdout.write(self.style.SUCCESS("ChromaDB: OK"))
        except Exception as exc:
            raise CommandError(f"ChromaDB: FAILED - {exc}") from exc

        try:
            get_ollama_service().health()
            self.stdout.write(self.style.SUCCESS("Ollama: OK"))
        except Exception as exc:
            raise CommandError(f"Ollama: FAILED - {exc}") from exc
