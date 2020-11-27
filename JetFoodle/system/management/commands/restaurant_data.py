from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
import csv

from django.shortcuts import get_object_or_404

from system.models import Restaurant


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Restaurant.objects.all().delete()"""

        with open('system/management/commands/restaurants.csv', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                name = row[0]
                location = row[1]
                owner = get_object_or_404(User, username=row[2])
                new_restaurant = Restaurant(name=name, location=location, owner=owner)
                new_restaurant.save()
