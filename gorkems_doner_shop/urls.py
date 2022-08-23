from django.urls import path
from .views import GorkemsDonerShop


urlpatterns = [
    path('', GorkemsDonerShop.shop, name='shop'),
    path('cart/', GorkemsDonerShop.cart, name='cart'),
    path('checkout/', GorkemsDonerShop.checkout, name="checkout"),
    path('orders/', GorkemsDonerShop.orders, name='orders'),
    path('single-order/<transaction>',
        GorkemsDonerShop.single_order_history,
        name='single_order'),
    path('make-payment-paypal/<transaction>',
        GorkemsDonerShop.paypal_payment,
        name='paypal-payment'),
    path('paypal-payment-canceled/',
        GorkemsDonerShop.paypal_cancel_payment,
        name='paypal_payment_canceled'),
    path('order-complete/', GorkemsDonerShop.paypal_complete_payment,
        name='paypal_payment_complete'),
]
