"""Các API quản lý khóa học dành cho giảng viên."""

from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from common.permissions import (
    IsOwnerOrReadOnly,
    IsTeacher,
)

from .models import Course, Lesson, Section
from .serializers import (
    CourseCreateUpdateSerializer,
    CourseDetailSerializer,
    CourseSerializer,
    LessonCreateUpdateSerializer,
    LessonSerializer,
    SectionCreateUpdateSerializer,
    SectionSerializer,
)


class TeacherCourseViewSet(viewsets.ModelViewSet):
    """
    Cho phép giảng viên quản lý khóa học của mình.

    GET    /api/teacher/courses/
    POST   /api/teacher/courses/
    GET    /api/teacher/courses/{id}/
    PUT    /api/teacher/courses/{id}/
    PATCH  /api/teacher/courses/{id}/
    DELETE /api/teacher/courses/{id}/
    """

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeacher,
        IsOwnerOrReadOnly,
    ]

    def get_queryset(self):
        """Chỉ trả về các khóa học của giảng viên hiện tại."""

        return (
            Course.objects.filter(teacher=self.request.user)
            .select_related("teacher")
            .order_by("-created_at", "id")
        )

    def get_serializer_class(self):
        """Chọn serializer theo thao tác hiện tại."""

        if self.action in [
            "create",
            "update",
            "partial_update",
        ]:
            return CourseCreateUpdateSerializer

        if self.action == "retrieve":
            return CourseDetailSerializer

        return CourseSerializer

    def perform_create(self, serializer):
        """Gán giảng viên hiện tại khi tạo khóa học."""

        serializer.save(teacher=self.request.user)


class TeacherSectionViewSet(viewsets.ModelViewSet):
    """
    Cho phép giảng viên quản lý chương trong khóa học.

    GET    /api/teacher/sections/
    POST   /api/teacher/sections/
    GET    /api/teacher/sections/{id}/
    PUT    /api/teacher/sections/{id}/
    PATCH  /api/teacher/sections/{id}/
    DELETE /api/teacher/sections/{id}/
    """

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeacher,
    ]

    # Curriculum editor needs every section of the selected course.
    pagination_class = None

    def get_queryset(self):
        """Chỉ trả về các chương thuộc khóa học của giảng viên hiện tại."""

        queryset = Section.objects.filter(
            course__teacher=self.request.user
        ).select_related(
            "course",
            "course__teacher",
        )

        course_id = self.request.query_params.get("course")

        if course_id:
            queryset = queryset.filter(course_id=course_id)

        return queryset.order_by(
            "course_id",
            "sort_order",
            "id",
        )

    def get_serializer_class(self):
        """Chọn serializer theo thao tác hiện tại."""

        if self.action in [
            "create",
            "update",
            "partial_update",
        ]:
            return SectionCreateUpdateSerializer

        return SectionSerializer

    def perform_create(self, serializer):
        """Kiểm tra quyền sở hữu khóa học khi tạo chương."""

        course = serializer.validated_data.get("course")

        if course.teacher != self.request.user:
            raise PermissionDenied("You can only create sections for your own courses.")

        serializer.save()

    def perform_update(self, serializer):
        """Kiểm tra quyền sở hữu khóa học khi sửa chương."""

        course = serializer.validated_data.get(
            "course",
            serializer.instance.course,
        )

        if course.teacher != self.request.user:
            raise PermissionDenied("You can only update sections for your own courses.")

        serializer.save()


class TeacherLessonViewSet(viewsets.ModelViewSet):
    """
    Cho phép giảng viên quản lý bài học.

    GET    /api/teacher/lessons/
    POST   /api/teacher/lessons/
    GET    /api/teacher/lessons/{id}/
    PUT    /api/teacher/lessons/{id}/
    PATCH  /api/teacher/lessons/{id}/
    DELETE /api/teacher/lessons/{id}/
    """

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeacher,
    ]

    # Curriculum editor needs every lesson of the selected course.
    pagination_class = None

    def get_queryset(self):
        """Chỉ trả về các bài học thuộc khóa học của giảng viên hiện tại."""

        queryset = Lesson.objects.filter(
            section__course__teacher=self.request.user
        ).select_related(
            "section",
            "section__course",
            "section__course__teacher",
        )

        course_id = self.request.query_params.get(
            "section__course"
        ) or self.request.query_params.get("course")
        section_id = self.request.query_params.get("section")

        if course_id:
            queryset = queryset.filter(section__course_id=course_id)

        if section_id:
            queryset = queryset.filter(section_id=section_id)

        return queryset.order_by(
            "section_id",
            "sort_order",
            "id",
        )

    def get_serializer_class(self):
        """Chọn serializer theo thao tác hiện tại."""

        if self.action in [
            "create",
            "update",
            "partial_update",
        ]:
            return LessonCreateUpdateSerializer

        return LessonSerializer

    def get_serializer_context(self):
        """Thêm request để serializer xây dựng URL tài liệu."""

        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        """Kiểm tra quyền sở hữu chương khi tạo bài học."""

        section = serializer.validated_data.get("section")

        if section.course.teacher != self.request.user:
            raise PermissionDenied(
                "You can only create lessons for sections in your own courses."
            )

        serializer.save()

    def perform_update(self, serializer):
        """Kiểm tra quyền sở hữu chương khi sửa bài học."""

        section = serializer.validated_data.get(
            "section",
            serializer.instance.section,
        )

        if section.course.teacher != self.request.user:
            raise PermissionDenied(
                "You can only update lessons for sections in your own courses."
            )

        serializer.save()
