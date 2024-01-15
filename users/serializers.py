from rest_framework.serializers import HyperlinkedModelSerializer
from .models import CustomUser
from rest_framework import serializers

class UserModelSerializer(HyperlinkedModelSerializer):
    """Сериалайзер класса CustomUser для представления"""
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'user_name', 'email', 'role']


# class UserModelSerializerFull(HyperlinkedModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'first_name', 'last_name', 'user_name', 'email',
#                   'date_joined', 'updated', 'is_staff', 'is_active',
#                   'is_superuser', 'role']


class UserRegisterSerializer(serializers.HyperlinkedModelSerializer):
    """Сериалайзер класса CustomUser для регистрации"""

    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = CustomUser
        fields = ['id', 'user_name', 'email', 'password', 'role']

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError('Email and password are required.')

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email is already registered.')

        return data
