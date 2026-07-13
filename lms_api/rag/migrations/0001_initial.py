import rag.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="RagDocument",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("original_name", models.CharField(max_length=255)),
                ("file", models.FileField(upload_to=rag.models.rag_document_upload_to)),
                ("file_type", models.CharField(max_length=20)),
                ("mime_type", models.CharField(blank=True, max_length=120)),
                ("size_bytes", models.PositiveBigIntegerField(default=0)),
                ("checksum", models.CharField(blank=True, db_index=True, max_length=64)),
                ("status", models.CharField(choices=[("pending", "Pending"), ("processing", "Processing"), ("ready", "Ready"), ("failed", "Failed")], db_index=True, default="pending", max_length=20)),
                ("chunk_count", models.PositiveIntegerField(default=0)),
                ("error_message", models.TextField(blank=True)),
                ("processed_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="rag_documents", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="RagConversation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(default="New chat", max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("documents", models.ManyToManyField(blank=True, related_name="rag_conversations", to="rag.ragdocument")),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="rag_conversations", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-updated_at"]},
        ),
        migrations.CreateModel(
            name="RagChunk",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("vector_id", models.CharField(max_length=100, unique=True)),
                ("chunk_index", models.PositiveIntegerField()),
                ("content", models.TextField()),
                ("page_number", models.PositiveIntegerField(blank=True, null=True)),
                ("section_title", models.CharField(blank=True, max_length=255)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("document", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="chunks", to="rag.ragdocument")),
            ],
            options={"ordering": ["chunk_index"]},
        ),
        migrations.CreateModel(
            name="RagMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("user", "User"), ("assistant", "Assistant")], max_length=20)),
                ("content", models.TextField()),
                ("citations", models.JSONField(blank=True, default=list)),
                ("model_name", models.CharField(blank=True, max_length=100)),
                ("response_time_ms", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("conversation", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="messages", to="rag.ragconversation")),
            ],
            options={"ordering": ["created_at", "id"]},
        ),
        migrations.AddIndex(
            model_name="ragdocument",
            index=models.Index(fields=["owner", "status"], name="rag_doc_owner_status_idx"),
        ),
        migrations.AddIndex(
            model_name="ragconversation",
            index=models.Index(fields=["owner", "updated_at"], name="rag_conv_owner_updated_idx"),
        ),
        migrations.AddConstraint(
            model_name="ragchunk",
            constraint=models.UniqueConstraint(fields=("document", "chunk_index"), name="rag_unique_document_chunk"),
        ),
        migrations.AddIndex(
            model_name="ragchunk",
            index=models.Index(fields=["document", "chunk_index"], name="rag_chunk_doc_index_idx"),
        ),
        migrations.AddIndex(
            model_name="ragmessage",
            index=models.Index(fields=["conversation", "created_at"], name="rag_msg_conv_created_idx"),
        ),
    ]
