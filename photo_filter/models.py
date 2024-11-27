import os
from django.utils.timezone import now
from django.db import models

def truncate_filename(instance, filename):
    # Truncate the name if it's too long
    max_length = 100
    name, ext = os.path.splitext(filename)
    if len(name) > max_length:
        name = name[:max_length]
    return f'photos/originals/{name}_{now().strftime("%Y%m%d%H%M%S")}{ext}'

class Photo(models.Model):
    original_image = models.ImageField(upload_to=truncate_filename, max_length=255)
    filtered_image = models.ImageField(upload_to='photos/filtered/', blank=True, null=True)
    description = models.TextField(default='', blank=True)
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Photo {self.id} - {self.description[:20]}"
