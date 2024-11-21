from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
)
from .serializers import SnippetDocumentSerializer
from .documents import SnippetDocument


class SnippetViewSet(DocumentViewSet):
    document = SnippetDocument
    serializer_class = SnippetDocumentSerializer
    lookup_field = "id"

    # Puedes agregar filtros personalizados aquí
    filter_backends = [
        FilteringFilterBackend,
    ]

    # Ejemplo de filtros personalizados
    search_fields = (
        "title",
        "code",
    )
    filter_fields = {
        "linenos": "linenos",
        "language": "language",
        "style": "style",
        "created": "created",
        "owner": "owner",
    }
