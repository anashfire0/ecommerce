from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from . import views

app_name='accounts'

urlpatterns = [
    url(r'^login/$', views.login_page, name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout',),
    url(r'^register/$', views.register_page, name='register',),
    url(r'^register/guest/$', views.guest_register_view, name='guest_register',),
]