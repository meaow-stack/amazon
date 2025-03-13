import os
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.db import IntegrityError
from django.views.decorators.http import require_POST
from .models import User, Product, Cart, CartItem
import stripe
from .recomendations import get_recommendations  # Assuming this is your recommendation module

# Stripe configuration
stripe.api_key = settings.STRIPE_SECRET_KEY

# Home view: Main landing page for all users
def home(request):
    """Renders the home page with featured products and personalized content for logged-in users."""
    products = Product.objects.all()
    context = {'products': products}

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        context['cart_items'] = cart.cartitem_set.all()
        context['username'] = request.user.username
        try:
            context['recommended_products'] = get_recommendations(request.user)[:5]
        except Exception as e:
            messages.error(request, f"Recommendations unavailable: {str(e)}")
            context['recommended_products'] = Product.objects.order_by('?')[:5]

    return render(request, 'home.html', context)

# Login view: Authenticates users
def user_login(request):
    """Handles user login with username and password."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

# Personalized Products view: Dedicated page for user-specific recommendations
@login_required
def personalized_products(request):
    """Displays a full list of recommended products tailored to the logged-in user."""
    try:
        recommended_products = get_recommendations(request.user)
    except Exception as e:
        messages.error(request, f"Recommendations unavailable: {str(e)}")
        recommended_products = Product.objects.order_by('?')[:10]

    context = {
        'recommended_products': recommended_products,
        'username': request.user.username,
    }
    return render(request, 'personalized_products.html', context)

# Static Pages
def about(request):
    """Renders the About page."""
    return render(request, 'about.html')

def terms(request):
    """Renders the Terms page."""
    return render(request, 'terms.html')

def contact(request):
    """Renders the Contact page."""
    return render(request, 'contact.html')

# Cart view: Displays user's cart with items and total
@login_required
def cart(request):
    """Renders the cart page with items and total price."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    context = {
        'cart_items': cart_items,
        'cart': cart,
    }
    return render(request, 'cart.html', context)

# Logout view: Ends user session
def user_logout(request):
    """Logs out the user and redirects to home."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

# Register view: Creates a new user account
def register(request):
    """Handles user registration with username, email, and password."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        try:
            user = User.objects.create_user(username=username, email=email, password=password, is_admin=False)
            user.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Account created!')
            return redirect('home')
        except IntegrityError:
            messages.error(request, f'The username "{username}" is already taken. Please try another.')
    return render(request, 'register.html')

# User Dashboard: Main page for logged-in users
@login_required
def user_dashboard(request):
    """Displays products, cart, and recommendations for the logged-in user."""
    products = Product.objects.all()
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    recommended_products = get_recommendations(request.user)
    context = {
        'products': products,
        'cart_items': cart_items,
        'recommended_products': recommended_products,
    }
    return render(request, 'user_dashboard.html', context)

# Admin Dashboard: Product management for admins
@login_required
def admin_dashboard(request):
    """Renders the admin dashboard for product management."""
    if not request.user.is_admin:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    products = Product.objects.all()
    return render(request, 'admin_dashboard.html', {'products': products})

# Add Product: Admin-only product creation
@login_required
def add_product(request):
    """Allows admins to add a new product."""
    if not request.user.is_admin:
        messages.error(request, 'Unauthorized access.')
        return redirect('home')
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        stock = request.POST['stock']
        image = request.FILES.get('image')
        try:
            product = Product(name=name, description=description, price=float(price), stock=int(stock), image=image)
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('admin_dashboard')
        except ValueError:
            messages.error(request, 'Price must be a number and stock must be an integer.')
    return render(request, 'add_product.html')

# Edit Product: Admin-only product updates
@login_required
def edit_product(request, product_id):
    """Allows admins to edit an existing product."""
    if not request.user.is_admin:
        messages.error(request, 'Unauthorized access.')
        return redirect('home')
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.description = request.POST['description']
        try:
            product.price = float(request.POST['price'])
            product.stock = int(request.POST['stock'])
            if request.FILES.get('image'):
                product.image = request.FILES['image']
            product.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('admin_dashboard')
        except ValueError:
            messages.error(request, 'Price must be a number and stock must be an integer.')
    return render(request, 'edit_product.html', {'product': product})

# Delete Product: Admin-only product removal
@login_required
def delete_product(request, product_id):
    """Allows admins to delete a product."""
    if not request.user.is_admin:
        messages.error(request, 'Unauthorized access.')
        return redirect('home')
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('admin_dashboard')

# Add to Cart: Adds or increments product in cart
@login_required
def add_to_cart(request, product_id):
    """Adds a product to the user’s cart or increases its quantity."""
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart')

# Delete Cart Item: Removes an item from the cart
@login_required
def delete_cart_item(request, cart_item_id):
    """Removes a specific item from the user’s cart."""
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from cart!')
    return redirect('cart')

# Update Cart: AJAX endpoint for quantity updates
@login_required
@require_POST
def update_cart(request, item_id):
    """Updates the quantity of a cart item via AJAX."""
    try:
        cart = Cart.objects.get(user=request.user)
        item = CartItem.objects.get(id=item_id, cart=cart)
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            return JsonResponse({'success': False, 'error': 'Quantity must be at least 1', 'old_quantity': item.quantity})
        item.quantity = quantity
        item.save()
        return JsonResponse({
            'success': True,
            'item_total': float(item.product.price * item.quantity),
            'cart_total': float(cart.get_total_price())
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found', 'old_quantity': 1})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e), 'old_quantity': 1})

# Search: Product search functionality
def search(request):
    """Searches products by name or description."""
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        products = Product.objects.all()
    context = {'products': products}
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        context['cart_items'] = cart.cartitem_set.all()
        context['username'] = request.user.username
        context['recommended_products'] = get_recommendations(request.user)[:5]
        if request.user.is_admin:
            return render(request, 'admin_dashboard.html', context)
    return render(request, 'home.html', context)

# Checkout: Handles payment processing
@login_required
def checkout(request):
    """Renders checkout page and creates Stripe payment intent."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    total = cart.get_total_price()
    if request.method == 'POST':
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(total * 100),
                currency='usd',
                metadata={'user_id': request.user.id},
            )
            return JsonResponse({'client_secret': intent['client_secret']})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    context = {
        'cart_items': cart_items,
        'total': total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'checkout.html', context)

# Payment Success: Confirms successful payment
@login_required
def payment_success(request):
    """Clears cart and confirms payment success."""
    cart = Cart.objects.get(user=request.user)
    cart.cartitem_set.all().delete()
    messages.success(request, 'Payment completed successfully!')
    return render(request, 'payment_success.html')

@login_required
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return redirect('cart')  # assuming your cart page is named 'cart'

# ... (other imports remain the same)

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart': cart})

@login_required
@require_POST
def update_cart(request, item_id):
    try:
        cart = Cart.objects.get(user=request.user)
        item = CartItem.objects.get(id=item_id, cart=cart)
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            return JsonResponse({'success': False, 'error': 'Quantity must be at least 1', 'old_quantity': item.quantity})
        item.quantity = quantity
        item.save()
        return JsonResponse({
            'success': True,
            'item_total': float(item.product.price * item.quantity),
            'cart_total': float(cart.get_total_price())
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found', 'old_quantity': 1})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e), 'old_quantity': 1})

@login_required
def delete_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from cart!')
    return redirect('cart')

