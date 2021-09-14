# Generated by Django 3.2.3 on 2021-08-13 12:23

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0022_alter_book_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='categories',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(choices=[('Fiction', 'Fiction'), ('Nonfiction', 'Nonfiction'), ('Literature', 'Literature'), ('Business', 'Business'), ('Academic', 'Academic'), ('Economics', 'Economics'), ('Mathematics', 'Mathematics'), ('Romance', 'Romance'), ('Horror', 'Horror'), ('Comedy', 'Comedy'), ('Religion and Spirituality', 'Religion and Spirituality'), ('Christianity', 'Christianity'), ('Islamic', 'Islamic'), ('Science Fiction', 'Science Fiction'), ('For Student', 'For Student'), ('Others', 'Others')], max_length=100), blank=True, null=True, size=None),
        ),
    ]
