from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save

from .utils import Mailchimp

mailchimp = Mailchimp()

class MarketingPreference(models.Model):
    user                 = models.OneToOneField(settings.AUTH_USER_MODEL)
    subscribed           = models.BooleanField(default=True)
    mailchimp_subscribed = models.NullBooleanField()
    mailchimp_msg        = models.TextField(null=True, blank=True)
    timestamp            = models.DateTimeField(auto_now_add=True)
    updated              = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.email)


def marketing_pref_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        status_code, response_data = mailchimp.add_email(instance.user.email)
        print(status_code, response_data)
post_save.connect(marketing_pref_create_receiver, sender=MarketingPreference)


def make_marketing_pref_receiver(sender, instance, created, *args, **kwargs):
    if created: #if user is created
        MarketingPreference.objects.get_or_create(user=instance)
post_save.connect(make_marketing_pref_receiver, sender=settings.AUTH_USER_MODEL)

def marketing_pref_update_receiver(sender, instance, *args, **kwargs):
    if instance.subscribed != instance.mailchimp_subscribed:
        #update in mailchimp server
        if instance.subscribed:
            status_code, response_data = mailchimp.subscribe(instance.user.email)
        else:
            status_code, response_data = mailchimp.unsubscribe(instance.user.email)

        #update our server based on return value of mailchimp server
        if response_data.get('status') == 'subscribed':
            instance.subscribed = True
            instance.mailchimp_subscribed = True
            instance.mailchimp_msg = response_data
        else:
            instance.subscribed = False
            instance.mailchimp_subscribed = False
            instance.mailchimp_msg = response_data
pre_save.connect(marketing_pref_update_receiver, sender=MarketingPreference)
