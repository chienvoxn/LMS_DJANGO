"""Khai báo URL gốc của hệ thống LMS."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from enrollments.views import (
    RemoveStudentFromCourseView,
    StudentMyCoursesAPIView,
    TeacherCourseStudentsView,
)
from users.auth_views import (
    ChangePasswordAPIView,
    CustomTokenObtainPairView,
    MeAPIView,
    RegisterView,
    StudentPublicProfileAPIView,
)

urlpatterns = [
    # =====================================================
    # Django Admin
    # =====================================================
    path(
        "admin/",
        admin.site.urls,
    ),
    # =====================================================
    # Xác thực
    # =====================================================
    path(
        "api/auth/register/",
        RegisterView.as_view(),
        name="auth-register",
    ),
    path(
        "api/auth/login/",
        CustomTokenObtainPairView.as_view(),
        name="auth-login",
    ),
    path(
        "api/auth/refresh/",
        TokenRefreshView.as_view(),
        name="auth-refresh",
    ),
    path(
        "api/auth/me/",
        MeAPIView.as_view(),
        name="auth-me",
    ),
    path(
        "api/auth/change-password/",
        ChangePasswordAPIView.as_view(),
        name="auth-change-password",
    ),
    # =====================================================
    # API của các ứng dụng
    # =====================================================
    path(
        "api/users/",
        include("users.urls"),
    ),
    path(
        "api/",
        include("courses.urls"),
    ),
    path(
        "api/enrollments/",
        include("enrollments.urls"),
    ),
    path(
        "api/",
        include("assessments.urls"),
    ),
    path(
        "api/",
        include("reviews.urls"),
    ),
    path(
        "api/",
        include("analytics.urls"),
    ),
    path(
        "api/",
        include("chat.urls"),
    ),
    # =====================================================
    # API dành cho học viên
    # =====================================================
    path(
        "api/student/my-courses/",
        StudentMyCoursesAPIView.as_view(),
        name="student-my-courses",
    ),
    path(
        "api/students/<int:student_id>/profile/",
        StudentPublicProfileAPIView.as_view(),
        name="student-public-profile",
    ),
    # =====================================================
    # Giảng viên quản lý học viên
    # =====================================================
    path(
        ("api/teacher/courses/" "<int:course_id>/students/"),
        TeacherCourseStudentsView.as_view(),
        name="teacher-course-students",
    ),
    path(
        ("api/teacher/courses/" "<int:course_id>/students/" "<int:student_id>/"),
        RemoveStudentFromCourseView.as_view(),
        name="teacher-course-student-remove",
    ),
]


# Phục vụ media trực tiếp trong môi trường development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
