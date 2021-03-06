"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from . import views
from cart.views import cart_home
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^contact/$', views.contact_view, name='contact'),
    url(r'^checkout/address/create/$',checkout_address_create_view, name='checkout_address_create'),
    url(r'^checkout/address/reuse/$',checkout_address_reuse_view, name='checkout_address_reuse'),
    url(r'^user/',include('accounts.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^products/', include('products.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^marketing/', include('marketing.urls')),

]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)