from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SavedSearchViewSet

router = DefaultRouter()
router.register(r'', SavedSearchViewSet, basename='savedsearch')

urlpatterns = [
    path('', include(router.urls)),
]
