
from django.core.management import BaseCommand

from learning.models import Payment, Course
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):

        user1 = User.objects.first()
        user2 = User.objects.last()

        course1 = Course.objects.first()
        course2 = Course.objects.last()

        payments = [
            {"id": 1, "user": user1, "course": course1, "amount": 100000, "method": "CASH"},
            {"id": 2, "user": user1, "course": course2, "amount": 80000, "method": "CASH"},
            {"id": 3, "user": user2, "course": course1, "amount": 97000, "method": "TRANSFER"},
        ]

        Payment.objects.all().delete()

        for p in payments:
            Payment.objects.create(**p)