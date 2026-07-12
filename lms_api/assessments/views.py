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
    "TeacherQuizViewSet",
    "QuestionCreateAPIView",
    "QuestionDetailAPIView",
    "ChoiceCreateAPIView",
    "ChoiceDetailAPIView",
    "CourseQuizzesListAPIView",
    "QuizDetailAPIView",
    "QuizStartAPIView",
    "QuizSubmitAPIView",
    "QuizAttemptsMeAPIView",
    "TeacherAssignmentViewSet",
    "SubmissionGradeAPIView",
    "CourseAssignmentsListAPIView",
    "AssignmentDetailAPIView",
    "AssignmentSubmitAPIView",
    "AssignmentMySubmissionAPIView",
    "upload_file_view",
]
