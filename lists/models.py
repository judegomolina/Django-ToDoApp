from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class List(models.Model):
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('list_edit', args=[str(self.id)])


class Bullet(models.Model):
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField()
    list = models.ForeignKey(
        List,
        on_delete=models.CASCADE,
        related_name='bullets',
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('list_edit', args=[str(self.list.id)])

