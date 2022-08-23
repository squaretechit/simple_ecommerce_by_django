from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gorkems_doner_theme.urls')),
    path('', include('gorkems_doner_shop.urls')),
    path('', include('gorkems_doner_user.urls')),
    path('', include('gorkems_doner_admin.urls')),
    path('', include('gorkems_doner_message.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('paypal/', include("paypal.standard.ipn.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
