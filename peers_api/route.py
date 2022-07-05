from django.urls import path
from .consumers import WSConsume


ws_urlpatterns = [
               path("ws/cons", WSConsume.as_asgi())
               
               ]