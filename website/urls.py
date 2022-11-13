from django.urls import path
from .views import IndexView,LoopView,NotLoopView,AccessView,CareView,InfoView



urlpatterns = [
    path('',IndexView.as_view()),
    path('index',IndexView.as_view()),
    path('loop/',LoopView.as_view()),
    path('notloop/',NotLoopView.as_view()),
    path('access/',AccessView.as_view()),
    path('care/',CareView.as_view()),
    path('info/',InfoView.as_view()),
    ]