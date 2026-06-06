from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from apps.customers.models import Client, Domain

from django_tenants.utils import get_public_schema_name
from django.db import connection

@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'paid_until')

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if connection.schema_name != get_public_schema_name():
            return qs.none()
        return qs


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain', 'tenant', 'is_primary']
