from rest_framework import serializers

from .models import Product, Comment


class ProductSerializer(serializers.ModelSerializer):
    # this is for changing the property name from get_discount to my_discount, look how it works
    # my_discount = serializers.SerializerMethodField(read_only=True)

    comments = serializers.SerializerMethodField(read_only=True)
    commentCount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        # fields can be fields, property or instance methods like getDiscount
        fields = '__all__'

    def get_comments(self, obj):
        comments = obj.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    def get_commentCount(self, obj):
        comments = obj.comment_set.all()
        return len(comments)
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


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
