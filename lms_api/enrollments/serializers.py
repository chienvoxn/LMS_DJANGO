"""Các serializer của đăng ký học và thanh toán."""

from rest_framework import serializers

from .models import (
    CartItem,
    Enrollment,
    LessonProgress,
    Payment,
)

# =========================================================
# Đăng ký và tiến độ
# =========================================================


class CourseBasicSerializer(serializers.Serializer):
    """Thông tin khóa học cơ bản trong đăng ký."""

    id = serializers.IntegerField()
    title = serializers.CharField()
    thumbnail_url = serializers.URLField(allow_null=True)
    level = serializers.CharField()
    category = serializers.CharField()


class EnrollmentSerializer(serializers.ModelSerializer):
    """Định dạng thông tin đăng ký khóa học."""

    course = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "course",
            "progress_percent",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    def get_course(self, obj):
        """Trả về thông tin cơ bản của khóa học."""

        return {
            "id": obj.course.id,
            "title": obj.course.title,
            "thumbnail_url": obj.course.thumbnail_url,
            "level": obj.course.level,
            "category": obj.course.category,
        }


class LessonProgressSerializer(serializers.ModelSerializer):
    """Định dạng tiến độ của một bài học."""

    lesson = serializers.SerializerMethodField()

    class Meta:
        model = LessonProgress
        fields = [
            "id",
            "lesson",
            "is_completed",
            "completed_at",
        ]

    def get_lesson(self, obj):
        """Trả về thông tin cơ bản của bài học."""

        return {
            "id": obj.lesson.id,
            "title": obj.lesson.title,
        }


# =========================================================
# Thông tin học viên dành cho giảng viên
# =========================================================


class StudentInCourseSerializer(serializers.Serializer):
    """Định dạng học viên đang tham gia khóa học."""

    student_id = serializers.IntegerField()
    full_name = serializers.CharField()
    email = serializers.EmailField()
    avatar_url = serializers.URLField(
        allow_null=True,
        allow_blank=True,
    )
    enrolled_at = serializers.DateTimeField()
    enrollment_type = serializers.CharField(
        allow_null=True,
        allow_blank=True,
    )
    price_paid = serializers.FloatField(allow_null=True)
    total_lessons = serializers.IntegerField()
    completed_lessons = serializers.IntegerField()
    progress_percentage = serializers.FloatField()
    last_accessed_lesson_id = serializers.IntegerField(allow_null=True)
    last_accessed_lesson_title = serializers.CharField(
        allow_null=True,
        allow_blank=True,
    )
    last_accessed_at = serializers.DateTimeField(allow_null=True)
    quiz_attempts_count = serializers.IntegerField()
    assignments_submitted_count = serializers.IntegerField()


# =========================================================
# Giỏ hàng
# =========================================================


class CartItemSerializer(serializers.ModelSerializer):
    """Định dạng một khóa học trong giỏ hàng."""

    course_id = serializers.IntegerField(
        source="course.id",
        read_only=True,
    )
    course_title = serializers.CharField(
        source="course.title",
        read_only=True,
    )
    course_thumbnail = serializers.CharField(
        source="course.thumbnail_url",
        read_only=True,
        allow_null=True,
    )
    course_price = serializers.DecimalField(
        source="course.price",
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )
    price_at_add = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = CartItem
        fields = [
            "id",
            "course_id",
            "course_title",
            "course_thumbnail",
            "course_price",
            "price_at_add",
            "created_at",
        ]


# =========================================================
# Thanh toán
# =========================================================


class PaymentHistorySerializer(serializers.ModelSerializer):
    """Định dạng lịch sử thanh toán."""

    course_id = serializers.SerializerMethodField()
    course_title = serializers.SerializerMethodField()
    course_thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            "id",
            "reference_code",
            "course_id",
            "course_title",
            "course_thumbnail",
            "amount",
            "currency",
            "status",
            "source",
            "created_at",
        ]

    def get_course_id(self, obj):
        """Trả về ID khóa học nếu còn tồn tại."""

        return obj.course.id if obj.course else None

    def get_course_title(self, obj):
        """Trả về tiêu đề khóa học nếu còn tồn tại."""

        return obj.course.title if obj.course else None

    def get_course_thumbnail(self, obj):
        """Trả về ảnh khóa học nếu còn tồn tại."""

        return obj.course.thumbnail_url if obj.course else None
