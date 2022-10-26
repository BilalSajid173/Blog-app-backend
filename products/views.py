from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from .models import Product, Comment
from account.models import User
from .serializers import ProductSerializer, CommentSerializer
from account.serializers import UserProfileSerializer
# from .permissions import IsStaffEditorPermission

# Create your views here.


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = "pk"

# can also do like this then use product_detail_view inside urlpatterns
# product_detail_view = ProductDetailAPIView.as_view()


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # authentication_classes = [authentication.SessionAuthentication]
    # parser_classes = [permissions.IsAuthenticated] -->with this the user can do anything just by being authenticated
    # with the django model permissions the user can only do what is defined in the admin panel for the user
    permission_classes = [permissions.IsAuthenticated]

    # we can use this function on Createapiview to add additional data to the product
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # print(serializer) for whole serializer
        # playing around with it
        print(serializer.validated_data)  # only for data
        # content = serializer.validated_data.get('content') or None
        # if content is None:
        #     content = serializer.validated_data.get('title')
        # serializer.save(content=content)


product_create_view = ProductCreateAPIView.as_view()


class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        # print(request.user)
        try:
            queryset = Product.objects.get(pk=kwargs['pk']).user
        except ObjectDoesNotExist:
            return Response({"msg": "No post with this id"}, status=status.HTTP_404_NOT_FOUND)
        # print(queryset)
        # serializer = self.get_serializer(data=request.data)
        if request.user != queryset:
            return Response({"msg": "Forbidden"})
        return self.update(request, *args, **kwargs)
        # if serializer.is_valid(raise_exception=True):
        # serializer.save()
        # return Response({"msg": "haha"})
        # self.perform_update(serializer)
        # print(self.kwargs['pk'])
        # if not instance.content:
        #     instance.content = instance.title


product_update_view = ProductUpdateAPIView.as_view()


class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        print(request.user)
        try:
            queryset = Product.objects.get(pk=kwargs['pk']).user
        except ObjectDoesNotExist:
            return Response({"msg": "No post with this id"}, status=status.HTTP_404_NOT_FOUND)
        print(queryset)
        # serializer = self.get_serializer(data=request.data)
        if request.user != queryset:
            return Response({"msg": "Forbidden"})
        else:
            self.destroy(request, *args, **kwargs)
            return Response({"msg": "Success"})


product_delete_view = ProductDestroyAPIView.as_view()


class ProductListAPIView(generics.ListAPIView):
    # not gonna use this method because we can just use the productlistcreateapiview
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = "pk"


product_list_view = ProductListAPIView.as_view()


@api_view(['GET'])
def search_list(request):
    qs = Product.objects.all()
    tag = request.query_params.get('search')  # Get query parameter
    print(request.query_params)
    qs = qs.filter(Q(title__icontains=tag) | Q(
        tags__icontains=tag) | Q(category__icontains=tag))
    postsserializer = ProductSerializer(qs, many=True)
    qs = User.objects.all()
    qs = qs.filter(Q(name__icontains=tag) | Q(
        email__icontains=tag) | Q(address__icontains=tag))
    userserializer = UserProfileSerializer(qs, many=True)
    return Response({"posts": postsserializer.data, "users": userserializer.data})


@api_view(['GET'])
def product_list(request):
    qs = Product.objects.all()
    y = len(qs)
    tag = request.query_params.get('tag')  # Get query parameter
    page = int(request.query_params.get("page"))
    sort = request.query_params.get("sort")
    print(request.query_params)
    if tag is not None:
        qs = qs.filter(tags__icontains=tag)
        y = len(qs)
        print(qs)
    if sort == "latest":
        print("h")
        qs = qs.order_by("-created_at")
    else:
        qs = qs.order_by("-likesCount", "-commentCount")
    x = len(qs)
    if (page*10) <= x:
        qs = qs[(page-1)*10:page*10]
    else:
        qs = qs[(page-1)*10:]
    serializer = ProductSerializer(qs, many=True)
    return Response({"data": serializer.data, "totalPosts": y})


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        print(serializer.validated_data)


comment_create_view = CommentCreateAPIView.as_view()


class CommentUpdateAPIView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        try:
            queryset = Comment.objects.get(pk=kwargs['pk']).user
        except ObjectDoesNotExist:
            return Response({"msg": "No comment with this id"}, status=status.HTTP_404_NOT_FOUND)
        if request.user != queryset:
            return Response({"msg": "Forbidden"})
        return self.update(request, *args, **kwargs)


comment_update_view = CommentUpdateAPIView.as_view()


class CommentDestroyAPIView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        print(request.user)
        try:
            queryset = Comment.objects.get(pk=kwargs['pk']).user
        except ObjectDoesNotExist:
            return Response({"msg": "No post with this id"}, status=status.HTTP_404_NOT_FOUND)
        if request.user != queryset:
            return Response({"msg": "Forbidden"})
        else:
            self.destroy(request, *args, **kwargs)
            return Response({"msg": "Success"})


comment_delete_view = CommentDestroyAPIView.as_view()


class CommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    # lookup_field = "pk"
    lookup_url_kwarg = "product_id"

    def get_queryset(self):
        product_id = self.kwargs.get(self.lookup_url_kwarg)
        comments = Comment.objects.filter(product_id=product_id)
        return comments


comment_list_view = CommentListAPIView.as_view()


# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def addComment(request, pk):
#     user = request.user
#     product = Product.objects.get(pk=pk)
#     data = request.data

#     # 1 - Review already exists
#     alreadyExists = product.comment_set.filter(user=user).exists()
#     if alreadyExists:
#         content = {'detail': 'Product already reviewed'}
#         return Response(content, status=status.HTTP_400_BAD_REQUEST)

#     comment = Comment.objects.create(
#         user=user,
#         product=product,
#         name=user.name,
#         comment=data['comment']
#     )
#     return Response('Review Added')


# Skipped Product mixins part, look at it later

# function based view for create, list and detail views
# to test these, replace the functon in url with views.product_alt_view


# @api_view(["GET", "POST"])
# def product_alt_view(request, pk=None):
#     method = request.method
#     if method == "GET":
#         if pk is not None:
#             # m-1
#             # queryset = Product.objects.filter(pk=pk)
#             # if not queryset.exists()
#             # raise Http404
#             # m-2
#             obj = get_object_or_404(Product, pk=pk)
#             data = ProductSerializer(obj, many=False).data
#             return Response(data)
#         # url args??
#         # get request -> detail view
#         # list view
#         queryset = Product.objects.all()
#         data = ProductSerializer(queryset, many=True).data
#         return Response(data)
#     if method == "POST":
#         serializer = ProductSerializer(data=request.data)
#         # raise exception will catch an invalid error and throw it.
#         if serializer.is_valid(raise_exception=True):
#             content = serializer.validated_data.get('content') or None
#             if content is None:
#                 content = serializer.validated_data.get('title')
#             serializer.save(content=content)
#             return Response(serializer.data)
#         return Response({"Error": "Not good"}, status=400)
