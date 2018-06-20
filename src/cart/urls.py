from django.conf.urls import url
from . import views

app_name='cart'

urlpatterns = [
    url(r'^$', views.cart_home, name='home'),
    url(r'^update/$', views.cart_update, name='update'),
    url(r'^checkout/$', views.checkout_home, name='checkout_home'),
    url(r'^success/$', views.checkout_success, name='success'),
    url(r'^api/$', views.cart_detail_api_view, name='cart_api'),
]