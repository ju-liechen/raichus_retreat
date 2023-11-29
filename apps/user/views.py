from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect

from django.contrib.auth.tokens import PasswordResetTokenGenerator


def signup(request):
    error = None

    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT)

    if request.method == 'POST':
        email = request.POST.get('email', '').lower().strip()
        password = request.POST.get('password', '').strip()

        if '@' not in email or '.' not in email:
            error = 'Please enter a valid email.'
        elif len(password) < settings.MIN_PASSWORD_LENGTH:
            error = f'Password must be at least {settings.MIN_PASSWORD_LENGTH} characters.'
        elif not get_user_model().objects.filter(email=email).exists():
            user = get_user_model().objects.create_user(email=email, password=password)
            user.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT)
        else:
            error = 'User already exists.'

    return render(request, 'user/signup.html', context={'error': error})


def login_(request):
    error = None

    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT)

    if request.method == 'POST':
        email = request.POST.get('email', '').lower().strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT)
        else:
            error = 'Invalid email or password.'

    return render(request, 'user/login.html', context={'error': error})


def logout_(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT)
