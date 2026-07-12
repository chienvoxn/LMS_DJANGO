"""Khai báo URL cho đánh giá và xếp hạng khóa học."""

from django.urls import path

from .views import (
    CourseRatingSummaryAPIView,
    CourseReviewDetailAPIView,
    CourseReviewListCreateAPIView,
    MyCourseReviewAPIView,
)

urlpatterns = [
    # Danh sách, tạo hoặc cập nhật đánh giá khóa học
    path(
        "courses/<int:course_id>/reviews/",
        CourseReviewListCreateAPIView.as_view(),
        name="course-reviews-list-create",
    ),
    # Điểm trung bình và tổng số đánh giá
    path(
        "courses/<int:course_id>/rating-summary/",
        CourseRatingSummaryAPIView.as_view(),
        name="course-rating-summary",
    ),
    # Đánh giá của người dùng hiện tại
    path(
        "courses/<int:course_id>/my-review/",
        MyCourseReviewAPIView.as_view(),
        name="course-my-review",
    ),
    # Chi tiết, cập nhật hoặc xóa đánh giá
    path(
        "reviews/<int:pk>/",
        CourseReviewDetailAPIView.as_view(),
        name="review-detail",
    ),
]
