from django.db import models
from ckeditor.fields import RichTextField


class IndependentSp(models.Model):
    title = models.CharField(max_length=200, unique=True)
    question = models.TextField()

    def __str__(self):
        return self.title


class IntegratedSp(models.Model):
    title = models.CharField(max_length=200, unique=True)
    passage = RichTextField(blank=True)
    conversation = models.FileField(upload_to='speaking_conv/')

    def __str__(self):
        return self.title
