
from django.urls import path, include
from rest_framework import routers

from learning.apps import LearningConfig

from learning.views import CourseViewSet, LessonViewSet, CourseListAPIView, CourseCreateAPIView, \
    CourseRetrieveAPIView, CourseUpdateAPIView, CourseDestroyAPIView, PaymentListAPIView, Unsubscribe, Subscribe, \
    Product, Price, PaymentLink

app_name = LearningConfig.name

course_router = routers.DefaultRouter()
course_router.register(r'course', CourseViewSet)

lesson_router = routers.DefaultRouter()
lesson_router.register(r'lesson', LessonViewSet)

urlpatterns = [
    path('course/', CourseListAPIView.as_view(), name='course_list'),
    path('course/create/', CourseCreateAPIView.as_view(), name='course_create'),
    path('course/<int:pk>/', CourseRetrieveAPIView.as_view(), name='course_retrieve'),
    path('course/<int:pk>/update/', CourseUpdateAPIView.as_view(), name='course_update'),
    path('course/<int:pk>/delete/', CourseDestroyAPIView.as_view(), name='course_destroy'),
    path('course/<int:course_id>/subscribe/', Subscribe.as_view(), name='course_subscribe'),
    path('course/<int:course_id>/unsubscribe/', Unsubscribe.as_view(), name='course_unsubscribe'),

    path('course/<int:course_id>/product/', Product.as_view(), name='course_product'),
    path('course/<int:course_id>/price/', Price.as_view(), name='course_price'),
    path('course/<int:course_id>/payment_link/', PaymentLink.as_view(), name='course_price'),

    path('', include(lesson_router.urls)),

    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
]
