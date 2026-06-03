from paytechuz.integrations.django.views import BaseClickWebhookView
from .models import Invoice


class ClickWebhookView(BaseClickWebhookView):
    def successfully_payment(self, params, transaction):
        invoice = Invoice.objects.get(id=transaction.account_id)
        invoice.status = 'paid'
        invoice.save()

    def cancelled_payment(self, params, transaction):
        invoice = Invoice.objects.get(id=transaction.account_id)
        invoice.status = 'cancelled'
        invoice.save()