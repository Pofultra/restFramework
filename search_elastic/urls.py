from rest_framework.routers import SimpleRouter

from .views import SnippetViewSet

router = SimpleRouter()

router.register("documents", SnippetViewSet, basename="snippet-search")

urlpatterns = router.urls