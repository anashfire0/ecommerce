from django.shortcuts import render, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView, View
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.conf import settings

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .forms import MarketingPreferenceForm
from .models import MarketingPreference
from .utils import Mailchimp

mailchimp = Mailchimp()

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


class MailmailChimpWebhookView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args **kwargs)

    def post(self, request, *args, **kwargs):
        data = reques.POST
        list_id = data.get('data[list_id]')
        if settings.MAILCHIMP_EMAIL_LIST_ID == str(list_id):

            hook_type = data.get('type')
            email = data.get('data[email]')
            response_status, response = mailchimp.check_subscription_status(email)
            sub_status = response['status']
            is_subbed, mailchimp_subbed = None, None

            if sub_status == 'subscribed':
                is_subbed, mailchimp_subbed = True, True
            elif sub_status == 'unsubscribed':
                is_subbed, mailchimp_subbed = False, False

            if None not in (is_subbed, mailchimp_subbed):
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(
                        subscribed=is_subbed, 
                        mailchimp_subscribed=mailchimp_subbed, 
                        mailchimp_msg=str(data)
                    )
        return HttpResponse('Thank You', status=200)
