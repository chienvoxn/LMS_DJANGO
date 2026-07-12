"""Các API quản lý đánh giá và xếp hạng khóa học."""

from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response

from courses.models import Course
from enrollments.models import Enrollment

from .models import CourseReview
from .serializers import (
    CourseRatingSummarySerializer,
    CourseReviewCreateUpdateSerializer,
    CourseReviewSerializer,
)

# =========================================================
# Danh sách và tạo đánh giá
# =========================================================


class CourseReviewListCreateAPIView(generics.ListCreateAPIView):
    """
    Trả về danh sách đánh giá hoặc tạo đánh giá khóa học.

    GET:
        Mọi người đều có thể xem đánh giá.

    POST:
        Người dùng phải đăng nhập và đã đăng ký khóa học.
        Nếu đã có đánh giá, hệ thống cập nhật đánh giá đó.
    """

    serializer_class = CourseReviewSerializer

    def get_permissions(self):
        """Chọn quyền truy cập theo phương thức HTTP."""

        if self.request.method == "GET":
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """Lấy đánh giá của khóa học đã xuất bản."""

        course_id = self.kwargs["course_id"]

        return (
            CourseReview.objects.filter(
                course_id=course_id,
                course__is_published=True,
            )
            .select_related(
                "user",
                "course",
            )
            .order_by("-created_at")
        )

    def create(self, request, *args, **kwargs):
        """Tạo mới hoặc cập nhật đánh giá của người dùng."""

        course_id = self.kwargs["course_id"]

        course = get_object_or_404(
            Course,
            id=course_id,
            is_published=True,
        )

        is_enrolled = Enrollment.objects.filter(
            student=request.user,
            course=course,
        ).exists()

        if not is_enrolled:
            return Response(
                {
                    "detail": (
                        "You must enroll in this course " "before leaving a review."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            review = CourseReview.objects.get(
                course=course,
                user=request.user,
            )

            serializer = CourseReviewCreateUpdateSerializer(
                review,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                CourseReviewSerializer(review).data,
                status=status.HTTP_200_OK,
            )

        except CourseReview.DoesNotExist:
            serializer = CourseReviewCreateUpdateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            review = serializer.save(
                course=course,
                user=request.user,
            )

            return Response(
                CourseReviewSerializer(review).data,
                status=status.HTTP_201_CREATED,
            )


# =========================================================
# Chi tiết đánh giá
# =========================================================


class CourseReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Xem, cập nhật hoặc xóa một đánh giá.

    Mọi người có thể xem đánh giá.
    Chỉ chủ sở hữu mới được sửa hoặc xóa.
    """

    queryset = CourseReview.objects.all().select_related(
        "user",
        "course",
    )
    serializer_class = CourseReviewSerializer

    def get_permissions(self):
        """Chọn quyền truy cập theo phương thức HTTP."""

        if self.request.method == "GET":
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        """Dùng serializer nhập liệu khi cập nhật."""

        if self.request.method in ["PUT", "PATCH"]:
            return CourseReviewCreateUpdateSerializer

        return CourseReviewSerializer

    def get_object(self):
        """Lấy đánh giá và kiểm tra quyền sở hữu."""

        review = super().get_object()

        if self.request.method in [
            "PUT",
            "PATCH",
            "DELETE",
        ]:
            if review.user != self.request.user:
                raise PermissionDenied(
                    "You can only update or delete " "your own reviews."
                )

        return review


# =========================================================
# Thống kê đánh giá
# =========================================================


class CourseRatingSummaryAPIView(generics.GenericAPIView):
    """Trả về điểm trung bình và tổng số đánh giá."""

    permission_classes = [permissions.AllowAny]
    serializer_class = CourseRatingSummarySerializer

    def get(self, request, course_id):
        """Tính thống kê đánh giá của khóa học."""

        course = get_object_or_404(
            Course,
            id=course_id,
            is_published=True,
        )

        result = CourseReview.objects.filter(course=course).aggregate(
            average_rating=Avg("rating"),
            total_reviews=Count("id"),
        )

        data = {
            "average_rating": (
                round(result["average_rating"], 2) if result["average_rating"] else 0.0
            ),
            "total_reviews": (result["total_reviews"] or 0),
        }

        serializer = self.get_serializer(data)

        return Response(serializer.data)


# =========================================================
# Đánh giá của người dùng hiện tại
# =========================================================


class MyCourseReviewAPIView(generics.RetrieveAPIView):
    """Trả về đánh giá của người dùng cho một khóa học."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseReviewSerializer

    def get_object(self):
        """Tìm đánh giá theo khóa học và người dùng."""

        course_id = self.kwargs["course_id"]

        course = get_object_or_404(
            Course,
            id=course_id,
            is_published=True,
        )

        try:
            return CourseReview.objects.get(
                course=course,
                user=self.request.user,
            )

        except CourseReview.DoesNotExist:
            raise NotFound("You have not reviewed this course yet.")
