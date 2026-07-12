"""Tập hợp các API view của ứng dụng assessments."""

from .assignment_views import (
    AssignmentDetailAPIView,
    AssignmentMySubmissionAPIView,
    AssignmentSubmitAPIView,
    CourseAssignmentsListAPIView,
    SubmissionGradeAPIView,
    TeacherAssignmentViewSet,
)
from .quiz_views import (
    ChoiceCreateAPIView,
    ChoiceDetailAPIView,
    CourseQuizzesListAPIView,
    QuestionCreateAPIView,
    QuestionDetailAPIView,
    QuizAttemptsMeAPIView,
    QuizDetailAPIView,
    QuizStartAPIView,
    QuizSubmitAPIView,
    TeacherQuizViewSet,
)
from .upload_views import upload_file_view

__all__ = [
    # Quiz dành cho giảng viên
    "TeacherQuizViewSet",
    "QuestionCreateAPIView",
    "QuestionDetailAPIView",
    "ChoiceCreateAPIView",
    "ChoiceDetailAPIView",
    # Quiz dành cho học viên
    "CourseQuizzesListAPIView",
    "QuizDetailAPIView",
    "QuizStartAPIView",
    "QuizSubmitAPIView",
    "QuizAttemptsMeAPIView",
    # Bài tập dành cho giảng viên
    "TeacherAssignmentViewSet",
    "SubmissionGradeAPIView",
    # Bài tập dành cho học viên
    "CourseAssignmentsListAPIView",
    "AssignmentDetailAPIView",
    "AssignmentSubmitAPIView",
    "AssignmentMySubmissionAPIView",
    # Upload file
    "upload_file_view",
]
