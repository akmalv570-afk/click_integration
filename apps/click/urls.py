from django.urls import path
from .views import ClickWebhookAPIView

urlpatterns = [
    path('webhook/', ClickWebhookAPIView.as_view(), name='click_webhook'),
]