from django.db import models
from users.models import CustomUser

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    course_title = models.CharField(verbose_name='course_title',
                                    max_length=250, unique=True)
    course_description = models.TextField(verbose_name='course_description',
                                          **NULLABLE)
    teacher = models.ForeignKey(CustomUser, **NULLABLE,
                                on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.course_title}'


class Subscription(models.Model):
    """Класс подписки на курс, имеет статус да или нет"""
    created_datetime = models.DateTimeField(auto_now_add=True)
    subscription_status = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser,
                                related_name='student_subscriptions',
                                on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                related_name='teacher_subscriptions',
                                null=True,
                                blank=True)

    def __str__(self):
        return f'подписка на курс {self.course.course_title}'

    def save(self, *args, **kwargs):
        if not self.teacher:
            self.teacher = self.course.teacher
        super().save(*args, **kwargs)
