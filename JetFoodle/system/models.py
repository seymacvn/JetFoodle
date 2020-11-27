from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Kategori")

    def __str__(self):
        return self.name


class Tag(models.Model):
    headline = models.CharField(max_length=20, verbose_name="Tag İsmi")

    def __str__(self):
        return self.headline


class Food(models.Model):
    name = models.CharField(max_length=50, verbose_name="Yemek")
    picture = models.ImageField(upload_to="images", null=True, blank=True, verbose_name="Resim")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name="Yemek Kategorisi")
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Sahibi")
    name = models.CharField(max_length=50, verbose_name="Restaurant İsmi")
    location = models.CharField(max_length=50, verbose_name="Konum")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class RestaurantsFood(models.Model):
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE, verbose_name="Restoran")
    food = models.ForeignKey("Food", on_delete=models.CASCADE, verbose_name="Yemek")
    price = models.FloatField(verbose_name="Fiyat")
    score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], blank=True)
    score_count = models.IntegerField(default=0, verbose_name="Puanlayan kişi sayısı")
    total_points = models.IntegerField(default=0)
    missing_points = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(5)], blank=True)

    def __str__(self):
        return self.restaurant.name


class Comment(models.Model):
    food = models.ForeignKey("RestaurantsFood", on_delete=models.CASCADE, related_name="comments")
    comment_owner = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="yorum_sahibi")
    comment_content = models.CharField(max_length=200, verbose_name="yorum")
    comment_rate = models.IntegerField(default=3, validators=[MinValueValidator(0), MaxValueValidator(5)], blank=True)
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_missing_rate = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], blank=True)

    def __str__(self):
        return self.comment_content

    class Meta:
        ordering = ['-comment_date']



