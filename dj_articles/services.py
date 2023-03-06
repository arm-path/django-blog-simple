from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import resolve

from .models import Article


def change_queryset(**kwargs):
    slug = resolve(kwargs["url_address"]).kwargs['slug']
    if Article.objects.filter(slug=slug):
        if Article.objects.get(slug=slug).author == kwargs["current_user"]:
            return kwargs["super_objects"].all()
    return kwargs["manager_objects"]


def pagination(request, objects, count_objects, json=False):
    paginator = Paginator(objects, count_objects)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj




