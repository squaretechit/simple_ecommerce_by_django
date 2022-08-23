from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Category, Product, UsersCart, Order, OrderItem


admin.site.site_header = 'Gorkems Doner Admin Dashboard'
admin.site.site_title = 'Gorkems Doner'
admin.site.index_title = 'Gorkems Doner Administration'
admin.site.unregister(Group)


@admin.register(Category)
class CustomCategory(admin.ModelAdmin):
    list_display = ('category', 'date', 'description')

@admin.register(Product)
class CustomAdminProduct(admin.ModelAdmin):
    list_display = ('name', 'category', 'product_status', 'price')
    fields = ('name', 'category', 'product_status', 'price', 'description')


@admin.register(UsersCart)
class CustomUserCart(admin.ModelAdmin):
    list_display = ('cart_date', 'user', 'product_name', 'price', 'quantity', 'total_price')
    list_display_links = None

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date_ordered', 'transaction_id', 'total_price',
                    'payment_by', 'paypal_transaction_id', 'order_comment', 'order_status', 'paid_amount')
    search_fields = ['transaction_id']
    list_filter = ('date_ordered', 'payment_by', 'order_status', 'paid_amount')
    list_display_links = None

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(OrderItem)
class CustomOrderItem(admin.ModelAdmin):
    list_display = ('order', 'product', 'price', 'quantity', 'total_price')
    list_display_links = None

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
