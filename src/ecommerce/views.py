from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .forms import ContactForm

def home(request):
    return render(request, 'home_page.html')

# class ContactView(TemplateView):
#     template_name='contact.html'
#     form_class = ContactForm

#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super(ContactView, self).get_context_data(**kwargs)
#         context.update({'form': self.form_class()})
#         return context

#     def post(self, request, *args, **kwargs):
#         print(request.POST)
#         if request.is_ajax():
#             print('&'*500)
#             return JsonResponse({'message':'thankyou'})

def contact_view(request):
    contact_form = ContactForm(request.POST or None)
    print(str(request.is_ajax()).rjust(300,'#'))
    if contact_form.is_valid():
       if request.is_ajax():
            return JsonResponse({'message':'success'})
    else:
        if request.is_ajax():
            return HttpResponse(contact_form.errors.as_json(), status=400, content_type='application/json')
    return render(request, 'contact.html', {'form': ContactForm()})