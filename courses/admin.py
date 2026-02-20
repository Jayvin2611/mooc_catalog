from django.contrib import admin
from django.utils.html import format_html
from .models import Course, Lesson, Enrollment, LessonProgress, Instructor


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    """Admin configuration for Instructor model."""
    list_display = ['name', 'profile_pic_preview', 'course_count', 'created_at']
    search_fields = ['name', 'bio']
    list_filter = ['created_at']

    def profile_pic_preview(self, obj):
        if obj.profile_pic_url:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />', obj.profile_pic_url)
        return "No image"
    profile_pic_preview.short_description = 'Profile'

    def course_count(self, obj):
        return obj.courses.count()
    course_count.short_description = 'Courses'


class LessonInline(admin.TabularInline):
    """Inline admin for lessons within a course."""
    model = Lesson
    extra = 1
    fields = ['title', 'content', 'youtube_url', 'order']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin configuration for Course model."""
    list_display = ['title', 'thumbnail_preview', 'instructor', 'short_description', 'created_at', 'lesson_count']
    search_fields = ['title', 'short_description', 'instructor__name']
    list_filter = ['instructor', 'created_at']
    inlines = [LessonInline]

    def thumbnail_preview(self, obj):
        if obj.thumbnail_url:
            return format_html('<img src="{}" width="60" height="40" style="border-radius: 4px; object-fit: cover;" />', obj.thumbnail_url)
        return "No image"
    thumbnail_preview.short_description = 'Thumbnail'

    def lesson_count(self, obj):
        return obj.lessons.count()
    lesson_count.short_description = 'Lessons'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Admin configuration for Lesson model."""
    list_display = ['title', 'course', 'order', 'has_video', 'created_at']
    search_fields = ['title', 'course__title']
    list_filter = ['course', 'created_at']
    ordering = ['course', 'created_at']

    def has_video(self, obj):
        return bool(obj.youtube_url)
    has_video.boolean = True
    has_video.short_description = 'Video'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """Admin configuration for Enrollment model."""
    list_display = ['user', 'course', 'enrolled_at']
    search_fields = ['user__username', 'course__title']
    list_filter = ['enrolled_at', 'course']


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    """Admin configuration for LessonProgress model."""
    list_display = ['user', 'lesson', 'viewed_at']
    search_fields = ['user__username', 'lesson__title']
    list_filter = ['viewed_at', 'lesson__course']
