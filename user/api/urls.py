from django.urls import path
from .views import CreateBookViews, UserProfileDetailView, UserProfileView

urlpatterns = [
    path("books/<book_slug>/add_view/", CreateBookViews.as_view(), name="add_view"),
    path("user/", UserProfileView.as_view(), name="user"),
    path("user/<int:pk>/", UserProfileDetailView.as_view(), name="user-detail")
]