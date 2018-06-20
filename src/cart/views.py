from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Cart
from products.models import Product
from accounts.forms import LoginForm, GuestForm

from orders.models import Order
from billing.models import BillingProfile
from accounts.models import Guest
from addresses.forms import AddressForm
from addresses.models import Address


def cart_home(request):
    cart, is_new = Cart.objects.new_or_get(request)
    return render(request, 'cart/home.html', {'cart': cart})


def cart_detail_api_view(request):
    cart, new_obj = Cart.objects.new_or_get(request)

    products = [
    {'id': x.id,
    'url': x.get_absolute_url(),
    'name':x.title,
    'price':x.price
    }for x in cart.products.all()]

    cart_data = {'products': products, 'subtotal': cart.subtotal, 'total': cart.total}
    print(cart_data)
    return JsonResponse(cart_data)


def cart_update(request):
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)
    cart, _ = Cart.objects.new_or_get(request)
    print(request.is_ajax())

    if product in cart.products.all():
        cart.products.remove(product)
        added = False
    else:
        cart.products.add(product)
        added = True
    request.session['cart_items'] = cart.products.count()
    if request.is_ajax():
        json_data={
            'added': added,
            'removed': not added,
            'cartCount': request.session.get('cart_items'),
            }
        print('sending json to ajax')
        return JsonResponse(json_data)
        # return JsonResponse({'message': 'error 400'}, status=400)
    return redirect('cart:home')

def checkout_home(request):
    cart, billing_profile, order = None, None, None
    address_qs=None
    cart, is_cart_new = Cart.objects.new_or_get(request)

    if is_cart_new or not cart.products.exists():
        redirect('cart:home')

    billing_profile, _ = BillingProfile.objects.new_or_get(request)

    if billing_profile is not None:
        order, _ = Order.objects.new_or_get(billing_profile, cart)

        #adding addresses to the order using session dictionary
        billing_address_id, shipping_address_id = request.session.get('billing_address_id'), request.session.get('shipping_address_id')
        if billing_address_id:
            order.billing_address = Address.objects.get(id=billing_address_id)
        if shipping_address_id:
            order.shipping_address = Address.objects.get(id=shipping_address_id)
        order.save()

        #use addresses to display them right away
        if request.user.is_authenticated():
            address_qs = Address.objects.filter(billing_profile=billing_profile)

    #finalize checkout
    if request.method == 'POST':
        if order.mark_paid():
            del request.session['cart_id']
            del request.session['cart_items']
            return redirect('cart:success')

    context = {'order': order,
               'billing_profile': billing_profile,
               'form': LoginForm(),
               'guest_form': GuestForm(),
               'address_form': AddressForm(),
               'address_qs': address_qs,
               }
    return render(request, 'cart/checkout_home.html', context)

def checkout_success(request):
    return render(request, 'cart/checkout_success.html',)