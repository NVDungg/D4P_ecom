from django.urls import path
from .views import CartItemView, CartItemDeleteView, add_cart, RemoveCartItemView

urlpatterns = [
    path("", CartItemView.as_view(), name="cart_view"),
    path('add_cart/<int:product_id>/', add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', CartItemDeleteView.as_view(), name='delete_cart'),
    path('remove_cart_items/<int:product_id>/<int:cart_item_id>/', RemoveCartItemView.as_view(), name='remove_cart_item')
]
