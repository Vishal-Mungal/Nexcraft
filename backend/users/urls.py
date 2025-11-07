from django.urls import path
from .views import register, login, submit_quiz_score, get_quiz_history, apply_job
from .views import save_learning_progress

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path("quiz/submit/", submit_quiz_score),
    path("quiz/history/", get_quiz_history, name="quiz_history"),
    path("job/apply/", apply_job),
    path("learning/progress/", save_learning_progress, name="save_learning_progress"),
]
