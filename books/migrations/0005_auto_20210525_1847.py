# Generated by Django 3.2.3 on 2021-05-25 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20210525_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(blank=True, choices=[('Fiction', 'Fiction'), ('Nonfiction', 'Nonfiction'), ('Academic', 'Academic'), ('Romance', 'Romance'), ('Horror', 'Horror'), ('Comedy', 'Comedy'), ('Religion', 'Religion and Spirituality'), ('Christianity', 'Christianity'), ('Islamic', 'Islamic'), ('Science Fiction', 'Science Fiction'), ('Others', 'Others')], max_length=100),
        ),
    ]
