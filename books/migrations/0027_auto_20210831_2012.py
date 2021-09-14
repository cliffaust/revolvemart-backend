# Generated by Django 3.2.3 on 2021-08-31 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0026_auto_20210831_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='estimated_shipping_cost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='final_shipping_cost',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
