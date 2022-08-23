from django.db import models
from django.contrib.auth.models import User

from ckeditor_uploader.fields import RichTextUploadingField

import uuid


class Category(models.Model):
    category = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    description = RichTextUploadingField(blank=True, null=True)

    def __str__(self):
        return str(self.category)


class Product(models.Model):
    product_ststus_choise =[
        ('outofstock', 'Out Of Stock'),
        ('instock', 'In Stock'),
    ]
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_category")
    description = RichTextUploadingField(blank=True)
    product_status= models.CharField(max_length=255, choices=product_ststus_choise, default='instock')
    price = models.FloatField()

    def __str__(self):
        return str(self.name)


class UsersCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_user")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_product")
    product_name = models.CharField(max_length=255)
    price = models.FloatField()
    quantity = models.IntegerField()
    total_price = models.FloatField()
    cart_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    total_price = models.FloatField()
    paid_amount = models.FloatField(default=0.00)
    payment_by = models.CharField(max_length=255)
    order_comment = models.TextField(blank=True)
    order_status = models.CharField(max_length=100)
    date_ordered = models.DateTimeField(auto_now_add=True)
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False)
    paypal_transaction_id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.customer.username)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    product_name = models.CharField(max_length=255)
    price = models.FloatField()
    quantity = models.IntegerField()
    total_price = models.FloatField()

    def __str__(self):
        return f"Ordered by {self.user}, on {self.product}"


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    street_address_optional = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    different_shipping_address = models.BooleanField()
    different_first_name = models.CharField(max_length=255, blank=True)
    different_last_name = models.CharField(max_length=255, blank=True)
    different_email = models.EmailField(max_length=255, blank=True)
    different_phone = models.CharField(max_length=255, blank=True)
    different_country = models.CharField(max_length=255, blank=True)
    different_street_address = models.CharField(max_length=255, blank=True)
    different_street_address_optional = models.CharField(max_length=255, blank=True)
    different_city = models.CharField(max_length=255, blank=True)
    different_postcode = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
