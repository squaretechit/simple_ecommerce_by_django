from django.apps import AppConfig


class GorkemsDonerShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gorkems_doner_shop'

    def ready(self):
        import gorkems_doner_shop.paypal_hooks
