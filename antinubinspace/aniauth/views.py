from django.shortcuts import render


def register(request):
    return render(request, "account.html")

def login(request):
    return render(request, "account.html")

def logout(request):
    return render(request, "account.html")