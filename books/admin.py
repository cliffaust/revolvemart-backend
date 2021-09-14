from django.contrib import admin
from .models import Book, BookImage, BookReview, Order, ShippingAddress, Cart, ShippingNote


admin.site.register(Book)
admin.site.register(BookImage)
admin.site.register(BookReview)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(ShippingAddress)
admin.site.register(ShippingNote)