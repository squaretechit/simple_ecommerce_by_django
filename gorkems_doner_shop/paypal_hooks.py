from django.conf import settings
from django.shortcuts import get_object_or_404
from django.dispatch import receiver

from paypal.standard.ipn.signals import valid_ipn_received

from .models import Order


@receiver(valid_ipn_received)
def paypal_payment_check(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == 'Completed':
        if ipn_obj.receiver_email == settings.PAYPAL_RECEIVER_EMAIL:
            order_done = get_object_or_404(Order, pk=ipn_obj.invoice)
            if float(ipn_obj.mc_gross) == float(order_done.total_price)\
                    and ipn_obj.mc_currency == 'EUR':
                order_done.order_status = 'Pending'
                order_done.paypal_transaction_id = ipn_obj.transaction_id
                order_done.save()
                # Send Email From Here
    else:
        try:
            order_done = get_object_or_404(Order, pk=ipn_obj.invoice)
            order_done.delete()
        except:
            pass
