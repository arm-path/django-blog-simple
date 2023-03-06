from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .mixins import AdministrativePanelMixin, ArticleCreateMixin, ArticleUpdateMixin, FilterMixin
from .mixins import ArticleListMixin, ArticleDetailMixin, SendCommentMixin, CommentMixin
from .models import Article
from .serializers import CommentSerializer
from .services import pagination


class ArticleListView(ArticleListMixin, ListView):
    template_name = 'dj_articles/article_list.html'
    extra_context = {'title': 'Список статей'}
    paginate_by = 7


class ArticleDetailView(SendCommentMixin, ArticleDetailMixin, DetailView):
    template_name = 'dj_articles/article_detail.html'


class CommentPublishedView(LoginRequiredMixin, CommentMixin, View):
    action = 'Published'
    response = 'published'


class CommentDeleteView(LoginRequiredMixin, CommentMixin, View):
    action = 'Deleted'
    response = 'success'


def comment_more(request, slug):
    if not Article.objects.filter(slug=slug):
        return JsonResponse({'error': True}, status=404)
    comments = pagination(request, Article.objects.get(slug=slug).comments.all(), 2)
    comments_serializer = CommentSerializer(comments.object_list, many=True)
    return JsonResponse({'comments': comments_serializer.data, 'nextPage': comments.has_next()})


class ArticleReputation(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        if not Article.objects.filter(slug=self.kwargs['slug']):
            return JsonResponse({'success': False}, status=404)
        article = Article.objects.get(slug=self.kwargs['slug'])
        article.reputation.add(request.user)
        return JsonResponse({'success': True})


class AdministrativePanelView(LoginRequiredMixin, FilterMixin, AdministrativePanelMixin, ListView):
    template_name = 'dj_articles/administrative_panel.html'
    login_url = reverse_lazy('user_authentication')
    paginate_by = 7


class ArticleCreateView(ArticleCreateMixin, CreateView):
    template_name = 'dj_articles/article_create_or_update.html'
    success_url = reverse_lazy('administrative_panel')
    extra_context = {'title': 'Добавление статьии', 'action': 'Добавить'}


class ArticleUpdateView(ArticleUpdateMixin, UpdateView):
    template_name = 'dj_articles/article_create_or_update.html'
    success_url = reverse_lazy('administrative_panel')
    extra_context = {'title': 'Обновление статьии', 'action': 'Обновить'}


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('administrative_panel')
