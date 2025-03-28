from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import LeksemaroUserCreationForm

class RegisterView(CreateView):
    form_class = LeksemaroUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"