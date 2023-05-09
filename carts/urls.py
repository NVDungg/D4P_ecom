from django.urls import path
from .views import ItemCartView, add_cart

urlpatterns = [
    path("", ItemCartView.as_view(), name="cart_view"),
    path('add_cart/<int:product_id>/', add_cart, name='add_cart'),
]
