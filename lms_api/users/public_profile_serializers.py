"""Serializer cho hồ sơ công khai của học viên và giảng viên."""

from rest_framework import serializers


class StudentPublicProfileSerializer(serializers.Serializer):
    """Hồ sơ công khai và thống kê của học viên."""

    id = serializers.IntegerField()
    full_name = serializers.CharField(allow_blank=True)
    avatar_url = serializers.URLField(
        allow_null=True,
        allow_blank=True,
    )
    bio = serializers.CharField(allow_blank=True)
    country = serializers.CharField(allow_blank=True)
    language = serializers.CharField()

    social_links = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()

    def get_social_links(self, obj):
        """Trả về các liên kết mạng xã hội."""

        if hasattr(obj, "social_links"):
            if isinstance(obj.social_links, dict):
                return obj.social_links

            if isinstance(obj.social_links, str):
                import json

                try:
                    return json.loads(obj.social_links)
                except:
                    return {}

        return {
            "linkedin": "",
            "facebook": "",
            "github": "",
        }

    def get_stats(self, obj):
        """Tính các chỉ số học tập của học viên."""

        from assessments.models import (
            StudentQuizAttempt,
            Submission,
        )
        from courses.models import Lesson
        from django.db.models import Count, Q
        from enrollments.models import (
            Enrollment,
            LessonProgress,
        )
        from reviews.models import CourseReview

        enrollments = Enrollment.objects.filter(student=obj)
        total_enrolled_courses = enrollments.count()

        completed_courses_count = 0

        enrollments_with_progress = enrollments.select_related(
            "course"
        ).prefetch_related("lesson_progresses")

        for enrollment in enrollments_with_progress:
            course = enrollment.course

            total_lessons = Lesson.objects.filter(section__course=course).count()

            if total_lessons > 0:
                completed_lessons = LessonProgress.objects.filter(
                    enrollment=enrollment,
                    is_completed=True,
                ).count()

                if completed_lessons >= total_lessons:
                    completed_courses_count += 1

        total_reviews = CourseReview.objects.filter(user=obj).count()

        total_quiz_attempts = StudentQuizAttempt.objects.filter(student=obj).count()

        total_assignments_submitted = Submission.objects.filter(student=obj).count()

        member_since = obj.date_joined.date().isoformat() if obj.date_joined else None

        return {
            "total_enrolled_courses": (total_enrolled_courses),
            "total_completed_courses": (completed_courses_count),
            "total_reviews": total_reviews,
            "total_quiz_attempts": (total_quiz_attempts),
            "total_assignments_submitted": (total_assignments_submitted),
            "member_since": member_since,
        }

    def get_courses(self, obj):
        """Trả về các khóa học và tiến độ tương ứng."""

        from courses.models import Lesson
        from enrollments.models import (
            Enrollment,
            LessonProgress,
        )

        enrollments = (
            Enrollment.objects.filter(student=obj)
            .select_related("course")
            .prefetch_related("lesson_progresses__lesson")
            .order_by("-created_at")
        )

        courses_data = []

        for enrollment in enrollments:
            course = enrollment.course

            total_lessons = Lesson.objects.filter(section__course=course).count()

            completed_lessons = LessonProgress.objects.filter(
                enrollment=enrollment,
                is_completed=True,
            ).count()

            if total_lessons > 0:
                progress_percentage = round(
                    (completed_lessons / total_lessons) * 100,
                    2,
                )
            else:
                progress_percentage = 0.0

            course_data = {
                "course_id": course.id,
                "title": course.title,
                "thumbnail_url": (course.thumbnail_url or None),
                "progress_percentage": (progress_percentage),
                "enrolled_at": (
                    enrollment.created_at.isoformat() if enrollment.created_at else None
                ),
                "completed_lessons": completed_lessons,
                "total_lessons": total_lessons,
            }

            courses_data.append(course_data)

        return courses_data


class InstructorPublicProfileSerializer(serializers.Serializer):
    """Hồ sơ công khai và thống kê của giảng viên."""

    id = serializers.IntegerField()
    full_name = serializers.CharField(allow_blank=True)
    headline = serializers.CharField(allow_blank=True)
    bio = serializers.CharField(allow_blank=True)
    avatar_url = serializers.URLField(
        allow_null=True,
        allow_blank=True,
    )
    country = serializers.CharField(allow_blank=True)

    social_links = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()

    def get_social_links(self, obj):
        """Trả về các liên kết mạng xã hội."""

        if hasattr(obj, "social_links") and obj.social_links:
            if isinstance(obj.social_links, dict):
                return obj.social_links

            if isinstance(obj.social_links, str):
                import json

                try:
                    return json.loads(obj.social_links)
                except:
                    return {}

        return {
            "facebook": "",
            "linkedin": "",
            "github": "",
            "website": "",
        }

    def get_stats(self, obj):
        """Tính các chỉ số tổng quan của giảng viên."""

        from courses.models import Course
        from django.db.models import Avg, Count
        from enrollments.models import Enrollment
        from reviews.models import CourseReview

        instructor_courses = Course.objects.filter(teacher=obj)

        total_courses = instructor_courses.count()

        total_enrollments = Enrollment.objects.filter(
            course__in=instructor_courses
        ).count()

        total_students = (
            Enrollment.objects.filter(course__in=instructor_courses)
            .values("student")
            .distinct()
            .count()
        )

        rating_data = CourseReview.objects.filter(
            course__in=instructor_courses
        ).aggregate(
            avg_rating=Avg("rating"),
            total_reviews=Count("id"),
        )

        member_since = obj.date_joined.date().isoformat() if obj.date_joined else None

        return {
            "total_students": total_students,
            "total_enrollments": total_enrollments,
            "total_reviews": (rating_data["total_reviews"] or 0),
            "average_rating": (
                round(rating_data["avg_rating"], 2)
                if rating_data["avg_rating"]
                else 0.0
            ),
            "total_courses": total_courses,
            "member_since": member_since,
        }

    def get_courses(self, obj):
        """Trả về khóa học và thống kê của giảng viên."""

        from courses.models import Course
        from django.db.models import Avg, Count
        from enrollments.models import Enrollment
        from reviews.models import CourseReview

        courses = Course.objects.filter(teacher=obj).select_related("teacher")

        course_ids = list(courses.values_list("id", flat=True))

        enrollments_data = (
            Enrollment.objects.filter(course_id__in=course_ids)
            .values("course_id")
            .annotate(total_students=Count("id"))
        )

        enrollments_map = {
            item["course_id"]: item["total_students"] for item in enrollments_data
        }

        reviews_data = (
            CourseReview.objects.filter(course_id__in=course_ids)
            .values("course_id")
            .annotate(
                avg_rating=Avg("rating"),
                total_reviews=Count("id"),
            )
        )

        reviews_map = {
            item["course_id"]: {
                "avg_rating": (
                    round(item["avg_rating"], 2) if item["avg_rating"] else 0.0
                ),
                "total_reviews": (item["total_reviews"] or 0),
            }
            for item in reviews_data
        }

        courses_data = []

        for course in courses:
            course_id = course.id

            review_info = reviews_map.get(
                course_id,
                {
                    "avg_rating": 0.0,
                    "total_reviews": 0,
                },
            )

            courses_data.append(
                {
                    "course_id": course.id,
                    "title": course.title,
                    "thumbnail_url": (course.thumbnail_url or None),
                    "rating": (review_info["avg_rating"]),
                    "total_reviews": (review_info["total_reviews"]),
                    "total_students": (
                        enrollments_map.get(
                            course_id,
                            0,
                        )
                    ),
                }
            )

        return courses_data
