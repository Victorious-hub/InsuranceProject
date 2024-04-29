from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('affiliates/', include('apps.affiliates.urls')),
    path('main/', include('apps.main.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
