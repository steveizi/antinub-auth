from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def profile(request): return render(request, 'dashboard/base.djhtml')

@login_required
def apikeys(request): return render(request, 'dashboard/apikeys.djhtml')