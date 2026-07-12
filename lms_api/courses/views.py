"""Các API công khai và API học nội dung khóa học."""

from django.db.models import Prefetch
from rest_framework import (
    filters,
    generics,
    permissions,
    viewsets,
)
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from enrollments.models import Enrollment

from .models import Course, Lesson, Section
from .serializers import (
    CourseCurriculumSerializer,
    CourseDetailSerializer,
    CourseSerializer,
    LessonSerializer,
)


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Cung cấp danh sách và chi tiết khóa học đã xuất bản.

    GET /api/courses/
    GET /api/courses/{id}/
    """

    queryset = Course.objects.filter(is_published=True).select_related("teacher")

    permission_classes = [AllowAny]

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = [
        "title",
        "subtitle",
        "description",
    ]
    ordering_fields = [
        "created_at",
        "price",
        "title",
    ]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        """Chọn serializer theo loại thao tác."""

        if self.action == "retrieve":
            return CourseDetailSerializer

        return CourseSerializer

    def get_serializer_context(self):
        """Thêm request vào context của serializer."""

        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_queryset(self):
        """Lọc khóa học theo danh mục và trình độ."""

        queryset = super().get_queryset()

        category = self.request.query_params.get(
            "category",
            None,
        )
        if category:
            queryset = queryset.filter(category=category)

        level = self.request.query_params.get(
            "level",
            None,
        )
        if level:
            queryset = queryset.filter(level=level)

        return queryset


class CourseCurriculumAPIView(generics.RetrieveAPIView):
    """
    Trả về chương trình học gồm các chương và bài học.

    GET /api/courses/{id}/curriculum/
    """

    queryset = Course.objects.filter(is_published=True).prefetch_related(
        Prefetch(
            "sections",
            queryset=Section.objects.order_by(
                "sort_order",
                "id",
            ),
        ),
        Prefetch(
            "sections__lessons",
            queryset=Lesson.objects.order_by(
                "sort_order",
                "id",
            ),
        ),
    )

    serializer_class = CourseCurriculumSerializer
    permission_classes = [AllowAny]
    lookup_field = "pk"

    def get_serializer_context(self):
        """Thêm request để xác định trạng thái hoàn thành."""

        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class LessonDetailAPIView(generics.RetrieveAPIView):
    """
    Trả về chi tiết một bài học.

    Người dùng phải đăng nhập và đã đăng ký khóa học.

    GET /api/lessons/{id}/
    """

    queryset = Lesson.objects.select_related(
        "section",
        "section__course",
    )
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def get_serializer_context(self):
        """Thêm request để xây dựng URL tài liệu."""

        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_object(self):
        """Kiểm tra quyền truy cập bài học."""

        lesson = super().get_object()
        course = lesson.section.course

        is_enrolled = Enrollment.objects.filter(
            student=self.request.user,
            course=course,
        ).exists()

        if not is_enrolled:
            raise PermissionDenied(
                detail=("You must enroll in this course first " "to access lessons.")
            )

        return lesson


class CourseCategoriesListAPIView(APIView):
    """
    Trả về danh sách danh mục của các khóa học đã xuất bản.

    GET /api/courses/categories/
    """

    permission_classes = [AllowAny]

    def get(self, request):
        """Lấy danh sách danh mục duy nhất."""

        categories = (
            Course.objects.filter(
                is_published=True,
                category__isnull=False,
            )
            .exclude(category="")
            .values_list("category", flat=True)
            .distinct()
            .order_by("category")
        )

        return Response(
            {
                "categories": list(categories),
            }
        )
