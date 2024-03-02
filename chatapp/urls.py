from django.urls import path,include
from chatapp.views import ResgisterView,OTPverificationView

urlpatterns = [
    
    path('register/',ResgisterView.as_view(),name='register'),
    path('otp/',OTPverificationView.as_view(),name='otp'),
]
