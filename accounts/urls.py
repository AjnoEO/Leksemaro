from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .forms import LeksemaroAuthenticationForm
from .views import RegisterView

app_name = 'accounts'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(authentication_form=LeksemaroAuthenticationForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
