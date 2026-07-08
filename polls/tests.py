from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Question, Choice

User = get_user_model()

# test voor de polls model
class QuestionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="john",
            password="secret123"
        )

    def test_create_question(self):
        question = Question.objects.create(
            owner=self.user,
            question_text="What's your favorite color?"
        )

        self.assertEqual(question.question_text, "What's your favorite color?")
        self.assertEqual(question.owner, self.user)
        self.assertFalse(question.archived)

    def test_question_str(self):
        question = Question.objects.create(
            owner=self.user,
            question_text="Test question"
        )

        self.assertEqual(str(question), "Test question")

class ChoiceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="john",
            password="secret123"
        )

        self.question = Question.objects.create(
            owner=self.user,
            question_text="Tea or coffee?"
        )

    def test_create_choice(self):
        choice = Choice.objects.create(
            question=self.question,
            choice_text="Coffee"
        )

        self.assertEqual(choice.question, self.question)
        self.assertEqual(choice.votes, 0)

    def test_choice_str(self):
        choice = Choice.objects.create(
            question=self.question,
            choice_text="Tea"
        )

        self.assertEqual(str(choice), "Tea")