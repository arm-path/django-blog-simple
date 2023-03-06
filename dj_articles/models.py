from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse_lazy

User = get_user_model()


class Category(models.Model):
    title = models.CharField('Название', unique=True, max_length=255)
    slug = models.SlugField('URL', unique=True, max_length=255)
    description = models.TextField('Описание', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(models.Model):
    title = models.CharField('Название', unique=True, max_length=65)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Категория')
    slug = models.SlugField('URL', unique=True, max_length=65)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Article(models.Model):
    title = models.CharField('Название', max_length=255)
    slug = models.SlugField('URL', max_length=255, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Категория')
    image = models.ImageField('Изображение', upload_to='article/%Y/', blank=True, null=True)
    text = models.TextField('Текст статьии')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Теги')
    created = models.DateTimeField('Создано', auto_now_add=True)
    updated = models.DateTimeField('Обновлено', auto_now=True)
    reputation = models.ManyToManyField(User, blank=True, related_name='article_reputation', verbose_name='Репутация')
    comments = GenericRelation('dj_comments.Comment', object_id_field='object_id', content_type_field='source')

    def get_absolute_url(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse_lazy('article_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse_lazy('article_delete', kwargs={'slug': self.slug})

    def __str__(self):
        return f'Статья: {self.title} | {self.author.name}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьии'
        ordering = ('-created',)
