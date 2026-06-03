from django.urls import path
from .views import ClickWebhookView, InvoiceCreateView

urlpatterns = [
    path('webhook/', ClickWebhookView.as_view(), name='click_webhook'),
    path('invoice/create/', InvoiceCreateView.as_view(), name='invoice_create'),
]