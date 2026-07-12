"""ViewSet quản lý tài khoản và hồ sơ người dùng."""

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response

from .models import User
from .serializers import (
    ProfileSerializer,
    UserRegisterSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """Quản lý người dùng và các thao tác hồ sơ."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        """Chọn serializer theo action hiện tại."""

        if self.action == "register":
            return UserRegisterSerializer

        return UserSerializer

    @action(
        detail=False,
        methods=["post"],
        url_path="register",
    )
    def register(self, request):
        """Đăng ký một tài khoản mới."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=False,
        methods=["get"],
        url_path="me",
    )
    def me(self, request):
        """Trả về thông tin người dùng hiện tại."""

        if request.user.is_authenticated:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        return Response(
            {"detail": ("Authentication required.")},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    @action(
        detail=True,
        methods=["get"],
        url_path="profile",
        permission_classes=[AllowAny],
    )
    def profile(self, request, pk=None):
        """Trả về hồ sơ công khai của một người dùng."""

        user = get_object_or_404(
            User,
            id=pk,
        )

        serializer = ProfileSerializer(user)

        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get", "put", "patch"],
        url_path="me/profile",
        permission_classes=[IsAuthenticated],
    )
    def my_profile(self, request):
        """Xem hoặc cập nhật hồ sơ hiện tại."""

        user = request.user

        if request.method == "GET":
            serializer = ProfileSerializer(user)
            return Response(serializer.data)

        elif request.method in ["PUT", "PATCH"]:
            serializer = ProfileSerializer(
                user,
                data=request.data,
                partial=request.method == "PATCH",
            )

            if serializer.is_valid():
                serializer.save()

                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK,
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
