from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegisterSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model = User
        fields = ['email','first_name','last_name','username','password','password2','uuid']

        def validate(self,valid):
            password = valid.get('password')
            password2 = valid.get('password2')
            first_name = valid.get('first_name')
            last_name = valid.get('last_name')

            if first_name == last_name:
                raise serializers.ValidationError('first_name and last_name can\'t be same')
            if password != password2:
                raise serializers.ValidationError('password1 and password2 should be same')
            return valid
        

class OTPSerializer(serializers.Serializer):

    usr_otp=serializers.CharField(max_length=100)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        token["is_admin"] = user.is_admin
        # token["uuid"] = user.uuid
        return token
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = ['email', 'first_name', 'last_name', 'phone', 'image']

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone',instance.phone)
        instance.first_name=validated_data.get('first_name',instance.first_name)
        instance.last_name=validated_data.get('last_name',instance.last_name)
        instance.image = validated_data.get('image',instance.image)
        instance.save()
        return instance
    

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("old_password", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance

