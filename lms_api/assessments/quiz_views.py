from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import (
    generics,
    permissions,
    status,
    viewsets,
)
from rest_framework.response import Response

from common.permissions import IsTeacher
from enrollments.models import Enrollment

from .models import (
    Choice,
    Question,
    Quiz,
    StudentAnswer,
    StudentQuizAttempt,
)
from .serializers import (
    ChoiceCreateSerializer,
    ChoiceSerializer,
    QuestionCreateSerializer,
    QuestionSerializer,
    QuizDetailStudentSerializer,
    QuizDetailTeacherSerializer,
    QuizSerializer,
    QuizSubmitSerializer,
    StudentQuizAttemptSerializer,
)

# =========================================================
# Giảng viên quản lý bài kiểm tra
# =========================================================


class TeacherQuizViewSet(viewsets.ModelViewSet):
    """Giảng viên quản lý các bài kiểm tra của mình."""

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeacher,
    ]
    serializer_class = QuizSerializer

    def get_queryset(self):
        """Chỉ lấy bài kiểm tra thuộc khóa học của giảng viên."""

        return Quiz.objects.filter(course__teacher=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return QuizDetailTeacherSerializer

        return QuizSerializer

    def perform_create(self, serializer):
        """Chỉ cho phép tạo quiz trong khóa học của mình."""

        course = serializer.validated_data["course"]

        if course.teacher != self.request.user:
            raise permissions.PermissionDenied(
                "You can only create quizzes for your own courses."
            )

        serializer.save()


class QuestionCreateAPIView(generics.CreateAPIView):
    """Tạo câu hỏi cho một bài kiểm tra."""

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeacher,
    ]
    serializer_class = QuestionCreateSerializer

    def post(self, request, quiz_id):
        """Tạo câu hỏi trong quiz thuộc giảng viên hiện tại."""

        quiz = get_object_or_404(
            Quiz,
            id=quiz_id,
            course__teacher=request.user,
        )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question = serializer.save(quiz=quiz)

        return Response(
            QuestionSerializer(question).data,
            status=status.HTTP_201_CREATED,
        )


class QuestionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Xem, cập nhật hoặc xóa một câu hỏi."""

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeacher,
    ]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def get_queryset(self):
        """Chỉ truy cập câu hỏi thuộc quiz của giảng viên."""

        return Question.objects.filter(quiz__course__teacher=self.request.user)


class ChoiceCreateAPIView(generics.CreateAPIView):
    """Tạo phương án trả lời cho một câu hỏi."""

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeacher,
    ]
    serializer_class = ChoiceCreateSerializer

    def post(self, request, question_id):
        """Tạo phương án trong câu hỏi thuộc giảng viên."""

        question = get_object_or_404(
            Question,
            id=question_id,
            quiz__course__teacher=request.user,
        )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        choice = serializer.save(question=question)

        return Response(
            ChoiceSerializer(choice).data,
            status=status.HTTP_201_CREATED,
        )


class ChoiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Xem, cập nhật hoặc xóa một phương án."""

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeacher,
    ]
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()

    def get_queryset(self):
        """Chỉ truy cập phương án thuộc giảng viên."""

        return Choice.objects.filter(question__quiz__course__teacher=self.request.user)


# =========================================================
# Học viên làm bài kiểm tra
# =========================================================


class CourseQuizzesListAPIView(generics.ListAPIView):
    """Danh sách quiz đã xuất bản của một khóa học."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuizSerializer

    def get_queryset(self):
        """Lọc quiz đã xuất bản theo khóa học."""

        course_id = self.kwargs["course_id"]

        return Quiz.objects.filter(
            course_id=course_id,
            is_published=True,
        )


class QuizDetailAPIView(generics.RetrieveAPIView):
    """Chi tiết quiz dành cho học viên."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuizDetailStudentSerializer
    queryset = Quiz.objects.filter(is_published=True)


class QuizStartAPIView(generics.CreateAPIView):
    """Bắt đầu hoặc tiếp tục một lần làm quiz."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentQuizAttemptSerializer

    def post(self, request, pk):
        """Tạo attempt hoặc trả lại attempt đang thực hiện."""

        quiz = get_object_or_404(
            Quiz,
            id=pk,
            is_published=True,
        )

        is_enrolled = Enrollment.objects.filter(
            student=request.user,
            course=quiz.course,
        ).exists()

        if not is_enrolled:
            return Response(
                {"detail": ("You must enroll in this course first.")},
                status=status.HTTP_403_FORBIDDEN,
            )

        attempt = StudentQuizAttempt.objects.filter(
            student=request.user,
            quiz=quiz,
            status="in_progress",
        ).first()

        if not attempt:
            attempt = StudentQuizAttempt.objects.create(
                student=request.user,
                quiz=quiz,
                status="in_progress",
                started_at=timezone.now(),
            )
            created = True
        else:
            created = False

        serializer = self.get_serializer(attempt)

        return Response(
            serializer.data,
            status=(status.HTTP_201_CREATED if created else status.HTTP_200_OK),
        )


class QuizSubmitAPIView(generics.CreateAPIView):
    """Nộp bài kiểm tra và tính điểm."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuizSubmitSerializer

    def post(self, request, pk):
        """Lưu câu trả lời và hoàn thành lần làm bài."""

        quiz = get_object_or_404(
            Quiz,
            id=pk,
            is_published=True,
        )

        is_enrolled = Enrollment.objects.filter(
            student=request.user,
            course=quiz.course,
        ).exists()

        if not is_enrolled:
            return Response(
                {"detail": ("You must enroll in this course first.")},
                status=status.HTTP_403_FORBIDDEN,
            )

        attempt = StudentQuizAttempt.objects.filter(
            student=request.user,
            quiz=quiz,
            status="in_progress",
        ).first()

        if not attempt:
            attempt = StudentQuizAttempt.objects.create(
                student=request.user,
                quiz=quiz,
                status="in_progress",
                started_at=timezone.now(),
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        answers_data = serializer.validated_data["answers"]

        total_points = sum(question.points for question in quiz.questions.all())
        obtained_points = 0

        for answer_data in answers_data:
            question_id = answer_data.get("question")
            choice_id = answer_data.get("selected_choice")

            if not question_id or not choice_id:
                continue

            try:
                question = Question.objects.get(
                    id=question_id,
                    quiz=quiz,
                )
                choice = Choice.objects.get(
                    id=choice_id,
                    question=question,
                )

                StudentAnswer.objects.update_or_create(
                    attempt=attempt,
                    question=question,
                    defaults={"selected_choice": choice},
                )

                if choice.is_correct:
                    obtained_points += question.points

            except (
                Question.DoesNotExist,
                Choice.DoesNotExist,
            ):
                continue

        percentage = obtained_points / total_points * 100 if total_points > 0 else 0

        attempt.score = obtained_points
        attempt.status = "completed"
        attempt.completed_at = timezone.now()
        attempt.save()

        return Response(
            {
                "score": obtained_points,
                "total_points": total_points,
                "percentage": round(percentage, 2),
            },
            status=status.HTTP_200_OK,
        )


class QuizAttemptsMeAPIView(generics.ListAPIView):
    """Lịch sử làm một quiz của học viên hiện tại."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentQuizAttemptSerializer

    def get_queryset(self):
        """Lọc attempt theo học viên và quiz."""

        quiz_id = self.kwargs["pk"]

        return StudentQuizAttempt.objects.filter(
            student=self.request.user,
            quiz_id=quiz_id,
        ).order_by("-started_at")
