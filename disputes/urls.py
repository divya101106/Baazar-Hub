from django.urls import path
from .views import create_dispute, dispute_detail, my_disputes

urlpatterns = [
    path('create/', create_dispute, name='create_dispute'),
    path('create/<int:offer_id>/', create_dispute, name='create_dispute_for_offer'),
    path('<int:dispute_id>/', dispute_detail, name='dispute_detail'),
    path('my-disputes/', my_disputes, name='my_disputes'),
]

