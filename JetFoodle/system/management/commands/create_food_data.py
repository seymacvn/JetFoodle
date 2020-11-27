from django.core.management.base import BaseCommand
from system.models import Comment, RestaurantsFood


def search(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False


class Command(BaseCommand):

    def handle(self, *args, **options):
        tags = ["#pizza", "#kakaolu", "#kek", "#meyveli_tatlı", "#sütlü_tatlı", "#şerbetli_tatlı", "#vejeteryan",
                "#vegan", "#balık", "#tavuk", "#et", "#sebze", "#zeytinyaglı", "#fit", "#yöresel_lezzetler",
                "#kızartma", "#yaglı", "#saglıklı", "#kebap", "#patates", "#kıyma", "#eksi", "#acı", "#tuzlu", "#tatlı",
                "#soğuk", "#sıcak", "#fast_food", "#ev_yemegi", "#köfte"]

        file = open("foods.txt", "w")
        restaurant_foods = RestaurantsFood.objects.all()
        for restaurant_food in restaurant_foods:
            line = str(restaurant_food.id)
            food = restaurant_food.food
            foods_tag = food.tags.all()
            tag_array = []
            for tag in foods_tag:
                tag_array.append(tag.headline)

            for tag in tags:
                if search(tag_array, tag):
                    line = line + ", 1"
                else:
                    line = line + ", 0"

            line = line + " \n"
            file.write(line)
