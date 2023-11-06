import uuid
import jwt
from django.db import models
from helpers.models import TrackingModel
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta


class UserManager(BaseUserManager):
    def create_user(self,email,password:None,**extra_fields):
        if not email:
            raise ValueError(_("The email is Required"))
        email = self.normalize_email(email=email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("SuperUser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("SuperUser must have is_superuser=True"))
        
        return self.create_user(email,password,**extra_fields)
    

class User(AbstractUser):
    id = models.CharField(max_length=8, unique=True, primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['username']


    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def token(self):
        token = jwt.encode(
            {
            'username':self.username,
            'email':self.email,
            'exp':datetime.utcnow() + timedelta(hours=24)
            },
            settings.SECRET_KEY,
            algorithm='HS256'
            )
        return token