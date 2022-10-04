from django.urls import path

from . import views

urlpatterns = [
    path('addproduct', views.addProduct, name="add_product"),
    path('getallproducts/', views.getAllProducts, name="get_products"),
]
