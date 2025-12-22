from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Question, Answer, Tag, QuestionLike
from .utils import paginate
from .forms import AskForm, AnswerForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Q

@require_POST
@login_required
def like_question_view(request):
    """
    AJAX обработчик лайков.
    Ожидает POST параметры: question_id, value (1).
    """
    question_id = request.POST.get('question_id')
    value = request.POST.get('value')
    
    try:
        question = Question.objects.get(pk=question_id)
        value = int(value)
        if value != QuestionLike.UP:
            raise ValueError('Invalid like value')

        existing_like = QuestionLike.objects.filter(
            user=request.user,
            question=question
        ).first()

        if existing_like:
            existing_like.delete()
            user_liked = False
        else:
            QuestionLike.objects.update_or_create(
                user=request.user,
                question=question,
                defaults={'value': QuestionLike.UP}
            )
            user_liked = True
        
        likes = question.questionlike_set.filter(value=QuestionLike.UP).count()
        
        return JsonResponse({
            'status': 'ok', 
            'likes': likes,
            'user_liked': user_liked,
        })
        
    except Question.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Вопрос не найден'}, status=404)
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Неверные данные'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_POST
@login_required
def correct_answer_view(request):
    """
    AJAX обработчик отметки правильного ответа.
    Ожидает POST параметры: question_id, answer_id.
    """
    question_id = request.POST.get('question_id')
    answer_id = request.POST.get('answer_id')
    
    try:
        question = Question.objects.get(pk=question_id)
        answer = Answer.objects.get(pk=answer_id)
        
        # Проверка: только автор вопроса может отмечать правильный ответ
        if request.user != question.author:
             return JsonResponse({'status': 'error', 'message': 'Нет прав'}, status=403)
             
        if answer.question != question:
            return JsonResponse({'status': 'error', 'message': 'Ответ не от этого вопроса'}, status=400)

        # Снимаем галочку со всех остальных ответов этого вопроса
        question.answer_set.update(is_correct=False)
        
        # Ставим галочку нужному
        answer.is_correct = True
        answer.save()
        
        return JsonResponse({'status': 'ok'})
        
    except (Question.DoesNotExist, Answer.DoesNotExist):
        return JsonResponse({'status': 'error', 'message': 'Объект не найден'}, status=404)

def index(request):
    new_questions = Question.objects.new()
    context = paginate(request, new_questions, per_page=4)

    return render(request, 'qa/index.html', context)

def new_question_view(request):
    return render(request, 'qa/AddQuestion.html')

def question_detail_view(request, question_id):
    question_qs = (
        Question.objects.annotate(
            likes_count=Count('questionlike', filter=Q(questionlike__value=QuestionLike.UP))
        )
        .select_related('author')
        .prefetch_related('tags')
    )
    question = get_object_or_404(question_qs, pk=question_id)
    answers = question.get_answers()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            login_url = f"{reverse('users:login')}?next={request.path}"
            return redirect(login_url)

        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect('qa:question_detail', question_id=question.id)
    else:
        answer_form = AnswerForm()

    user_liked = False
    if request.user.is_authenticated:
        user_liked = QuestionLike.objects.filter(user=request.user, question=question).exists()

    context = {
        'question': question,
        'answers': answers,
        'answer_form': answer_form,
        'user_liked': user_liked,
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

class NewQuestionView(LoginRequiredMixin, CreateView):
    """Создание нового вопроса"""
    model = Question
    form_class = AskForm
    template_name = 'qa/AddQuestion.html'
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        # Присваиваем автора перед сохранением
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # После создания идем на страницу вопроса
        return reverse('qa:question_detail', kwargs={'question_id': self.object.id})

class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование вопроса (только автор)"""
    model = Question
    form_class = AskForm
    template_name = 'qa/AddQuestion.html' # Используем тот же шаблон
    pk_url_kwarg = 'question_id' # Имя параметра в URL
    login_url = reverse_lazy('users:login')

    def test_func(self):
        # Проверка прав: текущий юзер должен быть автором вопроса
        obj = self.get_object()
        return obj.author == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True # Флаг для шаблона, чтобы менять заголовок
        return context

    def get_success_url(self):
        return reverse('qa:question_detail', kwargs={'question_id': self.object.id})


class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление вопроса (только автор)"""
    model = Question
    pk_url_kwarg = 'question_id'
    template_name = 'qa/question_confirm_delete.html' 
    success_url = reverse_lazy('qa:index')
    login_url = reverse_lazy('users:login')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class AnswerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование ответа (только автор)"""
    model = Answer
    form_class = AnswerForm
    template_name = 'qa/answer_form.html'
    pk_url_kwarg = 'answer_id'
    login_url = reverse_lazy('users:login')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.object.question
        context['is_edit'] = True
        return context

    def get_success_url(self):
        return reverse('qa:question_detail', kwargs={'question_id': self.object.question_id})


class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление ответа (только автор)"""
    model = Answer
    pk_url_kwarg = 'answer_id'
    template_name = 'qa/answer_confirm_delete.html'
    login_url = reverse_lazy('users:login')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_success_url(self):
        return reverse('qa:question_detail', kwargs={'question_id': self.object.question_id})
