
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from learning.models import Course, Lesson, Payment, Subscription
from learning.paginators import MyPaginator
from learning.permissions import NotModerator, IsOwnerOrModerator, LessonPermission
from learning.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from learning.services import get_or_create_product, get_or_create_price, get_or_create_payment_link


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
    permission_classes = [IsAuthenticated]

    def create(self, request, course_id=None):
        user_id = request.user.pk
        if not Subscription.objects.filter(user_id=user_id, course_id=course_id).exists():
            s = Subscription(user_id=user_id, course_id=course_id)
            s.save()
        return Response(status=201)

class Unsubscribe(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, course_id):
        user_id = request.user.pk
        Subscription.objects.filter(user_id=user_id, course_id=course_id).delete()
        return Response(status=204)

class Product(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):

        prod_pk, prod_id = get_or_create_product(course_id)
        if not prod_pk:
            return Response(status=prod_id)

        return Response(
            {"pk": prod_pk, "id": prod_id},
            status=200
        )

class Price(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):

        course = Course.objects.filter(pk=course_id).get()
        prod_pk, prod_id = get_or_create_product(course_id)
        if not prod_pk:
            return Response(status=prod_id)

        price_pk, price_id = get_or_create_price(prod_pk, course.price * 100)
        if not price_pk:
            return Response(status=price_id)

        return Response(
            {"pk": price_pk, "id": price_id},
            status=200
        )


class PaymentLink(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):

        course = Course.objects.filter(pk=course_id).get()

        prod_pk, prod_id = get_or_create_product(course_id)
        if not prod_pk:
            return Response(status=prod_id)

        price_pk, price_id = get_or_create_price(prod_pk, course.price * 100)
        if not price_pk:
            return Response(status=price_id)

        link_pk, link_id, link_url = get_or_create_payment_link(price_pk, request.user.id)
        if not link_pk:
            return Response(status=link_id)

        return Response(
            {
                "prod_pk": prod_pk, "prod_id": prod_id,
                "price_pk": price_pk, "price_id": price_id,
                "link_pk": link_pk, "link_id": link_id, "url": link_url
            },
            status=200
        )
