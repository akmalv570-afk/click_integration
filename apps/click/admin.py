from django.contrib import admin
from .models import ClickPayment, Order



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id',)

    search_fields = ('id',)


admin.site.register(ClickPayment)
