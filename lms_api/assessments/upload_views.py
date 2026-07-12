import os
import uuid

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import permissions, status
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.response import Response


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def upload_file_view(request):
    """Tải file lên thư mục media/uploads."""

    if "file" not in request.FILES:
        return Response(
            {"detail": "No file provided"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    file = request.FILES["file"]

    file_ext = os.path.splitext(file.name)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"

    upload_path = f"uploads/{unique_filename}"

    saved_path = default_storage.save(
        upload_path,
        ContentFile(file.read()),
    )

    file_url = f"/media/{saved_path}"

    return Response(
        {
            "url": file_url,
            "file_url": file_url,
            "attachment_url": file_url,
            "filename": file.name,
        },
        status=status.HTTP_201_CREATED,
    )
