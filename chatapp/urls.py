from django.urls import path,include
from chatapp.views import ResgisterView,OTPverificationView,MyObtainTokenPairView,UserProfileView,ChangePasswordView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    
    path('register/',ResgisterView.as_view(),name='register'),
    path('otp/',OTPverificationView.as_view(),name='otp'),
    path('login/',MyObtainTokenPairView.as_view(),name='login'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("userprofile/", UserProfileView.as_view(), name="userprofile"),
    path("changepassword/", ChangePasswordView.as_view(), name="changepassword"),


]
