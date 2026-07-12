"""Các API đăng ký và tiến độ dành cho học viên."""

from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from courses.models import Course, Lesson

from .models import Enrollment, LessonProgress
from .serializers import EnrollmentSerializer


class EnrollCourseAPIView(generics.CreateAPIView):
    """Đăng ký một khóa học đã xuất bản."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EnrollmentSerializer

    def create(self, request, course_id=None):
        """Tạo đăng ký cho người dùng hiện tại."""

        try:
            course = Course.objects.get(
                id=course_id,
                is_published=True,
            )
        except Course.DoesNotExist:
            return Response(
                {"detail": ("Course not found or not published.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user,
            course=course,
            defaults={"progress_percent": 0},
        )

        if not created:
            return Response(
                {"detail": ("You are already enrolled in this course.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(enrollment)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class MyEnrollmentsListAPIView(generics.ListAPIView):
    """Trả về các đăng ký của người dùng hiện tại."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        """Lọc đăng ký theo người dùng hiện tại."""

        return (
            Enrollment.objects.filter(student=self.request.user)
            .select_related("course")
            .order_by("-created_at")
        )


class CompleteLessonAPIView(generics.CreateAPIView):
    """Đánh dấu một bài học đã hoàn thành."""

    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, lesson_id=None):
        """Cập nhật bài học và tính lại phần trăm tiến độ."""

        try:
            lesson = Lesson.objects.select_related(
                "section",
                "section__course",
            ).get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response(
                {"detail": "Lesson not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        course = lesson.section.course

        try:
            enrollment = Enrollment.objects.get(
                student=request.user,
                course=course,
            )
        except Enrollment.DoesNotExist:
            return Response(
                {"detail": ("You must enroll in this course first.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        lesson_progress, created = LessonProgress.objects.get_or_create(
            enrollment=enrollment,
            lesson=lesson,
            defaults={"is_completed": False},
        )

        if not lesson_progress.is_completed:
            lesson_progress.is_completed = True
            lesson_progress.completed_at = timezone.now()
            lesson_progress.save()

        total_lessons = Lesson.objects.filter(section__course=course).count()

        completed_lessons = LessonProgress.objects.filter(
            enrollment=enrollment,
            is_completed=True,
        ).count()

        if total_lessons > 0:
            progress_percent = int((completed_lessons * 100) / total_lessons)
        else:
            progress_percent = 0

        enrollment.progress_percent = progress_percent
        enrollment.save()

        return Response(
            {
                "lesson_id": lesson.id,
                "completed": True,
                "progress_percent": progress_percent,
                "message": "Lesson marked as completed.",
            },
            status=status.HTTP_200_OK,
        )


class StudentMyCoursesAPIView(generics.ListAPIView):
    """Trả về khóa học và tiến độ của học viên."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Tổng hợp thông tin khóa học của học viên."""

        enrollments = (
            Enrollment.objects.filter(student=request.user)
            .select_related(
                "course",
                "course__teacher",
            )
            .prefetch_related("lesson_progresses__lesson")
            .order_by("-created_at")
        )

        result = []

        for enrollment in enrollments:
            course = enrollment.course

            total_lessons = Lesson.objects.filter(section__course=course).count()

            completed_lessons = LessonProgress.objects.filter(
                enrollment=enrollment,
                is_completed=True,
            ).count()

            last_lesson_progress = (
                LessonProgress.objects.filter(enrollment=enrollment)
                .select_related("lesson")
                .order_by(
                    "-completed_at",
                    "-id",
                )
                .first()
            )

            if enrollment.progress_percent >= 100:
                status_value = "completed"
            elif enrollment.progress_percent > 0:
                status_value = "in_progress"
            else:
                status_value = "in_progress"

            instructor_name = ""

            if hasattr(course.teacher, "full_name") and course.teacher.full_name:
                instructor_name = course.teacher.full_name
            else:
                instructor_name = course.teacher.email or ""

            last_accessed_lesson_id = None
            last_accessed_lesson_title = None

            if last_lesson_progress and last_lesson_progress.lesson:
                last_accessed_lesson_id = last_lesson_progress.lesson.id
                last_accessed_lesson_title = last_lesson_progress.lesson.title

            course_data = {
                "course_id": course.id,
                "course_title": course.title,
                "course_thumbnail": (course.thumbnail_url or ""),
                "instructor_name": instructor_name,
                "progress_percentage": float(enrollment.progress_percent),
                "total_lessons": total_lessons,
                "completed_lessons": completed_lessons,
                "last_accessed_lesson_id": (last_accessed_lesson_id),
                "last_accessed_lesson_title": (last_accessed_lesson_title),
                "status": status_value,
                "enrolled_at": (
                    enrollment.created_at.isoformat() if enrollment.created_at else None
                ),
                "enrollment_type": (enrollment.enrollment_type),
                "granted_certificate": (enrollment.granted_certificate),
            }

            result.append(course_data)

        return Response(
            result,
            status=status.HTTP_200_OK,
        )
