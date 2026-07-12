from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import IsTeacher

from .serializers import (
    TeacherAnalyticsSummarySerializer,
    TeacherCourseStatsSerializer,
)
from .services import (
    get_teacher_course_stats,
    get_teacher_engagement,
    get_teacher_summary,
    get_teacher_time_series,
)


class TeacherAnalyticsSummaryView(generics.GenericAPIView):
    """Trả về thống kê tổng quan của giảng viên."""

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeacher,
    ]

    def get(self, request, *args, **kwargs):
        summary_data = get_teacher_summary(request.user)
        serializer = TeacherAnalyticsSummarySerializer(summary_data)
        return Response(serializer.data)


class TeacherAnalyticsCoursesView(generics.GenericAPIView):
    """Trả về thống kê theo từng khóa học."""

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeacher,
    ]

    def get(self, request, *args, **kwargs):
        courses_data = get_teacher_course_stats(request.user)
        serializer = TeacherCourseStatsSerializer(
            courses_data,
            many=True,
        )
        return Response(serializer.data)


class TeacherAnalyticsTimeSeriesView(APIView):
    """Trả về thống kê theo tháng."""

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeacher,
    ]

    def get(self, request, *args, **kwargs):
        months = int(request.query_params.get("months", 6))
        result = get_teacher_time_series(
            request.user,
            months,
        )
        return Response(
            result,
            status=status.HTTP_200_OK,
        )


class TeacherAnalyticsEngagementView(APIView):
    """Trả về chỉ số tương tác học tập."""

    permission_classes = [
        permissions.IsAuthenticated,
        IsTeacher,
    ]

    def get(self, request, *args, **kwargs):
        result = get_teacher_engagement(request.user)
        return Response(
            result,
            status=status.HTTP_200_OK,
        )
