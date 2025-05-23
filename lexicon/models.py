from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from datetime import timedelta

class Language(models.Model):
    """Язык"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name="название")

    class Meta:
        verbose_name = "язык"
        verbose_name_plural = "языки"

    @property
    def word_classes(self):
        return WordClass.objects.filter(language=self).all()

    @property
    def word_count(self):
        return sum([wc.word_count for wc in self.word_classes])
    
    @property
    def words_to_repeat(self):
        return Lexeme.objects.filter(word_class__language=self, next_repetition__lte=timezone.now()).count()

    def __str__(self):
        return f"Язык '{self.name}' | {self.user}"

class WordClass(models.Model):
    """Часть речи"""
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name="название")

    class Meta:
        verbose_name = "часть речи"
        verbose_name_plural = "части речи"

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
    name = models.CharField(max_length=128, verbose_name="название")

    class Meta:
        verbose_name = "лексическая категория"
        verbose_name_plural = "лексические категории"

    @property
    def language(self): return self.word_class.language

    @property
    def user(self): return self.word_class.user

    def __str__(self):
        return f"Лексическая категория '{self.name}' | {self.language}"

class LexicalCategoryValue(models.Model):
    """Значение лексической категории"""
    lexical_category = models.ForeignKey(LexicalCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name="значение")

    class Meta:
        verbose_name = "значение лексической категории"
        verbose_name_plural = "значения лексической категории"

    @property
    def language(self): return self.lexical_category.language

    @property
    def user(self): return self.lexical_category.user

    def __str__(self):
        return f"{self.lexical_category.name}={self.name} | {self.language}"

class Lexeme(models.Model):
    """Лексема (слово)"""
    def default_next_repetition():
        return timezone.now() + timedelta(minutes=6)

    word_class = models.ForeignKey(WordClass, on_delete=models.CASCADE)
    word = models.CharField(max_length=256, verbose_name="слово")
    lexical_category_values = models.ManyToManyField(LexicalCategoryValue, blank=True)
    last_repetition = models.DateTimeField(default=timezone.now)
    coefficient = models.SmallIntegerField(default=1) # last_repetition / (6 * 10 ** coefficient)
    next_repetition = models.DateTimeField(default=default_next_repetition)

    class Meta:
        verbose_name = "лексема"
        verbose_name_plural = "лексемы"
        # TODO: Проверка, что лексические категории берутся из правильной части речи

    @property
    def language(self): return self.word_class.language

    @property
    def user(self): return self.word_class.user

    def __str__(self):
        lexcat_values = [f"{catval.lexical_category}={catval.name}" for catval in self.lexical_category_values.all()]
        result = f"{self.word_class.name} '{self.word}' | "
        if lexcat_values: result += " | ".join(lexcat_values) + " | "
        result += f" | {self.language}"
        return result

class Meaning(models.Model):
    """Значение слова"""
    lexeme = models.ForeignKey(Lexeme, on_delete=models.CASCADE)
    number = models.SmallIntegerField(default=1)
    translation = models.CharField(max_length=256, verbose_name="Перевод")

    class Meta:
        verbose_name = "значение"
        verbose_name_plural = "значения"

    @property
    def language(self): return self.lexeme.language

    @property
    def user(self): return self.lexeme.user

    def __str__(self):
        return f"'{self.translation}' ('{self.lexeme.word}') | {self.language}"
