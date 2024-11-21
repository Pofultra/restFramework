from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import SnippetDocument

class SnippetDocumentSerializer(DocumentSerializer):
    class Meta:
        document = SnippetDocument
        fields = (
            'id',
            'title',
            'code',
            # 'linenos',
            'language',
            # 'style',
            'created',
            'owner',
        )
