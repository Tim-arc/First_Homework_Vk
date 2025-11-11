from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

class QuestionManager(models.Manager):
    def new(self):
        """Возвращает самые новые вопросы."""
        return self.order_by('-created_at')

    def best(self):
        """Возвращает лучшие вопросы (отсортированные по количеству лайков)."""
        return self.annotate(likes_count=Count('questionlike')).order_by('-likes_count')

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Question(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=200)
    text = models.TextField(verbose_name='Текст вопроса')
    created_at = models.DateTimeField(verbose_name='Создан в', auto_now_add=True)
    changed_at = models.DateTimeField(verbose_name='Изменен в', auto_now=True)
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='Теги')

    # Подключаем наш кастомный менеджер
    objects = QuestionManager()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Answer(models.Model):
    text = models.TextField(verbose_name='Текст ответа')
    created_at = models.DateTimeField(verbose_name='Создан в', auto_now_add=True)
    changed_at = models.DateTimeField(verbose_name='Изменен в', auto_now=True)
    question = models.ForeignKey(Question, verbose_name='Вопрос', on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)

    def __str__(self):
        return f"Ответ {self.author.username} на '{self.question.title}'"
    
    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

class QuestionLike(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name='Вопрос', on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='Создан в', auto_now_add=True)
    changed_at = models.DateTimeField(verbose_name='Изменен в', auto_now=True)

    class Meta:
        unique_together = ('user', 'question')
        verbose_name = 'Лайк вопроса'
        verbose_name_plural = 'Лайки вопросов'


class AnswerLike(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, verbose_name='Ответ', on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='Создан в', auto_now_add=True)
    changed_at = models.DateTimeField(verbose_name='Изменен в', auto_now=True)

    class Meta:
        unique_together = ('user', 'answer')
        verbose_name = 'Лайк ответа'
        verbose_name_plural = 'Лайки ответов'