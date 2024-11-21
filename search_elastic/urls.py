from django.urls import path, include
from rest_framework.routers import DefaultRouter

from snippets import views

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'search', views.SnippetViewSet, basename='search')

urlpatterns = [
    path('', include(router.urls)),
]