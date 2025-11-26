from django.shortcuts import render, get_object_or_404
from .models import (
    Question, 
    Answer, 
    Tag,
    )
from .utils import paginate

def index(request):
    new_questions = Question.objects.new()
    context = paginate(request, new_questions, per_page=4)

    return render(request, 'qa/index.html', context)

def new_question_view(request):
    return render(request, 'qa/AddQuestion.html')

def question_detail_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = question.get_answers()
    
    context = {
        'question': question,
        'answers': answers,
    }
    
    return render(request, 'qa/Question.html', context)

def filtred_view(request):
    return render(request, 'qa/FiltredBase.html')

def best_questions_view(request):
    best_questions = Question.objects.best()
    context = paginate(request, best_questions, per_page=4)

    return render(request, 'qa/best.html', context)

def questions_by_tag_view(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    questions = Question.objects.by_tag(tag_name)
    context = paginate(request, questions, per_page=4)
    context['tag'] = tag
    
    return render(request, 'qa/tag_questions.html', context)
