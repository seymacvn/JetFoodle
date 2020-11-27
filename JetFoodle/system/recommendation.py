import pandas as pd


def food_recommendation(users_comments):
    foods_df = pd.read_csv("system/data/foods.csv").copy()
    ratings_df = pd.read_csv("system/data/rating.csv").copy()
    foods_copy = foods_df.copy(deep=True)
    user_food_ratings = users_comments
    user_food_ratings = pd.DataFrame(user_food_ratings)
    user_food_id = foods_df[foods_df['food_id'].isin(user_food_ratings['food_id'])]
    user_food_ratings = pd.merge(user_food_id, user_food_ratings)
    user_df = foods_copy[foods_copy.food_id.isin(user_food_ratings.food_id)]
    user_df.reset_index(drop=True, inplace=True)
    user_df.drop(['food_id'], axis=1, inplace=True)
    user_profile = user_df.T.dot(user_food_ratings.rate)
    foods_copy = foods_copy.set_index(foods_copy.food_id)
    foods_copy.drop(['food_id'], axis=1, inplace=True)
    recommendation_table_df = (foods_copy.dot(user_profile)) / user_profile.sum()
    recommendation_table_df.sort_values(ascending=False, inplace=True)
    copy = foods_df.copy(deep=True)
    copy = copy.set_index('food_id', drop=True)
    top_20_index = recommendation_table_df.index[:].tolist()
    return top_20_index
