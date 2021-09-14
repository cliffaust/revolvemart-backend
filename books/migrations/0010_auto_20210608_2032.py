# Generated by Django 3.2.3 on 2021-06-08 20:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_alter_book_cover_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookimage',
            name='date_posted',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(blank=True, choices=[('Fiction', 'Fiction'), ('Nonfiction', 'Nonfiction'), ('Academic', 'Academic'), ('Romance', 'Romance'), ('Horror', 'Horror'), ('Comedy', 'Comedy'), ('Religion and Spirituality', 'Religion and Spirituality'), ('Christianity', 'Christianity'), ('Islamic', 'Islamic'), ('Science Fiction', 'Science Fiction'), ('Others', 'Others')], max_length=100),
        ),
    ]
