from django.contrib import admin
from django.urls import path
from . import views

app_name = "system"

urlpatterns = [
    path('yourRestaurants/', views.YourRestaurants.as_view(), name="your_restaurants"),
    path('restaurant/<int:RestId>', views.Detail.as_view(), name="detail"),
    path('delete_restaurant/<int:rest_id>', views.DeleteRestaurant.as_view(), name="DeleteRestaurant"),
    path('delete_food/<int:RestId>/<int:FoodId>', views.DeleteFood.as_view(), name="delete_food"),
    path('add_food/<int:rest_id>', views.AddFood.as_view(), name="addFood"),
    path('addRestaurant/', views.AddRestaurant.as_view(), name="addRestaurant"),
    path('all-restaurants/', views.AllRestaurants.as_view(), name='AllRestaurants'),
    path('all-foods/', views.AllFoods.as_view(), name="AllFoods"),
    path('selected-restaurant/<int:rest_id>', views.SelectedRestaurant.as_view(), name="SelectedRestaurant"),
    path('selected-food/<int:food_id>', views.SelectedFood.as_view(), name="SelectedFood"),
    path('detail-food/<int:FoodId>', views.DetailFood.as_view(), name="DetailFood"),
    path('search/', views.SearchRestaurantView.as_view(), name='search_results'),
    path('searchfood/', views.SearchFoodView.as_view(), name='search_food_results'),
    path('search-category-food/', views.SearchCategoryFood.as_view(), name='search_category_food_results'),
    path('comment/<int:FoodId>', views.AddComment.as_view(), name='add_comment'),
    path('selected-category/<str:category_name>', views.SelectedCategory.as_view(), name='selected_category'),
    path('recommendation', views.RecommenderSystem.as_view()),
    path('delete_comment/<int:comment_id>/<int:food_id>', views.DeleteComment.as_view(), name="delete_comment"),
    path('your-comments', views.YourComments.as_view(), name="your_comments"),
    path('update-restaurant/<int:rest_id>', views.UpdateRestaurant.as_view(), name="update_restaurant"),

]
