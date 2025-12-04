from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OfferViewSet, create_offer

router = DefaultRouter()
router.register(r'', OfferViewSet, basename='offer')

urlpatterns = [
    path('create/', create_offer, name='create_offer'),
    path('', include(router.urls)),
]
