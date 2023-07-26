
from rest_framework import serializers

from learning.models import Course, Lesson, Payment, Subscription
from learning.validators import VideoValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoValidator(field="video")]

class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = ["id", "owner", "title", "description", "lessons_count", "lessons", "subscription"]

    def get_lessons_count(self, instance):
        return Lesson.objects.filter(course=instance.id).count()

    def get_subscription(self, instance):
        user_id = self.context["request"].user.id
        return Subscription.objects.filter(user_id=user_id, course_id=instance.id).exists()

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
