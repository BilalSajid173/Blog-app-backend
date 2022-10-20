from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
# from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
# from rest_framework.permissions import IsAuthenticated
# from .utils import get_tokens_for_user
# from .serializers import RegistrationSerializer, PasswordChangeSerializer

from account.serializers import UserProfileSerializer, UserRegistrationSerializer, LoginSerializer, UserFollowingSerializer
from .models import User, UserFollowing
from products.models import Product, Comment
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView

# from rest_framework_simplejwt.tokens import RefreshToken


# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)

#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }

class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"msg": "Reg successful", "serializer_data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserLoginView(APIView):
#     def post(self, request, format=None):
#         serializer = LoginSerializerWithToken(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             print(serializer.data)
#             email = serializer.data.get('email')
#             password = serializer.data.get('password')
#             print(email, password)
#             user = authenticate(request, email=email, password=password)
#             print(user)
#             if user is not None:
#                 return Response({"msg": "login success", "data": serializer.data})
#             else:
#                 return Response({"msg": "error"})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.data['email']
        password = request.data['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            serializer = LoginSerializer(user)
            # if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Login Success', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, many=False)
        # if serializer.is_valid(raise_exception=True):
        return Response({"User": serializer.data})


class GetProfileView(APIView):

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"msg": "No user with this id"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(user, many=False)
        return Response({"msg": "Update Successful", "serializer_data": serializer.data}, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserFollowingView(generics.CreateAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserFollowingSerializer
    queryset = UserFollowing.objects.all()

    def post(self, request, *args, **kwargs):
        print(request.user)
        print(request.data.get('user_id'))
        try:
            queryset = User.objects.get(pk=request.data.get('user_id'))
        except ObjectDoesNotExist:
            return Response({"msg": "No user with this id"}, status=status.HTTP_404_NOT_FOUND)
        print(queryset)
        # serializer = self.get_serializer(data=request.data)
        if request.user != queryset:
            return Response({"msg": "Forbidden"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            self.create(request, *args, **kwargs)
            return Response({"msg": "Success"}, status=status.HTTP_200_OK)


class RemoveUserFollowingView(generics.DestroyAPIView):
    queryset = UserFollowing.objects.all()
    serializer_class = UserFollowingSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_fields = ('user_id', 'following_user_id')

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, *args, **kwargs):
        print(request.user)
        try:
            queryset = User.objects.get(pk=kwargs['user_id'])
        except ObjectDoesNotExist:
            return Response({"msg": "No user with this id"}, status=status.HTTP_404_NOT_FOUND)
        print(queryset)
        # serializer = self.get_serializer(data=request.data)
        if request.user != queryset:
            return Response({"msg": "Forbidden"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            self.destroy(request, *args, **kwargs)
            return Response({"msg": "Success"}, status=status.HTTP_200_OK)


# prevent more than one like and dislike here, same for save
class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        try:
            post = Product.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"msg": "No user with this id"}, status=status.HTTP_404_NOT_FOUND)
        user.likedPosts.add(post)
        user.save()
        post.likesCount += 1
        post.save()
        return Response({"msg": "Like Success"}, status=status.HTTP_200_OK)


class LikeCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        try:
            comment = Comment.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"msg": "No comment with this id"}, status=status.HTTP_404_NOT_FOUND)
        user.likedComments.add(comment)
        comment.likesCount += 1
        print(request.data)
        if request.data.get("unlike"):
            comment.dislikesCount -= 1
            user.dislikedComments.remove(comment)
        user.save()
        comment.save()
        return Response({"msg": "Like Success"}, status=status.HTTP_200_OK)


class UnLikeCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        try:
            comment = Comment.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"msg": "No comment with this id"}, status=status.HTTP_404_NOT_FOUND)
        user.dislikedComments.add(comment)
        comment.dislikesCount += 1
        print(request.data)
        if request.data.get("like"):
            comment.likesCount -= 1
            user.likedComments.remove(comment)
        user.save()
        comment.save()
        return Response({"msg": "Unlike Success"}, status=status.HTTP_200_OK)


class RemoveLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        try:
            comment = Comment.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"msg": "No comment with this id"}, status=status.HTTP_404_NOT_FOUND)
        user.likedComments.remove(comment)
        comment.likesCount -= 1
        user.save()
        comment.save()
        return Response({"msg": "Remove Like Success"}, status=status.HTTP_200_OK)


class RemoveUnLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        try:
            comment = Comment.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"msg": "No comment with this id"}, status=status.HTTP_404_NOT_FOUND)
        user.dislikedComments.remove(comment)
        comment.dislikesCount -= 1
        user.save()
        comment.save()
        return Response({"msg": "Remove dislike Success"}, status=status.HTTP_200_OK)


class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        try:
            post = Product.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"msg": "No user with this id"}, status=status.HTTP_404_NOT_FOUND)
        user.likedPosts.remove(post)
        user.save()
        post.likesCount -= 1
        post.save()
        return Response({"msg": "unlike Success"}, status=status.HTTP_200_OK)


class SavePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        try:
            post = Product.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"msg": "No user with this id"}, status=status.HTTP_404_NOT_FOUND)
        user.savedPosts.add(post)
        user.save()
        return Response({"msg": "Success"}, status=status.HTTP_200_OK)


class UnSavePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        try:
            post = Product.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"msg": "No user with this id"}, status=status.HTTP_404_NOT_FOUND)
        user.savedPosts.remove(post)
        user.save()
        return Response({"msg": "Success"}, status=status.HTTP_200_OK)
