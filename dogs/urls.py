
from django.urls import path, include
from dogs.apps import DogsConfig
from dogs.views import DogListAPIView, DogCreateAPIView
from dogs.views import BreedViewSet, AncestorViewSet

from rest_framework import routers

app_name = DogsConfig.name

breed_router = routers.DefaultRouter()
breed_router.register(r'breed', BreedViewSet)

anc_router = routers.DefaultRouter()
anc_router.register(r'ancestor', AncestorViewSet)

urlpatterns = [
    path('', DogListAPIView.as_view(), name='dog_list'),
    path('create/', DogCreateAPIView.as_view(), name='dog_create'),
    path('', include(breed_router.urls)),
    path('', include(anc_router.urls)),
]
