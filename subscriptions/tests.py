from django.test import TestCase

from django.test import TestCase
from rest_framework.test import APIClient

class SubscriptionAPITests(TestCase):
    def setUp(self):
        # I initialize the testing client to simulate API requests
        self.client = APIClient()

    def test_webhook_requires_authentication(self):
        # I simulate a POST request to the webhook without providing a JWT token
        response = self.client.post(
            '/api/subscriptions/webhook/payment/', 
            {'username': 'user1', 'tier': 'PREMIUM'}, 
            format='json'
        )
        
        # I assert that the system correctly rejects the request with a 401 status code
        self.assertEqual(response.status_code, 401)