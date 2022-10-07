from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    # this is for changing the property name from get_discount to my_discount, look how it works
    # my_discount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        # fields can be fields, property or instance methods like getDiscount
        fields = [
            'user',
            'id',
            'title',
            'content',
            'created_at',
            'category',
            'imageId',
            'created_at',
            'commentCount',
            'likesCount'
        ]

    # def get_my_discount(self, obj):
        # this obj is the instance thats calling this serializer
        # print(obj.id)
        # obj.user -> user.username
        # using the try and catch block because when we use the serializermodelfield with a modelserializer its assumed
        # that there is a instance attached to it, which is not usually the case (1:20 time stamp)
        # try:
        # return obj.get_discount()
        # except:
        #     return None
