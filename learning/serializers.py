
from rest_framework import serializers
from rest_framework.fields import IntegerField

from learning.models import Course, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    # lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = ["id", "owner", "title", "description", "lessons_count"]

    def get_lessons_count(self, instance):
        return Lesson.objects.filter(course=instance.id).count()

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
