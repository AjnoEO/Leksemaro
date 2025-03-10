from django.db import models
from django.contrib.auth.models import User

class Language(models.Model):
    """Язык"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)

    @property
    def word_classes(self):
        return WordClass.objects.filter(language=self).all()

    @property
    def word_count(self):
        return sum([wc.word_count for wc in self.word_classes])

    def __str__(self):
        return f"Язык '{self.name}' | {self.user}"

class WordClass(models.Model):
    """Часть речи"""
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = "word classes"

    @property
    def user(self): return self.language.user

    @property
    def word_count(self):
        return Lexeme.objects.filter(word_class=self).count()

    def __str__(self):
        return f"Часть речи '{self.name}' | {self.language}"

class LexicalCategory(models.Model):
    """Лексическая категория (род, склонение, спряжение и пр.)"""
    word_class = models.ForeignKey(WordClass, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = "lexical categories"

    @property
    def language(self): return self.word_class.language

    @property
    def user(self): return self.word_class.user

    def __str__(self):
        return f"Лексическая категория '{self.name}' | {self.language}"

class LexicalCategoryValue(models.Model):
    """Значение лексической категории"""
    lexical_category = models.ForeignKey(LexicalCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)

    @property
    def language(self): return self.lexical_category.language

    @property
    def user(self): return self.lexical_category.user

    def __str__(self):
        return f"{self.lexical_category.name}={self.name} | {self.language}"

class Lexeme(models.Model):
    """Лексема (слово)"""
    word_class = models.ForeignKey(WordClass, on_delete=models.CASCADE)
    word = models.CharField(max_length=256)
    lexical_category_values = models.ManyToManyField(LexicalCategoryValue)

    # TODO: Проверка, что лексические категории берутся из правильной части речи

    @property
    def language(self): return self.word_class.language

    @property
    def user(self): return self.word_class.user

    def __str__(self):
        lexcat_values = [f"{catval.lexical_category}={catval.name}" for catval in self.lexical_category_values.all()]
        return (
            f"{self.word_class.name} '{self.word}' | " + " | ".join(lexcat_values) + f" | {self.language}"
        )
