from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
#from aniauth.forms import RegistrationForm


# WORK VIEWS - User shouldn't actually end up on these pages.
def account(request):
    return redirect('/account/profile')


# REAL views
"""
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            user = authenticate(email=form.cleaned_data.get('email'), password=form.cleaned_data.get('password'))
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect("/")
            
            form.add_error(None, ValidationError('Invalid Email/Password combination', code='invalid'))
            return render(request, "login.djhtml", {'form': form})
    else:
        form = LoginForm()
    
    return render(request, "login.djhtml", {'form': form})
"""
def register(request): return render(request, "account_base.djhtml")

@login_required
def profile(request): return render(request, "account_base.djhtml")