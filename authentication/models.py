from django.db import models
from helpers.models import TrackingModel
from django.contrib.auth.models import(PermissionsMixin,UserManager,AbstractBaseUser)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models
from helpers.models import TrackingModel  
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import jwt
from datetime import datetime, timedelta


from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """Create and return a regular user with an email, username, and password."""
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        """Create and return a superuser with an email, username, and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TrackingModel):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)  # Added username field
    access_token = models.CharField(max_length=255, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    email_verified = models.BooleanField(
        _('email_verified'), 
        default=False,
        help_text=_('Designates whether this user has verified their email.')
    )
    
    objects = UserManager()
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'  # Authentication still uses email
    REQUIRED_FIELDS = ['username']  # Username is now required

    def __str__(self):
        return self.email

    def token(self):
        token=jwt.encode(
         {'username': self.username, 'email':self.email, 
        'exp': datetime.utcnow() + timedelta(hours=24)},
        settings.SECRET_KEY,algorithm='HS256')
        
        return token