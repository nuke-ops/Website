# Generated by Django 5.0 on 2023-12-13 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0002_alter_stream_rtmp_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='authorization_required',
            field=models.BooleanField(default=False),
        ),
    ]
