from django.urls import path

from . import views

urlpatterns = [
    path("", views.product_create_view),
    path("all/", views.product_list_view),
    path("<int:pk>/update/", views.product_update_view),
    path("<int:pk>/delete/", views.product_delete_view),
    path("<int:pk>/", views.ProductDetailAPIView.as_view()),
    path("<int:pk>/addcomment/", views.addComment),
    path("<int:user_id>/<int:product_id>/deletecomment/",
         views.DeleteCommentView.as_view()),
    path("<int:user_id>/<int:product_id>/updatecomment/",
         views.UpdateCommentView.as_view())
]
