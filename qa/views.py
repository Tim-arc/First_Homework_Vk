from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Question, Answer, Tag
from .utils import paginate
from .forms import AskForm, AnswerForm

def index(request):
    new_questions = Question.objects.new()
    context = paginate(request, new_questions, per_page=4)

    return render(request, 'qa/index.html', context)

def new_question_view(request):
    return render(request, 'qa/AddQuestion.html')

def question_detail_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
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

    context = {
        'question': question,
        'answers': answers,
        'answer_form': answer_form,
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
