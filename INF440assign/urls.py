from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin site
    path('', lambda request: redirect('upload_photo', permanent=False)),  # Redirect root to upload page
    path('photo_filter/', include('photo_filter.urls')),  # Include photo_filter app URLs
]

# Serve media files during development (only for DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
