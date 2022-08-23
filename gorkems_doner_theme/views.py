from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail

from .forms import ContactForm


class GorkemsDonerTheme:

    def contact(self):
        if self.method == 'POST':
            form = ContactForm(self.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                mail = f"Hello admin,\n I am {name},\n my Email {email}," \
                            f"\n I want to talk on {subject},\n Message: {message}"
                send_mail(
                    f"Message from {get_current_site(self).domain}",
                    mail,
                    settings.EMAIL_HOST_USER,
                    ['mdshariffoysalshoron@gmail.com'],
                    fail_silently=False,)
                messages.success(self, f"Thank you for your inquiry! \
                                        We will get back to you within 48 hours.")
                return redirect('contact')
        else:
            form = ContactForm()
        return render(self, 'theme/contact.html', {'form': form})

    def privacy_policy(self):
        return render(self, 'theme/privacy-policy.html')

    def terms_of_service(self):
        return render(self, 'theme/terms-service.html')
