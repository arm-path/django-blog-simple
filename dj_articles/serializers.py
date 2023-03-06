from rest_framework import serializers
from django.contrib.auth import get_user_model

from dj_comments.models import Comment
from .models import Article

User = get_user_model()


class ArticleSerializer(serializers.ModelSerializer):
    detail_url = serializers.CharField(source='get_absolute_url', read_only=True)
    change_url = serializers.CharField(source='get_update_url', read_only=True)
    delete_url = serializers.CharField(source='get_delete_url', read_only=True)

    class Meta:
        model = Article
        fields = ['pk', 'title', 'slug', 'created', 'updated', 'detail_url', 'change_url', 'delete_url']


class UserCommentSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', ]


class ArticleCommentSerializer(serializers.ModelSerializer):
    author = UserCommentSerilizer()

    class Meta:
        model = Article
        fields = ['slug', 'author']


class CommentSerializer(serializers.ModelSerializer):
    article = ArticleCommentSerializer(source='get_related_object', read_only=True)
    user = UserCommentSerilizer(read_only=True)
    url_delete = serializers.CharField(source='get_url_delete', read_only=True)
    url_published = serializers.CharField(source='get_url_published', read_only=True)

    class Meta:
        model = Comment
        fields = ['pk', 'user', 'article', 'text', 'created', 'published', 'url_delete', 'url_published']
