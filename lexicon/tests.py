from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Language

def create_test_user(testcase: TestCase = None, num: int = 1):
    u = User.objects.create(username=f"test_user_{num}")
    p = "test_password"
    u.set_password(p)
    u.save()
    if testcase: testcase.client.login(username=u.username, password=p)
    return u

def create_test_language(user: User, num: int = 1):
    l = Language.objects.create(user=user, name=f"test_language_{1}")
    return l

class UserModelTests(TestCase):
    def test_user_creation(self):
        user = create_test_user()
        user_id = user.pk
        self.assertEqual(User.objects.get(pk=user_id).get_username(), user.username)
        self.assertListEqual(list(User.objects.all()), [user])

class LanguageListViewTests(TestCase):
    def test_empty_list(self):
        create_test_user(self)
        response = self.client.get(reverse("lexicon:index"))
        self.assertContains(response, "Пока нет языков", status_code=200)
    
    def test_one_language(self):
        user = create_test_user(self)
        language = create_test_language(user)
        response = self.client.get(reverse("lexicon:index"))
        self.assertContains(response, language.name, status_code=200)
    
    def test_other_users_language(self):
        create_test_user(self)
        another_user = create_test_user(num=2)
        language = create_test_language(another_user)
        response = self.client.get(reverse("lexicon:index"))
        self.assertContains(response, "Пока нет языков", status_code=200)
        self.assertNotContains(response, language.name)

class LanguageViewTests(TestCase):
    def test_existing_language(self):
        user = create_test_user(self)
        language = create_test_language(user)
        response = self.client.get(reverse("lexicon:language", args=(language.id,)))
        self.assertContains(response, language.name, status_code=200)

    def test_language_not_found_error(self):
        create_test_user(self)
        other_user = create_test_user(num=2)
        language = create_test_language(other_user)
        response = self.client.get(reverse("lexicon:language", args=(language.id,)))
        self.assertEqual(response.status_code, 404)
