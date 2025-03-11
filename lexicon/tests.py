from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Language, WordClass, Lexeme

class Counter:
    def __init__(self):
        self.__val = 0
    
    @property
    def get(self):
        self.__val += 1
        return self.__val

c = Counter()

def create_test_user(testcase: TestCase = None):
    """Укажи `testcase` (`self`), чтобы залогиниться от лица пользователя"""
    u = User.objects.create(username=f"test_user_{c.get}")
    p = "test_password"
    u.set_password(p)
    u.save()
    if testcase: testcase.client.login(username=u.username, password=p)
    return u

def create_test_language(user: User):
    l = Language.objects.create(user=user, name=f"test_language_{c.get}")
    return l

def create_test_word_class(language: Language):
    wc = WordClass.objects.create(language=language, name=f"test_word_class_{c.get}")
    return wc

def create_test_lexeme(word_class: WordClass):
    lex = Lexeme.objects.create(word_class=word_class, word=f"test_lexeme_{c.get}")
    return lex

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
        another_user = create_test_user()
        language = create_test_language(another_user)
        response = self.client.get(reverse("lexicon:index"))
        self.assertContains(response, "Пока нет языков", status_code=200)
        self.assertNotContains(response, language.name)

class LanguageViewTests(TestCase):
    def test_existing_language(self):
        user = create_test_user(self)
        language = create_test_language(user)
        response = self.client.get(reverse("lexicon:language", args=(language.pk,)))
        self.assertContains(response, language.name, status_code=200)

    def test_language_not_found_error(self):
        create_test_user(self)
        other_user = create_test_user()
        language = create_test_language(other_user)
        response = self.client.get(reverse("lexicon:language", args=(language.pk,)))
        self.assertEqual(response.status_code, 404)
    
    def test_one_word_class(self):
        user = create_test_user(self)
        language = create_test_language(user)
        word_class = create_test_word_class(language)
        response = self.client.get(reverse("lexicon:language", args=(language.pk,)))
        self.assertContains(response, word_class.name, status_code=200)

    def test_word_class_in_other_language(self):
        user = create_test_user(self)
        language = create_test_language(user)
        language_2 = create_test_language(user)
        word_class = create_test_word_class(language_2)
        response = self.client.get(reverse("lexicon:language", args=(language.pk,)))
        self.assertContains(response, "Пока нет частей речи", status_code=200)
        self.assertNotContains(response, word_class.name)

class WordClassViewTests(TestCase):
    def test_existing_language(self):
        user = create_test_user(self)
        language = create_test_language(user)
        word_class = create_test_word_class(language)
        response = self.client.get(reverse("lexicon:word_class", args=(word_class.pk,)))
        self.assertContains(response, word_class.name, status_code=200)

    def test_language_not_found_error(self):
        create_test_user(self)
        other_user = create_test_user()
        language = create_test_language(other_user)
        word_class = create_test_word_class(language)
        response = self.client.get(reverse("lexicon:word_class", args=(word_class.pk,)))
        self.assertEqual(response.status_code, 404)
    
    def test_one_lexeme(self):
        user = create_test_user(self)
        language = create_test_language(user)
        word_class = create_test_word_class(language)
        lexeme = create_test_lexeme(word_class)
        response = self.client.get(reverse("lexicon:word_class", args=(word_class.pk,)))
        self.assertContains(response, lexeme.word, status_code=200)

    def test_lexeme_in_other_word_class(self):
        user = create_test_user(self)
        language = create_test_language(user)
        word_class = create_test_word_class(language)
        word_class_2 = create_test_word_class(language)
        lexeme = create_test_lexeme(word_class_2)
        response = self.client.get(reverse("lexicon:word_class", args=(word_class.pk,)))
        self.assertContains(response, "Пока нет слов", status_code=200)
        self.assertNotContains(response, lexeme.word)
