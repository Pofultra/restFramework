from django_filters import rest_framework as filters
from .models import Snippet, LANGUAGE_CHOICES


class SnippetFilter(filters.FilterSet):
    owner = filters.CharFilter(field_name="owner__username", lookup_expr="icontains")
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    created__gte = filters.DateTimeFilter(field_name="created", lookup_expr="gte")
    created__lte = filters.DateTimeFilter(field_name="created", lookup_expr="lte")
    language = filters.ChoiceFilter(field_name="language", choices=LANGUAGE_CHOICES)

    class Meta:
        model = Snippet
        fields = ["owner", "title", "created__gte", "created__lte", "language"]
