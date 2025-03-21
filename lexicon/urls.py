from django.urls import path
from . import views

app_name = "lexicon"
urlpatterns = [
    path("", views.LanguageListView.as_view(), name="index"),
    path("language/<int:pk>", views.LanguageView.as_view(), name="language"),
    path("wordclass/<int:pk>", views.WordClassView.as_view(), name="word_class"),
    path("add_lexeme/<int:word_class>", views.LexemeCreateView.as_view(), name="add_lexeme"),
    path("add_word_class/<int:language>", views.WordClassCreateView.as_view(), name="add_word_class"),
    path("add_language", views.LanguageCreateView.as_view(), name="add_language"),
]
