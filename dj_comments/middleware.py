import threading
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve

_local_storage = threading.local()


class RequestGetUser(MiddlewareMixin):

    def process_request(self, request):
        _local_storage.url_address = request.path_info

        if request.user:
            _local_storage.user = request.user


def get_user_for_storage():
    user = getattr(_local_storage, 'user', None)
    user = None if user is None or user.is_anonymous else user
    return user


def get_url_for_storage():
    return getattr(_local_storage, 'url_address', None)
