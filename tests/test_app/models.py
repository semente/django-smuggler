from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=255)
    path = models.SlugField(unique=True)
    body = models.TextField()
