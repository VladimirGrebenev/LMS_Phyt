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
    """View для класса CustomUser для регистрации нового пользователя"""
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        email = serializer.validated_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'This email is already registered.')
        serializer.save()

    def post(self, request, *args, **kwargs):
        # Extract the necessary data from the request
        email = request.data.get('email')
        password = request.data.get('password')
        extra_fields = {
            'user_name': request.data.get('user_name'),
            # Add any additional fields you need for user creation
        }

        # Validate the data
        if not email or not password:
            return Response({'error': 'Email and password are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'This email is already registered.'},
                            status=status.HTTP_400_BAD_REQUEST)
        # Create a new user
        try:
            user = CustomUser.objects.create_user(email=email,
                                                  password=password,
                                                  **extra_fields)
            # if user:
            #     users_tasks.send_welcome_email(user.id)

        except ValueError as e:
            return Response({'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'User registered successfully.'},
                        status=status.HTTP_201_CREATED)