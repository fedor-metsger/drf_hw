
import re

from rest_framework import serializers


class VideoValidator():

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        pattern = re.compile("^https://youtu.be/")
        video = dict(value).get(self.field)
        if video and not pattern.match(video.lower()):
            raise serializers.ValidationError("Можно размещать только ссылки на YouTube.")
