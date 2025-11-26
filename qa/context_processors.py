from django.db.models import Count
from .models import Tag
from django.contrib.auth.models import User

def popular_tags(request):
    """
    Контекстный процессор для добавления списка популярных тегов в контекст всех шаблонов.
    """
    
    popular_tags = Tag.objects.annotate(
        question_count=Count('question')
    ).order_by('-question_count')[:10]
    
    return {
        'popular_tags': popular_tags
    }

def popular_members(request):
    """
    Контекстный процессор для добавления списка популярных участников в контекст всех шаблонов.
    """
    
    popular_members = User.objects.annotate(
        answer_count=Count('answer')
    ).order_by('-answer_count')[:3]
    
    return {
        'popular_members': popular_members
    }