from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OfferViewSet, create_offer, accept_offer, reject_offer

router = DefaultRouter()
router.register(r'', OfferViewSet, basename='offer')

urlpatterns = [
    path('create/', create_offer, name='create_offer'),
    path('<int:offer_id>/accept/', accept_offer, name='accept_offer'),
    path('<int:offer_id>/reject/', reject_offer, name='reject_offer'),
    path('', include(router.urls)),
]
