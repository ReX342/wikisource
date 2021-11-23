from django.db import models

# Create your models here.
# https://learndjango.com/tutorials/django-markdown-tutorial
class Entry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title