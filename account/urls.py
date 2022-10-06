from django.urls import path, include
from .views import LoginView, UserRegistrationView
urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name='login'),
]
