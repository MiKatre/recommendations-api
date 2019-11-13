# Quick access to collab filtering functionality
from fastai.collab import *
#from fastai.tabular import *
from .gdrive import GDrive
import pandas as pd
import time

path = Path('app/data/')

def falsify_id(user_id):
    return f"999999{user_id}"
def add_tt(movie_id):
    return f"tt{movie_id}"
    

def create_dataset(ratings, external_dataset_path):
    start = time.time()

    external_ids = pd.read_csv(external_dataset_path/'links.csv', converters={'imdbId': str, 'tmdbId': str})
    external_ids['imdbId'] = external_ids['imdbId'].apply(add_tt)

    movies = pd.read_csv(external_dataset_path/'movies.csv')

    external_ids = external_ids.merge(movies, left_on='movieId', right_on='movieId')

    ml20m_ratings = pd.read_csv(external_dataset_path/'ratings.csv')

    ml20m_ratings = ml20m_ratings[:5000000] # First 5M

    # add 999999 in front of every id of the dataset
    ml20m_ratings['userId'] = ml20m_ratings['userId'].apply(falsify_id)

    # Replace movieId by imdb_id
    ratings_and_external_ids = ml20m_ratings.merge(external_ids[['imdbId', 'movieId']], left_on='movieId', right_on='movieId')

    # add 999999 in front of every id of each movieId
    ratings_and_external_ids['movieId'] = ratings_and_external_ids['movieId'].apply(falsify_id)

    db_ratings = pd.DataFrame(ratings)

    # Append cinetimes ratings to dataset ratings 
    full_ratings = ratings_and_external_ids.append(db_ratings, sort=True)

    full_ratings = full_ratings.merge(external_ids, left_on='imdbId', right_on='imdbId')

    # Only keep columns that are relevant (more will be later)
    full_ratings = full_ratings[['imdbId', 'rating', 'userId']]
    print(full_ratings.count())
    print(full_ratings.tail())

    full_ratings.to_csv(index=False, path_or_buf=path/'cinetimes-dataset.csv')

    google_drive = GDrive()
    google_drive.upload_data()

    print(f"Predictions uploaded in {time.time() - start} ({(time.time() - start) /60}mn)")
    return full_ratings

def get_available_predictions():
    google_drive = GDrive()
    google_drive.download_predictions()
    df = pd.read_csv(path/'predictions.csv')
    prediction_list = df.values.tolist() # [[user_id, imdb_id, predicted_rating]...]

    return prediction_list
    

def fully_retrain_model_and_update_recommendations(ratings, external_dataset_path):
    ratings = create_dataset(ratings, external_dataset_path)

    ###################
    # Train the model #
    ###################

    data = CollabDataBunch.from_df(ratings, seed=42, valid_pct=0.1, bs=128)
    y_range = [0,5.5]
    learn = collab_learner(data, n_factors=40, y_range=y_range, wd=1e-1)
    learn.lr_find()
    learn.recorder.plot(skip_end=15)
    learn.fit_one_cycle(5, 5e-3)
    learn.save('prodmodel')


    ########################
    # Make recommendations #
    ########################
    
    # Only keep my users
    all_users = ratings.loc[ratings['userId'] < 999999]

    # Get array of users id
    my_users = all_users['userId'].unique()

    # Get array of all movies id
    all_movie_ids = ratings['imdbId'].unique()

    data = []
    for user_id in my_users:
        # Get list of all movies rated by the userId
        user_rated_rows = ratings.loc[ratings['userId'] == user_id]
        user_rated_ids = user_rated_rows['imdbId'].unique()
    
        # Remove the movie_ids that user_x has rated from the list of all movie ids
        movie_ids_to_pred = np.setdiff1d(all_movie_ids, user_rated_ids)
        
        # Create a dataframe with movies not rated by user
        
        for movie_id in movie_ids_to_pred:
            data.append({
                'userId': user_id,
                'imdbId': movie_id,
                'rating': None,
            })
        
    df_to_predict = pd.DataFrame(data=data)

    # Predict
    predictions = []
    for idx in range(len(df_to_predict)):
        row = df_to_predict.iloc[idx]
        movie_id = row['imdbId']
        user_id = row['userId']
        y, pred, raw_pred = learn.predict(row)
        prediction = {'userId': user_id, 'movie_id': movie_id, 'prediction': pred.item()}
        predictions.append(prediction)
        if pred.item() > 4.0: 
            print(movie_id, pred.item())

    # Sort predictions
    full_predictions = pd.DataFrame(predictions)
    sorted_predictions = full_predictions.sort_values(by='prediction', ascending=False)


    sorted_filtered_predictions = sorted_predictions[0:0]
    for user_id in my_users:
        this_user_df = sorted_predictions.loc[sorted_predictions['userId'] == user_id]
        # Limit to the 500 first recommendations
        this_user_df = this_user_df[0:500]
        sorted_filtered_predictions = sorted_filtered_predictions.append(this_user_df)

    return sorted_filtered_predictions.values.tolist()# [[user_id, imdb_id, predicted_rating]...]














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