from django.urls import path, include
from .views import LoginView, UserRegistrationView, ProfileView, UserUpdateAPIView, GetProfileView
urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('editprofile/', UserUpdateAPIView.as_view(), name='editprofile'),
    path('getprofile/<int:pk>/', GetProfileView.as_view(), name='getprofile'),
]
