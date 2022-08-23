from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib import messages
from django.utils.html import strip_tags
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse

from .token import account_activation_token, password_reset_token
from .forms import LoginForm, RegisterForm, PassChangeForm, PassResetEmailForm, PassRestForm, ProfileInfoChangeForm
from .models import UserProfile

from gorkems_doner_shop.models import UsersCart

from datetime import datetime
from urllib.parse import urlencode
import requests


class GorkemsDonerUsers:

    def register(self):
        if self.user.is_authenticated:
            return redirect('profile')
        elif self.method == 'POST':
            form = RegisterForm(self.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                phone = form.cleaned_data['phone_number']
                country = form.cleaned_data['country']
                street = form.cleaned_data['street']
                postcode = form.cleaned_data['postcode']
                city = form.cleaned_data['city']
                user = User.objects.create_user(first_name=first_name,
                                                last_name=last_name,
                                                email=email,
                                                username=username,
                                                password=password)
                user.is_active = False
                user.save()
                user_profile = UserProfile(
                                        user=user,
                                        phone=phone,
                                        country=country,
                                        street=street,
                                        postcode=postcode,
                                        city=city
                                    )
                user_profile.save()
                current_site = get_current_site(self)
                email_subject = f"Account Activation Link for {current_site.domain}"
                final_email = render_to_string('activeaccount/activate.html', {
                        'user': first_name,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user)
                    })
                email_message = strip_tags(final_email)
                main_email = EmailMultiAlternatives(
                    email_subject,
                    email_message,
                    settings.EMAIL_HOST_USER,
                    [email],
                )
                main_email.attach_alternative(final_email, "text/html")
                main_email.send()
                messages.success(self, f"Your account is created successfully. Please check your email and activate "
                                       f"your account. Otherwise you can't access our services. If you have not "
                                       f"activate your account, We will delete your data in 7 business "
                                       f"days. Thank you!")
                return redirect('register')
        else:
            form = RegisterForm()
        return render(self, 'gorkems_doner_user/register.html', {'form': form})

    def activate_account_view(self, uidb64, token):
        if self.user.is_authenticated:
            return redirect('dashboard')
        else:
            try:
                uid = force_text(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            if user is not None and account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                return render(self, 'activeaccount/activate_success.html')
            elif not account_activation_token.check_token(user, token):
                return render(self, 'activeaccount/account_already_active.html')
            else:
                return render(self, 'activeaccount/activate_failed.html')

    def login(self):
        if self.user.is_authenticated:
            return redirect('profile')
        elif self.method == 'POST':
            form = LoginForm(self.POST)
            if form.is_valid():
                username = self.POST['username']
                password = self.POST['password']
                if User.objects.get(username=username).is_active:
                    user = auth.authenticate(username=username, password=password)
                    if user is not None:
                        auth.login(self, user)
                        self.session['usernameAll'] = username
                        if 'next' in self.POST:
                            return redirect(self.POST.get('next'))
                        else:
                            return redirect('shop')
                else:
                    messages.error(self, f"Your Account Is Not Activated.")
                    return redirect('login')
        else:
            form = LoginForm()
        return render(self, 'gorkems_doner_user/login.html', {'form': form})

    def logout(self):
        if self.user.is_authenticated:
            auth.logout(self)
        return redirect('login')

    def login_with_facebook(self):
        if self.scheme == 'http':
            redirect_uri = f"{self.scheme}s://{self.get_host()}{reverse('facebook_login')}"
        else:
            redirect_uri = f"{self.scheme}://{self.get_host()}{reverse('facebook_login')}"
        if('code' in self.GET):
            code = self.GET.get('code')
            url = 'https://graph.facebook.com/v12.0/oauth/access_token'
            params = {
                'client_id': settings.SOCIAL_AUTH_FACEBOOK_KEY,
                'client_secret': settings.SOCIAL_AUTH_FACEBOOK_SECRET,
                'code': code,
                'redirect_uri': redirect_uri,
            }
            response = requests.get(url, params=params)
            params = response.json()
            params.update({
                'fields': 'id,first_name,last_name,picture,birthday,email,gender,hometown,location'
            })
            url = 'https://graph.facebook.com/me'
            user_data = requests.get(url, params=params).json()
            email = user_data.get('email')
            if email:
                try:
                    user = get_object_or_404(User, email=email)
                    login(self, user)
                except:
                    user = User.objects.create_user(
                        first_name=user_data.get('first_name'),
                        last_name=user_data.get('last_name'),
                        email=email,
                        username=user_data.get('last_name'),
                        password=user_data.get('id')
                    )
                    user.save()
                    user_profile = UserProfile(user=user)
                    user_profile.save()
                    get_user = auth.authenticate(
                        username=user_data.get('last_name'),
                        password=user_data.get('id')
                    )
                    auth.login(self, get_user)
            else:
                messages.error(
                    self,
                    'Unable to login with Facebook Please try again'
                )
            return redirect('shop')
        else:
            url = "https://graph.facebook.com/oauth/authorize"
            params = {
                'client_id': settings.SOCIAL_AUTH_FACEBOOK_KEY,
                'redirect_uri': redirect_uri,
                'scope': 'email,public_profile,user_birthday,user_gender,user_hometown,user_location'
            }
            url += f"?{urlencode(params)}"
            return redirect(url)

    def login_with_google(self):
        if self.scheme == 'http':
            redirect_uri = f"{self.scheme}s://{self.get_host()}{reverse('google_login')}"
        else:
            redirect_uri = f"{self.scheme}://{self.get_host()}{reverse('google_login')}"
        if('code' in self.GET):
            params = {
                'grant_type': 'authorization_code',
                'code': self.GET.get('code'),
                'redirect_uri': redirect_uri,
                'client_id': settings.SOCIAL_AUTH_GOOGLE_KEY,
                'client_secret': settings.SOCIAL_AUTH_GOOGLE_SECRET
            }
            url = 'https://accounts.google.com/o/oauth2/token'
            response = requests.post(url, data=params)
            url = 'https://www.googleapis.com/oauth2/v1/userinfo'
            access_token = response.json().get('access_token')
            response = requests.get(url, params={'access_token': access_token})
            user_data = response.json()
            email = user_data.get('email')
            if email:
                try:
                    user = get_object_or_404(User, email=email)
                    login(self, user)
                except:
                    user = User.objects.create_user(
                        first_name=user_data.get('first_name'),
                        last_name=user_data.get('last_name'),
                        email=email,
                        username=user_data.get('last_name'),
                        password=user_data.get('id'))
                    user.save()
                    user_profile = UserProfile(user=user)
                    user_profile.save()
                    get_user = auth.authenticate(
                        username=user_data.get('last_name'),
                        password=user_data.get('id')
                        )
                    auth.login(self, get_user)
            else:
                messages.error(
                    self,
                    'Unable to login with Gmail Please try again'
                )
            return redirect('shop')
        else:
            url = str("https://accounts.google.com/o/oauth2/auth?client_id=%s&response_type=code&scope=%s&redirect_uri=%s&state=google")
            scope = [
                "https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/userinfo.email"
            ]
            scope = " ".join(scope)
            url = url % (settings.SOCIAL_AUTH_GOOGLE_KEY, scope, redirect_uri)
            return redirect(url)

    @login_required
    def profile(self):
        if self.method == 'POST':
            form = ProfileInfoChangeForm(self.POST, self.FILES)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone_number = form.cleaned_data['phone_number']
                street = form.cleaned_data['street']
                postcode = form.cleaned_data['postcode']
                city = form.cleaned_data['city']
                user_main_profile_update = User.objects.get(pk=self.user.id)
                user_profile_update = UserProfile.objects.get(pk=self.user.id)
                try:
                    profile_pic = self.FILES['profile_pic']
                    user_profile_update.profile_pic = profile_pic
                except:
                    pass
                user_main_profile_update.first_name = first_name
                user_main_profile_update.last_name = last_name
                user_main_profile_update.email = email
                user_profile_update.phone = phone_number
                user_profile_update.street = street
                user_profile_update.postcode = postcode
                user_profile_update.city = city
                user_profile_update.save()
                messages.success(self, f"Your profile is updated")
                return redirect('profile')
            else:
                context = {
                    'form': form,
                    'cart_status': UsersCart.objects.filter(user=self.user).count()
                }
        else:
            context = {
                'form': ProfileInfoChangeForm(),
                'cart_status': UsersCart.objects.filter(user=self.user).count()
            }
        return render(self, 'gorkems_doner_user/profile.html', context)

    @login_required
    def change_password(self):
        if self.method == 'POST':
            form = PassChangeForm(user=self.user, data=self.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(self, self.user)
                messages.success(self, 'Congratulation!! Your password was successfully updated!')
                return redirect('changepassword')
        else:
            form = PassChangeForm(user=self.user)
        return render(self, 'recoveraccount/changepassword.html', {'form': form})

    def password_reset_email(self):
        if self.method == 'POST':
            form = PassResetEmailForm(self.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                user = User.objects.get(email=email)
                user.is_active = False
                user.save()
                current_site = get_current_site(self)
                email_subject = 'Password Reset Link for Derkleineinder.com'
                final_email = render_to_string('recoveraccount/resetemail.html', {
                    'user': user.first_name,
                    'username': user.username,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': password_reset_token.make_token(user)
                })
                email_message = strip_tags(final_email)
                reset_main_email = EmailMultiAlternatives(
                    email_subject,
                    email_message,
                    settings.EMAIL_HOST_USER,
                    [email],
                )
                reset_main_email.attach_alternative(final_email, "text/html")
                reset_main_email.send()
                messages.success(self, f"An email with the password reset instructions is send to your givan email. "
                                       f"Please check your email and follow the instructions. Thank you!!")
                return redirect('pass_rest')
        else:
            form = PassResetEmailForm()
        return render(self, 'recoveraccount/resetform.html', {'form': form})

    def password_reset_form(self, uidb64, token):
        if self.user.is_authenticated:
            return redirect('dashboard')
        elif self.method == 'POST':
            try:
                uid = force_text(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            form = PassRestForm(self.POST)
            if form.is_valid():
                if user is not None and password_reset_token.check_token(user, token):
                    password = form.cleaned_data['password']
                    user.set_password(password)
                    user.is_active = True
                    user.save()
                    messages.success(self, 'Your Password has been set successfully.')
                    return redirect('login')
                else:
                    messages.error(self, 'This link is invalid. Please self a new one.')
                    return redirect('pass_rest')
        else:
            form = PassRestForm()
        return render(self, 'recoveraccount/resetconfirm.html', {'form': form})
