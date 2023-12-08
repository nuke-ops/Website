from django.urls import re_path

from dice.consumers import DiceConsumer

websocket_urlpatterns = [
    re_path(r"dice/", DiceConsumer.as_asgi()),
]
