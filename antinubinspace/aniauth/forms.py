from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone

from aniauth.admin import UserCreationForm
from aniauth.models import ConfirmationKey


class LoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=254)
          
    helper = FormHelper()
    helper.form_show_labels = False
    helper.layout = Layout(
        Field('username', placeholder='Email'),
        Field('password', placeholder='Password'),
        FormActions(
                    Submit('submit', 'Submit', css_class="btn-success"),
                    HTML("<a class='btn btn-danger' href='/'>Cancel</a>"),
                    ),
        )
    
    
class RegistrationForm(UserCreationForm):
    helper = FormHelper()
    helper.form_show_labels = False
    helper.layout = Layout(
        Field('email', placeholder='Email'),
        Field('password1', placeholder='Password'),
        Field('password2', placeholder='Confirm Password'),
        FormActions(
            Submit('submit', 'Submit', css_class="btn-success"),
            HTML("<a class='btn btn-danger' href='/'>Cancel</a>"),
        ),
    )
    
    
class ActivationForm(forms.Form):
    activation_key = forms.CharField(min_length=32, max_length=32, required=True)
    user = None
    
    error_messages = {
        'invalid_key': "This key is not valid.",
        'expired_key': "This key has expired. A new key has been sent.",
    }
    
    def clean_activation_key(self):
        activation_key = self.cleaned_data.get('activation_key')
        
        try:
            valid_key = ConfirmationKey.objects.get(activation_key=activation_key)
        except ConfirmationKey.DoesNotExist:
            raise forms.ValidationError(
                self.error_messages['invalid_key'],
                code='invalid_key',
            )
        
        self.user = valid_key.user
        if valid_key.key_expiration < timezone.now():
            raise forms.ValidationError(
                self.error_messages['expired_key'],
                code='expired_key',
            )
            # TODO: Send a new key to the user
        
        return activation_key
    
    def activate(self):
        if not self.user: return # Function has been called before validation.
        
        self.user.is_active = True # Activate the user
        self.user.save()
    
    helper = FormHelper()
    helper.form_show_labels = False
    helper.layout = Layout(
        Field('activation_key', placeholder='Activation Key'),
        FormActions(
            Submit('submit', 'Submit', css_class="btn-success"),
            HTML("<a class='btn btn-danger' href='/'>Cancel</a>"),
        )
    )