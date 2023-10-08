import re

from rest_framework.serializers import ValidationError


class UrlValidator:
    """Валидатор на проверку ссылки на урок"""
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        youtube_pattern = re.compile(r'^https:\/\/www\.youtube\.com\/')
        tmp_value = dict(value).get(self.field)
        if not bool(youtube_pattern.match(tmp_value)):
            raise ValidationError('Ссылка на видео должна быть с YouTube.')

