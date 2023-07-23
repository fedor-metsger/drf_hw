
from django.urls import path, include
from rest_framework import routers

from users.apps import UsersConfig

from users.views import UserViewSet


app_name = UsersConfig.name

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
