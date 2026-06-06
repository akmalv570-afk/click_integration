from django.core.management.base import BaseCommand
from apps.customers.models import Client, Domain
from decouple import config


class Command(BaseCommand):
    help = 'Create a new tenant'

    def handle(self, *args, **kwargs):
        schema_name = config('TENANT1_SCHEMA', default='tenant1')

        if Client.objects.filter(schema_name=schema_name).exists():
            self.stdout.write(f'{schema_name} already exists')
            return

        tenant = Client(
            schema_name=schema_name,
            name=config('TENANT1_NAME', default='First client'),
            on_trial=True
        )
        tenant.save()

        domain = Domain()
        domain.domain = config('TENANT1_DOMAIN', default='tenant1.localhost')
        domain.tenant = tenant
        domain.is_primary = True
        domain.save()

        self.stdout.write(f'{schema_name} created')