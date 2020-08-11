from django.urls import path
from .views import DetailInfoView

urlpatterns = [
    path('/detail/<int:product_id>/detailinfo', DetailInfoView.as_view())
]

