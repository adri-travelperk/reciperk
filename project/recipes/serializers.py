from .models import Recipe, Ingredient
from rest_framework import serializers


class IngredientNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientNameSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'ingredients']
        read_only_fields = ('id',)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe(**validated_data)
        recipe.save()

        for ingredient_dict in ingredients:
            name = ingredient_dict.get('name')
            ingredient = Ingredient(name=name, recipe=recipe)
            ingredient.save()

        return RecipeSerializer(recipe).data

    def update(self, instance, validated_data):
        recipe = instance
        if 'description' in validated_data:
            recipe.description = validated_data.get('description')
            recipe.save()

        if 'ingredients' in validated_data:
            Ingredient.objects.filter(recipe__id=recipe.id).delete()
            for ingredient_dict in validated_data.get('ingredients'):
                name = ingredient_dict.get('name')
                ingredient = Ingredient(name=name, recipe=recipe)
                ingredient.save()

        return RecipeSerializer(recipe).data