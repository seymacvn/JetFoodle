from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_object_or_404
from system.models import Restaurant, Food, RestaurantsFood
import csv


class Command(BaseCommand):

    def handle(self, *args, **options):

        with open('system/management/commands/menu.csv', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                row = [x.strip(' ') for x in row]
                restaurant = get_object_or_404(Restaurant, name=row[0])
                food = get_object_or_404(Food, name=row[1])
                new_food = RestaurantsFood(restaurant=restaurant, food=food)
                new_food.price = row[2]
                new_food.save()

