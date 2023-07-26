
import json

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory

from learning.models import Lesson, Course, Subscription
from learning.views import LessonViewSet
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='user', email='user@sky.pro',
            password='pbkdf2_sha256$600000$960zdQH5dHDCqHCxbD6qEM$otbdXsM6kg5daqUJYC282IO4/ddr4jcAm4WKA+dkIaI='
        )
        resp = self.client.post(
            "/token/",
            {'username': 'user', 'password': 'qwe123'},
            format='json'
        )
        self.token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            owner=self.user,
            title="Test course",
            description="Test course description"
        )
        self.lesson = Lesson.objects.create(
            owner=self.user,
            title="Test lesson",
            description="Test lesson description",
            course=self.course,
            video="https://youtu.be/qwerty123"
        )

    def tearDown(self) -> None:
        self.lesson.delete()
        self.course.delete()
        self.user.delete()

    def test_lesson_list(self):
        response = self.client.get(
            reverse('learning:lesson-list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(), {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.id,
                        "title": self.lesson.title,
                        "description": self.lesson.description,
                        "video": self.lesson.video,
                        "preview": None,
                        "owner": self.course.owner.id,
                        "course": self.course.pk
                    }
                ]
            }
        )

    def test_create_lesson(self):
        data = {
            "title": "Test lesson",
            "description": "Test lesson description",
            "course": self.course.pk,
            "video": "https://youtu.be/qwerty123"
        }

        response = self.client.post(
            reverse('learning:lesson-list'),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            2,
            Lesson.objects.all().count()
        )

    def test_update_lesson(self):
        data = {
            "title": "Test lesson 2",
            "description": "Test lesson description 2",
            "course": self.course.pk,
            "owner": self.course.owner.id,
            "video": "https://youtu.be/qwerty123"
        }

        response = self.client.put(
            reverse('learning:lesson-detail', args=[self.lesson.pk]),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.lesson.refresh_from_db()
        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.id,
                "title": self.lesson.title,
                "description": self.lesson.description,
                "video": self.lesson.video,
                "preview": None,
                "owner": self.course.owner.id,
                "course": self.course.pk
            }
        )

    def test_patch_lesson(self):
        data = {
            "title": "Test lesson 2",
            # "description": "Test lesson description 2",
            # "course": self.course,
            # "owner": 1,
            # "video": "https://youtu.be/qwerty123"
        }

        response = self.client.patch(
            reverse('learning:lesson-detail', args=[self.lesson.pk]),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.lesson.refresh_from_db()
        self.assertEqual(
            self.lesson.title,
            data['title']
        )

    def test_delete_lesson(self):
        lesson_id = self.lesson.pk
        response = self.client.delete(
            reverse('learning:lesson-detail', args=[lesson_id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        # self.lesson.refresh_from_db()
        self.assertEqual(
            Lesson.objects.filter(pk=lesson_id).exists(),
            False
        )

    def test_subscribe(self):
        response = self.client.post(
            reverse('learning:course_subscribe', args=[self.course.pk])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            Subscription.objects.filter(course_id=self.course.pk, user_id=self.user.pk).exists(),
            True
        )

    def test_unsubscribe(self):
        response = self.client.delete(
            reverse('learning:course_unsubscribe', args=[self.course.pk])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Subscription.objects.filter(course_id=self.course.pk, user_id=self.user.pk).exists(),
            False
        )
