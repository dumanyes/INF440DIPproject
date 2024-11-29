import os
from django.utils.timezone import now
from django.db import models


def truncate_filename(instance, filename):
    """
    Truncate the filename to a maximum length and append a timestamp to ensure uniqueness.
    """
    max_length = 100
    name, ext = os.path.splitext(filename)
    if len(name) > max_length:
        name = name[:max_length]
    return f'photos/originals/{name}_{now().strftime("%Y%m%d%H%M%S")}{ext}'


class Photo(models.Model):
    original_image = models.ImageField(
        upload_to=truncate_filename,
        max_length=255,
        verbose_name="Original Image",
        default="photos/originals/default.jpg"  # Default placeholder image
    )
    filtered_image = models.ImageField(
        upload_to='photos/filtered/',
        blank=True,
        null=True,
        verbose_name="Filtered Image",
        default="photos/filtered/default.jpg"  # Default filtered placeholder
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        default="No description provided."  # Default description
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active"
    )
    uploaded_at = models.DateTimeField(
        default=now,
        verbose_name="Uploaded At"
    )

    def __str__(self):
        """
        String representation for better identification.
        """
        return f"Photo {self.id} - {self.original_image.name.split('/')[-1]}"

    class Meta:
        """
        Additional metadata for the Photo model.
        """
        verbose_name = "Photo"
        verbose_name_plural = "Photos"
        ordering = ["-uploaded_at"]
