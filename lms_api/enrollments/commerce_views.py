"""Các API mua khóa học và lịch sử thanh toán."""

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course

from .models import Enrollment, Payment
from .serializers import PaymentHistorySerializer


class PurchaseCourseAPIView(APIView):
    """Đăng ký học thử hoặc mua khóa học."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id):
        """Xử lý đăng ký audit hoặc paid."""

        if request.user.role != "student":
            return Response(
                {"detail": ("Only students can purchase courses.")},
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

        if course.teacher == request.user:
            return Response(
                {"detail": ("You cannot purchase your own course.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        mode = request.data.get("mode", "paid")

        if mode not in ["audit", "paid"]:
            return Response(
                {"detail": ('Mode must be "audit" or "paid".')},
                status=status.HTTP_400_BAD_REQUEST,
            )

        existing = Enrollment.objects.filter(
            student=request.user,
            course=course,
        ).first()

        if existing and existing.enrollment_type == "paid":
            return Response(
                {
                    "message": "Already purchased",
                    "already_enrolled": True,
                    "enrollment_type": "paid",
                },
                status=status.HTTP_200_OK,
            )

        if existing and existing.enrollment_type == "audit" and mode == "paid":
            existing.enrollment_type = "paid"
            existing.price_paid = course.price or 0
            existing.save()

            Payment.objects.create(
                user=request.user,
                course=course,
                enrollment=existing,
                amount=existing.price_paid,
                currency="USD",
                status="succeeded",
                source="upgrade",
            )

            return Response(
                {
                    "message": ("Upgraded to paid enrollment"),
                    "already_enrolled": True,
                    "enrollment_type": "paid",
                },
                status=status.HTTP_200_OK,
            )

        if mode == "audit" and not existing:
            enrollment = Enrollment.objects.create(
                student=request.user,
                course=course,
                enrollment_type="audit",
                price_paid=0,
                progress_percent=0,
            )

            return Response(
                {
                    "message": "Enrolled as audit",
                    "already_enrolled": False,
                    "enrollment_type": "audit",
                },
                status=status.HTTP_201_CREATED,
            )

        if mode == "paid" and not existing:
            enrollment = Enrollment.objects.create(
                student=request.user,
                course=course,
                enrollment_type="paid",
                price_paid=course.price or 0,
                progress_percent=0,
            )

            Payment.objects.create(
                user=request.user,
                course=course,
                enrollment=enrollment,
                amount=enrollment.price_paid,
                currency="USD",
                status="succeeded",
                source="single",
            )

            return Response(
                {
                    "message": ("Course purchased successfully"),
                    "already_enrolled": False,
                    "enrollment_type": "paid",
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"detail": "Invalid enrollment state."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class PaymentHistoryListAPIView(APIView):
    """Trả về lịch sử thanh toán của người dùng."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Lấy các giao dịch theo thời gian mới nhất."""

        queryset = (
            Payment.objects.filter(user=request.user)
            .select_related("course")
            .order_by("-created_at")
        )

        serializer = PaymentHistorySerializer(
            queryset,
            many=True,
        )

        return Response(serializer.data)
