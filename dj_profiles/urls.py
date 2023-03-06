from django.urls import path, re_path

from .views import UserCreateView, UserAuthenticationView, UserLogoutView, ProfileDetailView
from .views import UserPasswordResetView, UserPasswordChangeView, UserPasswordResetConfirmView, user_activate

urlpatterns = [
    path('user-registration/', UserCreateView.as_view(), name='user_registration'),
    path('user-authentication/', UserAuthenticationView.as_view(), name='user_authentication'),
    path('user-logout/', UserLogoutView.as_view(), name='user_logout'),
    path('user-profile/<int:pk>/', ProfileDetailView.as_view(), name='user_profile'),
    path('user-password-change/', UserPasswordChangeView.as_view(), name='user_password_change'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            user_activate, name='activate_email'),
    path('user-password-reset/', UserPasswordResetView.as_view(), name='user_password_reset'),
    path('reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm')
]
