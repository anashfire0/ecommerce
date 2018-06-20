from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from accounts.models import Guest

User = get_user_model()


class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        guest_id = request.session.get('guest_id')
        billing_profile, is_billing_profile_created = None, None
        if request.user.is_authenticated():
            billing_profile, is_billing_profile_created = self.model.objects.get_or_create(
                user=request.user)
        elif guest_id is not None:
            billing_profile, is_billing_profile_created = self.model.objects.get_or_create(
                email=Guest.objects.get(id=guest_id).email)
        else:
            pass
        return billing_profile, is_billing_profile_created


class BillingProfile(models.Model):
    user      = models.OneToOneField(User, null=True, blank=True)
    email     = models.EmailField()
    active    = models.BooleanField(default=True)
    update    = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(
            user=instance, email=instance.email)
post_save.connect(user_created_receiver, sender=User)
