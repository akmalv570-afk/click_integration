from django.core.management.base import BaseCommand
from apps.customers.models import Client, Domain


class Command(BaseCommand):
    help = 'Create a new tenant'

    def handle(self, *args, **kwargs):
        if Client.objects.filter(schema_name='tenant1').exists():
            self.stdout.write('tenant1 already exists')
            return

        tenant = Client(
            schema_name='tenant1',
            name='First client',
            on_trial=True
        )
        tenant.save()

        domain = Domain()
        domain.domain = 'tenant1.localhost'
        domain.tenant = tenant
        domain.is_primary = True
        domain.save()

        self.stdout.write('tenant1 created')