from django import forms
from .models import Question, Tag, Answer
from django.core.exceptions import ValidationError

class AskForm(forms.ModelForm):
    tags = forms.CharField(
        label='Теги',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите теги через запятую'})
    )
    
    class Meta:
        model = Question
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок вопроса'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Опишите суть вашего вопроса подробно...', 'rows': 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['tags'] = ', '.join([t.name for t in self.instance.tags.all()])

    def clean_tags(self):
        tags_str = self.cleaned_data.get('tags')
        if not tags_str:
            return []
        
        tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
        return tag_names

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            tag_names = self.cleaned_data['tags']
            tags = []
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(name=name)
                tags.append(tag)
            
            instance.tags.set(tags)
            
        return instance

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Введите ваш ответ здесь...'}),
        }

