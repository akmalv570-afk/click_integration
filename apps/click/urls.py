from django.urls import path
from .views import ClickWebhookView

urlpatterns = [
    path('webhook/', ClickWebhookView.as_view(), name='click_webhook'),
]