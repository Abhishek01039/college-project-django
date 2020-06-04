from django.test import TestCase
from .models import FeedBack
from rest_framework.test import APITestCase

# Create your tests here.
class FeedBackTest(TestCase):
    def setUp(self):
        FeedBack.objects.create(studName="Abhi",email="abhishekghaskata1999@gmail.com")
        FeedBack.objects.create(studName="Harshit",email="harshitmangukiya@gmail.com")

    def test_feedback(self): 
        feedback=FeedBack.objects.get(studName="Abhi")
        self.assertEqual(feedback.email,"abhishekghaskata1999@gmail.com")

class StudTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        # url = reverse('account-list')
        data = {'name': 'DabApps'}
        response = self.client.post("", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, 'DabApps')