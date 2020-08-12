from django.urls import path
from .views import DetailInfoView

urlpatterns = [
#    path('/detail/<int:product_id>', ProductDetailView.as_view()),
#    path('/detail/<int:product_id>/pairwith', PairWithView.as_view()),
    path('/detail/<int:product_id>/detailinfo', DetailInfoView.as_view())
]

