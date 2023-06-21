import uuid

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.mail import send_mail


from .forms import SignUpForm, SettingsForm
from .models import Activation


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            activation_key = str(uuid.uuid4())
            activation = Activation(user=user, key=activation_key)
            activation.save()

            subject = 'Activate your account'
            message = f'Hi {user.email}, please click the following link to activate your account:' \
                      f' http://localhost:8000/accounts/signup/confirm/{activation_key}/'
            from_email = 'chess220807@gmail.com'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            return redirect('signup_done')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def signup_confirm(request, activation_key):
    try:
        activation = Activation.objects.get(key=activation_key)
    except Activation.DoesNotExist:
        return render(request, 'signup_confirm.html', {'success': False})
    if activation.user.is_active:
        return render(request, 'signup_confirm.html', {'success': False})
    activation.user.is_active = True
    activation.user.save()
    activation.delete()
    login(request, activation.user)
    return render(request, 'signup_confirm.html', {'success': True})


def signup_done(request):
    return render(request, 'signup_done.html')


def log_in(request):
    if request.method == 'POST':
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('posts')
        else:
            error_message = 'Invalid login credentials'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html', {})


@login_required
def settings(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your settings have been updated.')
            return redirect('settings')
    else:
        form = SettingsForm(instance=request.user)
    return render(request, 'settings.html', {'form': form})

