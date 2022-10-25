from rest_framework import serializers
from yaml import serialize
from account.models import User, UserFollowing
from rest_framework_simplejwt.tokens import RefreshToken
from products.models import Product, Comment
from products.serializers import ProductSerializer, CommentSerializer


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }

    # registration works even without the below create thing, error is also throw automatically for duplicate email
    # def create(self, validated_data):
    #     return User.objects.create(**validated_data)
    def save(self):
        # add all the fields that need to be inserted inside User()
        user = User(
            email=self.validated_data['email'], name=self.validated_data['name'])
        password = self.validated_data['password']
        # if password != password2:
        #     raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class LoginSerializer(serializers.ModelSerializer):
    # _id = serializers.SerializerMethodField(read_only=True)
    # email = serializers.EmailField(max_length=255)
    products = serializers.SerializerMethodField(read_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    likedPosts = serializers.SerializerMethodField()
    savedPosts = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    likedComments = serializers.SerializerMethodField()
    dislikedComments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    # def get__id(self, obj):
    #     return obj.id

    def get_products(self, obj):
        products = obj.product_set.all()
        serializer = ProductSerializer(products, many=True)
        return serializer.data

    def get_comments(self, obj):
        comments = obj.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    def get_following(self, obj):
        return FollowingSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj):
        return FollowersSerializer(obj.followers.all(), many=True).data

    def get_likedPosts(self, obj):
        return ProductSerializer(obj.likedPosts.all(), many=True).data

    def get_savedPosts(self, obj):
        return ProductSerializer(obj.savedPosts.all(), many=True).data

    def get_likedComments(self, obj):
        return CommentSerializer(obj.likedComments.all(), many=True).data

    def get_dislikedComments(self, obj):
        return CommentSerializer(obj.dislikedComments.all(), many=True).data


class UserProfileSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(read_only=True)
    password = serializers.CharField(
        max_length=128,
        write_only=True
    )
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    likedPosts = serializers.SerializerMethodField()
    savedPosts = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    likedComments = serializers.SerializerMethodField()
    dislikedComments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_products(self, obj):
        products = obj.product_set.all()
        serializer = ProductSerializer(products, many=True)
        return serializer.data

    def get_comments(self, obj):
        comments = obj.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def get_following(self, obj):
        return FollowingSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj):
        return FollowersSerializer(obj.followers.all(), many=True).data

    def get_likedPosts(self, obj):
        return ProductSerializer(obj.likedPosts.all(), many=True).data

    def get_savedPosts(self, obj):
        return ProductSerializer(obj.savedPosts.all(), many=True).data

    def get_likedComments(self, obj):
        return CommentSerializer(obj.likedComments.all(), many=True).data

    def get_dislikedComments(self, obj):
        return CommentSerializer(obj.dislikedComments.all(), many=True).data


class UserDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("name", "profilePic", "email")


class FollowingSerializer(serializers.ModelSerializer):

    userData = serializers.SerializerMethodField()

    class Meta:
        model = UserFollowing
        fields = ("id", "following_user_id", "created", "userData")

    def get_userData(self, obj):
        user = User.objects.get(pk=obj.following_user_id_id)
        serializer = UserDataSerializer(
            user, many=False)
        return serializer.data


class FollowersSerializer(serializers.ModelSerializer):

    userData = serializers.SerializerMethodField()

    class Meta:
        model = UserFollowing
        fields = ("id", "user_id", "created", "userData")

    def get_userData(self, obj):
        user = User.objects.get(pk=obj.user_id_id)
        serializer = UserDataSerializer(
            user, many=False)
        return serializer.data


class UserFollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFollowing
        fields = ("id", "following_user_id", "user_id", "created")
