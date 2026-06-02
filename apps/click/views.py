from rest_framework.views import APIView
from rest_framework.response import Response
from .services import ClickPaymentService


class ClickWebhookAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        service = ClickPaymentService()
        result = service.process_webhook(request.data)

        return Response(result)