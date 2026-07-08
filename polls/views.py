from django.db.models import Count, Prefetch
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from polls.models import Question, Choice
from polls.serializers import QuestionListSerializer, QuestionDetailSerializer, ChoiceSerializer

class QuestionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
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

        return QuestionDetailSerializer