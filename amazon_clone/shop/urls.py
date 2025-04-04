from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('personalized/', views.personalized_products, name='personalized_products'),  # New URL
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('cart/', views.cart, name='cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # ✅ Add this
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('delete_cart_item/<int:cart_item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('search/', views.search, name='search'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('about/', views.about, name='about'),  # New
    path('contact/', views.contact, name='contact'),
    path('terms/', views.terms, name='terms'),  # New
    path('signup/', views.signup, name='signup'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html'), name='change_password'),
    path('admin/orders/', views.orders, name='orders'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('set-address/', views.set_address, name='set_address'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),  # 🔥 Add this line
    #path('profile/', views.profile, name='profile'),
]
