import hashlib
import random

from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as admin_UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.mail import send_mail
from django.shortcuts import resolve_url

from accounts.models import User, ActivationKey


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords didn't match")
        return password2

    def save(self, commit=True, skip_activation=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = skip_activation # No email confirmation required by default.
        if commit:
            user.save()
            if not skip_activation:
                self.create_activation_key(user)
                self.send_activation_email(user)
        return user
    
    @staticmethod
    def create_activation_key(user):
        salt = hashlib.sha1(str(random.random())).hexdigest()[:-5]
        activation_key = hashlib.sha1(salt+user.email).hexdigest()
        # Key expires in 48 hours by default.
        
        confirmation_key, _ = ActivationKey.objects.update_or_create(
            user=user, value=activation_key)
        
        return confirmation_key
    
    @staticmethod
    def send_activation_email(user):
        # TODO: Use corp/alliance tag
        email_subject = "[A-NI] Activate Your Account"
        email_body = ("Thanks for registering! To complete the activation of "
                      "your account please click the following link:"
                      "\n{}?activation_key={}\n\nThis key will be valid for 48"
                      " hours from the time of registration."
                      ).format(resolve_url('activate'), user.activationkey)
        
        send_mail(email_subject, email_body, settings.DEFAULT_FROM_EMAIL,
                  [user.email], fail_silently=False)
        
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Password",
        help_text="Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>.")

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class ActivationKeyInline(admin.TabularInline):
    model = ActivationKey


class UserAdmin(admin_UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    inlines = [ActivationKeyInline]
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)