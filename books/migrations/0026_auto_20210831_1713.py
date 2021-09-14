# Generated by Django 3.2.3 on 2021-08-31 17:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0025_auto_20210831_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='order',
            name='updated_at',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]