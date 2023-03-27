from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Items
from datetime import datetime


# Create your views here.
def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').upper()
        password = request.POST.get('password')

        try:
            User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password does not exist')
    return render(request, 'login.html', {'page': page, 'messages': messages})


def logout_user(request):
    logout(request)
    return redirect('login')


def register_page(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.upper()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'register.html', {'form': form, 'messages': messages})


@login_required(login_url='login')
def home(request):
    all_items = Items.objects.filter(user=request.user)
    date = datetime.now()
    print(date)
    if request.method == 'POST':
        item = Items.objects.create(
            user=request.user,
            name=request.POST.get('item')
        )
    return render(request, 'index.html', {'all_items': all_items, 'date': date})


@login_required(login_url='login')
def delete_message(request, id):
    item = Items.objects.get(id=id)
    if request.method == 'POST':
        item.delete()
        return redirect('home')
    return render(request, 'delete_page.html', {"obj": item})
