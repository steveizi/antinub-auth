from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib import messages


# TODO: Tasks marked in base.djhtml

# WORK VIEWS - User shouldn't actually load these.
def account(request):
    return redirect('/account/profile')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        next_url = request.POST['next_url']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect(next_url)
            else:
                return redirect(next_url)
        
        return redirect(next_url)
    else:
        return redirect('/')

def logout(request):
    auth_logout(request)
    return redirect('/')


# REAL views
def register(request):
    return render(request, "account.djhtml")

def profile(request):
    return render(request, "account.djhtml")