# Generated by Django 3.2.3 on 2021-09-10 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_bookviews'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='phone',
        ),
    ]
