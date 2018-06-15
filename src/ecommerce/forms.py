from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=128)
    email = forms.EmailField(max_length=64)
    subject = forms.CharField(max_length=128)
