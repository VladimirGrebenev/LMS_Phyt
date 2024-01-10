from rest_framework.serializers import HyperlinkedModelSerializer
from .models import CustomUser


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


class UserRegisterSerializer(HyperlinkedModelSerializer):
    """Сериалайзер класса CustomUser для регистрации"""
    class Meta:
        model = CustomUser
        fields = ['id', 'user_name', 'email', 'password', 'role']
