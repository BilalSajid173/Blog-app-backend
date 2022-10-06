from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
# from rest_framework.permissions import IsAuthenticated
# from .utils import get_tokens_for_user
# from .serializers import RegistrationSerializer, PasswordChangeSerializer

from account.serializers import UserRegistrationSerializer, LoginSerializer
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView

# from rest_framework_simplejwt.tokens import RefreshToken


# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)

#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }


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
