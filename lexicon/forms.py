from django.contrib.auth import forms
from django import forms

from .models import Lexeme

class CustomForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
    
    template_name_div = "div.html"

class LexemeForm(forms.ModelForm, CustomForm):    
    class Meta:
        model = Lexeme
        fields = ("word_class", "word")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["word_class"].disabled = True
