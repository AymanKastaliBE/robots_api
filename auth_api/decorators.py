from django.urls import reverse
from functools import wraps
from django.shortcuts import redirect
from django.conf import settings


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # return redirect(reverse("auth_api:custom_token_create_view"))
            login_url = settings.LOGIN_URL_GET
            return redirect(reverse(login_url))
        return view_func(request, *args, **kwargs)
    return wrapper


def protect_login_page_from_logged_in_users(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            user_profile_url = settings.USER_PROFILE_URL
            return redirect(reverse(user_profile_url))
        return view_func(request, *args, **kwargs)
    return wrapper