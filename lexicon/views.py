from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy

from .forms import LexemeForm
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

class LexemeCreateView(generic.CreateView):
    form_class = LexemeForm
    template_name = "lexicon/forms/lexeme.html"
    
    def get_success_url(self):
        return reverse_lazy("lexicon:word_class", args=(self.kwargs['word_class_id'],))

    def get_initial(self):
        initial = super().get_initial()
        initial['word_class'] = WordClass.objects.get(pk=self.kwargs['word_class_id'])
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "word_class": WordClass.objects.get(pk=self.kwargs['word_class_id'])
        })
        return context
