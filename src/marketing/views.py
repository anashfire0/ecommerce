from django.shortcuts import render, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse

from .forms import MarketingPreferenceForm
from .models import MarketingPreference

class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
    form_class = MarketingPreferenceForm
    template_name = 'base/forms.html'
    success_url = reverse_lazy('marketing:marketing-pref')
    success_message = 'Preferences saved.'

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated():
            # return HttpResponse('Not allowed', status=400)
            return redirect(reverse('accounts:login') + '?next=' + reverse('marketing:marketing-pref'))
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        user = self.request.user
        obj, created = MarketingPreference.objects.get_or_create(user=user)
        return obj

    def get_context_data(self, **kwargs):
        context = super(MarketingPreferenceUpdateView, self).get_context_data(**kwargs)
        context.update({'title': 'Change the subscription'})
        return context

