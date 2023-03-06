from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages

from six import text_type


class TokenGenerator(PasswordResetTokenGenerator):
    """ Генерация токена """
    def _make_hash_value(self, user, timestamp):
        return (
                text_type(user.pk) + text_type(timestamp) + text_type(user.is_active))


account_activation_token = TokenGenerator()


def user_activate_email(request, uidb64, token):
    """ Активация пользователя по электронному адресу """
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        message = 'Спасибо за подтверждение по электронной почте. Теперь вы можете войти в свою учетную запись.'
        messages.success(request, message)
    else:
        messages.error(request, 'Ссылка активации недействительна!')
