"""Các API quản lý giỏ hàng khóa học."""

from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course

from .models import CartItem, Enrollment, Payment
from .serializers import CartItemSerializer


class CartListAPIView(APIView):
    """Trả về giỏ hàng của người dùng hiện tại."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Lấy danh sách, tổng tiền và số lượng sản phẩm."""

        items = CartItem.objects.filter(user=request.user).select_related("course")

        serializer = CartItemSerializer(
            items,
            many=True,
        )

        subtotal = sum([item.price_at_add for item in items])

        return Response(
            {
                "items": serializer.data,
                "subtotal": float(subtotal),
                "count": len(serializer.data),
            }
        )


class CartAddAPIView(APIView):
    """Thêm khóa học vào giỏ hàng."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Kiểm tra điều kiện và thêm khóa học."""

        user = request.user

        if user.role != "student":
            return Response(
                {"detail": ("Only students can add courses to cart.")},
                status=status.HTTP_403_FORBIDDEN,
            )

        course_id = request.data.get("course_id")

        if not course_id:
            return Response(
                {"detail": "course_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        course = get_object_or_404(
            Course,
            id=course_id,
            is_published=True,
        )

        if course.teacher_id == user.id:
            return Response(
                {"detail": ("You cannot add your own course to cart.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Enrollment.objects.filter(
            student=user,
            course=course,
            enrollment_type="paid",
        ).exists():
            return Response(
                {"detail": ("You already own this course.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            course=course,
            defaults={"price_at_add": course.price or 0},
        )

        if not created:
            return Response(
                {
                    "message": "Already in cart",
                    "already_in_cart": True,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "message": "Added to cart",
                "already_in_cart": False,
            },
            status=status.HTTP_201_CREATED,
        )


class CartItemDeleteAPIView(APIView):
    """Xóa một khóa học khỏi giỏ hàng."""

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, item_id):
        """Chỉ xóa mục thuộc người dùng hiện tại."""

        item = get_object_or_404(
            CartItem,
            id=item_id,
            user=request.user,
        )

        item.delete()

        return Response(
            {"message": "Item removed from cart"},
            status=status.HTTP_204_NO_CONTENT,
        )


class CartCheckoutAPIView(APIView):
    """Thanh toán toàn bộ hoặc một phần giỏ hàng."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Tạo đăng ký paid và giao dịch thanh toán."""

        user = request.user

        if user.role != "student":
            return Response(
                {"detail": ("Only students can checkout.")},
                status=status.HTTP_403_FORBIDDEN,
            )

        item_ids = request.data.get("item_ids", [])

        if item_ids:
            items = CartItem.objects.filter(
                user=user,
                id__in=item_ids,
            ).select_related("course")
        else:
            items = CartItem.objects.filter(user=user).select_related("course")

        if not items.exists():
            return Response(
                {"detail": "No items to checkout."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        created = []
        skipped = []

        for item in items:
            course = item.course

            if Enrollment.objects.filter(
                student=user,
                course=course,
                enrollment_type="paid",
            ).exists():
                skipped.append(course.id)
                continue

            enrollment = Enrollment.objects.create(
                student=user,
                course=course,
                enrollment_type="paid",
                price_paid=item.price_at_add,
            )

            Payment.objects.create(
                user=user,
                course=course,
                enrollment=enrollment,
                amount=enrollment.price_paid,
                currency="USD",
                status="succeeded",
                source="cart",
            )

            created.append(course.id)

        items.delete()

        return Response(
            {
                "message": "Checkout completed.",
                "enrolled_courses": created,
                "already_owned_courses": skipped,
            },
            status=status.HTTP_200_OK,
        )
