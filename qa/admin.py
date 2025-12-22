from django.contrib import admin
from . import models


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'likes_count')
    search_fields = ('title', 'text', 'author__username')
    list_filter = ('created_at', 'tags')
    filter_horizontal = ('tags',)

    def likes_count(self, obj):
        return obj.questionlike_set.filter(value=models.QuestionLike.UP).count()
    likes_count.short_description = 'Лайков'


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'author', 'is_correct', 'created_at')
    search_fields = ('text', 'author__username', 'question__title')
    list_filter = ('is_correct', 'created_at')


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(models.QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'user', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    search_fields = ('question__title', 'user__username')


@admin.register(models.AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('answer__question__title', 'user__username')
