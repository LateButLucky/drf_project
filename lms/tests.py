from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User
from .models import Course, Lesson, Subscription


class APITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='password123')
        self.course = Course.objects.create(owner=self.user, title='Test Course', preview='http://example.com',
                                            description='Course description')
        self.lesson = Lesson.objects.create(owner=self.user, course=self.course, title='Test Lesson',
                                            description='Lesson description', preview='http://example.com',
                                            video_url='http://youtube.com/watch?v=123456')

    def test_create_course(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('course-list')
        data = {
            'title': 'New Course',
            'preview': 'http://example.com',
            'description': 'New course description',
            'owner': self.user.id  # Добавляем поле owner
        }
        response = self.client.post(url, data, format='json')
        print(response.status_code)  # Выводим статус код для отладки
        print(response.data)  # Выводим данные ответа для отладки
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Course.objects.filter(title='New Course').exists())

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lesson-list-create')
        data = {
            'owner': self.user.id,
            'course': self.course.id,
            'title': 'New Lesson',
            'description': 'New Lesson description',
            'preview': 'http://example.com',
            'video_url': 'http://youtube.com/watch?v=123456'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lesson-detail', args=[self.lesson.id])
        data = {
            'title': 'Updated Lesson Title'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Lesson Title')

    def test_create_subscription(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('subscriptions')
        data = {'course_id': self.course.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_remove_subscription(self):
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        url = reverse('subscriptions')
        data = {'course_id': self.course.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
