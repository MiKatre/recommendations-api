# Quick access to collab filtering functionality
from fastai.collab import *
import pandas as pd

def falsify_id(user_id):
    return f"999999{user_id}"
def add_tt(movie_id):
    return f"tt{movie_id}"
    


def get_recommendations(ratings, external_dataset_path):
    external_ids = pd.read_csv(external_dataset_path/'links.csv', converters={'imdbId': str, 'tmdbId': str})
    external_ids['imdbId'] = external_ids['imdbId'].apply(add_tt)

    ml20m_ratings = pd.read_csv(external_dataset_path/'ratings.csv')
    print(ml20m_ratings.head())

    # add 999999 in front of every id of the dataset
    ml20m_ratings['userId'] = ml20m_ratings['userId'].apply(falsify_id)
    print(ml20m_ratings.head())

    # Replace movieId by imdb_id
    ratings_and_external_ids = ml20m_ratings.merge(external_ids[['imdbId', 'movieId']], left_on='movieId', right_on='movieId')
    print(ratings_and_external_ids.head())

    # add 999999 in front of every id of each movieId
    ratings_and_external_ids['movieId'] = ratings_and_external_ids['movieId'].apply(falsify_id)

    db_ratings = pd.DataFrame(ratings)
    print(db_ratings.head())

    # Append cinetimes ratings to dataset ratings 
    full_ratings = ratings_and_external_ids.append(db_ratings, sort=True)
    print(full_ratings.tail())

    return "hello"

'''
  Get the ratings from cinetimes and from ML100K
  Format and create a df with all of them (add 9999999 in front of not my id's)
  train the model
  save it to models/
'''
# async def download_file(url, dest):
#     if dest.exists(): return
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             data = await response.read()
#             with open(dest, 'wb') as f:
#                 f.write(data)


# async def setup_learner():
#     await download_file(export_file_url, path / export_file_name)
#     try:
#         learn = load_learner(path, export_file_name)
#         return learn
#     except RuntimeError as e:
#         if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
#             print(e)
#             message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
#             raise RuntimeError(message)
#         else:
#             raise


# path = untar_data(URLs.ML_SAMPLE)
# print(path)

# ratings = pd.read_csv(path/'ratings.csv')
# series2cat(ratings, 'userId', 'movieId')
# ratings.head()

# data = CollabDataBunch.from_df(ratings, seed=42)

# y_range = [0, 5.5]

# learn = collab_learner(data, n_factors=50, y_range=y_range)
# learn.fit_one_cycle(4, 5e-3)

# print(learn.predict(ratings.iloc[0]))

# def get_recommendations(user_id: int):
#     print('hello')



# def setup_dataset():
#     # Download ML100K
#     # Download latest db.ratings
#     # Add 999999 in front of ML100K ids
#     # Replace movie_id by tmdb_id
#     # Create the dataset from those two