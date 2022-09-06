from tkinter import CASCADE
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)

'''-----Custom user model created here------'''
class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(_('email address'), unique=True, max_length=100)
    first_name = models.CharField(_('first name'), max_length=50, null=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=50, null=True, blank=True)
    mobile_number = models.CharField(_('mobile number'), max_length=15, null =True, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_admin = models.BooleanField(_('admin'), default=False)
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


    def get_is_active(self):
        return self.is_active

    def get_email(self):
        return self.email

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='%(class)s_profile')
#     forget_password_token = models.CharField(max_length=100, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.user.email


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.title