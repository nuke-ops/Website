from django.db import models


class Stream(models.Model):
    title = models.CharField(max_length=255)
    rtmp_url = models.CharField(max_length=255)
    authorization_required = models.BooleanField(default=False)

    def __str__(self):
        return self.title
