
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from learning.models import Course, Lesson, Payment, Subscription
from learning.paginators import MyPaginator
from learning.permissions import NotModerator, IsOwnerOrModerator, LessonPermission
from learning.serializers import CourseSerializer, LessonSerializer, PaymentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by("id")
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MyPaginator

    def get_queryset(self):
        if "moderator" in [i.name for i in self.request.user.groups.all()]:
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user)

class CourseCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, NotModerator]

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

class CourseRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsOwnerOrModerator]

class CourseUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsOwnerOrModerator]

class CourseDestroyAPIView(generics.DestroyAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, NotModerator]

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all().order_by("id")
    serializer_class = LessonSerializer
    permission_classes = [LessonPermission]
    pagination_class = MyPaginator

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request):
        queryset = Lesson.objects.all().order_by("id")
        if not "moderator" in [i.name for i in self.request.user.groups.all()]:
            queryset = Lesson.objects.filter(owner=self.request.user).order_by("id")
        serializer = LessonSerializer(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'user', 'method')
    ordering_fields = ['date']
    permission_classes = [IsAuthenticated]

class Subscribe(generics.CreateAPIView):
    def create(self, request, course_id=None):
        user_id = request.user.pk
        if not Subscription.objects.filter(user_id=user_id, course_id=course_id).exists():
            s = Subscription(user_id=user_id, course_id=course_id)
            s.save()
        return Response(status=201)

class Unsubscribe(generics.DestroyAPIView):
    def delete(self, request, course_id):
        user_id = request.user.pk
        Subscription.objects.filter(user_id=user_id, course_id=course_id).delete()
        return Response(status=204)

