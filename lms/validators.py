import re
from rest_framework import serializers


def validate_youtube_url(value):
    youtube_regex = re.compile(
        r'^(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+$'
    )
    if not youtube_regex.match(value):
        raise serializers.ValidationError("URL не принадлежит youtube.com")
    return value
