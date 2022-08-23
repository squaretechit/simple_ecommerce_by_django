from django.urls import path
from .views import GorkemsDonerUsers


urlpatterns = [
    path('register/', GorkemsDonerUsers.register, name='register'),
    path('activate/<uidb64>/<token>', GorkemsDonerUsers.activate_account_view, name='activate'),
    path('login/', GorkemsDonerUsers.login, name='login'),
    path('facebook-login/', GorkemsDonerUsers.login_with_facebook, name='facebook_login'),
    path('google-login/', GorkemsDonerUsers.login_with_google, name='google_login'),
    path('logout/', GorkemsDonerUsers.logout, name='logout'),
    path('profile/', GorkemsDonerUsers.profile, name='profile'),
    path('change-password/', GorkemsDonerUsers.change_password, name='change_password'),
    path('password-reset/', GorkemsDonerUsers.password_reset_email, name='pass_rest'),
    path('password-reset-confirm/<uidb64>/<token>/', GorkemsDonerUsers.password_reset_form,
        name='password_reset_confirm'),
]
