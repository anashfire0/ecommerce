from django.db import models

from billing.models import BillingProfile

ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping')
)

class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile)
    address_type    = models.CharField(max_length=50, choices=ADDRESS_TYPES)
    address_line_1  = models.CharField(max_length=120)
    address_line_2  = models.CharField(max_length=120, blank=True, null=True)
    city            = models.CharField(max_length=50)
    country         = models.CharField(max_length=50, default='India')
    state           = models.CharField(max_length=50)
    postal_code     = models.CharField(max_length=50)

    def __str__(self):
        return str(self.billing_profile)