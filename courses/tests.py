from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Course, Lesson, Enrollment, LessonProgress


class CourseModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title='Test Course',
            short_description='A short description',
            long_description='A long description for testing'
        )

    def test_course_creation(self):
        self.assertEqual(self.course.title, 'Test Course')
        self.assertEqual(str(self.course), 'Test Course')


class LessonModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title='Test Course',
            short_description='Short desc',
            long_description='Long desc'
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Test Lesson',
            content='Lesson content',
            order=1
        )

    def test_lesson_creation(self):
        self.assertEqual(self.lesson.title, 'Test Lesson')
        self.assertEqual(self.lesson.course, self.course)


class CourseViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.course = Course.objects.create(
            title='Test Course',
            short_description='Short desc',
            long_description='Long desc'
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Test Lesson',
            content='Lesson content',
            order=1
        )

    def test_course_list_view(self):
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Course')

    def test_course_detail_view(self):
        response = self.client.get(reverse('course_detail', args=[self.course.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Course')
        self.assertContains(response, 'Log in to enroll')

    def test_course_detail_logged_in_not_enrolled(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('course_detail', args=[self.course.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enroll in this Course')

    def test_enroll_course(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('enroll_course', args=[self.course.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Enrollment.objects.filter(user=self.user, course=self.course).exists())

    def test_course_detail_logged_in_enrolled(self):
        self.client.login(username='testuser', password='testpass123')
        Enrollment.objects.create(user=self.user, course=self.course)
        response = self.client.get(reverse('course_detail', args=[self.course.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You are enrolled in this course')

    def test_lesson_detail_requires_enrollment(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('lesson_detail', args=[self.course.pk, self.lesson.pk])
        )
        self.assertEqual(response.status_code, 302)  # Redirect to course detail

    def test_lesson_detail_enrolled(self):
        self.client.login(username='testuser', password='testpass123')
        Enrollment.objects.create(user=self.user, course=self.course)
        response = self.client.get(
            reverse('lesson_detail', args=[self.course.pk, self.lesson.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Lesson')
        # Check progress was tracked
        self.assertTrue(
            LessonProgress.objects.filter(user=self.user, lesson=self.lesson).exists()
        )

    def test_my_courses_view(self):
        self.client.login(username='testuser', password='testpass123')
        Enrollment.objects.create(user=self.user, course=self.course)
        response = self.client.get(reverse('my_courses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Course')


class AuthViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_post(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after signup
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
