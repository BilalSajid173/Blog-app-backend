from django.urls import path
from .views import LoginView, UserRegistrationView, ProfileView, UserUpdateAPIView, GetProfileView, UserFollowingView, RemoveUserFollowingView
urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('editprofile/', UserUpdateAPIView.as_view(), name='editprofile'),
    path('getprofile/<int:pk>/', GetProfileView.as_view(), name='getprofile'),
    path('addfollowers/', UserFollowingView.as_view(), name="addfollowers"),
    path('removefollowers/<int:user_id>/<int:following_user_id>/',
         RemoveUserFollowingView.as_view(),
         name="removefollowers")
]
