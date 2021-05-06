from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, phone,first_name=None,last_name=None ,password=None):
        """
        Creates and saves a User with the given email,phone and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not phone:
            raise ValueError('Users must have an phone number')

        user = self.model(email=self.normalize_email(email),first_name=first_name,last_name=last_name ,phone_number=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, phone, password):
        """
        Creates and saves a staff user with the given email,phone and password.
        """
        user = self.create_user(email, phone, password=password, )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password):
        """
        Creates and saves a superuser with the given email,phone and password.
        """
        user = self.create_user(email, phone, password=password, )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class ProfileManager(models.Manager):
    pass
