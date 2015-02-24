from datetime import timedelta as tdelta

from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    An class implementing a fully featured ANIUser model with
    admin-compliant permissions.
    Email and password are required. Other fields are optional.
    """
    email = models.EmailField('email address', unique=True,
        error_messages={
            'unique': "A user with that email already exists.",
        })
    is_staff = models.BooleanField('staff status', default=False,
        help_text='Designates whether the user can log into this admin '
                    'site.')
    is_active = models.BooleanField('active', default=True,
        help_text='Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        """
        ANIUsers are identified by email address.
        """
        return self.email

    def get_short_name(self):
        """
        ANIUsers are identified by email address.
        """
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)
    
    
def activation_timeout():
        # Helper function for ConfirmationKey model
        return timezone.now() + tdelta(days=settings.ACTIVATION_KEY_TIMEOUT_DAYS)
    
class ActivationKey(models.Model):
    user = models.OneToOneField(User)
    value = models.CharField(max_length=40)
    expiration = models.DateTimeField(default=activation_timeout)
    
    def __str__(self):
        return self.value