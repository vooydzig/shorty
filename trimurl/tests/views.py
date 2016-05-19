import mock
from django.contrib.auth.models import User
from django.test import TestCase

from trimurl.models import Url


class TrimUrlTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com')
        self.user.save()

    def test_index_displays_form(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')

    def test_short_url_must_be_unique(self):
        with mock.patch('trimurl.models.Url._get_random_string') as ranom_mock:
            ranom_mock.side_effect = ['TEST', 'TEST', 'TEST2']
            self.client.post('/', data={'url': 'http://www.test1.com'})
            self.client.post('/', data={'url': 'http://www.test2.com'})
            self.assertEqual(ranom_mock.call_count, 3)
        self.assertEqual(Url.objects.first().short_url, 'TEST')
        self.assertEqual(Url.objects.last().short_url, 'TEST2')

    def test_adding_new_url_redirects_to_short_url_detail(self):
        self.assertEqual(Url.objects.count(), 0)
        response = self.client.post('/', data={'url': 'http://www.test.com'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/!'))
        self.assertEqual(Url.objects.count(), 1)

    def test_adding_existing_url_redirects_to_short_url_detail(self):
        self.client.post('/', data={'url': 'http://www.test.com'})
        pre_url = Url.objects.first()
        self.client.post('/', data={'url': 'http://www.test.com'})
        post_url = Url.objects.first()
        self.assertEqual(pre_url.original_url, post_url.original_url)
        self.assertEqual(pre_url.short_url, post_url.short_url)
        self.assertEqual(pre_url.author, post_url.author)

    def test_accessing_non_exising_url_returns_404(self):
        response = self.client.get('/nonexistingurl')
        self.assertEqual(response.status_code, 404)

    def test_accessing_exising_url_redirects_to_original_url(self):
        self.client.post('/', data={'url': 'http://www.test.com'})
        url = Url.objects.first()
        response = self.client.get('/%s' % url.short_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://www.test.com')

    def test_accesing_short_url_with_exclamation_point_gives_url_details(self):
        self.client.post('/', data={'url': 'http://www.test.com'})
        url = Url.objects.first()
        response = self.client.get('/!%s' % url.short_url)
        self.assertTemplateUsed(response, 'details.html')
