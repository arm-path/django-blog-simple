from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.core.mail.message import EmailMessage
from django.template import loader
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from dj_project.celery import app
from .services import account_activation_token


@app.task()
def send_email_registration(user_pk):
    User = get_user_model()
    user = User.objects.get(pk=user_pk)
    mail_subject = 'Ссылка для активации отправлена на ваш адрес электронной почты'
    message = render_to_string('dj_profiles/include/user_activate_message.html',
                               {'username': user.name,
                                'domain': '127.0.0.1:8000',
                                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                'token': account_activation_token.make_token(user)
                                })
    email = EmailMessage(mail_subject, message, from_email=settings.EMAIL_HOST_USER, to=[user.email, ])
    email.send()


@app.task
def password_recovery(subject_template_name, email_template_name, context, from_email, to_email,
                      html_email_template_name=None):
    UserModel = get_user_model()
    context['user'] = UserModel.objects.get(pk=context['user'])

    from_email = settings.EMAIL_HOST_USER
    subject = loader.render_to_string(subject_template_name, context)
    subject = "".join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)
    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, "text/html")
    email_message.send()
