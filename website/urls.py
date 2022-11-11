from django.urls import path
from .views import IndexView,LoopView,NotLoopView



urlpatterns = [
    path('',IndexView.as_view()),
    path('index',IndexView.as_view()),
    path('loop/',LoopView.as_view()),
    path('notloop/',NotLoopView.as_view()),
    ]