from django.http import HttpResponseForbidden, StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from stream.models import Stream
import os


def media_access(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    protected_path = os.path.join(settings.MEDIA_ROOT, "protected")

    if os.path.commonpath([file_path, protected_path]) == protected_path:
        if "hls" in path and path.endswith(".m3u8"):
            stream_title = os.path.basename(os.path.dirname(file_path))
            stream = get_object_or_404(Stream, title=stream_title)
            if stream.authorization_required and not request.user.is_authenticated:
                return HttpResponseForbidden("Not authorized to access this media.")

    def file_iterator(file_path, chunk_size=8192):
        with open(file_path, "rb") as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    response = StreamingHttpResponse(
        file_iterator(file_path), content_type="application/octet-stream"
    )
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{os.path.basename(file_path)}"'
    return response
