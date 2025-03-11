from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .models import Language, WordClass

class LanguageListView(generic.ListView, LoginRequiredMixin):
    template_name = "lexicon/language_list.html"
    context_object_name = "languages"

    def get_queryset(self):
        return Language.objects.filter(user=self.request.user)

class LanguageView(generic.DetailView, LoginRequiredMixin):
    template_name = "lexicon/language.html"

    def get_queryset(self):
        return Language.objects.filter(user=self.request.user)

class WordClassView(generic.DetailView, LoginRequiredMixin):
    template_name = "lexicon/word_class.html"
    context_object_name = "word_class"

    def get_queryset(self):
        return WordClass.objects.filter(language__user=self.request.user)
