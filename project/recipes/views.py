from .models import Recipe
from rest_framework import viewsets
from recipes.serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        name_search = self.request.query_params.get('name')
        description_search = self.request.query_params.get('description')

        queryset = Recipe.objects.all()

        queryset = queryset.filter(name__contains=name_search) if name_search else queryset
        queryset = queryset.filter(description__contains=description_search) if description_search else queryset

        return queryset