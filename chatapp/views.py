from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer
from .models import User
# Create your views here.
class ResgisterView(APIView):
    def post(self,request,**kwags):

        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.create_user(
                email= serializer.validated_data.get('email'),
                first_name= serializer.validated_data.get('first_name'),
                last_name= serializer.validated_data.get('last_name'),
                username= serializer.validated_data.get('username'),
                password= serializer.validated_data.get('password'),

            )
            return Response(serializer.data)
        return Response(serializer.errors)