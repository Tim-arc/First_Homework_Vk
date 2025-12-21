from . import views
from django.urls import path


urlpatterns = [
    path('ask/', views.NewQuestionView.as_view(), name='ask'),
    path('question/<int:question_id>/edit/', views.QuestionUpdateView.as_view(), name='question_edit'),
    path('question/<int:question_id>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
    path('answer/<int:answer_id>/edit/', views.AnswerUpdateView.as_view(), name='answer_edit'),
    path('answer/<int:answer_id>/delete/', views.AnswerDeleteView.as_view(), name='answer_delete'),

    path('question/<int:question_id>/', views.question_detail_view, name='question_detail'),
    path('tag/<str:tag_name>/', views.questions_by_tag_view, name='questions_by_tag'),
    path('best/', views.best_questions_view, name='best'),
    path('filtred/', views.filtred_view, name="filtred"),
    path('', views.index, name='index'),
]
