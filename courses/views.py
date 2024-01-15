from rest_framework import generics
from .models import Course, Subscription
from .serializers import CourseSerializer, SubscriptionSerializer
from rest_framework.pagination import LimitOffsetPagination
from .filters import CourseFilter, SubscriptionFilter
from drf_yasg.utils import swagger_auto_schema
from .permissions import IsModerator, IsTeacher
from rest_framework.permissions import IsAuthenticated

# пагинатор для Course
class CourseLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5


# пагинатор для Subscription
class SubscriptionLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5


class CourseListCreateView(generics.ListCreateAPIView):
    """List all Courses or create new Course"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CourseLimitOffsetPagination
    filterset_class = CourseFilter


class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """By Course pk, you can retrieve, update or patch, delete Course"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'DELETE':
            permission_classes = [IsAuthenticated, IsModerator]
        elif self.request.method in ['PUT', 'PATCH']:
            permission_classes = [IsAuthenticated, IsTeacher | IsModerator]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class SubscriptionListCreateView(generics.ListCreateAPIView):
    """List all Subscription or create new Subscription"""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    pagination_class = SubscriptionLimitOffsetPagination
    filterset_class = SubscriptionFilter


class SubscriptionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """By Subscription pk, you can retrieve, update or patch, delete
    Subscription"""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE']:
            permission_classes = [IsAuthenticated, IsModerator]
        elif self.request.method in ['GET', 'PUT', 'PATCH']:
            permission_classes = [IsAuthenticated, IsTeacher | IsModerator]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
