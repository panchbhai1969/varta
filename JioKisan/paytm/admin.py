from django.contrib import admin
from paytm.models import PaytmHistory
# Register your models here.
class PaytmHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'MID', 'TXNAMOUNT', 'STATUS')


admin.site.register(PaytmHistory, PaytmHistoryAdmin)
