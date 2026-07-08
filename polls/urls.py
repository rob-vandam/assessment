from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import QuestionViewSet, VoteViewSet

router = DefaultRouter()
router.register("questions", QuestionViewSet, basename="questions")
router.register("votes", VoteViewSet, basename="votes")

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name="api-token-auth"),
    path('', include(router.urls)),
]