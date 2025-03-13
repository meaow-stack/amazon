import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from shop.models import Cart, CartItem, Product
from django.db import models

def get_recommendations(user_id, num_recommendations=5):
    cart_items = CartItem.objects.select_related('cart__user', 'product').all()
    data = [{'user_id': item.cart.user.id, 'product_id': item.product.id, 'interaction': item.quantity} for item in cart_items]
    df = pd.DataFrame(data)
    if df.empty:
        popular_products = CartItem.objects.values('product_id').annotate(total_quantity=models.Sum('quantity')).order_by('-total_quantity')[:num_recommendations]
        return Product.objects.filter(id__in=[p['product_id'] for p in popular_products])
    user_item_matrix = df.pivot_table(index='user_id', columns='product_id', values='interaction', fill_value=0)
    user_similarity = cosine_similarity(user_item_matrix)
    user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)
    if user_id not in user_item_matrix.index:
        popular_products = CartItem.objects.values('product_id').annotate(total_quantity=models.Sum('quantity')).order_by('-total_quantity')[:num_recommendations]
        return Product.objects.filter(id__in=[p['product_id'] for p in popular_products])
    similar_users = user_similarity_df[user_id].sort_values(ascending=False)[1:]
    similar_users_ids = similar_users.index[:5]
    recommended_product_ids = user_item_matrix.loc[similar_users_ids].sum().sort_values(ascending=False).index
    user_products = set(user_item_matrix.loc[user_id][user_item_matrix.loc[user_id] > 0].index)
    recommendations = [pid for pid in recommended_product_ids if pid not in user_products][:num_recommendations]
    return Product.objects.filter(id__in=recommendations)