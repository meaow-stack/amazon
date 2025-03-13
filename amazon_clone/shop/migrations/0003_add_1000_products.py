from django.db import migrations
import random

def add_dummy_products(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    categories = ["Electronics", "Books", "Clothing", "Home & Kitchen", "Toys", "Sports"]
    adjectives = ["Premium", "Deluxe", "Classic", "Modern", "Portable", "Eco-Friendly"]
    items = [
        "Laptop", "Smartphone", "Headphones", "Book", "T-Shirt", "Jeans", "Sofa", "Lamp",
        "Puzzle", "Football", "Yoga Mat", "Blender", "Camera", "Watch", "Backpack"
    ]
    descriptions = [
        "High-performance device for all your needs.",
        "Latest model with cutting-edge features.",
        "Durable and stylish product for everyday use.",
        "Perfect addition to your collection."
    ]

    Product.objects.all().delete()  # Optional: remove if keeping existing data

    for i in range(1000):
        category = random.choice(categories)
        adjective = random.choice(adjectives)
        item = random.choice(items)
        name = f"{adjective} {category} {item} {i+1}"
        description = random.choice(descriptions)
        price = round(random.uniform(5.99, 999.99), 2)
        stock = random.randint(1, 100)
        Product.objects.create(
            name=name,
            description=description,
            price=price,
            stock=stock
        )

class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0001_initial'),  # Depends on initial Product model
    ]
    operations = [
        migrations.RunPython(add_dummy_products),
    ]