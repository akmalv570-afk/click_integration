import hashlib
from .models import Order, ClickPayment
from django.conf import settings


class ClickPaymentService:

    @staticmethod
    def verify_request_data(data, action):
        click_trans_id = data.get("click_trans_id")
        service_id = data.get("service_id")
        order_id = data.get("merchant_trans_id")
        amount = data.get("amount")
        error = data.get("error")
        sign_time = data.get("sign_time")
        sign_string = data.get("sign_string")

        required = [
            click_trans_id,
            service_id,
            order_id,
            amount,
            error,
            sign_time,
            sign_string
        ]

        if action == "1" and not data.get("merchant_prepare_id"):
            return False

        return all(required)

    @staticmethod
    def check_signature(data):
        action = data.get('action')
        merchant_prepare_id = data.get('merchant_prepare_id', '') if action == '1' else ''

        secret_key = settings.CLICK_SETTINGS['SECRET_KEY']
        sign_source = (
            f"{data.get('click_trans_id')}"
            f"{data.get('service_id')}"
            f"{secret_key}"
            f"{data.get('merchant_trans_id')}"
            f"{merchant_prepare_id}"
            f"{data.get('amount')}"
            f"{action}"
            f"{data.get('sign_time')}")
        expected_sign = hashlib.md5(sign_source.encode('utf-8')).hexdigest()

        return expected_sign == data.get('sign_string')

    def process_webhook(self, data):
        action = data.get('action')
        order_id = data.get('merchant_trans_id')
        amount = data.get('amount')
        error = data.get('error')

        if not self.verify_request_data(data, action):
            return {"error": "-8", "error_note": "So'rov ma'lumotlari to'liq emas"}

        # if not self.check_signature(data):
        #     return {"error": "-1", "error_note": "SIGN CHECK FAILED!"}

        if action not in ('0', '1'):
            return {"error": "-3", "error_note": "Action topilmadi"}

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return {"error": "-5", "error_note": "Buyurtma topilmadi"}

        if abs(float(amount) - float(order.total_price)) > 0.01:
            return {"error": "-2", "error_note": "Noto'g'ri summa"}

        if order.status == Order.Status.PAID:
            return {"error": "-4", "error_note": "Allaqachon to'langan"}

        payment, created = ClickPayment.objects.get_or_create(
            order=order,
            defaults={'amount': amount, 'status': ClickPayment.Status.PROCESSING}
        )

        if action == "0":
            payment.click_trans_id = data.get('click_trans_id')
            payment.click_paydoc_id = data.get('click_paydoc_id')
            payment.save()

            return {
                "click_trans_id": data.get('click_trans_id'),
                "merchant_trans_id": order_id,
                "merchant_prepare_id": payment.id,
                "error": "0",
                "error_note": "Success"
            }

        elif action == "1":
            if str(payment.id) != str(data.get('merchant_prepare_id')):
                return {"error": "-6", "error_note": "Tranzaksiya topilmadi"}

            if error and int(error) < 0:
                payment.status = ClickPayment.Status.REJECTED
                payment.save()
                order.status = Order.Status.CANCELED
                order.save()
                return {"error": "-9", "error_note": "Tranzaksiya bekor qilindi"}

            payment.status = ClickPayment.Status.CONFIRMED
            payment.click_trans_id = data.get('click_trans_id')
            payment.click_paydoc_id = data.get('click_paydoc_id')
            payment.save()

            order.status = Order.Status.PAID
            order.save()

            return {
                "click_trans_id": data.get('click_trans_id'),
                "merchant_trans_id": order_id,
                "error": "0",
                "error_note": "Success"
            }