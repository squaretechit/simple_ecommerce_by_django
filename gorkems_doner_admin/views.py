from django.contrib import messages
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from gorkems_doner_shop.models import Order, OrderItem, ShippingAddress

import datetime


class GorkemsDonerAdminView:

    # Admin Orders Page
    @login_required
    def admin_order(self):
        if self.user.is_superuser:
            all_user_orders = Order.objects.all().order_by('-date_ordered')
            page = self.GET.get('page', 1)
            paginator = Paginator(all_user_orders, 20)
            try:
                all_orders = paginator.page(page)
            except PageNotAnInteger:
                all_orders = paginator.page(1)
            except EmptyPage:
                all_orders = paginator.page(paginator.num_pages)
            context = {
                'site_header': 'Gorkems Doner Admin Dashboard',
                'all_user_orders': all_orders
            }
            return render(self, 'admin/orders.html', context)
        else:
            return redirect('login')

    # Admin Single Orders
    @login_required
    def admin_single_oder(self, transaction):
        if self.user.is_superuser:
            order_info = get_object_or_404(Order, transaction_id=transaction)
            order_item = OrderItem.objects.filter(order=order_info)
            shipping_address = ShippingAddress.objects.filter(order=order_info)
            total_price = []
            for price in order_item:
                total_price.append(price.total_price)
            if self.method == 'POST':
                options = self.POST['options']
                order_info.order_status = options
                order_info.save()
                messages.success(self, 'Order Status Changed')
                return redirect('admin_single_order', transaction=transaction)
            else:
                context = {
                    'transaction': transaction,
                    'site_header': 'Gorkems Doner Admin Dashboard',
                    'order': order_info,
                    'order_item': order_item,
                    'total_price_count': "{:.2f}".format(sum(total_price)),
                    'shipping_address': shipping_address
                }
            return render(self, 'admin/singleorder.html', context)
        else:
            return redirect('login')

    # Admin Income Statment
    @login_required
    def income_statment(self):
        if self.method == 'POST':
            form_date = self.POST['from-date']
            to_date = self.POST['to-date']
            new_form_date = form_date.split('/')
            new_to_date = to_date.split('/')
            check_from_date = datetime.datetime(
                year=int(new_form_date[2]),
                month=int(new_form_date[0]),
                day=int(new_form_date[1])
                )
            check_to_date = datetime.datetime(
                year=int(new_to_date[2]),
                month=int(new_to_date[0]),
                day=int(new_to_date[1])
                )
            all_order = Order.objects.filter(date_ordered__date__range=(check_from_date,check_to_date))
            delivered_order_status = []
            other_order_status = []
            paid_by_paypal = []
            cash_on_delivery = []
            delivered_orders_amount = []
            undelivered_orders_amount = []
            amount_paid_by_paypal = []
            amount_paid_by_cash_on_delivery = []
            for order in all_order:
                if order.order_status == 'Delivered':
                    delivered_order_status.append(order)
                    delivered_orders_amount.append(order.total_price)
                else:
                    other_order_status.append(order)
                    undelivered_orders_amount.append(order.total_price)
                if order.payment_by == 'Cash On Delivery':
                    cash_on_delivery.append(order)
                    amount_paid_by_cash_on_delivery.append(order.total_price)
                else:
                    paid_by_paypal.append(order)
                    amount_paid_by_paypal.append(order.total_price)
            if len(all_order) > 0:
                context = {
                    'site_header': 'Gorkems Doner Admin Dashboard',
                    'all_order': len(all_order),
                    'delivered_orders': len(delivered_order_status),
                    'other_order': len(other_order_status),
                    'paid_paypal': len(paid_by_paypal),
                    'cash_on_delivery': len(cash_on_delivery),
                    'delivered_orders_amount': "{:.2f}".format(sum(delivered_orders_amount)),
                    'undelivered_orders_amount': "{:.2f}".format(sum(undelivered_orders_amount)),
                    'amount_paid_by_paypal': "{:.2f}".format(sum(amount_paid_by_paypal)),
                    'amount_paid_by_cash_on_delivery': "{:.2f}".format(sum(amount_paid_by_cash_on_delivery))
                }
                messages.success(self, f"Your income statment is successfully generated.")
            else:
                context = {
                    'site_header': 'Gorkems Doner Admin Dashboard',
                    'all_order': len(all_order),
                }
                messages.error(self, f"Nothing Found. Please try again with valid dates.")
        else:
            context = {
                'site_header': 'Gorkems Doner Admin Dashboard',
            }
        return render(self, 'admin/incomestatment.html', context)

    # message page
    @login_required
    def message_for_admin(self):
        if self.user.is_superuser:
            context = {
                'site_header': 'Gorkems Doner Admin Dashboard',
            }
            return render(self, 'admin/message_for_admin.html', context)
        else:
            return redirect('login')
