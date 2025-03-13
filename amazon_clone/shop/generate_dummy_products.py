import os
import random
import django
from faker import Faker

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amazon_clone.settings")
django.setup()

from shop.models import Product

# Initialize Faker for realistic data
fake = Faker()

# Categories and tags for variety
categories = ["Electronics", "Books", "Clothing", "Home & Kitchen", "Toys", "Sports"]
adjectives = ["Premium", "Deluxe", "Classic", "Modern", "Portable", "Eco-Friendly"]
items = [
    "Laptop", "Smartphone", "Headphones", "Book", "T-Shirt", "Jeans", "Sofa", "Lamp",
    "Puzzle", "Football", "Yoga Mat", "Blender", "Camera", "Watch", "Backpack"
]

def generate_dummy_products(count=1000):
    for _ in range(count):
        category = random.choice(categories)
        adjective = random.choice(adjectives)
        item = random.choice(items)
        name = f"{adjective} {category} {item}"
        description = fake.text(max_nb_chars=200)
        price = round(random.uniform(5.99, 999.99), 2)
        stock = random.randint(1, 100)

        # Create and save the product
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock
            # image field omitted for simplicity; add a default or upload logic if needed
        )
        product.save()

    print(f"Generated {count} dummy products.")

if __name__ == "__main__":
    # Clear existing products (optional)
    Product.objects.all().delete()
    # Generate 1000 products
    generate_dummy_products(1000)