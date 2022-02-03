from django.urls import reverse
from rest_framework.test import APITestCase
from recipes.models import Recipe
from rest_framework import status


class AccountTests(APITestCase):
    fixtures = ['recipes/fixtures/recipes.yaml']
    recipes_url = reverse('recipes-list')
    recipe_id = '3c6a5111-c335-4f39-80ce-ca80bbefb410'
    filter_recipe_id = '3c6a5111-c335-4f39-80ce-ca80bbefb411'
    recipe_url = f'{recipes_url}{recipe_id}/'

    def test_get_recipe(self):
        response = self.client.get(self.recipe_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('name'), 'Fixture Test Recipe')

    def test_create_recipe(self):
        data = {
            "name": "Added Recipe",
            "description": "A recipe that has been added.",
            "ingredients": [
                {"name": "Added ingredient #1"},
                {"name": "Added ingredient #2"}
            ]
        }
        response = self.client.post(self.recipes_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 3)
        self.assertTrue(Recipe.objects.get(name='Added Recipe'))

    def test_list_recipes(self):
        response = self.client.get(self.recipes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_search_recipes_name(self):
        url_with_params = self.recipes_url + '?name=Filter'
        response = self.client.get(url_with_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0].get('id'), self.filter_recipe_id)

    def test_search_recipes_description(self):
        url_with_params = self.recipes_url + '?description=filtering'
        response = self.client.get(url_with_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0].get('id'), self.filter_recipe_id)

    def test_edit_recipe(self):
        data = {
            "description": "A recipe description that has been modified.",
            "ingredients": []
        }
        response = self.client.patch(self.recipe_url, data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response_data.get('description'), "A recipe description that has been modified.")
        self.assertEqual(response_data.get('ingredients'), [])

        self.assertEqual(Recipe.objects.get(pk=self.recipe_id).description, "A recipe description that has been modified.")
        self.assertEqual(Recipe.objects.get(pk=self.recipe_id).ingredients.count(), 0)

    def test_delete_recipe(self):
        self.assertEqual(Recipe.objects.filter(pk=self.recipe_id).count(), 1)
        response = self.client.delete(self.recipe_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.filter(pk=self.recipe_id).count(), 0)


