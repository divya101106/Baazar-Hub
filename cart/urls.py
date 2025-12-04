from django.urls import path
from .views import cart_view, add_to_cart, remove_from_cart, buy_now

urlpatterns = [
    path('', cart_view, name='cart_view'),
    path('add/<int:listing_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),
    path('buy-now/<int:listing_id>/', buy_now, name='buy_now'),
]

