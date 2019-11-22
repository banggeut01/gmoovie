from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

def index(request):
    accounts = User.objects.all()
    context = {
        'accounts': accounts
    }
    return render(request, 'accounts/index.html', context)

def detail(request, account_pk):
    account = get_object_or_404(User, id=account_pk)
    context = {
        'account': account
    }
    return render(request, 'accounts/profile.html', context)

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('movies:index')

def follow(request, account_pk):
    user_profile = get_object_or_404(get_user_model(), pk=account_pk)
    if request.user in user_profile.followers.all(): 
        user_profile.followers.remove(request.user)
    else:
        user_profile.followers.add(request.user)
    return redirect('accounts:detail', account_pk)