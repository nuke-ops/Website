from django.urls import path
from .views import stream_list, stream_create, stream_watch

urlpatterns = [
    path("stream/", stream_list, name="stream_list"),
    path("stream/create", stream_create, name="stream_create"),
    path("stream/<int:stream_id>/", stream_watch, name="stream_watch"),
]
