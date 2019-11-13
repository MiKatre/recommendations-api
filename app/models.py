from sqlalchemy.orm import Session
import time

def get_ratings(db: Session):
    ratings = []
    result = db.execute(
        'SELECT api_rating.object_id, api_rating.rating, api_rating.user_id, api_movie.imdb_id, '
        'api_movietranslation.id, api_movietranslation.title '
        'FROM dbmaster.api_rating '
        'JOIN dbmaster.api_movietranslation ON dbmaster.api_rating.object_id=dbmaster.api_movietranslation.id '
        'JOIN dbmaster.api_movie ON dbmaster.api_movietranslation.movie_id=dbmaster.api_movie.id '
        'WHERE api_movie.imdb_id IS NOT null')

    for row in result:
        rating = {}
        rating['imdbId'] = row['imdb_id']
        rating['movieId'] = row['object_id'] #Movietranslation
        rating['rating'] = row['rating']
        rating['userId'] = row['user_id']
        
        ratings.append(rating)

    return ratings

def insert_recommendations(db: Session, recommendations):
    start = time.time()

    # TODO: Drop table api_recommendation (but not commit yet)
    reset_table = db.execute('DELETE FROM dbmaster.api_recommendation')

    for row in recommendations:
        user_id = row[0]
        imdb_id = row[1]
        predicted_rating = row[2]

        result = db.execute(
            'INSERT INTO dbmaster.api_recommendation (predicted_rating, movie_id, user_id) '
            'SELECT :predicted_rating, api_movie.id as movie_id, :user_id '
            'FROM dbmaster.api_movie '
            'WHERE dbmaster.api_movie.imdb_id=:imdb_id'
            , 
            {'user_id': user_id, 'imdb_id': imdb_id, 'predicted_rating': predicted_rating})
        
        print(result)

    try:
        db.commit()
    except Exception as e:
        print("Imposible to commit changes to table api_recommendation. Rolling back changes")
        db.rollback()
        db.flush() 

    print(f"Inserted {len(recommendations)} rows in {time.time() - start}s ({(time.time() - start) / 60 } minutes)")

