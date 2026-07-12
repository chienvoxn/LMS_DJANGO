"""Các serializer của khóa học, chương học và bài học."""

from rest_framework import serializers

from .models import Course, Lesson, Section

# =========================================================
# Serializer cơ bản
# =========================================================


class LessonSerializer(serializers.ModelSerializer):
    """Định dạng thông tin đầy đủ của một bài học."""

    document_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            "id",
            "section",
            "title",
            "video_url",
            "document_file",
            "document_file_url",
            "content",
            "duration",
            "sort_order",
        ]

    def get_document_file_url(self, obj):
        """Trả về URL đầy đủ của tài liệu nếu tồn tại."""

        if obj.document_file:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(obj.document_file.url)

            return obj.document_file.url

        return None


class SectionSerializer(serializers.ModelSerializer):
    """Định dạng thông tin cơ bản của một chương học."""

    class Meta:
        model = Section
        fields = [
            "id",
            "course",
            "title",
            "sort_order",
        ]


# =========================================================
# Serializer khóa học
# =========================================================


class CourseSerializer(serializers.ModelSerializer):
    """Định dạng khóa học trong danh sách."""

    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "subtitle",
            "thumbnail_url",
            "price",
            "level",
            "category",
            "is_published",
            "created_at",
            "average_rating",
            "reviews_count",
        ]
        read_only_fields = [
            "created_at",
            "average_rating",
            "reviews_count",
        ]

    def get_average_rating(self, obj):
        """Tính điểm đánh giá trung bình của khóa học."""

        from django.db.models import Avg

        result = obj.reviews.aggregate(avg_rating=Avg("rating"))

        return round(result["avg_rating"], 2) if result["avg_rating"] else None

    def get_reviews_count(self, obj):
        """Trả về tổng số đánh giá của khóa học."""

        return obj.reviews.count()


class CourseDetailSerializer(serializers.ModelSerializer):
    """Định dạng thông tin chi tiết của khóa học."""

    teacher_id = serializers.IntegerField(
        source="teacher.id",
        read_only=True,
    )
    teacher_name = serializers.CharField(
        source="teacher.full_name",
        read_only=True,
    )
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    is_enrolled = serializers.SerializerMethodField()
    enrollment_type = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "subtitle",
            "description",
            "thumbnail_url",
            "price",
            "level",
            "category",
            "is_published",
            "created_at",
            "updated_at",
            "teacher",
            "teacher_id",
            "teacher_name",
            "average_rating",
            "reviews_count",
            "is_enrolled",
            "enrollment_type",
        ]
        read_only_fields = [
            "created_at",
            "updated_at",
            "average_rating",
            "reviews_count",
            "is_enrolled",
            "enrollment_type",
        ]

    def get_average_rating(self, obj):
        """Tính điểm đánh giá trung bình của khóa học."""

        from django.db.models import Avg

        result = obj.reviews.aggregate(avg_rating=Avg("rating"))

        return round(result["avg_rating"], 2) if result["avg_rating"] else None

    def get_reviews_count(self, obj):
        """Trả về tổng số đánh giá của khóa học."""

        return obj.reviews.count()

    def get_is_enrolled(self, obj):
        """Kiểm tra học viên hiện tại đã đăng ký khóa học chưa."""

        request = self.context.get("request")

        if not request or not request.user or not request.user.is_authenticated:
            return False

        if request.user.role != "student":
            return False

        from enrollments.models import Enrollment

        return Enrollment.objects.filter(
            student=request.user,
            course=obj,
        ).exists()

    def get_enrollment_type(self, obj):
        """Trả về loại đăng ký của học viên hiện tại."""

        request = self.context.get("request")

        if not request or not request.user or not request.user.is_authenticated:
            return None

        if request.user.role != "student":
            return None

        from enrollments.models import Enrollment

        enrollment = Enrollment.objects.filter(
            student=request.user,
            course=obj,
        ).first()

        return enrollment.enrollment_type if enrollment else None


# =========================================================
# Serializer chương trình học
# =========================================================


class CurriculumLessonSerializer(serializers.ModelSerializer):
    """Định dạng bài học kèm trạng thái hoàn thành."""

    is_completed = serializers.SerializerMethodField()
    document_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "video_url",
            "document_file",
            "document_file_url",
            "content",
            "duration",
            "sort_order",
            "is_completed",
        ]

    def get_document_file_url(self, obj):
        """Trả về URL đầy đủ của tài liệu nếu tồn tại."""

        if obj.document_file:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(obj.document_file.url)

            return obj.document_file.url

        return None

    def get_is_completed(self, obj):
        """Kiểm tra học viên đã hoàn thành bài học chưa."""

        request = self.context.get("request")

        if not request or not request.user or not request.user.is_authenticated:
            return False

        from enrollments.models import (
            Enrollment,
            LessonProgress,
        )

        try:
            enrollment = Enrollment.objects.get(
                student=request.user,
                course=obj.section.course,
            )

            lesson_progress = LessonProgress.objects.filter(
                enrollment=enrollment,
                lesson=obj,
                is_completed=True,
            ).first()

            return lesson_progress is not None

        except Enrollment.DoesNotExist:
            return False


class CurriculumSectionSerializer(serializers.ModelSerializer):
    """Định dạng chương học cùng danh sách bài học."""

    lessons = CurriculumLessonSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Section
        fields = [
            "id",
            "title",
            "sort_order",
            "lessons",
        ]


class CourseCurriculumSerializer(serializers.ModelSerializer):
    """Định dạng toàn bộ chương trình của khóa học."""

    sections = CurriculumSectionSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "subtitle",
            "description",
            "level",
            "sections",
        ]


# =========================================================
# Serializer CRUD dành cho giảng viên
# =========================================================


class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    """Dữ liệu tạo hoặc cập nhật khóa học."""

    class Meta:
        model = Course
        fields = [
            "title",
            "subtitle",
            "description",
            "thumbnail_url",
            "price",
            "level",
            "category",
            "is_published",
        ]


class SectionCreateUpdateSerializer(serializers.ModelSerializer):
    """Dữ liệu tạo hoặc cập nhật chương học."""

    class Meta:
        model = Section
        fields = [
            "course",
            "title",
            "sort_order",
        ]


class LessonCreateUpdateSerializer(serializers.ModelSerializer):
    """Dữ liệu tạo hoặc cập nhật bài học."""

    class Meta:
        model = Lesson
        fields = [
            "section",
            "title",
            "video_url",
            "document_file",
            "content",
            "duration",
            "sort_order",
        ]
