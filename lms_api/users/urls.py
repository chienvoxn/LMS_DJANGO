"""Khai báo URL cho tài khoản và hồ sơ người dùng."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .auth_views import (
    CustomTokenObtainPairView,
    InstructorPublicProfileAPIView,
    MeAPIView,
    RegisterView,
    TopInstructorsAPIView,
)
from .viewsets import UserViewSet

router = DefaultRouter()

router.register(
    r"",
    UserViewSet,
    basename="user",
)


urlpatterns = [
    # Xác thực
    path(
        "auth/register/",
        RegisterView.as_view(),
        name="auth-register",
    ),
    path(
        "auth/login/",
        CustomTokenObtainPairView.as_view(),
        name="auth-login",
    ),
    path(
        "auth/refresh/",
        TokenRefreshView.as_view(),
        name="auth-refresh",
    ),
    path(
        "auth/me/",
        MeAPIView.as_view(),
        name="auth-me",
    ),
    # Hồ sơ công khai của giảng viên
    path(
        "instructors/<int:instructor_id>/profile/",
        InstructorPublicProfileAPIView.as_view(),
        name="instructor-public-profile",
    ),
    path(
        "instructors/top/",
        TopInstructorsAPIView.as_view(),
        name="top-instructors",
    ),
    # API do UserViewSet cung cấp
    path(
        "",
        include(router.urls),
    ),
]
