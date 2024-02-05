import re

from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


class Passage(models.Model):
    title = models.CharField(max_length=200, unique=True)
    article = RichTextField(blank=True)
    source = models.URLField(blank=True)

    def __str__(self):
        return self.title

    @property
    def n_questions(self):
        return self.readingquestion_set.count()


paragraph = re.compile(r"paragraph (\d+)", re.IGNORECASE)


class ReadingQuestion(models.Model):
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE)
    idx = models.IntegerField(verbose_name='Index in passage')
    citation = RichTextField(blank=True)
    question = models.TextField()
    choice_a = models.TextField(blank=True)
    choice_b = models.TextField(blank=True)
    choice_c = models.TextField(blank=True)
    choice_d = models.TextField(blank=True)
    choice_e = models.TextField(blank=True)
    choice_f = models.TextField(blank=True)
    answer = models.CharField(max_length=6, blank=True)

    def __str__(self):
        return f"[Q{self.idx}] {self.passage.title}"

    @property
    def has_multiple_answer(self):
        return len(self.answer) > 1

    @property
    def question_paragraph_href(self):
        question_text = []
        all_paragraph_symbol = paragraph.finditer(self.question)
        p = 0  # pointer
        for symbol in all_paragraph_symbol:
            question_text.append(self.question[p:symbol.start()])
            question_text.append(f"<a href=\"#p{symbol.group(1)}\" onclick=\""
                                 f"highlight_paragraph({symbol.group(1)})\">"
                                 f"{self.question[symbol.start():symbol.end()]}</a>")
            p = symbol.end()
        question_text.append(self.question[p:])
        return ''.join(question_text)


class ReadingAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(ReadingQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=6, blank=True)
