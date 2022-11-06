from django.urls import path
from .views import IndexView


urlpatterns = [
    path('',IndexView.as_view()),
    path('/index',IndexView.as_view()),
    ]