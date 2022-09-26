from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'title',
            'content',
            'price',
            'sale_price',
            'my_discount'
        ]

    def get_my_discount(self, obj):
        # print(obj.id)
        # obj.user -> user.username
        # using the try and catch block because when we use the serializermodelfield with a modelserializer its assumed
        # that there is a instance attached to it, which is not usually the case (1:20 time stamp)
        try:
            return obj.get_discount()
        except:
            return None
