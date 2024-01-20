from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from reading.views import SelectPassage
from listening.views import SelectLecture
from .models import *


class SelectPractice(forms.Form):
    search_practice = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    practice = forms.ModelChoiceField(
        queryset=Practice.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        empty_label=None,
    )


@login_required(login_url='/login')
def app_center(req):
    context = {
        "select_practice": SelectPractice(),
        "select_passage": SelectPassage(),
        "select_lecture": SelectLecture(),
        "message": req.GET.get('message'),
    }
    return render(req, 'app_center.html', context)
