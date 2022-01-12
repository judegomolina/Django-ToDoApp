from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms.widgets import Widget


class CustomUser(AbstractUser):
    birthday = models.DateField(null=False, blank=False)
    date_created = models.DateField(auto_now_add=True)
    REQUIRED_FIELDS = ['email', 'birthday']
