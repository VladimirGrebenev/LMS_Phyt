from rest_framework import serializers
from .models import Course, Subscription


class CourseSerializer(serializers.ModelSerializer):
    """Сериалайзер класса Course"""

    class Meta:
        model = Course
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериалайзер для класса Subscription"""

    class Meta:
        model = Subscription
        fields = '__all__'
