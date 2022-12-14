# Generated by Django 3.2.10 on 2022-10-10 12:43

import billing.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='profile_image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=billing.models.upload_directory_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'jpg'])]),
        ),
    ]
