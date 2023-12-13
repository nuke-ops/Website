from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.shortcuts import get_object_or_404
import os
from stream.models import Stream


def media_access(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    protected_path = os.path.join(settings.MEDIA_ROOT, "protected")

    if os.path.commonpath([file_path, protected_path]) == protected_path:
        if "hls" in path and path.endswith(".m3u8"):
            stream_title = os.path.basename(file_path).split(".")[0]
            stream = get_object_or_404(Stream, title=stream_title)
            if stream.authorization_required:
                if not request.user.is_authenticated:
                    return HttpResponseForbidden("Not authorized to access this media.")

        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                response = HttpResponse(
                    file.read(), content_type="application/octet-stream"
                )
                response[
                    "Content-Disposition"
                ] = f'attachment; filename="{os.path.basename(file_path)}"'
                return response
        else:
            return HttpResponseForbidden("Requested media file does not exist.")
    else:
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                response = HttpResponse(
                    file.read(), content_type="application/octet-stream"
                )
                response[
                    "Content-Disposition"
                ] = f'attachment; filename="{os.path.basename(file_path)}"'
                return response
        else:
            return HttpResponseForbidden("Requested media file does not exist.")
