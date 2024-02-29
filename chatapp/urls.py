from django.urls import path,include
from chatapp.views import ResgisterView

urlpatterns = [
    
    path('register/',ResgisterView.as_view(),name='register'),
]
