from books.models import Book
from user.models import BookViews
from .serializer import BookViewsSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from .permissions import IsUserProfile
from .serializer import UserSerializer
from django.conf import settings
from user.models import CustomUser


class CreateBookViews(generics.CreateAPIView):
    serializer_class = BookViewsSerializer
    queryset = BookViews.objects.all()

    def get_user_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def perform_create(self, serializer):
        book_slug = self.kwargs.get("book_slug")
        book = generics.get_object_or_404(Book, slug=book_slug)

        ip = self.get_user_ip(self.request)
        book_queryset = BookViews.objects.filter(book=book, user_ip=ip)

        if book_queryset.exists():
            raise PermissionDenied("User has already viewed this post")
        return serializer.save(book=book, user_ip=ip)


class UserProfileView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.email

        return CustomUser.objects.filter(email=user)


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsUserProfile]

    def get_queryset(self):
        user = self.request.user.email

        return CustomUser.objects.filter(email=user)