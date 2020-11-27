from django.contrib import admin
from .models import Restaurant, Food, RestaurantsFood, Comment, Category, Tag


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ["name", "location"]
    list_display_links = ["name", "location"]
    search_fields = ["name"]

    class Meta:
        model = Restaurant


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_display_links = ["name"]
    search_fields = ["name"]

    class Meta:
        model = Category


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["headline"]
    list_display_links = ["headline"]
    search_fields = ["headline"]

    class Meta:
        model = Tag


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "picture"]
    list_display_links = ["name", "category", "picture"]
    search_fields = ["name", "category"]

    class Meta:
        model = Food


@admin.register(RestaurantsFood)
class RestaurantsFoodAdmin(admin.ModelAdmin):
    list_display = ["restaurant", "food", "price", "score"]
    list_display_links = ["restaurant", "food", "price", "score"]

    class Meta:
        model = Food


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["food", "comment_owner", "comment_content", "comment_rate"]
    list_display_links = ["food", "comment_owner", "comment_content", "comment_rate"]
    search_fields = ["name"]

    class Meta:
        model = Comment

