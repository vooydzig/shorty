from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.utils.six import StringIO
import mock


class CreateFakeUsersTest(TestCase):
    def setUp(self):
        self.out = StringIO()

    def call(self, count):
        call_command('create_fake_users', str(count), stdout=self.out)

    def test_raises_error_when_api_limit_is_exceeded(self):
        with self.assertRaises(CommandError):
            self.call(5001)  # randomuser.me limits request to 5000 entries

    def test_creating_multiple_users_results_in_one_api_call(self):
        fields = ['login', 'name', 'last_name', 'email', 'password', 'registered']
        with mock.patch('requests.get') as req_mock:
            self.call(2)
            req_mock.assert_called_once_with('http://api.randomuser.me/',
                                             params={'inc': ','.join(fields), 'results': 2})

    def test_users_are_created_in_bulk(self):
        self.assertEqual(User.objects.count(), 0)
        with mock.patch('requests.get') as req_mock:
            req_mock.return_value.json.return_value = {
                'results': [
                    {'email': 'lillie.miles@example.com',
                     'registered': 1219138883,
                     'name': {'last': 'miles', 'first': 'lillie', 'title': 'miss'},
                     'login': {'password': 'iiiiiiii', 'salt': '1NSVniMR',
                               'sha1': 'f7f51f300660fa8f5e5f7c204cbefd64229035c0', 'username': 'browncat809',
                               'sha256': 'b99ba7bd330a79173cf9087de5098d31be538e93302d15654d707bf68276cc92',
                               'md5': '213fac457a6a09c8784605556c89954f'}
                     }
                ]
            }
            self.call(1)
            self.assertEqual(User.objects.count(), 1)
