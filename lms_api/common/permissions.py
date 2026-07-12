"""Các quyền truy cập dùng chung trong hệ thống."""

from rest_framework import permissions


class IsTeacher(permissions.BasePermission):
    """Chỉ cho phép người dùng có vai trò giảng viên truy cập."""

    def has_permission(self, request, view):
        """Kiểm tra người dùng đã đăng nhập và là giảng viên."""

        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "teacher"
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Cho phép mọi người đọc dữ liệu.

    Chỉ chủ sở hữu của đối tượng mới được phép chỉnh sửa.
    Đối tượng được kiểm tra phải có thuộc tính `teacher`.
    """

    def has_object_permission(self, request, view, obj):
        """Kiểm tra quyền đọc hoặc quyền sở hữu đối tượng."""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.teacher == request.user
