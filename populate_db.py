import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from listings.models import Category, Listing, ListingImage
from moderation.models import ModerationQueue
from services.listings_service import create_listing

def populate():
    # Create Categories
    categories = ['Electronics', 'Furniture', 'Vehicles', 'Services', 'Clothing', 'Books']
    for cat_name in categories:
        Category.objects.get_or_create(name=cat_name, slug=cat_name.lower())
    print("Categories created.")

    # Create Users
    users = ['seller1', 'seller2', 'buyer1']
    for username in users:
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password='password123')
    print("Users created.")

    # Create Listings
    seller1 = User.objects.get(username='seller1')
    seller2 = User.objects.get(username='seller2')
    
    electronics = Category.objects.get(name='Electronics')
    furniture = Category.objects.get(name='Furniture')

    # Listing 1: Approved (Low spam score)
    l1_data = {
        'title': 'iPhone 13 Pro Max - Great Condition',
        'description': 'Selling my iPhone 13 Pro Max. 256GB, Graphite. Battery health 90%. Comes with box and cable. No scratches.',
        'price': 800.00,
        'category_id': electronics.id
    }
    create_listing(seller1, l1_data)
    print("Listing 1 created (Should be Approved).")

    # Listing 2: Pending (High spam score trigger)
    # We need to trigger the heuristic. 
    # Heuristic 1: Short title/desc? No, that gives +20.
    # Heuristic 2: Keywords 'cash only', 'urgent'.
    l2_data = {
        'title': 'URGENT SALE: Sofa',
        'description': 'Moving out, must go today. Cash only. Call me.',
        'price': 50.00,
        'category_id': furniture.id
    }
    create_listing(seller2, l2_data)
    print("Listing 2 created (Should be Pending/Moderation).")

    # Listing 3: Approved
    l3_data = {
        'title': 'Wooden Dining Table',
        'description': 'Solid oak dining table with 4 chairs. Good condition, minor wear. Pick up only.',
        'price': 200.00,
        'category_id': furniture.id
    }
    create_listing(seller1, l3_data)
    print("Listing 3 created (Should be Approved).")

if __name__ == '__main__':
    populate()
