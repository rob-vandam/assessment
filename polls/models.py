from django.db import models
from django.conf import settings

class Question(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="questions")
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)
    def __str__(self):
        return self.question_text
    class Meta:
        verbose_name_plural = "Questions"
        ordering = ["-pub_date"]

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    #votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
    class Meta:
        verbose_name_plural = "Choices"

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votes', on_delete=models.CASCADE)
    choice = models.ForeignKey("Choice", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "choice"],
                name="unique_user_choice_vote"
            )
        ]