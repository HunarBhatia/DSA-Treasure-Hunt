from django.urls import path
from .views import LevelView, SubmitAnswerView

urlpatterns = [
    path('level/<int:level_number>/', LevelView.as_view(), name='level'),
    path('submit/', SubmitAnswerView.as_view(), name='submit'),
]