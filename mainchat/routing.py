from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from mainchat.consumer import ChatConsumer
websocket_urlpatterns = [
    re_path(r'^ws/(?P<room_name>[^/]+)/$', ChatConsumer.as_asgi()),
   
]
# the websocket will open at 127.0.0.1:8000/ws/<room_name>
application = ProtocolTypeRouter({
    'websocket':
        URLRouter(
            websocket_urlpatterns
        )
    ,
})