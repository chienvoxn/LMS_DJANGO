from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import (
    generics,
    permissions,
    status,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from common.permissions import IsTeacher
from enrollments.models import Enrollment

from .models import Assignment, Submission
from .serializers import (
    AssignmentDetailSerializer,
    AssignmentSerializer,
    SubmissionSerializer,
    SubmissionStudentSerializer,
)

# =========================================================
# Giảng viên quản lý bài tập
# =========================================================


class TeacherAssignmentViewSet(viewsets.ModelViewSet):
    """Giảng viên quản lý bài tập của mình."""

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeacher,
    ]
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        """Chỉ lấy bài tập thuộc khóa học của giảng viên."""

        return Assignment.objects.filter(course__teacher=self.request.user)

    def get_serializer_class(self):
        if self.action in [
            "retrieve",
            "update",
            "partial_update",
        ]:
            return AssignmentDetailSerializer

        return AssignmentSerializer

    def perform_create(self, serializer):
        """Chỉ tạo bài tập trong khóa học của mình."""

        course = serializer.validated_data["course"]

        if course.teacher != self.request.user:
            raise permissions.PermissionDenied(
                "You can only create assignments " "for your own courses."
            )

        serializer.save()

    @action(detail=True, methods=["get"])
    def submissions(self, request, pk=None):
        """Lấy toàn bộ bài nộp của bài tập."""

        assignment = self.get_object()

        submissions = Submission.objects.filter(assignment=assignment)

        serializer = SubmissionSerializer(
            submissions,
            many=True,
        )

        return Response(serializer.data)


class SubmissionGradeAPIView(generics.UpdateAPIView):
    """Giảng viên chấm điểm một bài nộp."""

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeacher,
    ]
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()

    def get_queryset(self):
        """Chỉ chấm bài thuộc khóa học của giảng viên."""

        return Submission.objects.filter(assignment__course__teacher=self.request.user)

    def patch(self, request, pk):
        """Cập nhật điểm, phản hồi và trạng thái bài nộp."""

        submission = self.get_object()

        grade = request.data.get("grade")
        feedback = request.data.get("feedback", "")

        if grade is None:
            return Response(
                {"detail": "Grade is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            grade = float(grade)
            max_points = submission.assignment.max_points

            if grade < 0 or grade > max_points:
                return Response(
                    {"detail": (f"Grade must be between " f"0 and {max_points}.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except (ValueError, TypeError):
            return Response(
                {"detail": "Invalid grade value."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        submission.grade = grade
        submission.feedback = feedback
        submission.status = "graded"
        submission.graded_at = timezone.now()
        submission.save()

        serializer = self.get_serializer(submission)

        return Response(serializer.data)


# =========================================================
# Học viên làm bài tập
# =========================================================


class CourseAssignmentsListAPIView(generics.ListAPIView):
    """Danh sách bài tập đã xuất bản của khóa học."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        """Lọc bài tập đã xuất bản theo khóa học."""

        course_id = self.kwargs["course_id"]

        return Assignment.objects.filter(
            course_id=course_id,
            is_published=True,
        )


class AssignmentDetailAPIView(generics.RetrieveAPIView):
    """Chi tiết bài tập đã xuất bản."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AssignmentDetailSerializer
    queryset = Assignment.objects.filter(is_published=True)


class AssignmentSubmitAPIView(generics.CreateAPIView):
    """Tạo mới hoặc cập nhật bài nộp."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubmissionStudentSerializer

    def post(self, request, pk):
        """Nộp bài hoặc cập nhật bài chưa được chấm."""

        assignment = get_object_or_404(
            Assignment,
            id=pk,
            is_published=True,
        )

        is_enrolled = Enrollment.objects.filter(
            student=request.user,
            course=assignment.course,
        ).exists()

        if not is_enrolled:
            return Response(
                {"detail": ("You must enroll in this course first.")},
                status=status.HTTP_403_FORBIDDEN,
            )

        content = request.data.get("content", "")

        try:
            submission = Submission.objects.get(
                assignment=assignment,
                student=request.user,
            )

            if submission.status == "graded":
                return Response(
                    {
                        "detail": (
                            "This submission has already "
                            "been graded and cannot be modified."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            submission.content = content
            submission.status = "submitted"
            submission.submitted_at = timezone.now()
            submission.save()

            created = False

        except Submission.DoesNotExist:
            submission = Submission.objects.create(
                assignment=assignment,
                student=request.user,
                content=content,
                status="submitted",
                submitted_at=timezone.now(),
            )

            created = True

        serializer = self.get_serializer(submission)

        return Response(
            serializer.data,
            status=(status.HTTP_201_CREATED if created else status.HTTP_200_OK),
        )


class AssignmentMySubmissionAPIView(generics.RetrieveAPIView):
    """Lấy bài nộp của học viên hiện tại."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubmissionStudentSerializer

    def get_object(self):
        """Lọc bài nộp theo bài tập và học viên."""

        assignment_id = self.kwargs["pk"]

        return get_object_or_404(
            Submission,
            assignment_id=assignment_id,
            student=self.request.user,
        )
