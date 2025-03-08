from django.contrib import admin

from .models import Language, WordClass, LexicalCategory, LexicalCategoryValue, Lexeme

admin.site.register([Language, WordClass, LexicalCategory, LexicalCategoryValue, Lexeme])
