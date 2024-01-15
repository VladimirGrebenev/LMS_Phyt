from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework import mixins, viewsets, generics
from .models import CustomUser
from .serializers import UserModelSerializer, UserRegisterSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status


class UserCustomViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """View для CRUD класса CustomUser с доступом только у администраторов"""
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    queryset = CustomUser.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return CustomUser.objects.filter(is_active=True)

class UserListAPIView(generics.ListAPIView):
    """View для класса CustomUser с доступом только у администраторов,
    для просмотра, с поддержкой версии API"""
    queryset = CustomUser.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.version == '0.2':
            return UserModelSerializerFull
        return UserModelSerializer

class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        email = serializer.validated_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email is already registered.')
        serializer.save()