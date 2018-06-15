from django.shortcuts import render, redirect
from .models import Cart
from products.models import Product
from accounts.forms import LoginForm, GuestForm

from orders.models import Order
from billing.models import BillingProfile
from accounts.models import Guest


def cart_home(request):
    cart, is_new = Cart.objects.new_or_get(request)
    return render(request, 'cart/home.html', {'cart': cart})


def cart_update(request):
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)
    cart, _ = Cart.objects.new_or_get(request)

    if product in cart.products.all():
        cart.products.remove(product)
    else:
        cart.products.add(product)
    request.session['cart_items'] = cart.products.count()
    return redirect('cart:home')


def checkout(request):
    cart, is_cart_new = Cart.objects.new_or_get(request)
    order = None
    if is_cart_new or not cart.products.exists():
        redirect('cart:home')
    else:
        order, is_order_new = Order.objects.get_or_create(cart=cart)
    billing_profile = None

    guest_id = request.session.get('guest_id')

    if request.user.is_authenticated():
        billing_profile, is_billing_profile_created = BillingProfile.objects.get_or_create(
            user=request.user)
    elif guest_id is not None:
        billing_profile, is_billing_profile_created = BillingProfile.objects.get_or_create(
            email=Guest.objects.get(id=guest_id).email)
    else:
        pass

    context = {'order': order,
               'billing_profile': billing_profile,
               'form': LoginForm(),
               'guest_form': GuestForm(),
               }
    return render(request, 'cart/checkout.html', context)
