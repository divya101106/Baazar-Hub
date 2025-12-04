from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ModerationQueueViewSet, moderation_dashboard, moderate_action

router = DefaultRouter()
router.register(r'', ModerationQueueViewSet, basename='moderation')

urlpatterns = [
    path('dashboard/', moderation_dashboard, name='moderation_dashboard'),
    path('action/<int:pk>/<str:action>/', moderate_action, name='moderate_action'),
    path('', include(router.urls)),
]
