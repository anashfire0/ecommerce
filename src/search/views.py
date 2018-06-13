from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product


class SearchProductView(ListView):
    template_name = 'search/view.html'

    def get_queryset(self, *args, **kwargs):
        q = self.request.GET.get('q')
        if q is not None:
            return Product.objects.search(q)
        return Product.objects.featured()
