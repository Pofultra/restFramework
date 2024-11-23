import copy
from abc import abstractmethod
from datetime import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from elasticsearch_dsl import Document, Q
from elasticsearch.exceptions import ConnectionError as ESConnectionError

from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from .documents import SnippetDocument
from .serializers import SnippetDocumentSerializer
from snippets.models import Snippet


class PaginatedElasticSearchAPIView(ModelViewSet, LimitOffsetPagination):
    document_class: Document = None

    @abstractmethod
    def generate_search_query(self, search_terms_list, param_filters):
        """This method should be overridden
        and return a Q() expression."""

    @action(methods=["GET"], detail=False)
    def search(self, request: Request):
        try:
            # Obtener los parámetros de la solicitud
            params = request.query_params

            # Obtener los términos de búsqueda
            search_terms = params.get("search", "")

            # Obtener los filtros
            param_filters = {
                key: value for key, value in params.items() if key != "search"
            }

            # Generar la query de búsqueda
            query = self.generate_search_query(search_terms, param_filters)

            # Ejecutar la búsqueda
            search = self.document_class.search().query(query)

            # Obtener los resultados de la búsqueda
            results = search.execute()

            # Serializar los resultados
            serializer = self.serializer_class(results, many=True)

            # Devolver la respuesta
            return Response(serializer.data)

        except ESConnectionError:
            return Response(
                {"error": "Connection error with the search service"}, status=503
            )
        except Exception as e:
            return Response({"error": f"Internal server error: {str(e)}"}, status=500)


class SnippetViewSet(PaginatedElasticSearchAPIView):
    document_class = SnippetDocument
    serializer_class = SnippetDocumentSerializer
    queryset = Snippet.objects.all()

    def generate_search_query(self, search_terms=None, param_filters={}):
        must_queries = []
        filter_queries = []

        # Text search
        if search_terms:
            must_queries.append(
                Q(
                    "multi_match",
                    query=search_terms,
                    fields=["title^2", "code"],
                    type="best_fields",
                    minimum_should_match="75%",
                )
            )

        # date filter
        if (
            param_filters.get("created_gte") is not None
            or param_filters.get("created_lte") is not None
        ):
            created_range = {}
            if param_filters.get("created_gte") is not None:
                created_range["gte"] = param_filters.get("created_gte")
            if param_filters.get("created_lte") is not None:
                created_range["lte"] = param_filters.get("created_lte")
            filter_queries.append(Q("range", created=created_range))

        # language filter
        if param_filters.get("language") is not None:
            filter_queries.append(Q("term", language=param_filters.get("language")))
        # style filter
        if param_filters.get("style") is not None:
            filter_queries.append(Q("term", style=param_filters.get("style")))

        # owner filter
        if param_filters.get("owner") is not None:
            filter_queries.append(Q('term', owner__username=param_filters.get("owner") ))
        # Build the complete query
        if must_queries or filter_queries:
            complte_query = Q(
                "bool",
                must=must_queries if must_queries else [Q("match_all")],
                filter=filter_queries,
            )

        return complte_query
