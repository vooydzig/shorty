from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import random, string


# Create your models here.

class Url(models.Model):
    author = models.ForeignKey(User)
    original_url = models.URLField()
    short_url = models.URLField()

    def trim(self):
        short_url = self._get_random_string()
        while Url.objects.filter(short_url=short_url).count() > 0:
            short_url = self._get_random_string()
        self.short_url = short_url

    def _get_random_string(self):
        return ''.join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(settings.SHORTENED_URL_LENGTH)
        )
