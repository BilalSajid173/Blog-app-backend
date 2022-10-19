from django.urls import path

from . import views

urlpatterns = [
    path("", views.product_create_view),
    path("all/", views.product_list_view),
    path("<int:pk>/update/", views.product_update_view),
    path("<int:pk>/delete/", views.product_delete_view),
    path("<int:pk>/", views.ProductDetailAPIView.as_view()),
    path("addcomment/", views.comment_create_view),
    path("deletecomment/<int:pk>/",
         views.comment_delete_view),
    path("updatecomment/<int:pk>/",
         views.comment_update_view),
    path("filter/", views.product_list),
]
