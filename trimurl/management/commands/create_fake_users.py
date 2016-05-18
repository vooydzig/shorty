import requests
from datetime import datetime

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Populates user pool with data from randomuser.me'
    _fields = ['login', 'name', 'last_name', 'email', 'password', 'registered']

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        count = options['count']
        if count > 5000:
            raise CommandError('You can create up to 5000 users at once')
        user_data = requests.get('http://api.randomuser.me/',
                                 params={'results': count, 'inc': ','.join(self._fields)})

        User.objects.bulk_create([
             User(
                 username=user['login']['username'],
                 first_name=user['name']['first'],
                 last_name=user['name']['last'],
                 email=user['email'],
                 password=user['login']['password'],
                 date_joined=timezone.make_aware(datetime.utcfromtimestamp(user['registered'])),
             ) for user in user_data.json().get('results', [])
        ])
        self.stdout.write(self.style.SUCCESS('Created %d users' % options['count']))
