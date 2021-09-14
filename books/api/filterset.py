from django_filters import rest_framework as filters
from rest_framework import fields
from books.models import Book, BookReview
from books.models import BOOK_CATEGORY, BOOK_CONDITION

RATES = (("1", "1"), ("2", "2"), ("3" "3"), ("4", "4"), ("5", "5"))


class BookFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    book_category = filters.ChoiceFilter(field_name="categories", lookup_expr='icontains', choices=BOOK_CATEGORY)
    book_condition = filters.ChoiceFilter(
        field_name="condition", choices=BOOK_CONDITION
    )

    class Meta:
        model = Book
        fields = [
            "min_price",
            "max_price",
            "book_category",
            "book_condition",
        ]


class ReviewFilter(filters.FilterSet):
    rate = filters.ChoiceFilter(field_name="rate", choices=RATES)

    class Meta:
        model = BookReview
        fields = ["rate"]
