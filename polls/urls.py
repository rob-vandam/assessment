from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import QuestionViewSet

router = DefaultRouter()
router.register("questions", QuestionViewSet, basename="questions")

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name="api-token-auth"),
    path('', include(router.urls)),
]