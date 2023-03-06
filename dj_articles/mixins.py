from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import Template, Context
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.generic.edit import FormMixin

from dj_comments.forms import CommentForm
from dj_comments.models import Comment
from .forms import ArticleCreateUpdateForm
from .models import Article, Category, Tag
from .serializers import ArticleSerializer
from .services import pagination


class ArticleListMixin:
    model = Article

    def get_queryset(self):
        if self.request.GET.get('search'):
            object_list = self.model.objects.filter(title__icontains=self.request.GET.get('search'))
        else:
            object_list = self.model.objects.all()
        return object_list


class ArticleDetailMixin:
    model = Article

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object, comments=pagination(request, self.object.comments.all(), 2))
        return self.render_to_response(context)


class SendCommentMixin(FormMixin):
    form_class = CommentForm

    @method_decorator(login_required(login_url='user_authentication'))
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        return self.form_valid(form) if form.is_valid() else self.form_invalid(form)

    def form_valid(self, form):
        self.comment = form.save(commit=False)
        self.comment.content_object = self.object
        self.comment.save()
        template = Template('{% include "dj_articles/include/comment_create.html" %}')
        context = Context({'comment': self.comment, 'object': self.object, 'request': self.request})
        return HttpResponse(template.render(context))

    def form_invalid(self, form):
        return JsonResponse({'error': 'Комментарий не был добавлен, произошла ошибка!'})


class CommentMixin:
    def get_comment(self, request, **kwargs):
        if not Article.objects.filter(slug=self.kwargs['slug']):
            raise Http404
        if not request.POST.get('comment') or not request.POST['comment'].isdigit():
            raise PermissionDenied
        comment = Comment.objects.get(pk=int(request.POST['comment']))
        if self.action == 'Published':
            if Article.objects.get(slug=self.kwargs['slug']).author != request.user:
                raise PermissionDenied
            comment.published = False if comment.published else True
            comment.save()
            return comment.published
        if self.action == 'Deleted':
            if Article.objects.get(slug=self.kwargs['slug']).author != request.user and comment.user != request.user:
                raise PermissionDenied
            comment.delete()
            return True

    def post(self, request, *args, **kwargs):
        return JsonResponse({self.response: self.get_comment(request, **kwargs)})


class AdministrativePanelMixin:
    model = Article

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_filter_data(context, 'Административная панель')

    def get(self, request, *args, **kwargs):
        context = super().get(request, *args, **kwargs).context_data
        if request.GET.get('json'):
            (articles, next_page) = self.get_articles()
            return JsonResponse({'articles': articles.data, 'nextPage': next_page})
        return self.render_to_response(context)


class FilterMixin:
    def get_filter_data(self, context, title):
        filter_elements = list(self.object_list.values('category', 'tags'))
        categories_pk = tuple(set([el['category'] for el in filter_elements]))
        tags_pk = tuple(set([el['tags'] for el in filter_elements]))
        context['categories'] = Category.objects.filter(pk__in=categories_pk).distinct()
        context['tags'] = Tag.objects.filter(pk__in=tags_pk).distinct()
        context['title'] = title
        return context

    def get_articles(self):
        tags = self.request.GET.get('tag')
        categories = self.request.GET.get('category')
        search = self.request.GET.get('search')
        tags_pk = [int(tag) for tag in tags.split(',')] if tags else None
        categories_pk = [int(category) for category in categories.split(',')] if categories else None
        if tags_pk and categories_pk:
            articles = Article.objects.filter(author=self.request.user, category__in=categories_pk,
                                              tags__in=tags_pk).distinct()
        elif categories_pk:
            articles = Article.objects.filter(author=self.request.user, category__in=categories_pk).distinct()
        elif tags_pk:
            articles = Article.objects.filter(author=self.request.user, tags__in=tags_pk).distinct()
        elif search:
            articles = Article.objects.filter(author=self.request.user, title__icontains=search)
        else:
            articles = Article.objects.filter(author=self.request.user).distinct()

        articles = pagination(self.request, articles, self.paginate_by)
        articles_serializer = ArticleSerializer(articles, many=True)

        return articles_serializer, articles.has_next()


class ArticleCreateMixin:
    form_class = ArticleCreateUpdateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.slug = slugify(form.cleaned_data['title'])
        self.object.save()
        messages.success(self.request, f'Статья "{self.object.title}" успешно добавлена!')
        return super().form_valid(form)


class ArticleUpdateMixin:
    model = Article
    form_class = ArticleCreateUpdateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.slug = slugify(form.cleaned_data['title'])
        self.object.save()
        messages.success(self.request, f'Статья: {self.object.title} успешно обновлена!')
        return super().form_valid(form)
