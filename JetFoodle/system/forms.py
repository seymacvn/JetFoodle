from django import forms
from .models import Restaurant, Food, RestaurantsFood


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ["name", "location"]


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ["name", "picture"]


class RestaurantsFoodForm(forms.ModelForm):
    class Meta:
        model = RestaurantsFood
        fields = ["food", "price"]

