from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from core.utils import book_image_thumbnail, book_cover_thumbnail
from django.utils import timezone
from imagekit.models import ProcessedImageField
from django.contrib.postgres.fields import ArrayField
from imagekit.processors import Resize

from phonenumber_field.modelfields import PhoneNumberField


BOOK_CATEGORY = (
    ("Fiction", "Fiction"),
    ("Nonfiction", "Nonfiction"),
    ("Literature", "Literature"),
    ("History", "History"),
    ("Business", "Business"),
    ("Academic", "Academic"),
    ("Economics", "Economics"),
    ("Mathematics", "Mathematics"),
    ("Romance", "Romance"),
    ("Horror", "Horror"),
    ("Comedy", "Comedy"),
    ("Religion and Spirituality", "Religion and Spirituality"),
    ("Christianity", "Christianity"),
    ("Islamic", "Islamic"),
    ("Science Fiction", "Science Fiction"),
    ("For Student", "For Student"),
    ("Others", "Others"),
)

BOOK_CONDITION = (
    ("Good", "Good"),
    ("Not very good", "Not very good"),
    ("Bad", "Bad"),
    ("Brand New", "Brand New"),
)


class Book(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    categories = ArrayField(models.TextField(max_length=100, choices=BOOK_CATEGORY), blank=True, null=True)
    condition = models.CharField(max_length=100, choices=BOOK_CONDITION, blank=True)
    stock = models.PositiveIntegerField()
    date_posted = models.DateField(default=timezone.now)
    cover_image = ProcessedImageField(
        upload_to=book_cover_thumbnail,
        processors=[Resize(500, 500)],
        format="JPEG",
        options={"quality": 60},
    )

    def __str__(self):
        return f"{ self.title } - { self.author }"

    def discount_percentage(self):
        if self.discount_price:
            return ((self.price - self.discount_price) / self.price) * 100

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_image = self.cover_image
            self.cover_image = None
            super(Book, self).save(*args, **kwargs)

            self.cover_image = saved_image
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")

        super(Book, self).save(*args, **kwargs)


class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book_images")
    image = ProcessedImageField(
        upload_to=book_image_thumbnail,
        processors=[Resize(500, 500)],
        format="JPEG",
        options={"quality": 60},
    )

    def __str__(self):
        return str(self.book)


class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rate = models.IntegerField(
        blank=True, null=True, validators=(MinValueValidator(0), MaxValueValidator(5))
    )
    message = models.CharField(max_length=500, blank=True, null=True)
    date_posted = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.rate)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book")
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    estimated_shipping_cost = models.FloatField(default=0)
    final_shipping_cost = models.FloatField(default=0)

    def __str__(self):
        return f"{self.quantity} of {self.book.title}"

    def total_book_price(self):
        return self.quantity * self.book.price

    def total_book_discount_price(self):
        if self.book.discount_price:
            return self.quantity * self.book.discount_price
        else:
            return

    def saving_amount(self):
        if self.book.discount_price:
            return self.total_book_price() - self.total_book_discount_price()
        else:
            return

    def final_price(self):
        if self.book.discount_price:
            return self.total_book_discount_price()
        else:
            return self.total_book_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateField(default=timezone.now)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="books")
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    shipping_address = models.ForeignKey(
        "ShippingAddress", on_delete=models.SET_NULL, null=True, blank=True
    )
    shipping_note = models.ForeignKey(
        "ShippingNote", on_delete=models.SET_NULL, null=True, blank=True
    )
    on_board = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    estimated_shipping_cost = models.FloatField(default=0)
    final_shipping_cost = models.FloatField(default=0)

    def __str__(self):
        return f"Order for { self.book.title } ({self.quantity} items) by {self.user}"


    def total_book_price(self):
        return self.quantity * self.book.price

    def total_book_discount_price(self):
        if self.book.discount_price:
            return self.quantity * self.book.discount_price
        else:
            return

    def saving_amount(self):
        if self.book.discount_price:
            return self.total_book_price() - self.total_book_discount_price()
        else:
            return

    def final_price(self):
        if self.book.discount_price:
            return self.total_book_discount_price()
        else:
            return self.total_book_price()


class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True)
    town = models.CharField(max_length=255, null=True)
    region = models.CharField(max_length=100, null=True)
    phone = PhoneNumberField(blank=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class ShippingNote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="note")
    note = models.TextField(null=True)

    def __str__(self):
        return str(self.user)
