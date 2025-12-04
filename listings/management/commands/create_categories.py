from django.core.management.base import BaseCommand
from listings.models import Category


class Command(BaseCommand):
    help = 'Creates default categories if they do not exist'

    def handle(self, *args, **options):
        default_categories = [
            'Electronics', 'Furniture', 'Vehicles', 'Services', 'Clothing', 'Books',
            'Home & Garden', 'Sports & Outdoors', 'Toys & Games', 'Other'
        ]
        
        created_count = 0
        for cat_name in default_categories:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': cat_name.lower().replace(' ', '-').replace('&', 'and')}
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat_name}'))
            else:
                self.stdout.write(f'Category already exists: {cat_name}')
        
        self.stdout.write(self.style.SUCCESS(f'\nTotal categories: {Category.objects.count()}'))
        if created_count > 0:
            self.stdout.write(self.style.SUCCESS(f'Created {created_count} new categories'))

