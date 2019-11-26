from django.shortcuts import render,redirect, get_object_or_404
from .models import User
from .forms import ChangeUserForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
# Create your views here.

def index(request):
    users = User.objects.all()

    context = {
        'users' : users
    }
    return render(request,'accounts/index.html',context)

def detail(request,user_pk):
    user = User.objects.get(pk=user_pk)
    context = {
        'puser':user
    }
    return render(request,'accounts/detail.html', context)

def signup(request):
    if request.method == 'POST':
        form = ChangeUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)
            return redirect('movies:index')
    else:
        form = ChangeUserForm()
    context = {
        'form' : form
    }
    return render(request,'accounts/signup.html',context)

def login(request):
    if request.method=='POST':
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request,user)
            return redirect('movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form
    }
    return render(request,'accounts/login.html',context)

def logout(request):
    auth_logout(request)
    return redirect('movies:index')

@require_POST
def follow(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if request.user.is_authenticated:
        if request.user != user:
            if request.user in user.followings.all():
                user.followings.remove(request.user)
            else:
                user.followings.add(request.user)
        return redirect('accounts:detail', user_pk)
    else:
        return redirect('accounts:login')