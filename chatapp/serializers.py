from rest_framework import serializers
from .models import User


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