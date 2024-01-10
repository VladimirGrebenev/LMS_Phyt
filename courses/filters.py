from django_filters import rest_framework as filters, DateFromToRangeFilter
from .models import Course, Subscription


class CourseFilter(filters.FilterSet):
    course_title = filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = Course
        fields = ['course_title']


class SubscriptionFilter(filters.FilterSet):
    created_datetime = DateFromToRangeFilter()

    class Meta:
        model = Subscription
        fields = ['created_datetime']
