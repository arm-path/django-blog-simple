from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.db.models import signals
from django.utils import timezone

from .managers import UserManager
from .tasks import send_email_registration


class User(AbstractBaseUser, PermissionsMixin):
    """ Модель пользователя """
    email = models.EmailField('Электронная почта', max_length=150, unique=True)
    name = models.CharField('Отображаемое имя', max_length=150, unique=True)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилие', max_length=150)
    image = models.ImageField('Изображение', upload_to='profiles/', blank=True, null=True)
    date_birth = models.DateField('Дата рождения', auto_now=False, auto_now_add=False)
    is_staff = models.BooleanField('Статус администратора', default=False,
                                   help_text='Определяет, может ли пользователь войти на сайт администратора.')
    is_active = models.BooleanField('Статус активации', default=False,
                                    help_text='Определяет, является ли пользователь действительным')

    date_joined = models.DateTimeField('Дата присоединения', default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'first_name', 'last_name', 'date_birth']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


def user_post_save(sender, instance, signal, *args, **kwargs):
    """ Подтверждение электронной почты. """
    if not instance.is_active and not instance.is_staff:
        send_email_registration.delay(instance.pk)


signals.post_save.connect(user_post_save, sender=User)
