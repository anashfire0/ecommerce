import math
from django.db import models
from django.db.models.signals import pre_save, post_save

from billing.models import BillingProfile

from ecommerce.utils import unique_order_id_generator
from cart.models import Cart

ORDER_STATUS_CHOICES = [
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded')
]


class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True)
    order_id = models.CharField(max_length=128, blank=True)
    cart = models.ForeignKey(Cart, related_name='orders')
    status = models.CharField(
        max_length=50, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(
        default=5.00, max_digits=15, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)
    active = models.BooleanField(default=True)

    def update_total(self):
        self.total = round(
            math.fsum((self.cart.total, self.shipping_total)), 2)
        return self.save()

    def __str__(self):
        return self.order_id


def pre_save_order_id_receiver(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


pre_save.connect(pre_save_order_id_receiver, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart = instance
        qs = Order.objects.filter(cart__id=cart.id)
        if qs.count() == 1:
            order = qs.first()
            order.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


post_save.connect(post_save_order, sender=Order)
