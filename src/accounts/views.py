from django.contrib.auth import login, authenticate, get_user_model
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import LoginForm, RegisterForm, GuestForm
from .models import Guest

def guest_register_view(request):
    form = GuestForm(request.POST or None)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_to = next_ or next_post or None

    if form.is_valid():
        guest = Guest.objects.create(email=form.cleaned_data['email'])
        request.session['guest_id'] = guest.id
        if is_safe_url(redirect_to, request.get_host()):
            return redirect(redirect_to)
        else: 
            return redirect('accounts:register')
    return redirect('accounts:register')

def login_page(request):
    form = LoginForm(request.POST or None)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_to = next_ or next_post or None

    if form.is_valid():
        user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_id']
            except:
                pass
            if is_safe_url(redirect_to, request.get_host()):
                return redirect(redirect_to)
            else: 
                return redirect('/')
    return render(request, 'accounts/login.html', {'form':form})

def register_page(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        get_user_model().objects.create_user(username=username, email=email, password=password)
        return redirect('/')
    return render(request, 'accounts/register.html', {'form':form})
