from django.test import TestCase
from django.urls import reverse


class ExceptionHandlerTestCase(TestCase):
    @staticmethod
    def get_url():
        return reverse('user:login')

    def test_structure_is_applied(self):
        url = self.get_url()

        response = self.client.get(url)

        self.assertIn('errors', response.data)

        self.assertIn('message', response.data['errors'])
        self.assertIn('fields', response.data['errors'])

    def test_structure_returns_fields(self):
        url = self.get_url()

        response = self.client.post(url)

        self.assertIn('email', response.data['errors']['fields'])
        self.assertIn('password', response.data['errors']['fields'])
