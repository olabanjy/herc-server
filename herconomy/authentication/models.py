import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.db.models.signals import post_save, post_init, pre_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
   
    def create_user(self, username, email, password=None ):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password ):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email,  password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    def create_moderator(self, username, is_moderator, email, password ):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Moderators must have a password.')

        user = self.create_user(username, email,  password)
        user.is_superuser = False
        user.is_staff = False
        user.is_moderator = True
        user.save()

        return user
   

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_moderator = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_is_moderator(self):
        return self.is_moderator

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'email':self.email,
            'username':self.username,
            'is_moderator':self.is_moderator,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='herconomy/user_profile/', default='default_profile_pics.jpg', blank=True)
    def __str__(self):
        return self.user.email

def profile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile.objects.get_or_create(user=instance)

    profile, created = Profile.objects.get_or_create(
        user=instance)

post_save.connect(profile_receiver, sender=settings.AUTH_USER_MODEL)