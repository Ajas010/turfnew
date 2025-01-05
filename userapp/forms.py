from django import forms
from .models import Userprofile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Userprofile
        fields = ("username",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Userprofile
        exclude = []