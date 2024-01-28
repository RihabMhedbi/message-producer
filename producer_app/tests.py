import base64

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework_api_key.models import APIKey

from producer_app.models import Message


class ProducerAPITests(TestCase):
    def setUp(self):
        self.username = 'test_user'
        self.password = 'test_password'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        _, self.api_key = APIKey.objects.create_key(name='webhook')

    def test_message_creation(self):
        url = '/messages/'
        client = Client()
        basic_auth = 'Basic ' + base64.b64encode(f"{self.username}:{self.password}".encode()).decode('utf-8')
        data = {'text': 'Test message'}
        response = client.post(url, data, format='json', HTTP_AUTHORIZATION=basic_auth)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Message.objects.count(), 1)

    def test_webhook_receiver_view(self):
        client = Client()
        api_key_auth = 'Api-Key ' + self.api_key

        message = Message.objects.create(text='Test message')

        webhook_url = reverse('webhook_receiver', kwargs={'message_id': message.id})
        data = {'result': 'Processed message result'}
        response = client.post(webhook_url, data, format='json', HTTP_AUTHORIZATION=api_key_auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_message = Message.objects.get(id=message.id)
        self.assertEqual(updated_message.text, 'Processed message result')
