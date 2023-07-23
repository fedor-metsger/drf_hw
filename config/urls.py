
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('dogs.urls', namespace='dogs')),
    path('', include('learning.urls', namespace='learning')),
    path('', include('users.urls', namespace='users')),
]
