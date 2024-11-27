from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

from photo_filter import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('upload_photo', permanent=False)),
    path('photo_filter/', include('photo_filter.urls')),
    path('about-us/', views.about_us, name='about_us'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
