
from django.urls import path, include
from rest_framework import routers

from learning.apps import LearningConfig

from learning.views import CourseViewSet, LessonRetrieveAPIView, LessonUpdateAPIView, LessonDestroyAPIView, \
    LessonViewSet, CourseListAPIView, CourseCreateAPIView, CourseRetrieveAPIView, CourseUpdateAPIView, \
    CourseDestroyAPIView, PaymentListAPIView
from learning.views import LessonListAPIView, LessonCreateAPIView


app_name = LearningConfig.name

course_router = routers.DefaultRouter()
course_router.register(r'course', CourseViewSet)

lesson_router = routers.DefaultRouter()
lesson_router.register(r'lesson', LessonViewSet)

urlpatterns = [
    # path('', include(course_router.urls)),
    path('course/', CourseListAPIView.as_view(), name='course_list'),
    path('course/create/', CourseCreateAPIView.as_view(), name='course_create'),
    path('course/<int:pk>/', CourseRetrieveAPIView.as_view(), name='course_list'),
    path('course/<int:pk>/update/', CourseUpdateAPIView.as_view(), name='course_create'),
    path('course/<int:pk>/delete/', CourseDestroyAPIView.as_view(), name='course_list'),

    path('', include(lesson_router.urls)),
    # path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    # path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    # path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_list'),
    # path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson_create'),
    # path('lesson/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson_list'),

    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
]
