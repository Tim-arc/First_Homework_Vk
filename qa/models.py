from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

class QuestionManager(models.Manager):
    def new(self):
        """Возвращает самые новые вопросы."""
        return self.get_queryset().select_related('author').prefetch_related('tags').annotate(
            answer_count=Count('answer'),
            like_count=Count('questionlike')
        ).order_by('-created_at')

    def best(self):
        """Возвращает лучшие вопросы (отсортированные по количеству лайков)."""
        return self.get_queryset().select_related('author').prefetch_related('tags').annotate(
            answer_count=Count('answer'),
            like_count=Count('questionlike')
        ).order_by('-like_count', '-created_at')
    
    def by_tag(self, tag_name):
        """
        Возвращает вопросы по тегу.
        """
        return self.new().filter(tags__name=tag_name)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Question(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=200)
    text = models.TextField(verbose_name='Текст вопроса', max_length=20000)

    created_at = models.DateTimeField(verbose_name='Создан в', auto_now_add=True, db_index=True)
    changed_at = models.DateTimeField(verbose_name='Изменен в', auto_now=True)
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, verbose_name='Теги')

    # Подключаем наш кастомный менеджер
    objects = QuestionManager()

    def __str__(self):
        return self.title

    def get_answers(self):
        return self.answer_set.select_related('author').order_by('-created_at')
    
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Answer(models.Model):
    text = models.TextField(verbose_name='Текст ответа', max_length=20000)
    created_at = models.DateTimeField(verbose_name='Создан в', auto_now_add=True, db_index=True)
    changed_at = models.DateTimeField(verbose_name='Изменен в', auto_now=True)
    question = models.ForeignKey(Question, verbose_name='Вопрос', on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Ответ пользователя #{self.author_id} на вопрос #{self.question_id}"
    
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