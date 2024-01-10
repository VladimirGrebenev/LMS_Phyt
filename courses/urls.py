from django.urls import path
from .views import (
    CourseListCreateView,
    CourseRetrieveUpdateDestroyView,
    SubscriptionListCreateView,
    SubscriptionRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='client-list-create'),
    path('courses/<uuid:pk>/', CourseRetrieveUpdateDestroyView.as_view(), name='client-retrieve-update-destroy'),
    path('subscriptions/', SubscriptionListCreateView.as_view(), name='dispatch-list-create'),
    path('subscriptions/<uuid:pk>/', SubscriptionRetrieveUpdateDestroyView.as_view(), name='dispatch-retrieve-update-destroy'),
]