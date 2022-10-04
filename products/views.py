from rest_framework import generics

from .models import Product
from .serializers import ProductSerializer

# Create your views here.


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = "pk"

# can also do like this then use product_detail_view inside urlpatterns
#product_detail_view = ProductDetailAPIView.as_view()


class ProductCreateAPIView(generics.CreateAPIView):
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


product_create_view = ProductCreateAPIView.as_view()
