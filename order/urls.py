from django.urls import path
from .views import CartItemView, RecommendItemView, QuantityView

urlpatterns = [
    path('/cart', CartItemView.as_view()),
    path('/cart/recommend', RecommendItemView.as_view()),
    path('/cart/quantity', QuantityView.as_view())
]
