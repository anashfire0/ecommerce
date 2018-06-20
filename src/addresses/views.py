from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from billing.models import BillingProfile
from .forms import AddressForm
from .models import Address

def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)

    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_to = next_ or next_post or None

    if form.is_valid():
        print(request.POST)
        instance = form.save(commit=False)
        instance.billing_profile, instance.address_type = BillingProfile.objects.new_or_get(request)[0], request.POST.get('address_type', 'shipping')

        if instance.billing_profile:
            address_type = request.POST.get('address_type', 'shipping')
            instance.save()
            request.session[address_type+'_address_id'] = instance.id
        else:
            print('no billing created')
            return redirect('cart:home')

        if is_safe_url(redirect_to, request.get_host()):
            return redirect(redirect_to)
    return redirect('cart:checkout_home')


def checkout_address_reuse_view(request):
    if request.user.is_authenticated():
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_to = next_ or next_post or None

        if request.method == 'POST':
            print(request.POST)
            shipping_address = request.POST.get('shipping_address', None)
            address_type = request.POST.get('address_type', 'shipping')
            billing_profile, is_billing_profile_new = BillingProfile.objects.new_or_get(request)
            qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
            if qs.exists():
                request.session[address_type+'_address_id'] = shipping_address

            if is_safe_url(redirect_to, request.get_host()):
                return redirect(redirect_to)
    return redirect('cart:checkout_home')


