from django.conf.urls import url
from . import views

app_name='products'

urlpatterns = [
    url(r'^$', views.ProductListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', views.ProductDetailView.as_view(),
     name='detail',),
]