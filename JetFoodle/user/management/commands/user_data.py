from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
import csv


class Command(BaseCommand):

    def handle(self, *args, **options):

        with open('user/management/commands/user.csv', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                username = row[0]
                password = row[1]
                new_user = User(username=username)
                new_user.set_password(password)
                new_user.save()

