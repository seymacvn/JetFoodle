from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_object_or_404
from system.models import Restaurant, Food, RestaurantsFood, Comment
import csv
from system.views import score_calculation


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('system/management/commands/comment.csv', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                row = [x.strip(' ') for x in row]
                restaurant = get_object_or_404(Restaurant, name=row[0])
                food = get_object_or_404(Food, name=row[1])
                comment_owner = get_object_or_404(User, username=row[2])
                restaurant_foods = get_object_or_404(RestaurantsFood, restaurant=restaurant, food=food)
                new_comment = Comment(food=restaurant_foods, comment_owner=comment_owner, comment_rate=row[3], comment_missing_rate=5-int(row[3]), comment_content=row[4])
                new_comment.save()
                score_calculation(restaurant_foods, row[3])

