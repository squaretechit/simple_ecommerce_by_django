from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers

from .models import SingleMessage

import json



class GorkemsDonerMessage:

    @login_required
    def single_message(self, receiver):
        if self.method == 'POST' and self.is_ajax():
            post_data = json.load(self)
            message_want_to_save = post_data["message"]
            put_message = SingleMessage(
                sender=self.user.username,
                receiver=receiver,
                message=message_want_to_save)
            put_message.save()
            return JsonResponse({'results': serializers.serialize("json", SingleMessage.objects.all())})
        else:
            context = {
                'user_url': receiver,
                'current_user_info': get_object_or_404(User, username=receiver)
            }
            return render(self, 'message/message.html', context)

    @login_required
    def realtime_message(self):
        if self.method == 'POST' and self.is_ajax():
            return JsonResponse({'results': serializers.serialize("json", SingleMessage.objects.all())})
