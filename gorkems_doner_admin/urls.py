from gorkems_doner_message.views import GorkemsDonerMessage
from django.urls import path
from .views import GorkemsDonerAdminView


urlpatterns = [
    path('admin-orders/', GorkemsDonerAdminView.admin_order, name='admin_order'),
    path('admin-single-order/<transaction>', GorkemsDonerAdminView.admin_single_oder, name='admin_single_order'),
    path('total-income/', GorkemsDonerAdminView.income_statment, name='income_statment'),
    path('all-message/', GorkemsDonerAdminView.message_for_admin, name='message_for_admin'),
]
