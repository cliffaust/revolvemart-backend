# Generated by Django 3.2.3 on 2021-08-31 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0024_alter_book_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='region',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='town',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
