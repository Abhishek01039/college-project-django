from django.test import TestCase
from .models import FeedBack
# Create your tests here.
class FeedBackTest(TestCase):
    def setUp(self):
        FeedBack.objects.create(studName="Abhi",email="abhishekghaskata")
        FeedBack.objects.create(studName=1,email="abhishekghaskata")

    def test_feedback(self): 
        feedback=FeedBack.objects.get(name="Abhi")
        self.assertEqual(feedback.email=="Abhi")