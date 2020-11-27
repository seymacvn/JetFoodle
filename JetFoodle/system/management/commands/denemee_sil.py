from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from system.models import Comment


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = get_object_or_404(User, username="seyma")
        comments = Comment.objects.filter(comment_owner=user)
        a = []
        for comment in comments:
            food = comment.food                                             #restaurantsfood objesi
            comment_owner = comment.comment_owner
            comment_rate = comment.comment_rate
            line = {"food_id": food.id, "owner_id": comment_owner.id, "rate": comment_rate}
            a.append(line)

        print(a)


