from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from snippets.models import Snippet


@registry.register_document
class SnippetDocument(Document):
    # owner_name = fields.TextField()

    class Index:
        name = "snippets"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Snippet
        fields = [
            "id",
            "title",
            "code",
            "linenos",
            "language",
            "style",
            "created",
            # "owner",
        ]

    # def prepare_owner_name(self, instance):
    #     return instance.owner.id
