from django.urls import path
from .views import (
    CourseListCreateView,
    CourseRetrieveUpdateDestroyView,
    SubscriptionListCreateView,
    SubscriptionRetrieveUpdateDestroyView,
    CourseDetailAPIView
)

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(),
         name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyView.as_view(),
         name='course-retrieve-update-destroy'),
    path('courses/<int:pk>/detail/', CourseDetailAPIView.as_view(),
         name='course_detail_api'),
    path('subscriptions/', SubscriptionListCreateView.as_view(),
         name='subscription-list-create'),
    path('subscriptions/<int:pk>/',
         SubscriptionRetrieveUpdateDestroyView.as_view(),
         name='subscription-retrieve-update-destroy'),
]
