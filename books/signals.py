from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Book
from django.utils.text import slugify
from core.utils import generate_random_string


@receiver(pre_save, sender=Book)
def create_book_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        slug = slugify(instance.title)
        random_string = generate_random_string()
        instance.slug = slug + "-" + random_string