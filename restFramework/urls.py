from django.urls import path, include


urlpatterns = [
    path('', include('snippets.urls')),
    path('elastic/', include('search_elastic.urls')),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]