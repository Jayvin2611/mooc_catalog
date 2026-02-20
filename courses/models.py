from django.db import models
from django.contrib.auth.models import User


class Instructor(models.Model):
    """Model representing a course instructor."""
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True, help_text="Short biography of the instructor")
    profile_pic = models.ImageField(upload_to='instructors/', blank=True, null=True)
    website = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_profile_pic_url(self):
        """Return profile pic URL or a default avatar."""
        if self.profile_pic:
            return self.profile_pic.url
        return None


class Course(models.Model):
    """Model representing a course in the catalog."""
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=500)
    long_description = models.TextField()
    thumbnail = models.ImageField(upload_to='courses/', blank=True, null=True, help_text="Course thumbnail image")
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_thumbnail_url(self):
        """Return thumbnail URL or None."""
        if self.thumbnail:
            return self.thumbnail.url
        return None


class Lesson(models.Model):
    """Model representing a lesson within a course."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    youtube_url = models.URLField(max_length=500, blank=True, null=True, help_text="Optional YouTube video URL")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_youtube_embed_url(self):
        """Convert YouTube URL to embed URL."""
        if not self.youtube_url:
            return None
        url = self.youtube_url
        if 'youtube.com/watch?v=' in url:
            video_id = url.split('watch?v=')[1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        elif 'youtube.com/embed/' in url:
            return url
        return None

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Enrollment(models.Model):
    """Model representing a user's enrollment in a course."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'course']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


class LessonProgress(models.Model):
    """Model tracking a user's progress on a lesson."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'lesson']
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.user.username} viewed {self.lesson.title}"
