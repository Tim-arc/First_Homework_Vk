import random
from django.core.management.base import BaseCommand
from users.models import Profile
from qa.models import Question, Tag, Answer, QuestionLike
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    help = 'Наполняет базу данных тестовыми данными на основе коэффициента (ratio).'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Коэффициент для наполнения базы данных.')

    @transaction.atomic
    def handle(self, *args, **options):
        ratio = options['ratio']
        
        # --- Очистка старых данных ---
        self.stdout.write(self.style.WARNING('Очистка старых данных...'))
        QuestionLike.objects.all().delete()
        Answer.objects.all().delete()
        Question.objects.all().delete()
        Tag.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()
        self.stdout.write(self.style.SUCCESS('Очистка завершена.'))

        num_users = ratio
        num_tags = ratio
        num_questions = ratio * 10
        num_answers = ratio * 100
        num_likes = ratio * 200

        self.stdout.write(self.style.SUCCESS(f'Начинаем генерацию данных с коэффициентом {ratio}...'))
        
        self.stdout.write('Генерация тегов...')
        fixed_tags = set(['perl', 'python', 'technopark', 'mysql', 'firefox'])
        
        for tag_name in fixed_tags:
            Tag.objects.get_or_create(name=tag_name)
            
        num_remaining_tags = num_tags - len(fixed_tags)
        if num_remaining_tags > 0:
            tags_to_create = [Tag(name=f'tag_{i}') for i in range(num_remaining_tags)]
            Tag.objects.bulk_create(tags_to_create)
            
        tags = list(Tag.objects.all())
        self.stdout.write(self.style.SUCCESS(f'Теги созданы. Всего: {len(tags)}'))

        # --- Генерация Пользователей и Профилей ---
        self.stdout.write('Генерация пользователей и профилей...')
        users_to_create = [User(username=f'user_{i}', email=f'user{i}@mail.ru', password='password123') for i in range(num_users)]
        User.objects.bulk_create(users_to_create)
        
        new_users = User.objects.order_by('-id')[:num_users]
        profiles_to_create = [Profile(user=user, nickname=f'cool_nick_{user.username}') for user in new_users]
        Profile.objects.bulk_create(profiles_to_create)
        users = list(User.objects.filter(is_superuser=False))
        self.stdout.write(self.style.SUCCESS(f'Пользователи и профили созданы.'))
        
        # --- Генерация Вопросов ---
        self.stdout.write('Генерация вопросов...')
        questions_to_create = []
        for i in range(num_questions):
            q = Question(author=random.choice(users), title=f'Вопрос номер {i}', text=f'Это полный текст для вопроса номер {i}. А это просто текст что бы проверить как смотрится страница с текстом вопроса номер {i}.')
            questions_to_create.append(q)
        Question.objects.bulk_create(questions_to_create)

        all_questions = Question.objects.order_by('-id')[:num_questions]
        for question in all_questions:
            num_tags_to_add = min(len(tags), random.randint(1, 3))
            question.tags.set(random.sample(tags, num_tags_to_add))
        questions = list(all_questions)
        self.stdout.write(self.style.SUCCESS(f'Вопросы созданы.'))
        
        # --- Генерация Ответов ---
        self.stdout.write('Генерация ответов...')
        answers_to_create = []
        for _ in range(num_answers):
            a = Answer(author=random.choice(users), question=random.choice(questions), text=f'Случайный ответ на случайный вопрос номер {random.randint(1, 1000)}.')
            answers_to_create.append(a)
        Answer.objects.bulk_create(answers_to_create)
        self.stdout.write(self.style.SUCCESS(f'Ответы созданы.'))

        # --- Генерация Лайков ---
        self.stdout.write('Генерация лайков...')
        likes_to_create = set()
        max_possible_likes = len(users) * len(questions)
        num_likes_to_generate = min(num_likes, max_possible_likes)
        
        while len(likes_to_create) < num_likes_to_generate:
            user = random.choice(users)
            question = random.choice(questions)
            likes_to_create.add((user.id, question.id))
            
        QuestionLike.objects.bulk_create(
            [QuestionLike(user_id=uid, question_id=qid) for uid, qid in likes_to_create],
            ignore_conflicts=True
        )
        self.stdout.write(self.style.SUCCESS(f'Лайки созданы.'))
        self.stdout.write(self.style.SUCCESS('Наполнение базы данных завершено!'))