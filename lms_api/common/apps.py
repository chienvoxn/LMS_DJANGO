from django.apps import AppConfig


class CommonConfig(AppConfig):
    """Cấu hình ứng dụng chứa các thành phần dùng chung."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "common"
