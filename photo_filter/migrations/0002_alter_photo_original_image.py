# Generated by Django 4.2.16 on 2024-11-25 19:24

from django.db import migrations, models
import photo_filter.models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_filter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='original_image',
            field=models.ImageField(upload_to=photo_filter.models.truncate_filename),
        ),
    ]
