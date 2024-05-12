from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SnippetViewSet, TagDetailAPIView, TagListAPIView

router = DefaultRouter()
router.register(r'snippets', SnippetViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tags/', TagListAPIView.as_view(), name='tag-list'),
    path('tag_snippet/<str:tag_name>/', TagDetailAPIView.as_view(), name='tag-detail'),
]
