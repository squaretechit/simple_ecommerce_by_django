from django.contrib.auth.models import User
from gorkems_doner_shop.models import UsersCart


def get_all_user(self):
    if self.user.is_authenticated:
        context = {
            'all_user': User.objects.exclude(username='admin').all(),
            'cart_status': UsersCart.objects.filter(user=self.user).count()
            }
    else:
        context = {
            'all_user': User.objects.exclude(username='admin').all()
            }
    return context
