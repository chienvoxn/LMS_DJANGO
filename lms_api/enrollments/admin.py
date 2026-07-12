"""Cấu hình Django Admin cho đăng ký và tiến độ."""

from django.contrib import admin

from .models import (
    CartItem,
    Certificate,
    Enrollment,
    LessonProgress,
)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """Quản lý đăng ký khóa học."""

    list_display = [
        "student",
        "course",
        "progress_percent",
        "created_at",
    ]
    list_filter = [
        "created_at",
        "course",
    ]
    search_fields = [
        "student__email",
        "course__title",
    ]
    readonly_fields = ["created_at"]


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    """Quản lý tiến độ bài học."""

    list_display = [
        "enrollment",
        "lesson",
        "is_completed",
    ]
    list_filter = [
        "is_completed",
        "enrollment__course",
    ]
    search_fields = [
        "enrollment__student__email",
        "lesson__title",
    ]


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    """Quản lý chứng chỉ."""

    list_display = [
        "user",
        "course",
        "certificate_code",
        "issued_at",
    ]
    list_filter = ["issued_at"]
    search_fields = [
        "user__email",
        "course__title",
        "certificate_code",
    ]
    readonly_fields = [
        "certificate_code",
        "issued_at",
    ]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Quản lý các mục trong giỏ hàng."""

    list_display = [
        "user",
        "course",
        "price_at_add",
        "created_at",
    ]
    list_filter = ["created_at"]
    search_fields = [
        "user__email",
        "course__title",
    ]
    readonly_fields = ["created_at"]
