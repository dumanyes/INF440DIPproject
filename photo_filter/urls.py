from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_photo, name='upload_photo'),  # Upload photo
    path('photo/<int:pk>/', views.photo_detail, name='photo_detail'),  # View uploaded or filtered photo
    path('about-us/', views.about_us, name='about_us'),  # About Us page
]

# Serve media files during development (only for DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
