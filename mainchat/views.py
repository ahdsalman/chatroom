from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from mainchat.models import Chating 
from mainchat.serializer import ChatSerializer

class MessageList(generics.ListCreateAPIView):
    queryset = Chating.objects.all()
    serializer_class = ChatSerializer
    ordering = ('-timestamp',)