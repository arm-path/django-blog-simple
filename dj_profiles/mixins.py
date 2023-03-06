from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.http import Http404, JsonResponse
from django.views.generic.edit import ModelFormMixin

from .forms import UserCreateForm, UserAuthenticationForm, ProfileChangeForm, UserPasswordChangeForm
from .serializers import UserSerializer

User = get_user_model()


class ProfileDetailMixin(ModelFormMixin):
    """ Профиль пользователя | Изменение пользователя"""
    model = User
    form_class = ProfileChangeForm
    queryset = User.objects.all()

    def get_queryset(self):
        if self.request.user.pk == self.kwargs.get('pk'):
            return self.queryset
        else:
            raise Http404()

    def get_initial(self):
        return model_to_dict(self.get_object())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        return self.form_valid(form) if form.is_valid() else self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        user_serializer = UserSerializer(self.object)
        return JsonResponse({'user': user_serializer.data, 'updated': True})

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors, 'updated': False})


class UserCreateMixin:
    """ Регистрация пользователя """
    model = User
    form_class = UserCreateForm

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        # email = form.cleaned_data['email']
        # password = form.cleaned_data['password1']
        # user = authenticate(username=email, password=password)
        # login(self.request, user)
        return form_valid


class UserAuthenticationMixin:
    """ Авторизация пользователя """
    form_class = UserAuthenticationForm

    def get_success_url(self):
        return self.success_url


class UserPasswordChangeMixin:
    """ Изменение пароля пользователя """
    form_class = UserPasswordChangeForm

    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'pk': self.request.user.pk})
