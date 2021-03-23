from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       PasswordResetForm)
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


def done_view(request, message):
    return render(request, 'custom_page.html', {message: message})


class SignUpView(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class LoginView(CreateView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('index')
    template_name = 'user_auth'


class PasswordChangeView(CreateView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'password_change.html'


class PasswordResetView(CreateView):
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_done')
    template_name = 'password_reset.html'
