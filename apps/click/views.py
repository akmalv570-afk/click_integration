from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from paytechuz.gateways.click import ClickGateway
from paytechuz.integrations.django.views import BaseClickWebhookView
from .models import Invoice
from drf_spectacular.utils import extend_schema


class ClickWebhookView(BaseClickWebhookView):
    def successfully_payment(self, params, transaction):
        invoice = Invoice.objects.get(id=transaction.account_id)
        invoice.status = 'paid'
        invoice.save()

    def cancelled_payment(self, params, transaction):
        invoice = Invoice.objects.get(id=transaction.account_id)
        invoice.status = 'cancelled'
        invoice.save()


class InvoiceCreateView(APIView):
    @extend_schema(request=None, responses=None)
    def post(self, request):
        amount = request.data.get('amount')

        if not amount:
            return Response({'error': 'amount required'}, status=400)

        invoice = Invoice.objects.create(
            user=request.user,
            amount=amount,
            status='pending'
        )

        gateway = ClickGateway(
            service_id=settings.PAYTECHUZ['CLICK']['SERVICE_ID'],
            merchant_id=settings.PAYTECHUZ['CLICK']['MERCHANT_ID'],
            merchant_user_id=settings.PAYTECHUZ['CLICK']['MERCHANT_USER_ID'],
            secret_key=settings.PAYTECHUZ['CLICK']['SECRET_KEY'],
            is_test_mode=settings.PAYTECHUZ['CLICK']['IS_TEST_MODE']
        )

        payment_url = gateway.create_payment(
            id=invoice.id,
            amount=invoice.amount,
        )

        return Response({
            'invoice_id': invoice.id,
            'payment_url': payment_url
        }, status=201)