from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime
from django.contrib import messages

# for Paypal Payments
from django.conf import settings
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

from .models import Category, Product, UsersCart, Order, OrderItem, ShippingAddress
from .forms import CheckoutForm

import json


class GorkemsDonerShop:

    # Shop Page
    def shop(self):
        if self.user.is_authenticated:
            if self.method == 'POST' and self.is_ajax():
                post_data = json.load(self)
                product = get_object_or_404(Product, id=post_data['product_id'])
                cart_status = UsersCart.objects.filter(user=self.user, product=product.id).first()
                if cart_status:
                    cart_status.quantity = str(int(cart_status.quantity) + 1)
                    cart_status.total_price = "{:.2f}".format(float(cart_status.quantity) * float(cart_status.price))
                    cart_status.save()
                else:
                    added_to_cart = UsersCart(
                        user=self.user,
                        product_name=product.name,
                        price=product.price,
                        product=product,
                        quantity='1',
                        total_price=product.price)
                    added_to_cart.save()
                return JsonResponse({
                    'results': UsersCart.objects.filter(user=self.user).count()
                })
            else:
                context = {
                    'categories': Category.objects.all(),
                    'products': Product.objects.all()
                }
        else:
            context = {
                'categories': Category.objects.all(),
                'products': Product.objects.all()
            }
        return render(self, 'gorkems_doner_shop/shop.html', context)

    # Cart Page
    @login_required
    def cart(self):
        if self.method == 'POST' and self.is_ajax():
            post_data = json.load(self)
            if post_data['delete'] == 'True':
                delete_product = get_object_or_404(UsersCart, pk=post_data['product_id'])
                delete_product.delete()
                return JsonResponse({
                    'results': 'successfully deleted.'
                })
            elif post_data['update'] == 'True':
                all_info = post_data['product']
                for single_product in all_info:
                    if int(all_info[single_product]) == 0:
                        update_cart = UsersCart.objects.filter(user=self.user, pk=single_product).first()
                        update_cart.delete()
                    else:
                        update_cart = UsersCart.objects.filter(user=self.user, pk=single_product).first()
                        update_cart.quantity = str(int(all_info[single_product]))
                        update_cart.total_price = "{:.2f}".format(float(all_info[single_product]) * float(update_cart.price))
                        update_cart.save()
                return JsonResponse({
                    'results': 'successfully updated.'
                })
            else:
                return JsonResponse({'results': 'False'})
        else:
            all_cart = UsersCart.objects.filter(user=self.user)
            minimum_total_price = []
            for price in all_cart:
                minimum_total_price.append(price.total_price)
            context = {
                'carts': all_cart,
                'minimum_total_price': sum(minimum_total_price)
                }
            return render(self, 'gorkems_doner_shop/cart.html', context)

    # Checkout
    @login_required
    def checkout(self):
        all_cart = UsersCart.objects.filter(user=self.user)
        minimum_total_price = []
        for price in all_cart:
            minimum_total_price.append(price.total_price)
        if sum(minimum_total_price) < 13:
            return redirect('cart')
        else:
            vat = (float("{:.2f}".format(sum(minimum_total_price))) * 7) / 100
            if self.method == 'POST':
                form = CheckoutForm(self.POST)
                if form.is_valid():
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    email = form.cleaned_data['email']
                    phone = form.cleaned_data['phone_number']
                    country = form.cleaned_data['country']
                    street_address = form.cleaned_data['street']
                    street_address_optional = form.cleaned_data['optional']
                    city = form.cleaned_data['city']
                    postcode = form.cleaned_data['post_code']
                    different_shipping_address = form.cleaned_data['different_shipping_address']
                    different_first_name = form.cleaned_data['different_first_name']
                    different_last_name = form.cleaned_data['different_last_name']
                    different_email = form.cleaned_data['different_email']
                    different_phone = form.cleaned_data['different_phone_number']
                    different_country = form.cleaned_data['different_country']
                    different_street_address = form.cleaned_data['different_street']
                    different_street_address_optional = form.cleaned_data['different_optional']
                    different_city = form.cleaned_data['different_city']
                    different_postcode = form.cleaned_data['different_post_code']
                    comment_on_the_order = form.cleaned_data['comment_on_the_order']
                    payment = form.cleaned_data['payment']
                    if payment == 'Cash On Delivery':
                        order_status = 'Pending'
                    else:
                        order_status = 'Unpaid'

                    place_order = Order(
                        customer=self.user,
                        total_price="{:.2f}".format(sum(minimum_total_price) + 2.90),
                        payment_by=payment,
                        order_comment=comment_on_the_order,
                        order_status=order_status
                    )
                    place_order.save()

                    for cart in all_cart:
                        order_item = OrderItem(
                            user=self.user,
                            order=place_order,
                            product=cart.product,
                            product_name=cart.product_name,
                            price=cart.price,
                            quantity=cart.quantity,
                            total_price=cart.total_price
                        )
                        order_item.save()
                        cart.delete()
                    save_shipping_address = ShippingAddress(
                        customer=self.user,
                        order=place_order,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone=phone,
                        country=country,
                        street_address=street_address,
                        street_address_optional=street_address_optional,
                        city=city,
                        postcode=postcode,
                        different_shipping_address=different_shipping_address,
                        different_first_name=different_first_name,
                        different_last_name=different_last_name,
                        different_email=different_email,
                        different_phone=different_phone,
                        different_country=different_country,
                        different_street_address=different_street_address,
                        different_street_address_optional=different_street_address_optional,
                        different_city=different_city,
                        different_postcode=different_postcode
                    )
                    save_shipping_address.save()
                    if payment == 'Paypal':
                        order_transaction = get_object_or_404(Order, transaction_id=place_order.transaction_id)
                        return redirect('paypal-payment', transaction=order_transaction.transaction_id)
                    else:
                        messages.success(self, f"Order done on Cash On Delivery.")
                        return redirect('orders')
                context = {
                    'form': CheckoutForm(self.POST),
                    'subtotal': "{:.2f}".format(sum(minimum_total_price)),
                    'vat': vat
                }
            else:
                context = {
                    'form': CheckoutForm(),
                    'subtotal': "{:.2f}".format(sum(minimum_total_price)),
                    'vat': vat,
                    'total': "{:.2f}".format(sum(minimum_total_price) + 2.90)
                }
            return render(self, 'gorkems_doner_shop/checkout.html', context)

    # Paypal Payment
    @login_required
    def paypal_payment(self, transaction):
        order = get_object_or_404(Order, transaction_id=transaction)
        host = self.get_host()
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': f"{ order.total_price }",
            'item_name': f"Ordered by { order.customer.first_name } { order.customer.last_name }",
            'invoice': str(order.id),
            'currency_code': 'EUR',
            'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host, reverse('paypal_payment_complete')),
            'cancel_return': 'http://{}{}'.format(host, reverse('paypal_payment_canceled')),
        }
        if self.method == 'POST' and self.is_ajax():
            return JsonResponse({'results': paypal_dict})
        else:
            context = {
                'form': PayPalPaymentsForm(initial=paypal_dict),
                'transaction': transaction
            }
            return render(self, 'gorkems_doner_shop/paypal_payment.html', context)

    # Paypal Complete Payment
    @login_required
    def paypal_complete_payment(self):
        return render(self, 'gorkems_doner_shop/paypal_complete_payment.html')

    # Paypal Cancel Payment
    @login_required
    def paypal_cancel_payment(self):
        return render(self, 'gorkems_doner_shop/paypal_cancel_payment.html')

    # Orders
    @login_required
    def orders(self):
        context = {
            'all_user_orders': Order.objects.filter(customer=self.user).order_by('-date_ordered')
        }
        return render(self, 'gorkems_doner_shop/orders.html', context)

    # Single Order History
    @login_required
    def single_order_history(self, transaction):
        order_info = get_object_or_404(Order, transaction_id=transaction)
        order_item = OrderItem.objects.filter(order=order_info)
        shipping_address = ShippingAddress.objects.filter(order=order_info)
        total_price = []
        for price in order_item:
            total_price.append(price.total_price)
        context = {
            'today': datetime.today(),
            'order': order_info,
            'order_item': order_item,
            'total_price_count': "{:.2f}".format(sum(total_price)),
            'shipping_address': shipping_address
        }
        return render(self, 'gorkems_doner_shop/single-orders.html', context)
