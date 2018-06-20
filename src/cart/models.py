from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save, m2m_changed

from products.models import Product

User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):

    def new_or_get(self, request):
        cart_id = request.session.get('cart_id')
        qs = Cart.objects.filter(id=cart_id)
        if qs.count() == 1:
            cart_obj = qs.first()
            is_new = False
            if request.user.is_authenticated() and cart_obj.user is None:
                cart_obj.user = request.user
            return cart_obj, is_new
        else:
            cart_obj = Cart.objects.new(user=request.user)
            request.session['cart_id'] = cart_obj.id
            is_new = True
            return cart_obj, is_new

    def new(self, user=None):
        if user and user.is_authenticated:
            return self.create(user=user)
        return self.create()


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    products = models.ManyToManyField(Product)
    subtotal = models.DecimalField(
        default=0.00, max_digits=15, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return f'{self.id}'


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action in ('post_add', 'post_remove', 'post_clear'):
        instance.subtotal = sum(
            product.price for product in instance.products.all())
        instance.save()
m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    instance.total = instance.subtotal + 20 if instance.subtotal > 0 else 0
pre_save.connect(pre_save_cart_receiver, sender=Cart)
