"""Tập hợp các API view của ứng dụng enrollments."""

from .certificate_views import (
    IssueCertificateAPIView,
    MyCertificateAPIView,
    MyCertificatesListAPIView,
)
from .commerce_views import (
    PaymentHistoryListAPIView,
    PurchaseCourseAPIView,
)
from .student_views import (
    CompleteLessonAPIView,
    EnrollCourseAPIView,
    MyEnrollmentsListAPIView,
    StudentMyCoursesAPIView,
)
from .teacher_views import (
    RemoveStudentFromCourseView,
    TeacherCourseStudentsView,
)

__all__ = [
    # Đăng ký và tiến độ học tập
    "EnrollCourseAPIView",
    "MyEnrollmentsListAPIView",
    "CompleteLessonAPIView",
    "StudentMyCoursesAPIView",
    # Quản lý học viên
    "TeacherCourseStudentsView",
    "RemoveStudentFromCourseView",
    # Mua khóa học và thanh toán
    "PurchaseCourseAPIView",
    "PaymentHistoryListAPIView",
    # Chứng chỉ
    "IssueCertificateAPIView",
    "MyCertificateAPIView",
    "MyCertificatesListAPIView",
]
