import os
import uuid

from django.core.files.storage import default_storage
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def upload_file_view(request):
    """Upload a non-empty file to media/uploads."""

    uploaded_file = request.FILES.get("file")

    if uploaded_file is None:
        return Response(
            {"detail": "No file provided."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if uploaded_file.size == 0:
        return Response(
            {"detail": "The selected file is empty."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    upload_path = f"uploads/{unique_filename}"

    # Save the uploaded file directly instead of reading it into ContentFile.
    saved_path = default_storage.save(upload_path, uploaded_file)

    file_url = default_storage.url(saved_path)

    return Response(
        {
            "url": file_url,
            "file_url": file_url,
            "attachment_url": file_url,
            "filename": uploaded_file.name,
            "size": uploaded_file.size,
        },
        status=status.HTTP_201_CREATED,
    )
