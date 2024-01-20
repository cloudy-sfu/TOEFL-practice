from django.db import models
from reading.models import Passage, ReadingQuestion
from listening.models import Lecture
from speaking.models import IndependentSp, IntegratedSp
from writing.models import IntegratedWt, AcDiscussion


class Practice(models.Model):
    practice_name = models.CharField(max_length=200)
    reading_list = models.ManyToManyField(Passage, blank=True)
    listening_list = models.ManyToManyField(Lecture, blank=True)
    speaking_1 = models.ForeignKey(
        IndependentSp, blank=True, null=True, on_delete=models.CASCADE)
    speaking_2 = models.ForeignKey(
        IntegratedSp, blank=True, null=True, on_delete=models.CASCADE,
        related_name='IntegratedSp_Q2')
    speaking_3 = models.ForeignKey(
        IntegratedSp, blank=True, null=True, on_delete=models.CASCADE,
        related_name='IntegratedSp_Q3')
    speaking_4 = models.ForeignKey(
        IntegratedSp, blank=True, null=True, on_delete=models.CASCADE,
        related_name='IntegratedSp_Q4')
    writing_1 = models.ForeignKey(
        IntegratedWt, blank=True, null=True, on_delete=models.CASCADE)
    writing_2 = models.ForeignKey(
        AcDiscussion, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.practice_name
