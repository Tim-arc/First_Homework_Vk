from .views import (
    index, 
    new_question_view,
    question_detail_view,
    filtred_view,
    profile_view,
    login_view,
    register_view,
)
from django.urls import path


urlpatterns = [
    path('', index, name='index'),
    path('ask/', new_question_view, name='ask'),
    path('question/', question_detail_view, name='question_detail'),
    path('filtred/', filtred_view, name="filtred"),
    path('profile/', profile_view, name="profile"),
    path('login/', login_view, name="login"),
    path('register/', register_view, name="register"),
]