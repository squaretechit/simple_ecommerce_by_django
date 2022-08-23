from django.urls import path
from .views import GorkemsDonerMessage


urlpatterns = [
    path('message/<receiver>', GorkemsDonerMessage.single_message, name='message'),
    path('realtime-message/', GorkemsDonerMessage.realtime_message, name='real_message')
]
