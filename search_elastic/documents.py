from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from snippets.models import Snippet

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])



@registry.register_document
class SnippetDocument(Document):

    class Index:
        name = 'snippets'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    owner = fields.ObjectField(
        properties={
            "id": fields.IntegerField(),
            "username": fields.TextField(),
        }
    )
    highlighted = fields.TextField()
    created = fields.DateField()
    title = fields.TextField()
    code = fields.TextField()
    linenos = fields.BooleanField()
    language = fields.KeywordField()
    style = fields.KeywordField()

    class Django:
        model = Snippet
