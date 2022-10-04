from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import ProductSerializer

# Create your views here.


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = "pk"

# can also do like this then use product_detail_view inside urlpatterns
# product_detail_view = ProductDetailAPIView.as_view()


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # we can use this function on Createapiview to add additional data to the product
    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        # print(serializer) for whole serializer
        # playing around with it
        print(serializer.validated_data)  # only for data
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = serializer.validated_data.get('title')
        serializer.save(content=content)


product_list_create_view = ProductListCreateAPIView.as_view()


# class ProductListAPIView(generics.ListAPIView):
#     # not gonna use this method because we can just use the productlistcreateapiview
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
# lookup_field = "pk"


# function based view for create, list and detail views
# to test these, replace the functon in url with views.product_alt_view
@api_view(["GET", "POST"])
def product_alt_view(request, pk=None):
    method = request.method
    if method == "GET":
        if pk is not None:
            # m-1
            # queryset = Product.objects.filter(pk=pk)
            # if not queryset.exists()
            # raise Http404
            # m-2
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        # url args??
        # get request -> detail view
        # list view
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)
    if method == "POST":
        serializer = ProductSerializer(data=request.data)
        # raise exception will catch an invalid error and throw it.
        if serializer.is_valid(raise_exception=True):
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = serializer.validated_data.get('title')
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({"Error": "Not good"}, status=400)
