from django import forms

from django.contrib.auth.forms import AuthenticationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field
from crispy_forms.bootstrap import FormActions


class LoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=254)
          
    helper = FormHelper()
    helper.form_show_labels = False
    helper.layout = Layout(
        Field('username', placeholder='Email'),
        Field('password', placeholder='Password'),
        FormActions(
                    Submit('submit', 'Submit'),
                    HTML("<a class='btn btn-default' href='/'>Cancel</a>"),
                    ),
        )
    
class RegistrationForm(forms.Form):
    # TODO: Finish registration Form
    pass