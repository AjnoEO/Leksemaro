from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Model
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import LanguageForm, WordClassForm, LexemeForm, MeaningFormSet
from .models import Language, WordClass, Meaning

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

def add_lexeme(request: HttpRequest, word_class: int):
    word_class: WordClass = get_object_or_404(WordClass, pk=word_class, language__user=request.user)
    if request.method == "POST":
        form = LexemeForm(request.POST, initial={'word_class': word_class})
        formset = MeaningFormSet(request.POST)
        if formset.is_valid():
            lexeme = form.save()
            for meaning_form in formset:
                meaning: Meaning = meaning_form.save(commit=False)
                meaning.lexeme = lexeme
                meaning.save()
            return redirect(reverse("lexicon:word_class", args=(word_class.id,)))
    else:
        form = LexemeForm(initial={'word_class': word_class})
        formset = MeaningFormSet()
    return render(request, "lexicon/forms/lexeme_with_meanings.html", {"form": form, "meanings": formset, "word_class": word_class})

class LexemeWithMeaningsCreateView(CustomCreateView):
    form_class = LexemeForm
    template_name = "lexicon/forms/lexeme_with_meanings.html"
    parent_field = "word_class"
    parent_class = WordClass
    user_arg = "language__user"
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['meanings'] = MeaningFormSet(self.request.POST)
        else:
            data['meanings'] = MeaningFormSet()
        return data

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
