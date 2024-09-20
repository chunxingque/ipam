# -*- encoding: utf-8 -*-

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect



from .forms import LoginForm, SignUpForm,CustomUserChangeForm


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/home/")
            else:
                msg = '账号密码错误'
        else:
            msg = '请填入账号密码'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


@login_required(login_url="/login/")
def user_add(request):
    msg = None
    success = False
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
        
            return redirect('/user/')

        else:
            return render(request, 'accounts/user_add.html', {"form": form, "msg": msg, "success": success})
    else:
        form = SignUpForm()
        return render(request, 'accounts/user_add.html', {"form": form, "msg": msg, "success": success})


@login_required(login_url="/login/")
def user_edit(request,pk):
    msg = None
    success = False
    user_obj = User.objects.get(id=pk)
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            msg = '用户修改成功'
            success = True

        return render(request, 'accounts/user_edit.html', {"form": form,"id": pk,"msg": msg, "success": success})
    else:
        form = CustomUserChangeForm(instance=user_obj)
        return render(request, 'accounts/user_edit.html', {"form": form, "id": pk, "msg": msg, "success": success})

@login_required(login_url="/login/")
def user_del(request,pk):
    user_obj = User.objects.get(id=pk)
    user_obj.delete()
    return HttpResponseRedirect('/user/')


@login_required(login_url="/login/")
@require_GET
def users_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    ip_addresses_obj = User.objects.all().order_by("id")
    paginator = Paginator(ip_addresses_obj, per_page=int(page_size))
    users = paginator.get_page(page)
    
    return render(request, 'accounts/users.html', {'users': users})

@login_required(login_url="/login/")
def password_change(request,pk):
    msg = None
    success = False
    user = User.objects.get(id=pk)
    
    if request.method == "POST":
        form = PasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            success = True
            msg = '密码修改成功'
        
        return render(request, 'accounts/password_change.html', {'form': form,'id': pk,"msg": msg, "success": success})
    else:
        form = PasswordChangeForm(user=user,initial={'old_password': '','new_password1': '', 'new_password2': ''})
        return render(request, 'accounts/password_change.html', {'form': form,'id': pk,"msg": msg, "success": success})