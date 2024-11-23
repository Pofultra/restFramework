from rest_framework import serializers

from snippets.models import Snippet
from .documents import SnippetDocument

class SnippetDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        document = SnippetDocument
        fields = [
            'owner',
            'highlighted',
            'created',
            'title',
            'code',
            'linenos',
            'language',
            'style',
        ]

    def to_representation(self, instance):
        data = instance
        # data = super().to_representation(instance)
        if isinstance(instance.owner, dict):
            data['owner'] = {
                'id': instance.owner['id'],
                'username': instance.owner['username'],
            }
        else:
            data['owner'] = {
                'id': instance.owner.id,
                'username': instance.owner.username,
            }
        return data