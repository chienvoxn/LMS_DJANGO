"""Các serializer quản lý tài khoản và hồ sơ người dùng."""

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Định dạng thông tin đầy đủ của người dùng."""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "role",
            "avatar_url",
            "bio",
            "headline",
            "country",
            "language",
            "date_joined",
            "last_login",
        ]
        read_only_fields = [
            "id",
            "date_joined",
            "last_login",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    """Kiểm tra dữ liệu đăng ký tài khoản."""

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password_confirm",
            "full_name",
            "role",
        ]

    def validate_email(self, value):
        """Kiểm tra email chưa được sử dụng."""

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")

        return value

    def validate(self, attrs):
        """Kiểm tra hai mật khẩu trùng khớp."""

        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password": ("Passwords do not match.")})

        return attrs

    def create(self, validated_data):
        """Tạo tài khoản với mật khẩu đã được mã hóa."""

        validated_data.pop("password_confirm")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data,
        )

        return user


# Giữ tên cũ để tương thích với các import hiện tại.
UserRegisterSerializer = RegisterSerializer


class ProfileSerializer(serializers.ModelSerializer):
    """Định dạng hồ sơ công khai và hồ sơ chỉnh sửa."""

    social_links = serializers.JSONField(
        required=False,
        allow_null=True,
    )
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "avatar_url",
            "full_name",
            "headline",
            "bio",
            "country",
            "social_links",
            "date_joined",
        ]
        read_only_fields = [
            "id",
            "date_joined",
        ]

    def validate_social_links(self, value):
        """Chuẩn hóa cấu trúc liên kết mạng xã hội."""

        if value is None:
            return {
                "facebook": "",
                "linkedin": "",
                "github": "",
                "website": "",
            }

        if not isinstance(value, dict):
            raise serializers.ValidationError("social_links must be a dictionary")

        default_links = {
            "facebook": "",
            "linkedin": "",
            "github": "",
            "website": "",
        }

        for key in default_links:
            if key not in value:
                value[key] = ""

        return value


# Export lại để giữ tương thích với code cũ.
from .public_profile_serializers import (  # noqa: E402
    InstructorPublicProfileSerializer,
    StudentPublicProfileSerializer,
)

__all__ = [
    "UserSerializer",
    "RegisterSerializer",
    "UserRegisterSerializer",
    "ProfileSerializer",
    "StudentPublicProfileSerializer",
    "InstructorPublicProfileSerializer",
]
