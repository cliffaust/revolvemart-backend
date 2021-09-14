import csv
from django.core.exceptions import PermissionDenied

from django.shortcuts import render
from django.http import HttpResponse
from .models import Book

# Create your views here.

def export(request):
    if not request.user.is_staff:
        raise PermissionDenied
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['id', 'title', 'author', 'description', 'price', 'categories'])

    for book in Book.objects.all().values_list('id', 'title', 'author', 'description', 'price', 'categories'):
        writer.writerow(book)

    response['Content-Dispositon'] = 'attachment; filename="books.csv"'

    return response
