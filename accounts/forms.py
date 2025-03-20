from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

class CustomForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
    
    template_name_div = "div.html"

class LeksemaroAuthenticationForm(AuthenticationForm, CustomForm):
    ...

class LeksemaroUserCreationForm(UserCreationForm, CustomForm):
    ...
