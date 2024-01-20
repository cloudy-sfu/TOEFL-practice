from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import ObjectDoesNotExist


class SelectPassage(forms.Form):
    search_passage = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    passage = forms.ModelChoiceField(
        queryset=Passage.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        empty_label=None,
    )
    show_answers = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False,
    )


@login_required(login_url='/login')
def view_reading(req):
    passage_form = SelectPassage(req.POST)
    if not passage_form.is_valid():
        return redirect('/?message=Request is invalid.')
    passage = passage_form.cleaned_data['passage']
    questions = passage.readingquestion_set.order_by('idx')
    answers = {q.idx: ReadingAnswer.objects.filter(
        question=q, user=req.user).order_by('-created_time') for q in questions}
    context = {
        "passage": passage,
        "questions": questions,
        "answers": answers,
        "show_answers": passage_form.cleaned_data['show_answers']
    }
    return render(req, 'reading.html', context)


class ReadingAnswerSheet(forms.Form):
    passage = forms.ModelChoiceField(queryset=Passage.objects.all(), required=True)

    def load_questions(self, passage):
        for question in passage.readingquestion_set.all():
            self.fields[question.idx.__str__()] = forms.MultipleChoiceField(
                choices=[('A', 'A'), ('B', 'B'), ('C', 'C'),
                         ('D', 'D'), ('E', 'E'), ('F', 'F')],
                required=False
            )


@login_required(login_url='/login')
def answer_reading(req):
    passage_id = req.POST.get('passage')
    try:
        passage = Passage.objects.get(id=passage_id)
    except (ObjectDoesNotExist, TypeError):
        return redirect('/?message=The program lost track of which passage you are '
                        'working on.')
    ras = ReadingAnswerSheet(req.POST)
    ras.load_questions(passage)
    if not ras.is_valid():
        return redirect('/?message=The POST data of answers is invalid.')
    for qid_str, letters in ras.cleaned_data.items():
        if qid_str.isdigit() and letters:
            try:
                question = ReadingQuestion.objects.get(passage=passage, idx=int(qid_str))
            except ObjectDoesNotExist:
                continue
            answer = ''.join(sorted(letters))
            reading_answer = ReadingAnswer(user=req.user, question=question, answer=answer)
            reading_answer.save()
    return redirect('/')
