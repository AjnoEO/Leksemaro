from django.test import TestCase
from django.contrib.auth.models import User

class UserModelTests(TestCase):
    def test_user_creation(self):
        user = User(username="test_user", password="test_password")
        user.save()
        self.assertIsNotNone(user)
        self.assertEqual(user.get_username(), "test_user")
