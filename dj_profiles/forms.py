from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.template import Template, Context

from .models import User
from .tasks import password_recovery


class UserCreateForm(UserCreationForm):
    """ Форма регистрации пользователя """

    class Meta:
        model = User
        fields = ('email', 'name', 'first_name', 'last_name', 'date_birth')
        widgets = {'date_birth': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        template = Template('{% include "dj_profiles/include/user_create_help_text.html" %}')
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            context = Context({'help_text': self.fields[field].help_text})
            self.fields[field].help_text = template.render(context)


class UserAuthenticationForm(AuthenticationForm):
    """ Форма авторизации пользователя """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control mb-3'


class UserChangeFormAdmin(UserChangeForm):
    """ Форма изменения данных пользователя """

    class Meta:
        model = User
        fields = ('name', 'first_name', 'last_name', 'date_birth')


class ProfileChangeForm(forms.ModelForm):
    """ Форма изменения данных пользователя """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'date_birth', 'image')


class UserPasswordChangeForm(SetPasswordForm):
    """ Форма изменения пароля пользователя """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplate': 'off'
            })


class UserPasswordResetForm(PasswordResetForm):
    """ Форма сброса пароля """
    email = forms.EmailField(
        label='Электронная почта',
        max_length=255,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'id_email', 'autocomplete': 'email'})
    )

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email,
                  html_email_template_name=None):
        context['user'] = context['user'].id  # Для сериализации данных при передаче в функцию delay.
        password_recovery.delay(subject_template_name=subject_template_name,
                                email_template_name=email_template_name,
                                context=context, from_email=from_email, to_email=to_email,
                                html_email_template_name=html_email_template_name)


class UserPasswordResetConfirmForm(SetPasswordForm):
    """ Форма смены пароля """
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='Подтвердите пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}))
