"""Cấu hình quản lý khóa học trong Django Admin."""

from django.contrib import admin

from .models import Course, Lesson, Section


class LessonInline(admin.TabularInline):
    """Hiển thị bài học trực tiếp trong trang quản lý chương."""

    model = Lesson
    extra = 1
    ordering = ["sort_order"]


class SectionInline(admin.TabularInline):
    """Hiển thị chương trực tiếp trong trang quản lý khóa học."""

    model = Section
    extra = 1
    ordering = ["sort_order"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Cấu hình trang quản lý khóa học."""

    list_display = [
        "title",
        "teacher",
        "level",
        "price",
        "is_published",
        "created_at",
    ]
    list_filter = [
        "level",
        "is_published",
        "category",
        "created_at",
    ]
    search_fields = [
        "title",
        "subtitle",
        "description",
    ]
    inlines = [SectionInline]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    """Cấu hình trang quản lý chương học."""

    list_display = [
        "title",
        "course",
        "sort_order",
    ]
    list_filter = ["course"]
    search_fields = ["title"]
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Cấu hình trang quản lý bài học."""

    list_display = [
        "title",
        "section",
        "duration",
        "sort_order",
    ]
    list_filter = ["section__course"]
    search_fields = ["title"]
