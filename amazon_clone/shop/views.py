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
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm
from .utils import send_verification_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from .models import User
from .models import Order
from .models import Address  # Assuming you have an Address model
from .forms import AddressForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout, get_user_model
import requests





# Stripe configuration
stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    """Renders the home page with featured products, personalized content, weather, and order status."""
    products = Product.objects.all()
    context = {'products': products}

    if request.user.is_authenticated:
        # Cart handling
        cart, _ = Cart.objects.get_or_create(user=request.user)
        context['cart_items'] = cart.cartitem_set.all()
        context['username'] = request.user.username

        # Product Recommendations
        try:
            context['recommended_products'] = get_recommendations(request.user)[:5]
        except Exception as e:
            messages.error(request, f"Recommendations unavailable: {str(e)}")
            context['recommended_products'] = Product.objects.order_by('?')[:5]

        # User Address
        try:
            address_obj = request.user.address  # OneToOne relation
            context['address'] = f"{address_obj.city}, {address_obj.state}"
        except Address.DoesNotExist:
            context['address'] = "Set your address"
            address_obj = None  # set None so weather section won't try to use it

        # Weather Information
        weather_info = "Weather unavailable"
        if address_obj:
            try:
                api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your actual API key
                city = address_obj.city
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                response = requests.get(url).json()
                if response.get("cod") == 200:
                    temp = response["main"]["temp"]
                    condition = response["weather"][0]["main"]
                    weather_info = f"{temp}°C, {condition}"
                    if "Rain" in condition or "Snow" in condition or temp < 0 or temp > 35:
                        weather_info += " (Not ideal for delivery)"
                    else:
                        weather_info += " (Good for delivery)"
                else:
                    weather_info = "City not found"
            except Exception as e:
                weather_info = f"Weather fetch failed: {str(e)}"
        context['weather_info'] = weather_info

        # Delivery Status (Last 5 orders)
        context['orders'] = Order.objects.filter(user=request.user).order_by('-created_at')[:5]

    return render(request, 'home.html', context)

# Login view: Authenticates users
# Dynamically get the User model
User = get_user_model()
# Debug: Print the User model to confirm
print(f"User model in views.py: {User}")

def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            next_url = request.GET.get('next', 'admin_dashboard')
            print(f"Authenticated user: {request.user.username}, is_staff: {request.user.is_staff}, redirecting to: {next_url}")
            if request.user.username == 'admin1' and 'manage-users' in next_url:
                return redirect('manage_users')
            return redirect(next_url)
        else:
            print(f"User {request.user.username} is not staff, redirecting to home")
            messages.error(request, "You do not have permission to access the admin dashboard.")
            return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user = User.objects.get(username=user.username)
            request.user = user
            if user.is_staff:
                next_url = request.POST.get('next', 'admin_dashboard')
                print(f"Logged in user: {user.username}, is_staff: {user.is_staff}, redirecting to: {next_url}")
                if user.username == 'admin1' and 'manage-users' in next_url:
                    return redirect('manage_users')
                return redirect(next_url)
            else:
                print(f"User {user.username} is not staff, redirecting to user_dashboard")
                messages.success(request, f"Welcome, {user.username}!")
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    
    next_url = request.GET.get('next', '')
    return render(request, 'login.html', {'next': next_url})
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
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        else:
            print("Form errors:", form.errors)  # Debug output
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

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


def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Email verified! You’re now logged in.")
        return redirect('home')
    else:
        messages.error(request, "Invalid verification link.")
        return redirect('signup')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_verification_email(user, request)
            messages.success(request, "Please check your email to verify your account.")
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
@login_required
def profile_view(request):
    form = None
    address = None
    cart_items = []
    orders = []

    if request.user.is_authenticated:
        # Try to get the user's address (OneToOne)
        address, created = Address.objects.get_or_create(user=request.user)

        if request.method == 'POST':
            form = AddressForm(request.POST, instance=address)
            if form.is_valid():
                form.save()
                return redirect('profile')
        else:
            form = AddressForm(instance=address)

        # Fetch cart items
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_items = CartItem.objects.filter(cart=cart)

        # Fetch orders
        orders = Order.objects.filter(user=request.user).order_by('-id')[:5]

    context = {
        'form': form,
        'address': address,
        'cart_items': cart_items,
        'orders': orders,
    }
    return render(request, 'profile.html', context)
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.address = request.POST.get('address', user.address)
        user.phone = request.POST.get('phone', user.phone)
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    return render(request, 'edit_profile.html')
def orders(request):
    return render(request, 'orders.html')

# shop/views.py
from django.shortcuts import render

@staff_member_required(login_url='login')
def manage_users(request):
    print(f"User authenticated: {request.user.is_authenticated}")
    print(f"User is staff: {request.user.is_staff}")
    print(f"User: {request.user.username if request.user.is_authenticated else 'Anonymous'}")

    # Debug: Print the User model being used
    print(f"User model in manage_users: {User}")
    users = User.objects.all()  # Should use shop.User via get_user_model()

    if request.method == 'POST':
        if 'make_staff' in request.POST:
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, id=user_id)
            user.is_staff = True
            user.save()
            messages.success(request, f"{user.username} is now a staff member!")
            return redirect('manage_users')
        elif 'remove_staff' in request.POST:
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, id=user_id)
            user.is_staff = False
            user.save()
            messages.success(request, f"{user.username} is no longer a staff member.")
            return redirect('manage_users')
        elif 'delete_user' in request.POST:
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, id=user_id)
            if user == request.user:
                messages.error(request, "You cannot delete your own account.")
            else:
                user.delete()
                messages.success(request, f"{user.username} has been deleted.")
            return redirect('manage_users')

    context = {
        'users': users,
    }
    return render(request, 'manage_users.html', context)

def set_address(request):
    user = request.user
    try:
        address = Address.objects.get(user=user)
    except Address.DoesNotExist:
        address = None

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            addr = form.save(commit=False)
            addr.user = user
            addr.save()
            return redirect('profile')  # or homepage or any other page
    else:
        form = AddressForm(instance=address)

    return render(request, 'set_address.html', {'form': form})

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Address

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_address_for_user(sender, instance, created, **kwargs):
    if created:
        Address.objects.create(user=instance)

@staff_member_required(login_url='login')
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        if username and email:
            user.username = username
            user.email = email
            user.save()
            messages.success(request, f"{user.username}'s details updated successfully!")
            return redirect('manage_users')
        else:
            messages.error(request, "Please fill in all fields.")
    context = {'user': user}
    return render(request, 'edit_user.html', context)
