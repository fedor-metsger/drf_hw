
from django.urls import path, include
from rest_framework import routers

from learning.apps import LearningConfig

from learning.views import CourseViewSet, LessonRetrieveAPIView, LessonUpdateAPIView, LessonDestroyAPIView
from learning.views import LessonListAPIView, LessonCreateAPIView


app_name = LearningConfig.name

course_router = routers.DefaultRouter()
course_router.register(r'course', CourseViewSet)

urlpatterns = [
    path('', include(course_router.urls)),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson_create'),
    path('lesson/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson_list'),
]
