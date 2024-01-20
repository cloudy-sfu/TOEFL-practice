from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import ObjectDoesNotExist


class SelectLecture(forms.Form):
    search_lecture = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    lecture = forms.ModelChoiceField(
        queryset=Lecture.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        empty_label=None,
    )
    show_answers = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False,
    )


@login_required(login_url='/login')
def view_lecture(req):
    lecture_form = SelectLecture(req.POST)
    if not lecture_form.is_valid():
        return redirect('/?message=Request is invalid.')
    lecture = lecture_form.cleaned_data['lecture']
    questions = lecture.listeningquestion_set.order_by('idx')
    answers = {q.idx: ListeningAnswer.objects.filter(
        question=q, user=req.user).order_by('-created_time') for q in questions}
    context = {
        "passage": lecture,
        "questions": questions,
        "answers": answers,
        "show_answers": lecture_form.cleaned_data['show_answers']
    }
    return render(req, 'listening.html', context)


class ListeningAnswerSheet(forms.Form):
    lecture = forms.ModelChoiceField(queryset=Lecture.objects.all(), required=True)

    def load_questions(self, lecture):
        for question in lecture.listeningquestion_set.all():
            self.fields[question.idx.__str__()] = forms.MultipleChoiceField(
                choices=[('A', 'A'), ('B', 'B'), ('C', 'C'),
                         ('D', 'D'), ('E', 'E'), ('F', 'F')],
                required=False
            )


@login_required(login_url='/login')
def answer_listening(req):
    passage_id = req.POST.get('passage')
    try:
        passage = Lecture.objects.get(id=passage_id)
    except (ObjectDoesNotExist, TypeError):
        return redirect('/?message=The program lost track of which passage you are '
                        'working on.')
    ras = ListeningAnswerSheet(req.POST)
    ras.load_questions(passage)
    if not ras.is_valid():
        return redirect('/?message=The POST data of answers is invalid.')
    for qid_str, letters in ras.cleaned_data.items():
        if qid_str.isdigit() and letters:
            try:
                question = ListeningQuestion.objects.get(passage=passage, idx=int(qid_str))
            except ObjectDoesNotExist:
                continue
            answer = ''.join(sorted(letters))
            listening_answer = ListeningAnswer(user=req.user, question=question,
                                               answer=answer)
            listening_answer.save()
    return redirect('/')
