from django.urls import path
from .views import LoginView, UserRegistrationView, ProfileView, UserUpdateAPIView, GetProfileView, UserFollowingView, RemoveUserFollowingView, LikePostView, UnlikePostView, SavePostView, UnSavePostView, UserListAPIView, LikeCommentView, UnLikeCommentView, RemoveLikeView, RemoveUnLikeView, ChangePasswordView, GetFollowingView, GetFollowersView
urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name='login'),
    path('all/', UserListAPIView.as_view(), name="allusers"),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('editprofile/', UserUpdateAPIView.as_view(), name='editprofile'),
    path('getprofile/<int:pk>/', GetProfileView.as_view(), name='getprofile'),
    path('addfollowers/', UserFollowingView.as_view(), name="addfollowers"),
    path('removefollowers/<int:user_id>/<int:following_user_id>/',
         RemoveUserFollowingView.as_view(),
         name="removefollowers"),
    path('likepost/<int:pk>/', LikePostView.as_view(), name="likepost"),
    path('unlikepost/<int:pk>/', UnlikePostView.as_view(), name="unlikepost"),
    path('savepost/<int:pk>/', SavePostView.as_view(), name="savepost"),
    path('unsavepost/<int:pk>/', UnSavePostView.as_view(), name="unsavepost"),
    path('likecomment/<int:pk>/', LikeCommentView.as_view(), name="likecomment"),
    path('removelikecomment/<int:pk>/',
         RemoveLikeView.as_view(), name="removelikecomment"),
    path('unlikecomment/<int:pk>/',
         UnLikeCommentView.as_view(), name="unlikecomment"),
    path('removeunlikecomment/<int:pk>/',
         RemoveUnLikeView.as_view(), name="removeunlikecomment"),
    path("changepassword/", ChangePasswordView.as_view(), name="changepassword"),
    path("getfollowing/<int:user_id>/", GetFollowingView.as_view(), name="following"),
    path("getfollowers/<int:following_user_id>/", GetFollowersView.as_view(), name="followers")
]
