from django.contrib.auth import forms
from django import forms

from .models import Language, WordClass, Lexeme

class CustomForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        if "disabled" in dir(self._meta):
            for f in self._meta.disabled:
                self.fields[f].disabled = True
    
    template_name_div = "div.html"

class LexemeForm(forms.ModelForm, CustomForm):    
    class Meta:
        model = Lexeme
        fields = ("word_class", "word")
        disabled = ("word_class",)

class WordClassForm(forms.ModelForm, CustomForm):
    class Meta:
        model = WordClass
        fields = ("language", "name")
        disabled = ("language",)

class LanguageForm(forms.ModelForm, CustomForm):
    class Meta:
        model = Language
        fields = ("user", "name")
        disabled = ("user",)
