from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Lesson, Enrollment, LessonProgress


def course_list(request):
    """Display all available courses."""
    courses = Course.objects.all()

    enrolled_courses_data = {}
    if request.user.is_authenticated:
        enrollments = Enrollment.objects.filter(user=request.user).select_related('course')

        for enrollment in enrollments:
            course = enrollment.course
            all_lessons = list(course.lessons.all())

            completed_lesson_ids = set(
                LessonProgress.objects.filter(
                    user=request.user,
                    lesson__course=course
                ).values_list('lesson_id', flat=True)
            )

            # Find next uncompleted lesson
            next_lesson = None
            for lesson in all_lessons:
                if lesson.id not in completed_lesson_ids:
                    next_lesson = lesson
                    break

            # If all completed, use first lesson for review
            if next_lesson is None and all_lessons:
                next_lesson = all_lessons[0]

            enrolled_courses_data[course.id] = {
                'next_lesson': next_lesson,
                'completed': len(completed_lesson_ids),
                'total': len(all_lessons),
            }

    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'enrolled_courses_data': enrolled_courses_data,
    })


def course_detail(request, pk):
    """Display course details and its lessons."""
    course = get_object_or_404(Course, pk=pk)
    lessons = course.lessons.all()

    is_enrolled = False
    viewed_lessons = set()

    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            user=request.user,
            course=course
        ).exists()

        if is_enrolled:
            viewed_lessons = set(
                LessonProgress.objects.filter(
                    user=request.user,
                    lesson__course=course
                ).values_list('lesson_id', flat=True)
            )

    # Get other courses by the same instructor
    other_courses = []
    if course.instructor:
        other_courses = Course.objects.filter(
            instructor=course.instructor
        ).exclude(pk=course.pk)[:4]

    context = {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled,
        'viewed_lessons': viewed_lessons,
        'other_courses': other_courses,
    }
    return render(request, 'courses/course_detail.html', context)


@login_required
def enroll_course(request, pk):
    """Enroll the current user in a course."""
    course = get_object_or_404(Course, pk=pk)

    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )

    if created:
        messages.success(request, f'You have successfully enrolled in "{course.title}"!')
    else:
        messages.info(request, f'You are already enrolled in "{course.title}".')

    return redirect('course_detail', pk=pk)


@login_required
def my_courses(request):
    """Display courses the current user is enrolled in."""
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')

    # Calculate progress for each enrollment
    courses_with_progress = []
    for enrollment in enrollments:
        course = enrollment.course
        all_lessons = list(course.lessons.all())
        total_lessons = len(all_lessons)

        completed_lesson_ids = set(
            LessonProgress.objects.filter(
                user=request.user,
                lesson__course=course
            ).values_list('lesson_id', flat=True)
        )
        completed_lessons = len(completed_lesson_ids)

        progress_percent = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0

        # Find next uncompleted lesson
        next_lesson = None
        for lesson in all_lessons:
            if lesson.id not in completed_lesson_ids:
                next_lesson = lesson
                break

        # If all completed, use first lesson for review
        if next_lesson is None and all_lessons:
            next_lesson = all_lessons[0]

        courses_with_progress.append({
            'enrollment': enrollment,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'progress_percent': round(progress_percent),
            'next_lesson': next_lesson,
        })

    return render(request, 'courses/my_courses.html', {'courses': courses_with_progress})


@login_required
def lesson_detail(request, course_pk, lesson_pk):
    """Display lesson details and track progress."""
    course = get_object_or_404(Course, pk=course_pk)
    lesson = get_object_or_404(Lesson, pk=lesson_pk, course=course)

    # Check if user is enrolled
    is_enrolled = Enrollment.objects.filter(
        user=request.user,
        course=course
    ).exists()

    if not is_enrolled:
        messages.warning(request, 'You must be enrolled in this course to view lessons.')
        return redirect('course_detail', pk=course_pk)

    # Track lesson progress
    LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )

    # Get all lessons for navigation
    all_lessons = list(course.lessons.all())
    current_index = next(
        (i for i, l in enumerate(all_lessons) if l.pk == lesson.pk),
        0
    )

    prev_lesson = all_lessons[current_index - 1] if current_index > 0 else None
    next_lesson = all_lessons[current_index + 1] if current_index < len(all_lessons) - 1 else None

    # Get viewed lessons for progress tracking
    viewed_lessons = set(
        LessonProgress.objects.filter(
            user=request.user,
            lesson__course=course
        ).values_list('lesson_id', flat=True)
    )

    context = {
        'course': course,
        'lesson': lesson,
        'all_lessons': all_lessons,
        'viewed_lessons': viewed_lessons,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
    }
    return render(request, 'courses/lesson_detail.html', context)
