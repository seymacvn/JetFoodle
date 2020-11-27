from django.core.management.base import BaseCommand
from system.models import Comment


class Command(BaseCommand):

    def handle(self, *args, **options):
        file = open("rating.txt", "w")
        comments = Comment.objects.all()
        for comment in comments:
            food = comment.food                                             #restaurantsfood objesi
            comment_owner = comment.comment_owner
            comment_rate = comment.comment_rate
            line = str(food.id) + ", " + str(comment_owner.id) + ", " + str(comment_rate) + " \n"
            file.write(line)
