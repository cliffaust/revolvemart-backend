# Generated by Django 3.2.3 on 2021-09-10 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0033_alter_shippingnote_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingnote',
            name='note',
            field=models.TextField(null=True),
        ),
    ]