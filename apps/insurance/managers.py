from django.contrib.auth.base_user import BaseUserManager
from django.db import models




class UserManager(BaseUserManager):
    def create_user(self, email, password,**extra_field):
        """
        Creates and saves a User with the given email,phone and password.
        """
        if not email:
            raise ValueError('Users must have an email address')


        user = self.model(email=self.normalize_email(email),username=self.normalize_email(email),
                          **extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password, **extra_field):
        """
        Creates and saves a superuser with the given email,phone and password.
        """
        user = self.create_user(email, password=password, **extra_field )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class ProfileManager(models.Manager):
    pass


class InsurerManager(BaseUserManager):
    def create_insurer_user(self, email, password, ** extra_field):
        """
        Creates and saves a User with the given email,phone and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), username=self.normalize_email(email),
                          **extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user


class AssessorManager(BaseUserManager):

    def create_assessor_user(self, email, password,eval_code):
        if not email:
            raise ValueError('Users must have an email address')

        assessor = self.model(email=self.normalize_email(email),username=self.normalize_email(email),
                          eval_code=eval_code)
        assessor.set_password(password)
        assessor.save(using=self._db)
        return assessor