from django.conf.urls import url
from . import views

app_name='cart'

urlpatterns = [
    url(r'^$', views.cart_home, name='home'),
    url(r'^update/$', views.cart_update, name='update',),
    url(r'^checkout/$', views.checkout, name='checkout',),
]