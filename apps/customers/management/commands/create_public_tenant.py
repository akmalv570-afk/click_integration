import os
from django.core.management.base import BaseCommand
from apps.customers.models import Client, Domain
from decouple import config

class Command(BaseCommand):
    help = 'Create public tenant'

    def handle(self, *args, **kwargs):
        if Client.objects.filter(schema_name='public').exists():
            self.stdout.write('⚠️ Public tenant already exists!')
            return

        tenant = Client(
            schema_name='public',
            name=config('PUBLIC_TENANT_NAME', default='IMB Edu'),
        )
        tenant.save()

        domain = Domain()
        domain.domain = config('DOMAIN', default='localhost')
        domain.tenant = tenant
        domain.is_active = True
        domain.save()

        self.stdout.write('Public tenant created')