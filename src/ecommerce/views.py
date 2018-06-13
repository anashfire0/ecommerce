from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .forms import ContactForm, LoginForm, RegisterForm

def home(request):
    return render(request, 'home_page.html')

def login_page(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(request, user)
            return redirect(reverse_lazy('home'))
        else:
            print('not authenticated')
    return render(request, 'auth/login.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('home')


def register_page(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        get_user_model().objects.create_user(username=username, email=email, password=password)
        return redirect('/')
    return render(request, 'auth/register.html', {'form':form})

class ContactView(TemplateView):
    template_name='contact.html'
    form_class = ContactForm

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context.update({'form': self.form_class()})
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)
