# import hashlib
# from time import strftime
# from django.conf import settings
#
#
# def generete_click_url(order_id, amount):
#
#     merchant_id = settings.CLICK_SETTINGS['MERCHANT_ID']
#     service_id = settings.CLICK_SETTINGS['SERVICE_ID']
#     secret_key = settings.CLICK_SETTINGS['SEKRET_KEY']
#     return_url = settings.CLICK_SETTINGS['RETURN_URL']
#
#     formant_amount = ":.2f".format(float(amount))
#     sing_time = strftime("%Y-%m-%d %H-%M-%S")
#
#     raw_sing = f"{sing_time}{service_id}{secret_key}{order_id}{formant_amount}"
#     sing_string = hashlib.md5(raw_sing.encode('utf-8')).hexdigest()
#
#     click_url = (
#         f"https://my.click.uz/services/pay?"
#         f"merchant_id={merchant_id}"
#         f"service_id={service_id}"
#         f"amount={formant_amount}"
#         f"transaction_param={order_id}"
#         f"return_url={return_url}"
#     )
#
#     return click_url