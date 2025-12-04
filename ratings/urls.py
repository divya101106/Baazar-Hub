from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RatingViewSet, create_rating

router = DefaultRouter()
router.register(r'', RatingViewSet, basename='rating')

urlpatterns = [
    path('create/<int:user_id>/', create_rating, name='create_rating'),
    path('create/<int:user_id>/offer/<int:offer_id>/', create_rating, name='create_rating'),
    path('', include(router.urls)),
]
