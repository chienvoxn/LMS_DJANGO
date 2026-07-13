from django.core.management.base import BaseCommand, CommandError

from rag.models import RagDocument
from rag.services.indexing import index_document


class Command(BaseCommand):
    help = "Re-index một hoặc toàn bộ tài liệu RAG."

    def add_arguments(self, parser):
        parser.add_argument("--document-id", type=int)
        parser.add_argument("--owner-id", type=int)

    def handle(self, *args, **options):
        queryset = RagDocument.objects.all().order_by("id")
        if options["document_id"]:
            queryset = queryset.filter(id=options["document_id"])
        if options["owner_id"]:
            queryset = queryset.filter(owner_id=options["owner_id"])
        if not queryset.exists():
            raise CommandError("Không tìm thấy tài liệu phù hợp.")

        for document in queryset:
            self.stdout.write(f"Indexing #{document.id}: {document.name}")
            try:
                index_document(document)
                self.stdout.write(self.style.SUCCESS("  OK"))
            except Exception as exc:
                self.stdout.write(self.style.ERROR(f"  FAILED: {exc}"))
