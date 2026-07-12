from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AssignmentDetailAPIView,
    AssignmentMySubmissionAPIView,
    AssignmentSubmitAPIView,
    ChoiceCreateAPIView,
    ChoiceDetailAPIView,
    CourseAssignmentsListAPIView,
    CourseQuizzesListAPIView,
    QuestionCreateAPIView,
    QuestionDetailAPIView,
    QuizAttemptsMeAPIView,
    QuizDetailAPIView,
    QuizStartAPIView,
    QuizSubmitAPIView,
    SubmissionGradeAPIView,
    TeacherAssignmentViewSet,
    TeacherQuizViewSet,
    upload_file_view,
)

teacher_router = DefaultRouter()

teacher_router.register(
    r"teacher/quizzes",
    TeacherQuizViewSet,
    basename="teacher-quizzes",
)
teacher_router.register(
    r"teacher/assignments",
    TeacherAssignmentViewSet,
    basename="teacher-assignments",
)


urlpatterns = [
    # Router dành cho giảng viên
    path("", include(teacher_router.urls)),
    # Giảng viên quản lý câu hỏi và phương án
    path(
        "teacher/quizzes/<int:quiz_id>/questions/",
        QuestionCreateAPIView.as_view(),
        name="question-create",
    ),
    path(
        "teacher/questions/<int:pk>/",
        QuestionDetailAPIView.as_view(),
        name="question-detail",
    ),
    path(
        "teacher/questions/<int:question_id>/choices/",
        ChoiceCreateAPIView.as_view(),
        name="choice-create",
    ),
    path(
        "teacher/choices/<int:pk>/",
        ChoiceDetailAPIView.as_view(),
        name="choice-detail",
    ),
    # Giảng viên quản lý bài nộp
    path(
        "teacher/assignments/<int:pk>/submissions/",
        TeacherAssignmentViewSet.as_view({"get": "submissions"}),
        name="assignment-submissions",
    ),
    path(
        "teacher/submissions/<int:pk>/grade/",
        SubmissionGradeAPIView.as_view(),
        name="submission-grade",
    ),
    # Học viên làm bài kiểm tra
    path(
        "courses/<int:course_id>/quizzes/",
        CourseQuizzesListAPIView.as_view(),
        name="course-quizzes",
    ),
    path(
        "quizzes/<int:pk>/",
        QuizDetailAPIView.as_view(),
        name="quiz-detail",
    ),
    path(
        "quizzes/<int:pk>/start/",
        QuizStartAPIView.as_view(),
        name="quiz-start",
    ),
    path(
        "quizzes/<int:pk>/submit/",
        QuizSubmitAPIView.as_view(),
        name="quiz-submit",
    ),
    path(
        "quizzes/<int:pk>/attempts/me/",
        QuizAttemptsMeAPIView.as_view(),
        name="quiz-attempts-me",
    ),
    # Học viên làm bài tập
    path(
        "courses/<int:course_id>/assignments/",
        CourseAssignmentsListAPIView.as_view(),
        name="course-assignments",
    ),
    path(
        "assignments/<int:pk>/",
        AssignmentDetailAPIView.as_view(),
        name="assignment-detail",
    ),
    path(
        "assignments/<int:pk>/submit/",
        AssignmentSubmitAPIView.as_view(),
        name="assignment-submit",
    ),
    path(
        "assignments/<int:pk>/my-submission/",
        AssignmentMySubmissionAPIView.as_view(),
        name="assignment-my-submission",
    ),
    # Upload file
    path(
        "upload/",
        upload_file_view,
        name="upload-file",
    ),
]
