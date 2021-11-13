from django import forms
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from customAdmin.forms import AccountAuthenticationForm
from .models import *

# Create your views here.


class admin_screen_view(View):
    def get(self, request):
        return render(request, 'admin/index.html', {})


def logout_screen_view(request):
    logout(request)
    return redirect('admin-login')


def login_screen_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('admin-dashboard')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('admin-dashboard')
    else:
        form = AccountAuthenticationForm()

    context['form'] = form
    return render(request, 'admin/login.html', context)
