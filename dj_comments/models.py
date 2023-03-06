from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Manager, Q
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse_lazy, resolve

from dj_comments.middleware import get_user_for_storage, get_url_for_storage
from .services import change_queryset_article

User = get_user_model()


class CommentObjectManager(Manager):
    def get_queryset(self):
        current_user = get_user_for_storage()
        url_address = get_url_for_storage()
        super_objects = super().get_queryset()
        manager_objects = super_objects.filter(Q(published=True) | Q(user=current_user))
        #  dj_articles.
        manager_objects = change_queryset_article(super_objects=super_objects, manager_objects=manager_objects,
                                                  url_address=url_address, current_user=current_user)
        return manager_objects


class Comment(models.Model):
    source = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='Источник')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('source', 'object_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user', verbose_name='Пользователь')
    text = models.CharField('Текст', max_length=255)
    created = models.DateTimeField('Создано', auto_now_add=True)
    published = models.BooleanField('Опубликовано', default=False)

    objects = CommentObjectManager()

    def __str__(self):
        return f'{self.user.name} | {self.text[:18]}'

    def get_related_object(self):
        return self.content_object

    def get_url_delete(self):
        if get_user_for_storage() == self.get_related_object().author or get_user_for_storage() == self.user:
            return reverse_lazy('comment_delete', kwargs={'slug': self.get_related_object().slug})
        else:
            return None

    def get_url_published(self):
        url = reverse_lazy('comment_published', kwargs={
            'slug': self.get_related_object().slug}) if get_user_for_storage() == self.get_related_object().author else None
        return url

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ['-created']


@receiver(pre_save, sender=Comment)
def set_user_for_comment(sender, instance, **kwargs):
    user = get_user_for_storage()
    if not user:
        raise Exception('Access denied, no user!')
    instance.user = user
