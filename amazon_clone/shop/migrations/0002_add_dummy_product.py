from django.db import migrations

def add_dummy_products(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    dummy_products = [
        {'name': 'Laptop', 'description': 'High-performance laptop', 'price': 999.99, 'stock': 10},
        {'name': 'Phone', 'description': 'Latest smartphone', 'price': 699.99, 'stock': 15},
        {'name': 'Headphones', 'description': 'Noise-cancelling headphones', 'price': 199.99, 'stock': 20},
        {'name': 'Book', 'description': 'Bestselling novel', 'price': 19.99, 'stock': 50},
    ]
    for product in dummy_products:
        Product.objects.create(**product)

class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(add_dummy_products),
    ]