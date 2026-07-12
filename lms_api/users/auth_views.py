"""Các API đăng ký, đăng nhập và bảo mật tài khoản."""

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import (
    validate_password,
)
from django.core.exceptions import ValidationError
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from .serializers import (
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Đăng ký tài khoản và trả về cặp JWT."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """Kiểm tra dữ liệu, tạo tài khoản và token."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": UserSerializer(user).data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status=status.HTTP_201_CREATED,
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    """Đăng nhập bằng địa chỉ email."""

    def post(self, request, *args, **kwargs):
        """Ánh xạ email sang trường SimpleJWT sử dụng."""

        if "email" in request.data:
            request.data["username"] = request.data["email"]

        return super().post(
            request,
            *args,
            **kwargs,
        )


class MeAPIView(generics.RetrieveAPIView):
    """Trả về người dùng đang đăng nhập."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Lấy tài khoản từ request hiện tại."""

        return self.request.user


class ChangePasswordAPIView(APIView):
    """Thay đổi mật khẩu của người dùng hiện tại."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Kiểm tra và lưu mật khẩu mới."""

        user = request.user

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password:
            return Response(
                {"old_password": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not new_password:
            return Response(
                {"new_password": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.check_password(old_password):
            return Response(
                {"old_password": ["Current password is incorrect."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            validate_password(
                new_password,
                user,
            )

        except ValidationError as error:
            return Response(
                {"new_password": list(error.messages)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.check_password(new_password):
            return Response(
                {
                    "new_password": [
                        "New password must be " "different from current password."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"detail": ("Password changed successfully.")},
            status=status.HTTP_200_OK,
        )


# Export lại các view cũ để giữ tương thích.
from .public_profile_views import (  # noqa: E402
    InstructorPublicProfileAPIView,
    StudentPublicProfileAPIView,
    TopInstructorsAPIView,
)

__all__ = [
    "RegisterView",
    "CustomTokenObtainPairView",
    "MeAPIView",
    "ChangePasswordAPIView",
    "StudentPublicProfileAPIView",
    "InstructorPublicProfileAPIView",
    "TopInstructorsAPIView",
]
