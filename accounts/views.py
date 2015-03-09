from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from accounts.forms import RegistrationForm, ActivationForm


@sensitive_post_parameters()
@csrf_protect
@never_cache
def register(request, template_name='accounts/register.djhtml',
        redirect_field_name=REDIRECT_FIELD_NAME,
        registration_form=RegistrationForm,
        current_app=None, extra_context=None):
    """
    Displays the registration form and handles the registration action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))
    
    if request.method == "POST":
        form = registration_form(request.POST)
        if form.is_valid():
            
            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.ACTIVATE_URL)
                
            # Register the user making sure to require email activation.
            form.save(skip_activation=False)
            
            return HttpResponseRedirect(redirect_to)
    else:
        form = registration_form()
        
    current_site = get_current_site(request)
    
    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

def activate(request, template_name='accounts/activate.djhtml',
        redirect_field_name=REDIRECT_FIELD_NAME,
        activation_form=ActivationForm,
        current_app=None, extra_context=None):
    """
    Displays the activation form and handles the activation action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))
    
    if request.method == "POST":
        form = activation_form(request.POST)    
        if form.is_valid():
            
            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_URL)
                
            # Activate the user
            form.activate()
            
            return HttpResponseRedirect(redirect_to)
    else:
        form = activation_form(request.GET)
        
    current_site = get_current_site(request)
    
    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)