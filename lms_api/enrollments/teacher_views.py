"""Các API quản lý học viên dành cho giảng viên."""

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from assessments.models import (
    Assignment,
    Quiz,
    StudentQuizAttempt,
    Submission,
)
from common.permissions import IsTeacher
from courses.models import Course, Lesson

from .models import Enrollment, LessonProgress
from .serializers import StudentInCourseSerializer


class TeacherCourseStudentsView(generics.GenericAPIView):
    """Trả về học viên đang tham gia khóa học."""

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeacher,
    ]
    serializer_class = StudentInCourseSerializer

    def get(self, request, course_id, *args, **kwargs):
        """Tổng hợp tiến độ và hoạt động của từng học viên."""

        course = get_object_or_404(
            Course,
            id=course_id,
        )

        if course.teacher != request.user:
            return Response(
                {
                    "detail": (
                        "You do not have permission to view "
                        "students for this course."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        enrollments = (
            Enrollment.objects.filter(course=course)
            .select_related("student")
            .prefetch_related("lesson_progresses__lesson")
        )

        search_query = request.query_params.get(
            "q",
            "",
        ).strip()

        if search_query:
            enrollments = enrollments.filter(
                Q(student__full_name__icontains=(search_query))
                | Q(student__email__icontains=(search_query))
            )

        total_lessons = Lesson.objects.filter(section__course=course).count()

        students_data = []

        for enrollment in enrollments:
            student = enrollment.student

            completed_lessons = LessonProgress.objects.filter(
                enrollment=enrollment,
                is_completed=True,
            ).count()

            if total_lessons > 0:
                progress_percentage = (completed_lessons / total_lessons) * 100
            else:
                progress_percentage = 0.0

            status_filter = request.query_params.get(
                "status",
                "",
            ).strip()

            if status_filter == "completed":
                if completed_lessons < total_lessons:
                    continue
            elif status_filter == "in_progress":
                if completed_lessons >= total_lessons:
                    continue

            last_lesson_progress = (
                LessonProgress.objects.filter(enrollment=enrollment)
                .select_related("lesson")
                .order_by("-id")
                .first()
            )

            last_accessed_lesson_id = None
            last_accessed_lesson_title = None
            last_accessed_at = None

            if last_lesson_progress:
                last_accessed_lesson_id = last_lesson_progress.lesson.id
                last_accessed_lesson_title = last_lesson_progress.lesson.title
                last_accessed_at = last_lesson_progress.completed_at

                if not last_accessed_at:
                    last_accessed_at = enrollment.created_at

            quiz_attempts_count = (
                StudentQuizAttempt.objects.filter(
                    student=student,
                    quiz__course=course,
                    status="completed",
                )
                .values("quiz")
                .distinct()
                .count()
            )

            assignments_submitted_count = Submission.objects.filter(
                student=student,
                assignment__course=course,
            ).count()

            student_data = {
                "student_id": student.id,
                "full_name": student.full_name or "",
                "email": student.email,
                "avatar_url": student.avatar_url or None,
                "enrolled_at": enrollment.created_at,
                "enrollment_type": (enrollment.enrollment_type),
                "price_paid": (
                    float(enrollment.price_paid) if enrollment.price_paid else 0.0
                ),
                "total_lessons": total_lessons,
                "completed_lessons": completed_lessons,
                "progress_percentage": round(
                    progress_percentage,
                    2,
                ),
                "last_accessed_lesson_id": (last_accessed_lesson_id),
                "last_accessed_lesson_title": (last_accessed_lesson_title or None),
                "last_accessed_at": last_accessed_at,
                "quiz_attempts_count": (quiz_attempts_count),
                "assignments_submitted_count": (assignments_submitted_count),
            }

            students_data.append(student_data)

        serializer = self.get_serializer(
            students_data,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class RemoveStudentFromCourseView(generics.GenericAPIView):
    """Xóa học viên và dữ liệu liên quan khỏi khóa học."""

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeacher,
    ]

    def delete(
        self,
        request,
        course_id,
        student_id,
        *args,
        **kwargs,
    ):
        """Xóa đăng ký, tiến độ, bài làm và lần làm quiz."""

        course = get_object_or_404(
            Course,
            id=course_id,
        )

        if course.teacher != request.user:
            return Response(
                {
                    "detail": (
                        "You do not have permission to remove "
                        "students from this course."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            enrollment = Enrollment.objects.get(
                course=course,
                student_id=student_id,
            )
        except Enrollment.DoesNotExist:
            return Response(
                {"detail": ("Student is not enrolled in this course.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        LessonProgress.objects.filter(enrollment=enrollment).delete()

        quizzes = Quiz.objects.filter(course=course)

        StudentQuizAttempt.objects.filter(
            student_id=student_id,
            quiz__in=quizzes,
        ).delete()

        assignments = Assignment.objects.filter(course=course)

        Submission.objects.filter(
            student_id=student_id,
            assignment__in=assignments,
        ).delete()

        enrollment.delete()

        return Response(
            {"message": "Student removed from course."},
            status=status.HTTP_200_OK,
        )
