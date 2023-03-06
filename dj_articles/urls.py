from django.urls import path

from .views import AdministrativePanelView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView
from .views import ArticleListView, ArticleDetailView
from .views import CommentPublishedView, CommentDeleteView, ArticleReputation, comment_more


urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('article/<slug:slug>', ArticleDetailView.as_view(), name='article_detail'),
    path('comment-published/article/<slug:slug>/', CommentPublishedView.as_view(), name='comment_published'),
    path('comment-delete/article/<slug:slug>/', CommentDeleteView.as_view(), name='comment_delete'),
    path('article-reputation/<slug:slug>/', ArticleReputation.as_view(), name='article_reputation'),
    path('article-comment-more/<slug:slug>/', comment_more, name='comment_more'),
    path('administrative-panel/', AdministrativePanelView.as_view(), name='administrative_panel'),
    path('administrative/article-create/', ArticleCreateView.as_view(), name='article_create'),
    path('administrative/article/<slug:slug>/update/', ArticleUpdateView.as_view(), name='article_update'),
    path('administrative/article/<slug:slug>/delete/', ArticleDeleteView.as_view(), name='article_delete')
]
