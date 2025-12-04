from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, chat_with_user

router = DefaultRouter()
router.register(r'', MessageViewSet, basename='message')

urlpatterns = [
    path('<int:user_id>/', chat_with_user, name='chat_with_user'),
    path('<int:user_id>/offer/<int:offer_id>/', chat_with_user, name='chat_with_user'),
    path('', include(router.urls)),
]
