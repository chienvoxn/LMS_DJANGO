from rest_framework import serializers

from .models import (
    Assignment,
    Choice,
    Question,
    Quiz,
    StudentQuizAttempt,
    Submission,
)

# =========================================================
# Phương án trả lời
# =========================================================


class ChoiceSerializer(serializers.ModelSerializer):
    """Phương án dành cho giảng viên, gồm đáp án đúng."""

    class Meta:
        model = Choice
        fields = ["id", "text", "is_correct"]


class ChoicePublicSerializer(serializers.ModelSerializer):
    """Phương án dành cho học viên, không lộ đáp án đúng."""

    class Meta:
        model = Choice
        fields = ["id", "text"]


class ChoiceCreateSerializer(serializers.ModelSerializer):
    """Dữ liệu tạo phương án trả lời."""

    class Meta:
        model = Choice
        fields = ["text", "is_correct"]


# =========================================================
# Câu hỏi
# =========================================================


class QuestionSerializer(serializers.ModelSerializer):
    """Câu hỏi dành cho giảng viên."""

    choices = ChoiceSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Question
        fields = [
            "id",
            "text",
            "question_type",
            "points",
            "order",
            "choices",
        ]


class QuestionPublicSerializer(serializers.ModelSerializer):
    """Câu hỏi dành cho học viên, không lộ đáp án đúng."""

    choices = ChoicePublicSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Question
        fields = [
            "id",
            "text",
            "question_type",
            "points",
            "order",
            "choices",
        ]


class QuestionCreateSerializer(serializers.ModelSerializer):
    """Dữ liệu tạo câu hỏi."""

    class Meta:
        model = Question
        fields = [
            "text",
            "question_type",
            "points",
            "order",
        ]


# =========================================================
# Bài kiểm tra
# =========================================================


class QuizSerializer(serializers.ModelSerializer):
    """Thông tin tóm tắt của bài kiểm tra."""

    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = [
            "id",
            "course",
            "title",
            "description",
            "is_published",
            "time_limit",
            "questions_count",
        ]

    def get_questions_count(self, obj):
        """Trả về số câu hỏi của bài kiểm tra."""

        return obj.questions.count()


class QuizDetailTeacherSerializer(serializers.ModelSerializer):
    """Chi tiết bài kiểm tra dành cho giảng viên."""

    questions = QuestionSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Quiz
        fields = [
            "id",
            "course",
            "title",
            "description",
            "is_published",
            "time_limit",
            "questions",
        ]


class QuizDetailStudentSerializer(serializers.ModelSerializer):
    """Chi tiết bài kiểm tra dành cho học viên."""

    questions = QuestionPublicSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Quiz
        fields = [
            "id",
            "course",
            "title",
            "description",
            "time_limit",
            "questions",
        ]


class StudentQuizAttemptSerializer(serializers.ModelSerializer):
    """Thông tin một lần làm bài kiểm tra."""

    class Meta:
        model = StudentQuizAttempt
        fields = [
            "id",
            "quiz",
            "student",
            "started_at",
            "completed_at",
            "score",
            "status",
        ]
        read_only_fields = [
            "student",
            "started_at",
            "completed_at",
            "score",
            "status",
        ]


class QuizSubmitSerializer(serializers.Serializer):
    """Dữ liệu nộp bài kiểm tra."""

    answers = serializers.ListField(
        child=serializers.DictField(),
        required=True,
    )

    def validate_answers(self, value):
        """Kiểm tra cấu trúc danh sách câu trả lời."""

        if not value:
            raise serializers.ValidationError("Answers cannot be empty.")

        for answer in value:
            if "question" not in answer or "selected_choice" not in answer:
                raise serializers.ValidationError(
                    "Each answer must have 'question' and " "'selected_choice' fields."
                )

            try:
                int(answer["question"])
                int(answer["selected_choice"])
            except (ValueError, TypeError):
                raise serializers.ValidationError(
                    "Question and selected_choice must be integers."
                )

        return value


# =========================================================
# Bài tập
# =========================================================


class AssignmentSerializer(serializers.ModelSerializer):
    """Thông tin tóm tắt của bài tập."""

    class Meta:
        model = Assignment
        fields = [
            "id",
            "course",
            "title",
            "description",
            "due_date",
            "max_points",
            "is_published",
            "created_at",
        ]


class AssignmentDetailSerializer(serializers.ModelSerializer):
    """Thông tin chi tiết của bài tập."""

    class Meta:
        model = Assignment
        fields = [
            "id",
            "course",
            "title",
            "description",
            "due_date",
            "max_points",
            "is_published",
            "attachment_url",
            "created_at",
        ]


# =========================================================
# Bài nộp
# =========================================================


class SubmissionSerializer(serializers.ModelSerializer):
    """Bài nộp dành cho giảng viên."""

    student_email = serializers.EmailField(
        source="student.email",
        read_only=True,
    )
    student_name = serializers.CharField(
        source="student.full_name",
        read_only=True,
    )

    class Meta:
        model = Submission
        fields = [
            "id",
            "assignment",
            "student",
            "student_email",
            "student_name",
            "content",
            "submitted_at",
            "graded_at",
            "grade",
            "feedback",
            "status",
        ]
        read_only_fields = [
            "student",
            "submitted_at",
            "graded_at",
            "status",
        ]


class SubmissionStudentSerializer(serializers.ModelSerializer):
    """Bài nộp của học viên hiện tại."""

    class Meta:
        model = Submission
        fields = [
            "id",
            "assignment",
            "content",
            "submitted_at",
            "graded_at",
            "grade",
            "feedback",
            "status",
        ]
        read_only_fields = [
            "assignment",
            "submitted_at",
            "graded_at",
            "grade",
            "feedback",
            "status",
        ]
