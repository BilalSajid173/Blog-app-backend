from rest_framework import serializers
from account.models import User
from rest_framework_simplejwt.tokens import RefreshToken


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


class LoginSerializer(serializers.ModelSerializer):
    # _id = serializers.SerializerMethodField(read_only=True)
    # email = serializers.EmailField(max_length=255)
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'address', 'education', 'token', 'about']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    # def get__id(self, obj):
    #     return obj.id
