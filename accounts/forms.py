from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone

from accounts.admin import UserCreationForm
from accounts.models import User


class LoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=254)
    
    error_messages = {
        'invalid_login': "Please enter a correct email and password. "
                         "Note that both fields may be case-sensitive.",
        'inactive': "This has not yet been activated. "
                    "Another activation email has been sent.",
    }
    
    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            UserCreationForm.create_activation_key(user)
            UserCreationForm.send_activation_email(user)
            
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )
          
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
    email = forms.EmailField(max_length=254, required=True)
    activation_key = forms.CharField(min_length=40, max_length=40, required=True)
    
    error_messages = {
        'invalid_key': "This email-key combination is not valid.",
        'expired_key': "This key has expired. A new key has been sent.",
    }
    
    def clean_activation_key(self):
        email = self.cleaned_data.get('email')
        activation_key = self.cleaned_data.get('activation_key')
        
        try:
            valid_user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError(
                self.error_messages['invalid_key'],
                code='invalid_key',
            )
        
        valid_key = valid_user.activationkey
        if not valid_key:
            raise forms.ValidationError(
                self.error_messages['invalid_key'],
                code='invalid_key',
            )
        
        if not valid_key.value == activation_key:
            raise forms.ValidationError(
                self.error_messages['invalid_key'],
                code='invalid_key',
            )
        
        self.user = valid_user
        
        if valid_key.expiration < timezone.now():
            raise forms.ValidationError(
                self.error_messages['expired_key'],
                code='expired_key',
            )
            UserCreationForm.create_activation_key(self.user)
            UserCreationForm.send_activation_email(self.user)
        
        return activation_key
    
    def activate(self):
        if not self.user: return # Function has been called before validation.
        
        self.user.is_active = True # Activate the user
        self.user.save()
        self.user.activationkey.delete() # Clear the now used activation key.
    
    helper = FormHelper()
    helper.form_show_labels = False
    helper.layout = Layout(
        Field('email', placeholder='Email Address'),
        Field('activation_key', placeholder='Activation Key'),
        FormActions(
            Submit('submit', 'Submit', css_class="btn-success"),
            HTML("<a class='btn btn-danger' href='/'>Cancel</a>"),
        )
    )