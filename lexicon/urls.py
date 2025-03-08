from django.urls import path
from . import views

app_name = "lexicon"
urlpatterns = [
    path("", views.LanguageListView.as_view(), name="index"),
    path("<int:pk>", views.LanguageView.as_view(), name="language")
]
