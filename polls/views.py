from django.db.models import Count, Prefetch
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions
from polls.models import Question, Choice
from polls.serializers import (QuestionListSerializer, QuestionDetailSerializer, ChoiceSerializer,
                               QuestionCreateSerializer, VoteSerializer,VoteCreateSerializer)


class CustomDjangoModelPermissions(DjangoModelPermissions):
    authenticated_users_only = True

class QuestionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    http_method_names = ["get","post"]
    def get_queryset(self):
        return (
            Question.objects
            .filter(archived=False)
            .select_related("owner")
            .prefetch_related(
                Prefetch("choices", queryset=Choice.objects.all())
            )
            .annotate(choice_count=Count("choices"))
        )

    def get_serializer_class(self):
        if self.action == "list":
            return QuestionListSerializer

        if self.action == "retrieve":
            return QuestionDetailSerializer

        if self.action == "create":
            return QuestionCreateSerializer

        return QuestionDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class VoteViewSet(ModelViewSet):

    def get_serializer_class(self):
        if self.action == "create":
            return VoteCreateSerializer
        return VoteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)