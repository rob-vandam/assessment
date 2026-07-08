from rest_framework import serializers

from .models import Question, Choice, Vote

#GET serializers

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = [
            "id",
            "question",
            "choice_text",
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

class VoteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    choice = serializers.StringRelatedField()

    class Meta:
        model = Vote
        fields = ["id", "user", "choice", "created_at"]

# POST serializers

class ChoiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = [
            "id",
            "choice_text",
        ]

class QuestionCreateSerializer(serializers.ModelSerializer):
    choices = ChoiceCreateSerializer(many=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "question_text",
            "pub_date",
            "choices",
        ]

    def validate_choices(self, value):
        if len(value) < 1:
            raise serializers.ValidationError(
                "Een question moet minstens 1 choice hebben."
            )
        return value

    def create(self, validated_data):
        choices_data = validated_data.pop("choices")
        question = Question.objects.create(**validated_data)
        Choice.objects.bulk_create(
            [Choice(question=question, **choice) for choice in choices_data]
        )
        return question

class VoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["choice"]