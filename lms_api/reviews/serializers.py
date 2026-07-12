"""Các serializer dành cho đánh giá khóa học."""

from rest_framework import serializers

from users.models import User

from .models import CourseReview

# =========================================================
# Thông tin người dùng
# =========================================================


class UserMinimalSerializer(serializers.ModelSerializer):
    """Thông tin người dùng rút gọn trong một đánh giá."""

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "email",
        ]
        read_only_fields = [
            "id",
            "full_name",
            "email",
        ]


# =========================================================
# Đánh giá khóa học
# =========================================================


class CourseReviewSerializer(serializers.ModelSerializer):
    """Định dạng dữ liệu danh sách và chi tiết đánh giá."""

    user = UserMinimalSerializer(read_only=True)

    class Meta:
        model = CourseReview
        fields = [
            "id",
            "course",
            "user",
            "rating",
            "comment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "course",
            "user",
            "created_at",
            "updated_at",
        ]


class CourseReviewCreateUpdateSerializer(serializers.ModelSerializer):
    """Dữ liệu tạo hoặc cập nhật đánh giá."""

    class Meta:
        model = CourseReview
        fields = [
            "rating",
            "comment",
        ]

    def validate_rating(self, value):
        """Kiểm tra điểm đánh giá nằm trong khoảng từ 1 đến 5."""

        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")

        return value


# =========================================================
# Thống kê đánh giá
# =========================================================


class CourseRatingSummarySerializer(serializers.Serializer):
    """Định dạng điểm trung bình và tổng số đánh giá."""

    average_rating = serializers.FloatField(allow_null=True)
    total_reviews = serializers.IntegerField()
