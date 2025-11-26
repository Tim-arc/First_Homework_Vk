from . import views
from django.urls import path


urlpatterns = [
    path('best/', views.best_questions_view, name='best'),
    path('ask/', views.new_question_view, name='ask'),
    path('question/<int:question_id>/', views.question_detail_view, name='question_detail'),
    path('question/', views.question_detail_view, name='question_detail'),
    path('tag/<str:tag_name>/', views.questions_by_tag_view, name='questions_by_tag'),
    # path('filtred/', views.filtred_view, name="filtred"),
    path('', views.index, name='index'),
]