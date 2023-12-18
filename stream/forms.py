from django import forms
from .models import Stream


class StreamForm(forms.ModelForm):
    class Meta:
        model = Stream
        fields = ["title", "rtmp_url"]

    def clean(self):
        cleaned_data = super().clean()
        rtmp_url = cleaned_data.get("rtmp_url")

        if not rtmp_url or not rtmp_url.startswith("rtmp://"):
            self.add_error(
                "rtmp_url", 'Enter a valid RTMP URL starting with "rtmp://".'
            )

        return cleaned_data
