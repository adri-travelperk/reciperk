from django.urls import include, path
from rest_framework import routers
from recipes import views

router = routers.DefaultRouter()
router.register(r'recipes', views.RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

