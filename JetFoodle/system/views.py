import null as null
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.views import View
from django.views.generic import ListView
from system.models import Restaurant, Food, RestaurantsFood, Comment, Category
from .forms import RestaurantForm, RestaurantsFoodForm
from .recommendation import food_recommendation


class Index(View):
    @staticmethod
    def get(request):
        return render(request, "index.html")


class YourRestaurants(View):
    @staticmethod
    @login_required(login_url="user:login")
    def get(request):
        restaurants = Restaurant.objects.filter(owner=request.user)
        return render(request, "dashboard.html", {"restaurants": restaurants})


class Detail(View):
    @staticmethod
    @login_required(login_url="user:login")
    def get(request, RestId):
        restaurant = Restaurant.objects.get(id=RestId)
        menu = RestaurantsFood.objects.filter(restaurant=restaurant)
        return render(request, "detailRestaurant.html", {"restaurant": restaurant, "menu": menu})


class DeleteRestaurant(View):
    @staticmethod
    @login_required(login_url="user:login")
    def get(request, rest_id):
        restaurant = get_object_or_404(Restaurant, id=rest_id)
        restaurant.delete()
        messages.success(request, "Restaurant Başarıyla Silindi..")
        return redirect("system:your_restaurants")


class DeleteFood(View):
    @staticmethod
    @login_required(login_url="user:login")
    def get(request, RestId, FoodId):
        food = get_object_or_404(RestaurantsFood, id=FoodId)
        food.delete()
        messages.success(request, "Yemek Başarıyla Silindi..")
        return redirect("system:detail", RestId=RestId)


class AddFood(View):
    @staticmethod
    @login_required(login_url="user:login")
    def get(request, rest_id):
        form = RestaurantsFoodForm(request.POST, request.FILES or None)
        context = {
            "form": form
        }
        return render(request, "addFood.html", context)

    @staticmethod
    def post(request, rest_id):
        form = RestaurantsFoodForm(request.POST, request.FILES or None)
        if form.is_valid():
            food = form.save(commit=False)
            food.restaurant = Restaurant.objects.get(id=rest_id)
            if food.score:
                food.save()
            else:
                food.score = 0
                food.missing_points = 5
                food.save()
            messages.success(request, "Yemek Başarıyla Eklendi..")
            restaurant = Restaurant.objects.get(id=rest_id)
            menu = RestaurantsFood.objects.filter(restaurant=restaurant)
            return render(request, "detailRestaurant.html", {"restaurant": restaurant, "menu": menu})


class AddRestaurant(View):
    @staticmethod
    @login_required(login_url="user:login")
    def get(request):
        form = RestaurantForm(request.POST or None)
        context = {
            "form": form
        }
        return render(request, "addRestaurant.html", context)

    @staticmethod
    def post(request):
        form = RestaurantForm(request.POST or None)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            restaurant.save()
            messages.success(request, "Restoran Başarıyla Oluşturuldu..")
            restaurants = Restaurant.objects.filter(owner=request.user)
            return render(request, "dashboard.html", {"restaurants": restaurants})


class AllRestaurants(ListView):
    model = Restaurant
    template_name = 'AllRestaurants.html'
    context_object_name = 'restaurants'
    paginate_by = 10
    queryset = Restaurant.objects.all()


class SelectedRestaurant(View):
    @staticmethod
    def get(request, rest_id):
        restaurant = Restaurant.objects.get(id=rest_id)
        menu = RestaurantsFood.objects.filter(restaurant=restaurant)
        return render(request, "SelectedRestaurant.html", {"restaurant": restaurant, "menu": menu})


class AllFoods(View):
    @staticmethod
    def get(request):
        foods = Food.objects.all()
        return render(request, "AllFoods.html", {"foods": foods})


class SelectedFood(View):
    @staticmethod
    def get(request, food_id):
        food = Food.objects.get(id=food_id)
        restaurant_foods = RestaurantsFood.objects.filter(food=food)
        food_items = restaurant_foods.order_by('price')
        return render(request, "SelectedFood.html", {"food": food, "food_items": food_items})


class SearchRestaurantView(View):
    model = Restaurant
    template_name = 'SearchedRestaurants.html'

    @staticmethod
    def get(request):
        keyword = request.GET.get('keyword')
        object_list = Restaurant.objects.filter(Q(name__icontains=keyword) | Q(location__icontains=keyword))
        return render(request, "SearchedRestaurants.html", {"restaurants": object_list, "keyword": keyword})


class SearchFoodView(View):
    model = Food
    template_name = 'SearchedFoods.html'

    @staticmethod
    def get(request):
        keyword = request.GET.get('keyword')
        object_list = Food.objects.filter(Q(name__icontains=keyword))
        return render(request, "SearchedFoods.html", {"foods": object_list, "keyword": keyword})


class SearchCategoryFood(View):
    model = Food
    template_name = 'SearchedFoods.html'

    @staticmethod
    def get(request):
        keyword = request.GET.get('keyword')
        category_name = request.GET.get('category')
        object_list = Food.objects.filter(Q(name__icontains=keyword) and Q(category=category_name))
        return render(request, "SearchedFoods.html", {"foods": object_list, "keyword": keyword})


class DetailFood(View):
    @staticmethod
    def get(request, FoodId):
        restaurants_food = RestaurantsFood.objects.get(id=FoodId)
        comments = restaurants_food.comments.all()
        return render(request, "DetailFoods.html", {"restaurants_food": restaurants_food, "comments": comments, "user": request.user})


def score_calculation(restaurants_food, comment_rate):
    total_points = restaurants_food.total_points + int(comment_rate)
    new_score = (total_points / (restaurants_food.score_count + 1))
    restaurants_food.score = new_score
    restaurants_food.missing_points = 5-int(new_score)
    restaurants_food.total_points = total_points
    restaurants_food.score_count = restaurants_food.score_count + 1
    restaurants_food.save()


class AddComment(View):
    @staticmethod
    @login_required(login_url="user:login")
    def post(request, FoodId):
        restaurants_food = get_object_or_404(RestaurantsFood, id=FoodId)
        comments = restaurants_food.comments.all()
        comment_rate = int(request.POST.get("comment_rate"))
        comment_control = Comment.objects.filter(comment_owner=request.user, food=restaurants_food)

        if comment_control:
            messages.warning(request, 'Bu ürünü daha önce değerlendirmişsiniz.')
            return render(request, "DetailFoods.html", {"restaurants_food": restaurants_food, "comments": comments})

        elif comment_rate < 0 or comment_rate > 5:
            messages.warning(request, 'Verdiğiniz puan 0-5 aralığında olmalıdır.')
            return render(request, "DetailFoods.html", {"restaurants_food": restaurants_food, "comments": comments})

        else:
            comment_content = request.POST.get("comment_content")
            new_comment = Comment(comment_rate=comment_rate, comment_content=comment_content, comment_missing_rate=5-comment_rate)
            new_comment.food = restaurants_food
            new_comment.comment_owner = request.user
            score_calculation(restaurants_food, comment_rate)
            new_comment.save()
            return render(request, "DetailFoods.html", {"restaurants_food": restaurants_food, "comments": comments})


class SelectedCategory(View):
    @staticmethod
    def get(request, category_name):
        food_category = get_object_or_404(Category, name=category_name)
        foods = Food.objects.filter(category=food_category)
        return render(request, "SelectedCategory.html", {"foods": foods, "category": category_name})


class RecommenderSystem(View):
    @staticmethod
    def get(request):
        comments = Comment.objects.filter(comment_owner=request.user)
        user_comment = []
        for comment in comments:
            food = comment.food
            comment_owner = comment.comment_owner
            comment_rate = comment.comment_rate
            line = {"food_id": food.id, "owner_id": comment_owner.id, "rate": comment_rate}
            user_comment.append(line)
        food_name = []
        foods_index = []
        top_20_index = food_recommendation(user_comment)
        for food_id in top_20_index:
            restaurant_food = get_object_or_404(RestaurantsFood, id=food_id)
            food = restaurant_food.food
            if food.name in food_name:
                pass
            else:
                foods_index.append(food_id)
                food_name.append(food.name)

        foods_index = foods_index[:9]
        foods = RestaurantsFood.objects.filter(pk__in=foods_index)
        first = foods[0:3]
        second = foods[3:6]
        third = foods[6:9]
        return render(request, "FoodRecommendation.html", {"foods": foods, "first": first, "second": second, "third": third})


class DeleteComment(View):
    @staticmethod
    def get(request, comment_id, food_id):
        comment = get_object_or_404(Comment, id=comment_id)
        restaurants_food = get_object_or_404(RestaurantsFood, id=food_id)
        restaurants_food.score_count = restaurants_food.score_count - 1
        restaurants_food.total_points = restaurants_food.total_points - comment.comment_rate
        if restaurants_food.score_count != 0:
            restaurants_food.score = restaurants_food.total_points / restaurants_food.score_count
        else:
            restaurants_food.score = 0
        restaurants_food.missing_points = 5 - int(restaurants_food.score)
        restaurants_food.save()
        comment.delete()
        if restaurants_food.score_count != 0:
            comments = restaurants_food.comments.all()
        else:
            comments = null
        messages.success(request, "Yorum Başarıyla Silindi..")
        return render(request, "DetailFoods.html", {"restaurants_food": restaurants_food, "comments": comments, "user": request.user})


class YourComments(View):
    @staticmethod
    def get(request):
        comments = Comment.objects.filter(comment_owner=request.user)
        return render(request, "YourComments.html", {"comments": comments})


class UpdateRestaurant(View):
    @staticmethod
    def get(request, rest_id):
        restaurant = get_object_or_404(Restaurant, id=rest_id)
        form = RestaurantForm(request.POST or None, instance=restaurant)
        return render(request, "UpdateRestaurant.html", {"form": form})

    @staticmethod
    def post(request, rest_id):
        restaurant = get_object_or_404(Restaurant, id=rest_id)
        form = RestaurantForm(request.POST or None, instance=restaurant)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            restaurant.save()
            messages.success(request, "Restoran başarıyla güncellendi.")
            restaurants = Restaurant.objects.filter(owner=request.user)
            return render(request, "dashboard.html", {"restaurants": restaurants})

