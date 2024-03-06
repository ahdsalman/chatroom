from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer,OTPSerializer,MyTokenObtainPairSerializer,UserProfileSerializer,ChangePasswordSerializer
from django.conf import settings
from .models import User
import random
import math
from chatapp.verify.smtp import send_otp
from datetime import datetime, timedelta
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

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
            otp = math.floor(random.randint(100000, 999999))
            print('otp',otp)
            expiration_time = datetime.now() + timedelta(minutes=1)
            request.session['email']=user.email
            request.session['otp']=otp
            subject = 'Your otp for email verification'
            message = f'your OTP is:{otp}'

            sender = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_otp(subject,message,sender,recipient_list)

            user_uuid = user.uuid
            response_data = serializer.data
            response_data['uuid']=user_uuid
            return Response(response_data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class OTPverificationView(APIView):
    def post(self,request,**kwags):

        serializer = OTPSerializer(data= request.data)
        if serializer.is_valid():
            usr_otp = serializer.validated_data.get('usr_otp')

            user_email = request.session.get('email')
            otp = request.session.get('otp')
            try :
                user=User.objects.get(email=user_email)
                if user.is_active:
                    if int(usr_otp) == int(otp):
                        return Response({'msg':'Registeration successful'},status=status.HTTP_200_OK)
                    return Response({'Msg':'Invalid otp'},status=status.HTTP_400_BAD_REQUEST)
                return Response({'Msg':'User is blocked'},status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                return Response({'Msg':f'User not found{e}'},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer




class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = self.request.user
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        except Exception as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
    def patch(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ChangePasswordView(APIView):
    serializer = ChangePasswordSerializer 
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data["old_password"]
        password = serializer.validated_data["password"]

        if not request.user.check_password(old_password):
            return Response(
                {"detail": "Old password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.user.set_password(password)
        request.user.save()
        return Response(
            {"detail": "Password changed successfully."}, status=status.HTTP_200_OK
        )


