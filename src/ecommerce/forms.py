from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=62)
    email = forms.EmailField(max_length=64)
    subject = forms.CharField(max_length=128)

    def clean_email(self):
        if not 'gmail' in self.cleaned_data['email']:
            raise forms.ValidationError('Must be gmail')
        return self.cleaned_data['email']

