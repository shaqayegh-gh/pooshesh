from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField

from apps.insurance.common.validators import mobile_char_check
from .common import BaseModel
from ..managers import UserManager


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'), blank=True, unique=True, max_length=255)
    username = models.EmailField(_('username'),unique=True)
    is_assessor = models.BooleanField(_('is_insurer') , default=False)
    is_active = models.BooleanField(_('active'), default=True,
                                 help_text=_(
                                     'Designates whether this user should be treated as active. '
                                     'Unselect this instead of deleting accounts.'),)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    phone_number = models.CharField(
        _('Phone number'), unique=True,
        validators=[mobile_char_check], max_length=10,
        error_messages={'wrong_phone_number': _('Wrong phone number')},
        help_text='write your phone number like 9121133445')

    is_verified = models.BooleanField(
        _('verified'), default=False,
        help_text=_('Designates whether this user has completed the email '
                    'verification process to allow login.'))

    otp = models.IntegerField(null=True,blank=True)
    user_slug = AutoSlugField(populate_from=['email'], unique=True)  # install django_extensions

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects= UserManager()
    def get_full_name(self):
        # The user is identified by their email address
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        # The user is identified by their email address
        return f"{self.first_name}"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

