# Generated by Django 3.2.3 on 2021-05-25 03:27

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover_image',
            field=models.ImageField(null=True, upload_to=core.utils.book_cover_thumbnail),
        ),
    ]
