from django.contrib import admin

from .models import Language, WordClass, LexicalCategory, LexicalCategoryValue, Lexeme, Meaning

admin.site.register([Language, WordClass, LexicalCategory, LexicalCategoryValue, Lexeme, Meaning])
