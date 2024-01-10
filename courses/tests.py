import json
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import (APIRequestFactory, force_authenticate,
                                 APIClient, APISimpleTestCase, APITestCase)
from mixer.backend.django import mixer
from .models import Course, Subscription
from users.models import CustomUser
from .views import (CourseListCreateView, CourseRetrieveUpdateDestroyView,
                    SubscriptionListCreateView,
                    SubscriptionRetrieveUpdateDestroyView,)


# Create your tests here.

class TestCourseListCreateView(TestCase):
    def test_get_courses_list_auth_user(self):
        """ Пробуем получить доступ к списку курсов авторизованным 
        пользователем """
        factory = APIRequestFactory()
        request = factory.get('/courses/')
        # авторизуемся, чтобы получить доступ
        custom_user = CustomUser.objects.create_superuser(
            'doomguy@mail.ru', 'iddqd', )
        force_authenticate(request, custom_user)
        view = CourseListCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_courses_list_guest(self):
        """ Пробуем получить доступ к списку курсов не авторизованным
        пользователем """
        factory = APIRequestFactory()
        request = factory.get('/courses/')
        view = CourseListCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_course_auth_user(self):
        """ Пробуем создать курс авторизованным пользователем """
        factory = APIRequestFactory()
        data = {
            'course_title': 'course_title',
            'course_description': 'description',
            'teacher': '',
        }
        request = factory.post('/courses/', data=data, format='json')
        # авторизуемся, чтобы получить доступ
        custom_user = CustomUser.objects.create_superuser(
            'doomguy@mail.ru', 'iddqd', )
        force_authenticate(request, custom_user)
        view = CourseListCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_course_guest(self):
        """ Пробуем создать курс не авторизованным пользователем """
        factory = APIRequestFactory()
        data = {
            'course_title': 'course_title',
            'course_description': 'description',
            'teacher': '',
        }
        request = factory.post('/courses/', data=data, format='json')
        view = CourseListCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_course_auth_user_incomplete_data(self):
        """ Пробуем создать курс с неполными данными """
        factory = APIRequestFactory()
        data = {
            # 'course_title': 'course_title', <<< неполные данные
            'course_description': 'description',
            'teacher': '',
        }
        request = factory.post('/courses/', data=data, format='json')
        # авторизуемся, чтобы получить доступ
        custom_user = CustomUser.objects.create_superuser(
            'doomguy@mail.ru', 'iddqd', )
        force_authenticate(request, custom_user)
        view = CourseListCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestCourseRetrieveUpdateDestroyView(TestCase):
    def test_get_course_detail_auth_user(self):
        """ Пробуем получить данные курса авторизованным пользователем """
        factory = APIRequestFactory()
        course = mixer.blend(Course, course_title='course_title',
                             course_description='course_description',
                             teacher='', )
        request = factory.get(f'/courses/{course.uu_id}/')
        # авторизуемся, чтобы получить доступ
        custom_user = CustomUser.objects.create_superuser(
            'doomguy@mail.ru', 'iddqd', )
        force_authenticate(request, custom_user)
        view = CourseRetrieveUpdateDestroyView.as_view()
        response = view(request, pk=course.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_course_detail_guest(self):
        """ Пробуем получить данные курса не авторизованным пользователем """
        factory = APIRequestFactory()
        course = mixer.blend(Course, course_title='course_title',
                             course_description='course_description',
                             teacher='', )
        request = factory.get(f'/courses/{course.uu_id}/')
        view = CourseRetrieveUpdateDestroyView.as_view()
        response = view(request, pk=course.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_course_auth_user(self):
        """ Редактируем данные клиента авторизованным пользователем """
        factory = APIRequestFactory()
        course = mixer.blend(Course, course_title='course_title',
                             course_description='course_description',
                             teacher='', )
        new_data = {
            'course_title': 'course_title',
            'course_description': 'description',
            'teacher': '',
        }

        url = reverse('course-retrieve-update-destroy',
                      kwargs={'pk': course.pk})
        request = factory.patch(url, data=new_data, format='json')
        # авторизуемся, чтобы получить доступ
        custom_user = CustomUser.objects.create_superuser(
            'doomguy@mail.ru', 'iddqd', )
        force_authenticate(request, custom_user)
        view = CourseRetrieveUpdateDestroyView.as_view()
        response = view(request, pk=course.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_course_guest(self):
        """ Редактируем данные курса не авторизованным пользователем """
        factory = APIRequestFactory()
        course = mixer.blend(Course, course_title='course_title',
                             course_description='course_description',
                             teacher='', )
        new_data = {
            'course_title': 'course_title',
            'course_description': 'description',
            'teacher': '',
        }

        url = reverse('course-retrieve-update-destroy',
                      kwargs={'pk': course.pk})
        request = factory.patch(url, data=new_data, format='json')
        view = CourseRetrieveUpdateDestroyView.as_view()
        response = view(request, pk=course.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_course_auth_user(self):
        """ Удаляем курс авторизованным пользователем """
        factory = APIRequestFactory()
        course = mixer.blend(Course, course_title='course_title',
                             course_description='course_description',
                             teacher='', )
        request = factory.delete(f'/courses/{course.uu_id}/')
        # авторизуемся, чтобы получить доступ
        custom_user = CustomUser.objects.create_superuser(
            'doomguy@mail.ru', 'iddqd', )
        force_authenticate(request, custom_user)
        view = CourseRetrieveUpdateDestroyView.as_view()
        response = view(request, pk=course.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_course_guest(self):
        """ Удаляем клиента не авторизованным пользователем """
        factory = APIRequestFactory()
        course = mixer.blend(Course, course_title='course_title',
                             course_description='course_description',
                             teacher='', )
        request = factory.delete(f'/courses/{course.uu_id}/')
        view = CourseRetrieveUpdateDestroyView.as_view()
        response = view(request, pk=course.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestSubscriptionListCreateView(TestCase):
    def test_get_subscriptions_list_auth_user(self):
        """ Пробуем получить доступ к списку подписок авторизованным
        пользователем """
        factory = APIRequestFactory()
        request = factory.get('/subscriptions/')
        # авторизуемся, чтобы получить доступ
        custom_user = CustomUser.objects.create_superuser(
            'doomguy@mail.ru', 'iddqd', )
        force_authenticate(request, custom_user)
        view = SubscriptionListCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_subscriptions_list_guest(self):
        """ Пробуем получить доступ к списку подписок не авторизованным
        пользователем """
        factory = APIRequestFactory()
        request = factory.get('/subscriptions/')
        view = SubscriptionListCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
