from django.contrib.auth import forms
from django import forms

from .models import Language, WordClass, Lexeme, Meaning

class CustomForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        if "disabled" in dir(self.Meta):
            for f in self.Meta.disabled:
                self.fields[f].disabled = True
    
    template_name_div = "div.html"

class LexemeForm(forms.ModelForm, CustomForm):    
    class Meta:
        model = Lexeme
        fields = ("word_class", "word")
        disabled = ("word_class",)

class MeaningForm(forms.ModelForm, CustomForm):
    class Meta:
        model = Meaning
        fields = ("translation",)

MeaningFormSet = forms.inlineformset_factory(Lexeme, Meaning, MeaningForm, extra=0, min_num=1)

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
