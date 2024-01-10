from django.core.management.base import BaseCommand

from users.models import CustomUser, UserRoles


class Command(BaseCommand):

    def handle(self, *args, **options):
        # добавляем тестовых пользователей
        CustomUser.objects.filter(email__startswith='test').delete()
        for i in range(3):
            CustomUser.objects.create_user(
                first_name=f'first name {i}',
                last_name=f'last name {i}',
                user_name=f'user{i}',
                email=f'test_mail{i}@mail.ru',
                password=f'pass{i}'
            )

        # добавляем тестовых учителей
        for i in range(3):
            CustomUser.objects.create_user(
                first_name=f'teacher name {i}',
                last_name=f'teacher name {i}',
                user_name=f'teacher{i}',
                email=f'test_teacher{i}@mail.ru',
                password=f'pass{i}',
                role=UserRoles.TEACHER
            )

        # добавляем тестового модератора
        CustomUser.objects.filter(email__startswith='moderator').delete()
        moderator = CustomUser(
            email='moderator@mail.ru',
            first_name='moderator_name',
            last_name='moderator_surname',
            user_name='moderator_name',
            is_staff=True,
            is_superuser=True,
            is_active=True,
            role=UserRoles.MODERATOR
        )
        moderator.set_password('123')
        moderator.save()

        # добавляем тестового админа superuser
        CustomUser.objects.filter(email='admin@mail.ru').delete()
        CustomUser.objects.create_superuser('admin@mail.ru', 'admin',
                                            user_name='admin',
                                            role=UserRoles.MODERATOR)
