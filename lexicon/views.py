from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Model
from django.views import generic
from django.urls import reverse_lazy

from .forms import LanguageForm, WordClassForm, LexemeForm
from .models import Language, WordClass

class LanguageListView(LoginRequiredMixin, generic.ListView):
    template_name = "lexicon/language_list.html"
    context_object_name = "languages"

    def get_queryset(self):
        return Language.objects.filter(user=self.request.user)

class LanguageView(LoginRequiredMixin, generic.DetailView):
    template_name = "lexicon/language.html"

    def get_queryset(self):
        return Language.objects.filter(user=self.request.user)

class WordClassView(LoginRequiredMixin, generic.DetailView):
    template_name = "lexicon/word_class.html"
    context_object_name = "word_class"

    def get_queryset(self):
        return WordClass.objects.filter(language__user=self.request.user)

class CustomCreateView(generic.CreateView):
    parent_field = None
    parent_class: type[Model] = Model
    user_arg = "user"

    @property
    def parent(self):
        if not self.parent_field:
            return {"user": self.request.user}
        return {
            self.parent_field: self.parent_class.objects.get(
                pk=self.kwargs[self.parent_field],
                **{self.user_arg: self.request.user}
            )
        }

    def get_success_url(self):
        return reverse_lazy(
            f"lexicon:{self.parent_field or 'index'}", 
            args=(self.kwargs[self.parent_field],) if self.parent_field else None
        )

    def get_initial(self):
        initial = super().get_initial()
        initial.update(self.parent)
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.parent)
        return context

class LexemeCreateView(CustomCreateView):
    form_class = LexemeForm
    template_name = "lexicon/forms/lexeme.html"
    parent_field = "word_class"
    parent_class = WordClass
    user_arg = "language__user"

class WordClassCreateView(CustomCreateView):
    form_class = WordClassForm
    template_name = "lexicon/forms/word_class.html"
    parent_field = "language"
    parent_class = Language

class LanguageCreateView(CustomCreateView):
    form_class = LanguageForm
    template_name = "lexicon/forms/language.html"
    parent_class = User
    
    # def get_success_url(self):
    #     return reverse_lazy(f"lexicon:index")
