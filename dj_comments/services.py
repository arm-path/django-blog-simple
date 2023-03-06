from django.urls import resolve

from dj_articles.models import Article


def change_queryset_article(**kwargs):
    slug = resolve(kwargs["url_address"]).kwargs.get('slug', None)
    if Article.objects.filter(slug=slug):
        if Article.objects.get(slug=slug).author == kwargs["current_user"]:
            return kwargs["super_objects"].all()

    return kwargs["manager_objects"]
