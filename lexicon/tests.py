from django.test import TestCase
from django.contrib.auth.models import User

class UserModelTests(TestCase):
    def test_user_creation(self):
        user = User.objects.create(username="test_user", password="test_password")
        user_id = user.pk
        self.assertEqual(User.objects.get(pk=user_id).get_username(), "test_user")
        self.assertListEqual(list(User.objects.all()), [user])
