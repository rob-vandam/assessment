import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from polls.models import Question, Choice


class Command(BaseCommand):
    help = "Generate demo data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--questions",
            type=int,
            default=10,
            help="Number of questions to generate"
        )

    def handle(self, *args, **options):
        amount = options["questions"]
        User = get_user_model()
        users = list(User.objects.all())

        if not users:
            raise CommandError('No users found')


        for index in range(amount):
            owner = random.choice(users)

            question = Question.objects.create(
                owner=owner,
                question_text=f"Demo Question {index + 1}",
                pub_date=timezone.now(),
            )

            for i in range(random.randint(2, 5)):
                Choice.objects.create(
                    question=question,
                    choice_text=f"Choice {i + 1}",
                    votes=random.randint(0, 100),
                )

        print(f"Created {amount} questions.")