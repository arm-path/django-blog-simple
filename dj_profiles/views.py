from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import UserPasswordResetForm, UserPasswordResetConfirmForm
from .mixins import ProfileDetailMixin, UserCreateMixin, UserAuthenticationMixin, UserPasswordChangeMixin
from .services import user_activate_email

User = get_user_model()


class ProfileDetailView(ProfileDetailMixin, DetailView):
    """ Профиль пользователя | Изменение пользователя"""
    template_name = 'dj_profiles/user_profile.html'


class UserCreateView(UserCreateMixin, CreateView):
    """ Регистрация пользователя """
    template_name = 'dj_profiles/user_registration.html'
    success_url = reverse_lazy('administrative_panel')


class UserAuthenticationView(UserAuthenticationMixin, LoginView):
    """ Авторизация пользователя """
    template_name = 'dj_profiles/user_authentication.html'
    success_url = reverse_lazy('administrative_panel')


class UserLogoutView(LogoutView):
    """ Выход пользователя """
    model = User
    next_page = reverse_lazy('article_list')


class UserPasswordChangeView(LoginRequiredMixin, UserPasswordChangeMixin, PasswordChangeView):
    """ Изменение пароля пользователя """
    login_url = reverse_lazy('user_authentication')
    template_name = 'dj_profiles/user_change_password.html'
    extra_context = {'title': 'Изменение пароля'}


class UserPasswordResetView(SuccessMessageMixin, PasswordResetView):
    """ Восстановление пароля пользователя """
    template_name = 'dj_profiles/user_change_password.html'
    form_class = UserPasswordResetForm
    success_url = reverse_lazy('user_authentication')
    success_message = 'Мы отправили вам инструкцию по установке нового пароля на указанный адрес электронной почты ' \
                      'Вы должны получить ее в ближайшее время.Если вы не получили письмо, пожалуйста, убедитесь, ' \
                      'что вы ввели адрес с которым Вы зарегистрировались, и проверьте папку со спамом.'


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """ Ввод нового пароля пользователя """
    form_class = UserPasswordResetConfirmForm
    template_name = 'dj_profiles/user_change_password.html'
    success_url = reverse_lazy('user_authentication')
    success_message = 'Пароль успешно изменен!'


def user_activate(request, uidb64, token):
    user_activate_email(request, uidb64, token)
    return redirect(reverse_lazy('user_authentication'))
