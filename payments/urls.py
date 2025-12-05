from django.urls import path
from .views import payment_page, payment_success

urlpatterns = [
    path('<int:offer_id>/', payment_page, name='payment_page'),
    path('<int:offer_id>/success/', payment_success, name='payment_success'),
]

