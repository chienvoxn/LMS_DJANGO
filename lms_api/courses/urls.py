"""Khai báo URL cho khóa học, chương học và bài học."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from enrollments.views import (
    CompleteLessonAPIView,
    EnrollCourseAPIView,
    IssueCertificateAPIView,
    MyCertificateAPIView,
    MyCertificatesListAPIView,
    PurchaseCourseAPIView,
)

from .teacher_views import (
    TeacherCourseViewSet,
    TeacherLessonViewSet,
    TeacherSectionViewSet,
)
from .views import (
    CourseCategoriesListAPIView,
    CourseCurriculumAPIView,
    CourseViewSet,
    LessonDetailAPIView,
)

# Router dành cho API công khai
router = DefaultRouter()
router.register(
    r"courses",
    CourseViewSet,
    basename="course",
)


# Router dành cho giảng viên
teacher_router = DefaultRouter()
teacher_router.register(
    r"teacher/courses",
    TeacherCourseViewSet,
    basename="teacher-courses",
)
teacher_router.register(
    r"teacher/sections",
    TeacherSectionViewSet,
    basename="teacher-sections",
)
teacher_router.register(
    r"teacher/lessons",
    TeacherLessonViewSet,
    basename="teacher-lessons",
)


urlpatterns = [
    # Danh mục và chương trình khóa học
    path(
        "courses/categories/",
        CourseCategoriesListAPIView.as_view(),
        name="course-categories",
    ),
    path(
        "courses/<int:pk>/curriculum/",
        CourseCurriculumAPIView.as_view(),
        name="course-curriculum",
    ),
    # Đăng ký và mua khóa học
    path(
        "courses/<int:course_id>/enroll/",
        EnrollCourseAPIView.as_view(),
        name="course-enroll",
    ),
    path(
        "courses/<int:course_id>/purchase/",
        PurchaseCourseAPIView.as_view(),
        name="course-purchase",
    ),
    # Chứng chỉ
    path(
        "courses/<int:course_id>/certificate/issue/",
        IssueCertificateAPIView.as_view(),
        name="certificate-issue",
    ),
    path(
        "courses/<int:course_id>/certificate/me/",
        MyCertificateAPIView.as_view(),
        name="certificate-me",
    ),
    # Bài học và tiến độ
    path(
        "lessons/<int:pk>/",
        LessonDetailAPIView.as_view(),
        name="lesson-detail",
    ),
    path(
        "lessons/<int:lesson_id>/complete/",
        CompleteLessonAPIView.as_view(),
        name="lesson-complete",
    ),
    # Các endpoint do router tạo
    path("", include(router.urls)),
    path("", include(teacher_router.urls)),
]
