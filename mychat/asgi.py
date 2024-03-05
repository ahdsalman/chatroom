"""
ASGI config for mychat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mychat.settings')

application = get_asgi_application()


 
import os 
  
from channels.auth import AuthMiddlewareStack 
from channels.routing import ProtocolTypeRouter, URLRouter 
from django.core.asgi import get_asgi_application 
import mainchat.routing 
  
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sampleProject.settings") 
  
application = ProtocolTypeRouter({ 
  "http": get_asgi_application(), 
  "websocket": AuthMiddlewareStack( 
        URLRouter( 
            mainchat.routing.websocket_urlpatterns 
        ) 
    ), 
}) 