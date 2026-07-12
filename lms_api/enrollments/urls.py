"""Khai báo URL cho đăng ký, thanh toán và giỏ hàng."""

from django.urls import path

from .cart_views import (
    CartAddAPIView,
    CartCheckoutAPIView,
    CartItemDeleteAPIView,
    CartListAPIView,
)
from .views import (
    CompleteLessonAPIView,
    MyCertificatesListAPIView,
    MyEnrollmentsListAPIView,
    PaymentHistoryListAPIView,
    StudentMyCoursesAPIView,
)

urlpatterns = [
    # Thông tin đăng ký của người dùng
    path(
        "me/",
        MyEnrollmentsListAPIView.as_view(),
        name="my-enrollments",
    ),
    path(
        "me/certificates/",
        MyCertificatesListAPIView.as_view(),
        name="my-certificates",
    ),
    path(
        "me/payments/",
        PaymentHistoryListAPIView.as_view(),
        name="payment-history",
    ),
    # Giỏ hàng
    path(
        "cart/",
        CartListAPIView.as_view(),
        name="cart-list",
    ),
    path(
        "cart/add/",
        CartAddAPIView.as_view(),
        name="cart-add",
    ),
    path(
        "cart/items/<int:item_id>/",
        CartItemDeleteAPIView.as_view(),
        name="cart-item-delete",
    ),
    path(
        "cart/checkout/",
        CartCheckoutAPIView.as_view(),
        name="cart-checkout",
    ),
]
