from django.contrib import admin
from .models import Invoice



@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id',)

    search_fields = ('id',)
