from rest_framework import generics
from .models import Course, Subscription
from .serializers import CourseSerializer, SubscriptionSerializer
from rest_framework.pagination import LimitOffsetPagination
from .filters import CourseFilter, SubscriptionFilter
from drf_yasg.utils import swagger_auto_schema
from .permissions import IsModerator, IsTeacher
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


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


class SubscriptionRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView):
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


class CourseDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=404)

        subscriptions = Subscription.objects.filter(course=course)
        course_detail = {
            'course_title': course.course_title,
            'course_description': course.course_description,
            'course_teacher': course.teacher.user_name,
            'course_student_count': subscriptions.count(),
            'subscriptions': [],
        }

        for subscription in subscriptions:
            course_detail['subscriptions'].append({
                'student_id': subscription.student.user_name,
                'created_datetime': subscription.created_datetime,
            })

        return Response(course_detail)

# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticated, IsTeacher | IsModerator])
# def subscription_detail(request, pk):
#     try:
#         subscription = Subscription.objects.get(pk=pk)
#     except Subscription.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = SubscriptionSerializer(subscription)
#         return Response(serializer.data)
#     elif request.method == 'PUT' or request.method == 'PATCH':
#         serializer = SubscriptionSerializer(subscription, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         subscription.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated, IsModerator])
# def create_subscription(request):
#     serializer = SubscriptionSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
