from django.urls import path
from votes import views


urlpatterns = [
    path('votes/', views.VoteList.as_view()),
]
