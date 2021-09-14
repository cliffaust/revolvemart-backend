from books.models import Book, BookImage, BookReview, Order, ShippingAddress, Cart, ShippingNote
from rest_framework.exceptions import PermissionDenied
from django.db.models import Case, When
from .serializer import (
    BookSerializer,
    BookImageSerializer,
    BookReviewSerializer,
    OrderSerializer,
    ShippingAddressSerializer,
    CartSerializer,
    ShippingNoteSerializer
)
from .pagination import BookPagination
from rest_framework.validators import ValidationError
from rest_framework import generics, serializers, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .filterset import BookFilter, ReviewFilter

from rest_framework.permissions import IsAuthenticated
from .permissions import IsUserBookInstance, ObjectPermission, OrderItemPermission

from core.recommendation import similar_books


class BookListViews(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "author"]
    pagination_class = BookPagination

    ordering_fields = [
        "date_posted",
        "stock",
        "price",
    ]


class BookRecommendationListViews(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        title_query = self.kwargs.get("title")
        book_titles = similar_books(title_query)[:6]

        preserved = Case(*[When(title=title, then=pos) for pos, title in enumerate(list(book_titles))])

        return Book.objects.filter(title__in=list(book_titles)).order_by(preserved)


class BookJustArrivedListViews(generics.ListAPIView):
    queryset = Book.objects.order_by('-date_posted', 'views')
    serializer_class = BookSerializer
    pagination_class = BookPagination

class BookUderPriceListViews(generics.ListAPIView):
    queryset = Book.objects.filter(price__lt = 30)
    serializer_class = BookSerializer
    pagination_class = BookPagination


class UserBookListViews(generics.ListAPIView):
    serializer_class = BookSerializer
    filter_backends = [OrderingFilter]
    pagination_class = BookPagination
    permission_classes = [IsAuthenticated]

    ordering_fields = [
        "date_posted",
        "stock",
        "price",
    ]

    def get_queryset(self):
        queryset = Book.objects.filter(user=self.request.user)

        return queryset


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    permission_classes = [ObjectPermission]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Book.objects.all()
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = Book.objects.filter(slug=slug)
        return queryset


class BookImageListView(generics.ListAPIView):
    serializer_class = BookImageSerializer

    def get_queryset(self):
        queryset = BookImage.objects.all()

        book_slug = self.kwargs.get("book_slug")
        if book_slug is not None:
            book = generics.get_object_or_404(Book, slug=book_slug)
            queryset = BookImage.objects.filter(book=book)

        return queryset


class BookImageCreateView(generics.CreateAPIView):
    queryset = BookImage.objects.all()
    serializer_class = BookImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        book_slug = self.kwargs.get("book_slug")
        book = generics.get_object_or_404(Book, slug=book_slug)
        book_queryset = Book.objects.filter(slug=book_slug, user=self.request.user)

        if not book_queryset.exists():
            raise PermissionDenied("You can't add an image to this book")
        return serializer.save(book=book)


class BookImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookImageSerializer
    permission_classes = [IsUserBookInstance]

    def get_queryset(self):

        book_slug = self.kwargs.get("book_slug")
        if book_slug is not None:
            book = generics.get_object_or_404(Book, slug=book_slug)
            queryset = BookImage.objects.filter(book=book)

            return queryset


class BookReviewListView(generics.ListAPIView):
    serializer_class = BookReviewSerializer
    filterset_class = ReviewFilter

    def get_queryset(self):
        queryset = BookReview.objects.all()

        book_slug = self.kwargs.get("book_slug")
        if book_slug is not None:
            book = generics.get_object_or_404(Book, slug=book_slug)
            queryset = BookReview.objects.filter(book=book)

            return queryset


class BookReviewCreateView(generics.CreateAPIView):
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        book_slug = self.kwargs.get("book_slug")
        book = generics.get_object_or_404(Book, slug=book_slug)

        review_queryset = BookReview.objects.filter(user=self.request.user, book=book)

        book_queryset = Book.objects.filter(slug=book_slug, user=self.request.user)

        if review_queryset.exists():
            raise ValidationError("User has already reviewed this book")

        elif book_queryset.exists():
            raise PermissionDenied("You can't make a review on your book")

        serializer.save(book=book, user=self.request.user)


class BookReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookReviewSerializer
    permission_classes = [ObjectPermission]

    def get_queryset(self):

        book_slug = self.kwargs.get("book_slug")
        if book_slug is not None:
            book = generics.get_object_or_404(Book, slug=book_slug)
            queryset = BookReview.objects.filter(book=book)

            return queryset


class ShippingAddressCreateView(generics.CreateAPIView):
    serializer_class = ShippingAddressSerializer
    queryset = ShippingAddress.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        address = ShippingAddress.objects.filter(user=self.request.user)

        if self.request.POST.get('default') == 'true':
            for data in address:
                data.default = False
                data.save()

            serializer.save(user=self.request.user)

        elif self.request.POST.get('default', 'false') == 'false':
            serializer.save(user=self.request.user)


class ShippingAddressListView(generics.ListAPIView):
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ShippingAddress.objects.filter(user=self.request.user)
        return queryset


class ShippingAddressDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAuthenticated, ObjectPermission]

    def get_queryset(self):
        queryset = ShippingAddress.objects.filter(user=self.request.user)
        return queryset

    def perform_update(self, serializer):
        address = ShippingAddress.objects.filter(user=self.request.user)

        if self.request.POST.get('default') == 'true':
            for data in address:
                data.default = False
                data.save()
            instance = self.get_object()
            instance.default = True
            instance.save()

            serializer.save()

        elif self.request.POST.get('default', 'false') == 'false':
            instance = self.get_object()
            instance.default = False
            instance.save()

            serializer.save()

        return Response(serializer.data)
            


class ShippingNoteView(generics.RetrieveUpdateAPIView):
    serializer_class = ShippingNoteSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset, created = ShippingNote.objects.get_or_create(user=self.request.user)
        return queryset


class CartItemAPIView(APIView):
    serializer_class = CartSerializer

    permission_classes = [IsAuthenticated, ObjectPermission]

    def post(self, request, book_slug, pk=None):
        book = generics.get_object_or_404(Book, slug=book_slug)
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1

        if book.stock > 0:
            cart = Cart.objects.create(
                user=request.user, book=book
            )
            
            if quantity > int(book.stock):
                raise PermissionDenied(
                    "Your Quantity is greater than what is in the stock"
                )
            else:
                

                cart.quantity = quantity


                cart.save()

            

            serializer_context = {"request": request}
            serializer = self.serializer_class(cart, context=serializer_context)

            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            raise PermissionDenied("Sorry, this item is out of stock")



class OrderCreateView(APIView):
    serializer_class = OrderSerializer

    permission_classes = [IsAuthenticated]

    def post(self, request, book_slug, address_pk, pk=None):
        book = generics.get_object_or_404(Book, slug=book_slug)
        
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1
        if book.stock > 0:
            
            shipping_address = generics.get_object_or_404(ShippingAddress, pk=address_pk, user=request.user)
            
                
            shipping_note = generics.get_object_or_404(
                ShippingNote, user = request.user
            )
            if quantity > int(book.stock):
                raise PermissionDenied(
                    "Your Quantity is greater than what is in the stock"
                )
            else:
            
                book.stock -= quantity
                book.save()


            serializer_context = {"request": request}
            serializer = self.serializer_class(data=request.data, context=serializer_context)

            if serializer.is_valid():
                serializer.save(user=request.user, shipping_address=shipping_address, shipping_note=shipping_note, book=book)

                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            raise PermissionDenied("Sorry, this item is out of stock")


class RemoveOrderApiView(APIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ObjectPermission]

    def delete(self, request):
        order = generics.get_object_or_404(Order, user=request.user, received=False)

        self.check_object_permissions(request, order)

        serializer_context = {"request": request}
        serializer = self.serializer_class(order, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer

    permission_classes = [IsAuthenticated, OrderItemPermission]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class UserOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    def get_serializer_class(self, *args, **kwargs):
        return OrderSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, received=False)


class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, OrderItemPermission]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, received=False)
