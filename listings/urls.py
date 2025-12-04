from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, CategoryViewSet, create_listing_view, listing_detail, my_listings, edit_listing

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'', ListingViewSet)

urlpatterns = [
    path('create/', create_listing_view, name='create_listing'),
    path('my-listings/', my_listings, name='my_listings'),
    path('<int:pk>/edit/', edit_listing, name='edit_listing'),
    path('<int:pk>/', listing_detail, name='listing_detail'),
    path('', include(router.urls)),
]
