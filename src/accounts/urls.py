from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from . import views

app_name='accounts'

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout',),
    url(r'^register/$', views.RegisterView.as_view(), name='register',),
    url(r'^register/guest/$', views.guest_register_view, name='guest_register',),
]