from django.contrib import admin

from .models import MarketingPreference

class MarketingPreferenceAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'subscribed', 'updated']
    readonly_fields = ['mailchimp_msg', 'mailchimp_subscribed', 'timestamp', 'updated']
    class Meta:
        model = MarketingPreference
        exclude = ()

admin.site.register(MarketingPreference, MarketingPreferenceAdmin)