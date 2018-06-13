from django.views.generic import ListView, DetailView
from django.shortcuts import render

from .models import Product
from cart.models import Cart

class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'products/product_list.html'

class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['cart'], _ = Cart.objects.new_or_get(self.request)
        return context
