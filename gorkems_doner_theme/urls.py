from django.urls import path
from .views import GorkemsDonerTheme


urlpatterns = [
    path('contact/', GorkemsDonerTheme.contact, name='contact'),
    path('privacy-policy/', GorkemsDonerTheme.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', GorkemsDonerTheme.terms_of_service, name='terms_of_service'),
]
