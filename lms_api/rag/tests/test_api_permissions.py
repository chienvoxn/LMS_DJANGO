from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase

from rag.models import RagDocument
from users.models import User


class RagPermissionTests(APITestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(
            email="a@example.com",
            password="password123",
        )
        self.user_b = User.objects.create_user(
            email="b@example.com",
            password="password123",
        )

    def test_anonymous_cannot_list_documents(self):
        response = self.client.get("/api/rag/documents/")
        self.assertIn(response.status_code, {401, 403})

    @patch("rag.views.index_document")
    def test_user_only_sees_own_documents(self, mocked_index):
        RagDocument.objects.create(
            owner=self.user_b,
            name="private",
            original_name="private.txt",
            file=SimpleUploadedFile("private.txt", b"secret"),
            file_type="txt",
            size_bytes=6,
        )
        self.client.force_authenticate(self.user_a)
        response = self.client.get("/api/rag/documents/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)
