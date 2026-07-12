"""Mô hình dữ liệu đánh giá khóa học."""

from django.conf import settings
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models


class CourseReview(models.Model):
    """
    Lưu đánh giá của người dùng dành cho khóa học.

    Mỗi người dùng chỉ được tạo một đánh giá cho mỗi khóa học.
    """

    course = models.ForeignKey(
        "courses.Course",
        related_name="reviews",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="course_reviews",
        on_delete=models.CASCADE,
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        help_text="Rating from 1 to 5 stars",
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("course", "user")
        ordering = ("-created_at",)
        db_table = "course_reviews"

    def __str__(self):
        return f"{self.course_id} - " f"{self.user_id} ({self.rating})"
