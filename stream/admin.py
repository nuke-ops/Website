from django.contrib import admin
from .models import Stream


class StreamAdmin(admin.ModelAdmin):
    list_display = ["title", "rtmp_url", "authorization_required"]
    list_filter = ["authorization_required"]


admin.site.register(Stream, StreamAdmin)
