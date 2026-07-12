from datetime import datetime, timezone as dt_timezone

from django.db.models import Avg, Count, Max, Q, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

from assessments.models import StudentQuizAttempt, Submission
from courses.models import Course
from enrollments.models import Certificate, Enrollment, LessonProgress
from reviews.models import CourseReview


def get_teacher_summary(teacher):
    """Lấy số liệu tổng quan của giảng viên."""

    teacher_courses = Course.objects.filter(teacher=teacher)

    total_courses = teacher_courses.count()

    total_enrollments = Enrollment.objects.filter(
        course__in=teacher_courses
    ).count()

    total_students = (
        Enrollment.objects.filter(course__in=teacher_courses)
        .values("student")
        .distinct()
        .count()
    )

    rating_agg = CourseReview.objects.filter(
        course__in=teacher_courses
    ).aggregate(
        average_rating=Avg("rating"),
        total_reviews=Count("id"),
    )

    enrollment_agg = Enrollment.objects.filter(
        course__in=teacher_courses
    ).aggregate(
        total_paid_enrollments=Count(
            "id",
            filter=Q(enrollment_type="paid"),
        ),
        total_audit_enrollments=Count(
            "id",
            filter=Q(enrollment_type="audit"),
        ),
        total_revenue=Sum(
            "price_paid",
            filter=Q(enrollment_type="paid"),
        ),
    )

    total_certificates_issued = Certificate.objects.filter(
        course__in=teacher_courses
    ).count()

    return {
        "total_courses": total_courses,
        "total_enrollments": total_enrollments,
        "total_students": total_students,
        "average_rating": (
            rating_agg["average_rating"]
            if rating_agg["average_rating"] is not None
            else 0.0
        ),
        "total_reviews": rating_agg["total_reviews"] or 0,
        "total_paid_enrollments": (
            enrollment_agg["total_paid_enrollments"] or 0
        ),
        "total_audit_enrollments": (
            enrollment_agg["total_audit_enrollments"] or 0
        ),
        "total_revenue": enrollment_agg["total_revenue"] or 0,
        "total_certificates_issued": total_certificates_issued,
    }


def get_teacher_course_stats(teacher):
    """Lấy số liệu của từng khóa học."""

    courses_stats = (
        Course.objects.filter(teacher=teacher)
        .annotate(
            enrollments_count=Count(
                "enrollments",
                distinct=True,
            ),
            unique_students_count=Count(
                "enrollments__student",
                distinct=True,
            ),
            average_rating=Avg("reviews__rating"),
            total_reviews=Count(
                "reviews",
                distinct=True,
            ),
            last_enrollment_at=Max("enrollments__created_at"),
            paid_enrollments=Count(
                "enrollments",
                filter=Q(
                    enrollments__enrollment_type="paid"
                ),
                distinct=True,
            ),
            audit_enrollments=Count(
                "enrollments",
                filter=Q(
                    enrollments__enrollment_type="audit"
                ),
                distinct=True,
            ),
            revenue=Sum(
                "enrollments__price_paid",
                filter=Q(
                    enrollments__enrollment_type="paid"
                ),
            ),
            certificates_issued=Count(
                "certificates",
                distinct=True,
            ),
        )
        .order_by("-created_at")
    )

    courses_data = []

    for course in courses_stats:
        course_data = {
            "course_id": course.id,
            "course_title": course.title,
            "course_thumbnail": (
                course.thumbnail_url
                if course.thumbnail_url
                else None
            ),
            "enrollments_count": course.enrollments_count or 0,
            "unique_students_count": (
                course.unique_students_count or 0
            ),
            "average_rating": (
                course.average_rating
                if course.average_rating is not None
                else 0.0
            ),
            "total_reviews": course.total_reviews or 0,
            "created_at": course.created_at,
            "last_enrollment_at": course.last_enrollment_at,
            "status": (
                "published"
                if course.is_published
                else "draft"
            ),
            "paid_enrollments": course.paid_enrollments or 0,
            "audit_enrollments": course.audit_enrollments or 0,
            "revenue": (
                float(course.revenue)
                if course.revenue
                else 0.0
            ),
            "certificates_issued": (
                course.certificates_issued or 0
            ),
        }
        courses_data.append(course_data)

    return courses_data


def get_teacher_time_series(teacher, months):
    """Lấy số liệu đăng ký theo tháng."""

    teacher_courses = Course.objects.filter(teacher=teacher)

    now = timezone.now()
    month_list = []

    for i in range(months - 1, -1, -1):
        if i == 0:
            target_date = now
        else:
            year = now.year
            month = now.month - i

            while month <= 0:
                month += 12
                year -= 1

            target_date = datetime(
                year,
                month,
                1,
                tzinfo=dt_timezone.utc,
            )

        month_key = target_date.strftime("%Y-%m")
        month_start = datetime(
            target_date.year,
            target_date.month,
            1,
            tzinfo=dt_timezone.utc,
        )

        month_list.append(
            {
                "month_key": month_key,
                "month_start": month_start,
            }
        )

    if month_list:
        earliest_month = month_list[0]["month_start"]
        enrollments = Enrollment.objects.filter(
            course__in=teacher_courses,
            created_at__gte=earliest_month,
        )
    else:
        enrollments = Enrollment.objects.filter(
            course__in=teacher_courses
        )

    monthly_stats_dict = {}

    for stat in (
        enrollments.annotate(
            month=TruncMonth("created_at")
        )
        .values("month")
        .annotate(
            paid_enrollments=Count(
                "id",
                filter=Q(enrollment_type="paid"),
            ),
            audit_enrollments=Count(
                "id",
                filter=Q(enrollment_type="audit"),
            ),
            revenue=Sum(
                "price_paid",
                filter=Q(enrollment_type="paid"),
            ),
        )
    ):
        month_key = stat["month"].strftime("%Y-%m")
        monthly_stats_dict[month_key] = {
            "paid_enrollments": (
                stat["paid_enrollments"] or 0
            ),
            "audit_enrollments": (
                stat["audit_enrollments"] or 0
            ),
            "revenue": (
                float(stat["revenue"])
                if stat["revenue"]
                else 0.0
            ),
        }

    result = []

    for month_info in month_list:
        month_key = month_info["month_key"]

        if month_key in monthly_stats_dict:
            result.append(
                {
                    "month": month_key,
                    "paid_enrollments": (
                        monthly_stats_dict[month_key][
                            "paid_enrollments"
                        ]
                    ),
                    "audit_enrollments": (
                        monthly_stats_dict[month_key][
                            "audit_enrollments"
                        ]
                    ),
                    "revenue": (
                        monthly_stats_dict[month_key]["revenue"]
                    ),
                }
            )
        else:
            result.append(
                {
                    "month": month_key,
                    "paid_enrollments": 0,
                    "audit_enrollments": 0,
                    "revenue": 0.0,
                }
            )

    return result


def get_teacher_engagement(teacher):
    """Lấy chỉ số tương tác học tập."""

    teacher_courses = Course.objects.filter(teacher=teacher)

    teacher_enrollments = Enrollment.objects.filter(
        course__in=teacher_courses
    )

    lessons_completed = LessonProgress.objects.filter(
        enrollment__in=teacher_enrollments,
        is_completed=True,
    ).count()

    paid_enrollments = teacher_enrollments.filter(
        enrollment_type="paid"
    )
    paid_enrollments_count = paid_enrollments.count()

    completed_enrollments = paid_enrollments.filter(
        progress_percent=100
    ).count()

    if paid_enrollments_count > 0:
        completion_rate = (
            completed_enrollments
            / paid_enrollments_count
        ) * 100
    else:
        completion_rate = 0.0

    quiz_attempts = StudentQuizAttempt.objects.filter(
        quiz__course__in=teacher_courses
    ).count()

    assignments_submitted = Submission.objects.filter(
        assignment__course__in=teacher_courses
    ).count()

    return {
        "lessons_completed": lessons_completed,
        "completion_rate": round(completion_rate, 1),
        "quiz_attempts": quiz_attempts,
        "assignments_submitted": assignments_submitted,
    }
