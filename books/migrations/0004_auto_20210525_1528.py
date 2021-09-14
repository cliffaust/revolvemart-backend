# Generated by Django 3.2.3 on 2021-05-25 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='condition',
            field=models.CharField(blank=True, choices=[('Good', 'Good'), ('Not very good', 'Not very good'), ('Bad', 'Bad'), ('Brand New', 'Brand New')], max_length=100),
        ),
    ]