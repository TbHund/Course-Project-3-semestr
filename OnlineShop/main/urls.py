from .views import CatalogView, ClothingItemDetailView
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
    path('item/<slug:slug>/', ClothingItemDetailView.as_view(), name='clothing_item_detail'),
    path('seria/', views.all_products_serialized, name='products_serialized')
]