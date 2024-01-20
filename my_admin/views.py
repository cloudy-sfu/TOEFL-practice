from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth import login, logout, authenticate


class LoginSheet(forms.Form):
    username = forms.CharField(max_length=64, required=True,
                               widget=forms.TextInput({"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput({"class": "form-control"}),
                               max_length=64, required=True)


def view_login(req, **kwargs):
    message = kwargs.get('message')
    context = {
        "login_form": LoginSheet(),
        "message": message,
    }
    return render(req, "login.html", context)


def add_login(req):
    sheet1 = LoginSheet(req.POST)
    if not sheet1.is_valid():
        return view_login(req, message="Login request is invalid.")
    user = authenticate(req,
                        username=sheet1.cleaned_data['username'],
                        password=sheet1.cleaned_data['password'])
    if not user:
        return view_login(req, message="Username or password is not correct.")
    login(req, user)
    return redirect("/")


@login_required(login_url='/main')
def delete_login(req):
    logout(req)
    return redirect('/login')
