import random
import string

ALPHANUMERIC_CHARS = string.ascii_lowercase + string.digits

STRING_LENGTH = 6


def generate_random_string(chars=ALPHANUMERIC_CHARS, length=STRING_LENGTH):
    return "".join(random.choice(chars) for _ in range(length))


def profile_image_thumbnail(instance, filename):
    return f"profile_images/{instance.id}/{filename}"


def book_image_thumbnail(instance, filename):
    return f"book-images/{instance.book.id}/{filename}"


def book_cover_thumbnail(instance, filename):
    return f"book-cover-image/{instance.id}/{filename}"
