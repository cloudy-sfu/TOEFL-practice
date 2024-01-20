from django.db import models
from ckeditor.fields import RichTextField


class IntegratedWt(models.Model):
    title = models.CharField(max_length=200, unique=True)
    passage = RichTextField()
    lecture = models.FileField(upload_to='writing_lec/')

    def __str__(self):
        return self.title


class AcDiscussion(models.Model):
    title = models.CharField(max_length=200, unique=True)
    passage = RichTextField()
    answer = RichTextField(blank=True)

    def __str__(self):
        return self.title
