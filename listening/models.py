from django.db import models
from django.contrib.auth.models import User


class Lecture(models.Model):
    title = models.CharField(max_length=200, unique=True)
    recording = models.FileField(upload_to='recording/')
    source = models.URLField(blank=True)
    original_text = models.TextField(blank=True)

    def __str__(self):
        return self.title

    @property
    def n_questions(self):
        return self.listeningquestion_set.count()


class ListeningQuestion(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    idx = models.IntegerField(verbose_name='Index in lecture')
    listen_again = models.FileField(upload_to='recording/', blank=True, null=True)
    question = models.TextField()
    choice_a = models.TextField(blank=True)
    choice_b = models.TextField(blank=True)
    choice_c = models.TextField(blank=True)
    choice_d = models.TextField(blank=True)
    choice_e = models.TextField(blank=True)
    choice_f = models.TextField(blank=True)
    answer = models.CharField(max_length=6, blank=True)

    def __str__(self):
        return f"[Q{self.idx}] {self.lecture.title}"

    @property
    def has_multiple_answer(self):
        return len(self.answer) > 1


class ListeningAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(ListeningQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=6, blank=True)
