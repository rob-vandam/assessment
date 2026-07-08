from rest_framework import serializers

from .models import Question, Choice

#GET serializers

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = [
            "id",
            "question",
            "choice_text",
            "votes",
        ]

class QuestionListSerializer(serializers.ModelSerializer):
    choice_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "question_text",
            "pub_date",
            "choice_count",
        ]

class QuestionDetailSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "question_text",
            "pub_date",
            "choices",
        ]
