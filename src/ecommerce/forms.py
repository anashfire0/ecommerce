from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

class ContactForm(forms.Form):
    name = forms.CharField(max_length=128)
    email = forms.EmailField(max_length=64)
    subject = forms.CharField(max_length=128)

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

