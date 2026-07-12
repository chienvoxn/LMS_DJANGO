"""Các API cấp và xem chứng chỉ."""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course, Lesson

from .models import Certificate, Enrollment, LessonProgress


class IssueCertificateAPIView(APIView):
    """Cấp chứng chỉ cho khóa học trả phí đã hoàn thành."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id):
        """Kiểm tra điều kiện và cấp chứng chỉ."""

        if request.user.role != "student":
            return Response(
                {"detail": ("Only students can request certificates.")},
                status=status.HTTP_403_FORBIDDEN,
            )

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

        try:
            enrollment = Enrollment.objects.get(
                student=request.user,
                course=course,
                enrollment_type="paid",
            )
        except Enrollment.DoesNotExist:
            return Response(
                {"detail": ("Certificate only for paid enrollments.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        existing_certificate = Certificate.objects.filter(
            user=request.user,
            course=course,
        ).first()

        if existing_certificate:
            return Response(
                {
                    "certificate_id": (existing_certificate.id),
                    "certificate_code": (existing_certificate.certificate_code),
                    "course_title": course.title,
                    "issued_at": (existing_certificate.issued_at),
                    "student_name": (request.user.full_name or request.user.email),
                },
                status=status.HTTP_200_OK,
            )

        total_lessons = Lesson.objects.filter(section__course=course).count()

        completed_lessons = LessonProgress.objects.filter(
            enrollment=enrollment,
            is_completed=True,
        ).count()

        if total_lessons == 0:
            return Response(
                {"detail": "Course has no lessons."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if completed_lessons < total_lessons:
            return Response(
                {"detail": "Course not completed yet."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        certificate = Certificate.objects.create(
            user=request.user,
            course=course,
            enrollment=enrollment,
        )

        enrollment.granted_certificate = True
        enrollment.save()

        return Response(
            {
                "certificate_id": certificate.id,
                "certificate_code": (certificate.certificate_code),
                "course_title": course.title,
                "issued_at": certificate.issued_at,
                "student_name": (request.user.full_name or request.user.email),
            },
            status=status.HTTP_201_CREATED,
        )


class MyCertificateAPIView(APIView):
    """Trả về chứng chỉ của người dùng theo khóa học."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, course_id):
        """Tìm chứng chỉ theo người dùng và khóa học."""

        try:
            certificate = Certificate.objects.get(
                user=request.user,
                course_id=course_id,
            )

            return Response(
                {
                    "certificate_id": certificate.id,
                    "certificate_code": (certificate.certificate_code),
                    "course_title": (certificate.course.title),
                    "issued_at": certificate.issued_at,
                    "student_name": (request.user.full_name or request.user.email),
                },
                status=status.HTTP_200_OK,
            )

        except Certificate.DoesNotExist:
            return Response(
                {"detail": "Certificate not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class MyCertificatesListAPIView(generics.ListAPIView):
    """Trả về toàn bộ chứng chỉ của người dùng."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Sắp xếp chứng chỉ theo thời gian cấp mới nhất."""

        certificates = (
            Certificate.objects.filter(user=request.user)
            .select_related(
                "course",
                "enrollment",
            )
            .order_by("-issued_at")
        )

        result = []

        for certificate in certificates:
            result.append(
                {
                    "certificate_id": certificate.id,
                    "certificate_code": (certificate.certificate_code),
                    "course_id": certificate.course.id,
                    "course_title": (certificate.course.title),
                    "issued_at": certificate.issued_at,
                    "student_name": (request.user.full_name or request.user.email),
                }
            )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )
