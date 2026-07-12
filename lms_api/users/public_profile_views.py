"""Các API hồ sơ công khai của học viên và giảng viên."""

from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    InstructorPublicProfileSerializer,
    StudentPublicProfileSerializer,
)

User = get_user_model()


class StudentPublicProfileAPIView(APIView):
    """Trả về hồ sơ công khai của một học viên."""

    permission_classes = [permissions.AllowAny]

    def get(self, request, student_id):
        """Lấy thông tin, thống kê và khóa học."""

        try:
            student = User.objects.get(id=student_id)

        except User.DoesNotExist:
            return Response(
                {"detail": "Student not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = StudentPublicProfileSerializer(student)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class InstructorPublicProfileAPIView(APIView):
    """Trả về hồ sơ công khai của một giảng viên."""

    permission_classes = [permissions.AllowAny]

    def get(self, request, instructor_id):
        """Lấy thông tin, thống kê và khóa học."""

        try:
            instructor = User.objects.get(
                id=instructor_id,
                role="teacher",
            )

        except User.DoesNotExist:
            return Response(
                {"detail": "Instructor not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = InstructorPublicProfileSerializer(instructor)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class TopInstructorsAPIView(APIView):
    """Trả về tối đa 10 giảng viên nổi bật."""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """Sắp xếp theo số học viên hoặc điểm đánh giá."""

        from courses.models import Course
        from django.db.models import Avg, Count
        from enrollments.models import Enrollment
        from reviews.models import CourseReview

        teachers = User.objects.filter(
            role="teacher",
            courses__is_published=True,
        ).distinct()

        instructors_data = []

        for teacher in teachers:
            courses = Course.objects.filter(
                teacher=teacher,
                is_published=True,
            )

            if courses.count() == 0:
                continue

            total_students = (
                Enrollment.objects.filter(course__in=courses)
                .values("student")
                .distinct()
                .count()
            )

            rating_data = CourseReview.objects.filter(course__in=courses).aggregate(
                avg_rating=Avg("rating"),
                total_reviews=Count("id"),
            )

            instructors_data.append(
                {
                    "id": teacher.id,
                    "full_name": (teacher.full_name or teacher.email),
                    "headline": (teacher.headline or ""),
                    "avatar_url": teacher.avatar_url,
                    "total_courses": courses.count(),
                    "total_students": total_students,
                    "average_rating": round(
                        rating_data["avg_rating"] or 0,
                        2,
                    ),
                    "total_reviews": (rating_data["total_reviews"] or 0),
                }
            )

        sort_by = request.query_params.get(
            "sort",
            "students",
        )

        if sort_by == "rating":
            instructors_data.sort(
                key=lambda item: (
                    item["average_rating"],
                    item["total_students"],
                ),
                reverse=True,
            )
        else:
            instructors_data.sort(
                key=lambda item: (
                    item["total_students"],
                    item["average_rating"],
                ),
                reverse=True,
            )

        return Response({"instructors": instructors_data[:10]})
