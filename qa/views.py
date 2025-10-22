from django.shortcuts import render

def index(request):
    return render(request, 'qa/base.html')

def new_question_view(request):
    return render(request, 'qa/AddQuestion.html')

def question_detail_view(request):
    return render(request, 'qa/Question.html')

def filtred_view(request):
    return render(request, 'qa/FiltredBase.html')

def profile_view(request):
    return render(request, 'qa/Profile.html')

def login_view(request):
    return render(request, 'qa/Login.html')

def register_view(request):
    return render(request, 'qa/Register.html')