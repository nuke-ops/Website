from django.urls import path
from .views import stream_list, create_stream, stream_details

urlpatterns = [
    path("stream/", stream_list, name="stream_list"),
    path("stream/create", create_stream, name="create_stream"),
    path("stream/<int:stream_id>/", stream_details, name="stream_detail"),
]
