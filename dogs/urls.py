
from django.urls import path, include
from dogs.apps import DogsConfig
from dogs.views import DogListAPIView, DogCreateAPIView, BreedRetrieveAPIView, BreedListAPIView, DogRetrieveAPIView
from dogs.views import BreedViewSet, AncestorViewSet

from rest_framework import routers

app_name = DogsConfig.name

breed_router = routers.DefaultRouter()
breed_router.register(r'breed', BreedViewSet)

anc_router = routers.DefaultRouter()
anc_router.register(r'ancestor', AncestorViewSet)

urlpatterns = [
    path('', DogListAPIView.as_view(), name='dog_list'),
    path('<int:pk>/', DogRetrieveAPIView.as_view(), name='dog_retrieve'),
    path('create/', DogCreateAPIView.as_view(), name='dog_create'),
    # path('', include(breed_router.urls)),
    path('breed/<int:pk>/', BreedRetrieveAPIView.as_view(), name='breed_retrieve'),
    path('breed/', BreedListAPIView.as_view(), name='breed_retrieve'),
    path('', include(anc_router.urls)),
]
