from django.conf.urls import url
from . import views

app_name='marketing'

urlpatterns = [
    url(r'settings/email/$', views.MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
]