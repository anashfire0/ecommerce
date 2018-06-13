from django.shortcuts import render, redirect
from .models import Cart
from products.models import Product

def cart_home(request):
    cart, is_new = Cart.objects.new_or_get(request)
    return render(request, 'cart/home.html', {'cart':cart})

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