from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import StreamForm
from .models import Stream


def stream_list(request):
    streams = Stream.objects.all()
    return render(request, "stream/stream_list.html", {"streams": streams})


def stream_details(request, stream_id):
    stream = Stream.objects.get(pk=stream_id)
    return render(request, "stream/stream_details.html", {"stream": stream})


def create_stream(request):
    if request.method == "POST":
        form = StreamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("stream_list")
    else:
        form = StreamForm()

    return render(request, "stream/create_stream.html", {"form": form})
