from django.shortcuts import render,redirect, get_object_or_404
from .models import User
from .forms import ChangeUserForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponseForbidden
# Create your views here.

# def index(request):
#     users = User.objects.all()

#     context = {
#         'users' : users
#     }
#     return render(request,'accounts/index.html',context)

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
            user.recommend = True
            user.save()
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
            user.recommend = True
            user.save()
            auth_login(request,user)
            return redirect('movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form
    }
    return render(request,'accounts/login.html',context)

def logout(request):
    user = request.user
    user.recommend = False
    user.save()
    auth_logout(request)
    return redirect('movies:index')

@login_required
def follow(request, user_pk):
    if request.is_ajax():
        user = get_object_or_404(User, pk=user_pk)
        is_followed = True
        if request.user in user.followings.all():
            user.followings.remove(request.user)
            is_followed = False
        else:
            user.followings.add(request.user)
            is_followed = True
        count = user.followings.count()
        return JsonResponse({'is_followed':is_followed,'count':count})
    else:
        return HttpResponseForbidden()