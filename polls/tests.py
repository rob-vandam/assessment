from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Permission, Group
from django.urls import reverse
from .models import Question, Choice, Vote
from django.db.utils import IntegrityError

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
        # self.assertEqual(choice.votes, 0)

    def test_choice_str(self):
        choice = Choice.objects.create(
            question=self.question,
            choice_text="Tea"
        )

        self.assertEqual(str(choice), "Tea")


class VoteModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="john",
            password="secret123"
        )

        self.question = Question.objects.create(
            owner=self.user,
            question_text="Tea or coffee?"
        )

        self.choice = Choice.objects.create(
            question=self.question,
            choice_text="Tea"
        )

    def test_user_can_vote(self):
        vote = Vote.objects.create(
            user=self.user,
            choice=self.choice
        )

        self.assertEqual(vote.user, self.user)
        self.assertEqual(vote.choice, self.choice)

    def test_user_cannot_vote_twice_for_same_choice(self):
        Vote.objects.create(user=self.user, choice=self.choice)

        with self.assertRaises(IntegrityError):
            Vote.objects.create(user=self.user, choice=self.choice)

# api GET tests
class QuestionListAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="john",
            password="secret"
        )

        cls.question = Question.objects.create(
            owner=cls.user,
            question_text="Tea or coffee?"
        )

        Choice.objects.create(
            question=cls.question,
            choice_text="Tea"
        )

        Choice.objects.create(
            question=cls.question,
            choice_text="Coffee"
        )

    def setUp(self):
        self.client.force_authenticate(self.user)

    def test_list_returns_200(self):
        url = reverse("questions-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_returns_expected_fields(self):
        url = reverse("questions-list")

        response = self.client.get(url)

        question = response.data[0]

        self.assertIn("id", question)
        self.assertIn("question_text", question)
        self.assertIn("pub_date", question)
        self.assertIn("choice_count", question)

        self.assertNotIn("choices", question)

class QuestionDetailAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="john",
            password="secret"
        )

        cls.question = Question.objects.create(
            owner=cls.user,
            question_text="Tea or coffee?"
        )

        Choice.objects.create(
            question=cls.question,
            choice_text="Tea"
        )

    def setUp(self):
        self.client.force_authenticate(self.user)

    def test_detail_contains_choices(self):
        url = reverse("questions-detail", args=[self.question.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("choices", response.data)
        self.assertEqual(len(response.data["choices"]), 1)

    def test_anonymous_user_gets_401(self):
        self.client.logout()

        url = reverse("questions-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# test for the auth token
class AuthTokenAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="john",
            password="secret123"
        )

    def test_token_is_returned_with_valid_credentials(self):
        url = reverse("api-token-auth")

        data = {
            "username": "john",
            "password": "secret123"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertTrue(len(response.data["token"]) > 0)

# api POST tests
class QuestionCreateAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="john",
            password="secret123"
        )

    def setUp(self):
        self.client.force_authenticate(self.user)

    def test_create_question_with_choices(self):
        url = reverse("questions-list")

        payload = {
            "question_text": "Wat is je favoriete programmeertaal?",
            "choices": [
                {"choice_text": "Python"},
                {"choice_text": "JavaScript"},
                {"choice_text": "Rust"},
            ]
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Question.objects.count(), 1)
        question = Question.objects.first()

        self.assertEqual(
            question.question_text,
            "Wat is je favoriete programmeertaal?"
        )

        self.assertEqual(Choice.objects.count(), 3)

        self.assertEqual(question.choices.count(), 3)

        choice_texts = set(question.choices.values_list("choice_text", flat=True))
        self.assertSetEqual(
            choice_texts,
            {"Python", "JavaScript", "Rust"}
        )
    # test of een vraag zonder antwoorden wordt geweigerd
    def test_create_question_without_choices_fails(self):
        url = reverse("questions-list")

        payload = {
            "question_text": "Test vraag",
            "choices": []
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("choices", response.data)

class VoteAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="john",
            password="secret123"
        )

        self.question = Question.objects.create(
            owner=self.user,
            question_text="Tea or coffee?"
        )

        self.choice = Choice.objects.create(
            question=self.question,
            choice_text="Tea"
        )

        self.client.force_authenticate(self.user)

    def test_user_can_create_vote(self):
        url = reverse("votes-list")

        payload = {
            "choice": self.choice.id
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vote.objects.count(), 1)

        vote = Vote.objects.first()
        self.assertEqual(vote.user, self.user)
        self.assertEqual(vote.choice, self.choice)

class QuestionCreatePermissionAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # gebruiker zonder add_question permissie
        cls.user_without_permission = User.objects.create_user(
            username="reader",
            password="secret123"
        )

        # gebruiker met add_question permissie
        cls.user_with_permission = User.objects.create_user(
            username="editor",
            password="secret123"
        )
        cls.user_with_permission.user_permissions.add(
            Permission.objects.get(codename="add_question")
        )

        cls.payload = {
            "question_text": "Test vraag",
            "choices": [
                {"choice_text": "Ja"},
                {"choice_text": "Nee"},
            ]
        }

    def test_post_forbidden_without_permission(self):
        self.client.force_authenticate(self.user_without_permission)
        url = reverse("questions-list")

        response = self.client.post(url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Question.objects.count(), 0)

    def test_post_allowed_with_permission(self):
        self.client.force_authenticate(self.user_with_permission)
        url = reverse("questions-list")

        response = self.client.post(url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)

    def test_post_requires_authentication(self):
        url = reverse("questions-list")

        response = self.client.post(url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_allowed_for_authenticated_user_without_permission(self):
        self.client.force_authenticate(self.user_without_permission)
        url = reverse("questions-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)