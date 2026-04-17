from django.conf import settings
from django.shortcuts import redirect


def login_required_custom(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:  # sorov.foydalanuvchi
            return func(request, *args, **kwargs)
        else:
            return redirect(settings.LOGIN_URL)

    return inner
