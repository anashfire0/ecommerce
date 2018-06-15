from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password' ,widget=forms.PasswordInput)

    def clean(self):
        if not self.cleaned_data['password'] == self.cleaned_data['password2']:
            raise ValidationError('Password mismatch')
        return self.cleaned_data

    def clean_username(self):
        if get_user_model().objects.filter(username__iexact=self.cleaned_data['username']).exists():
            raise ValidationError('Username is taken')
        return self.cleaned_data['username']

class GuestForm(forms.Form):
    email = forms.EmailField()