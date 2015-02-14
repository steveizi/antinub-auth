from django.shortcuts import render


# TODO: Tasks marked in base.djhtml

def register(request):
    return render(request, "account.djhtml")

def login(request):
    return render(request, "account.djhtml")

def logout(request):
    return render(request, "account.djhtml")