from django.urls import path
from .views import ProductListView, ProductDetailView, search, submit_review

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("category/<slug:category_slug>/", ProductListView.as_view(), name="product_category"),
    path("category/<slug:category_slug>/<slug:product_slug>/", ProductDetailView.as_view(), name="product_detail"),
    path("search/", search, name='search'),
    path("submit_review/<int:product_id>/", submit_review, name='submit_review'),
]
