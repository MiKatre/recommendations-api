from sqlalchemy.orm import Session

def get_ratings(db: Session):
    # result = db.execute('SELECT count(*) FROM dbmaster.api_movie')
    ratings = []
    result = db.execute(
        'SELECT api_movie.id as movie_id, api_movie.imdb_id, api_rating.* '
        'FROM dbmaster.api_rating JOIN dbmaster.api_movie '
        'ON dbmaster.api_rating.object_id=dbmaster.api_movie.id '
        'WHERE api_movie.imdb_id IS NOT null')

    for row in result:
        rating = {}
        rating['imdbId'] = row['imdb_id']
        rating['movieId'] = row['movie_id']
        rating['rating'] = row['rating']
        rating['userId'] = row['user_id']
        # rating['rating_id'] = row['id']
        # rating['headline'] = row['headline']
        # rating['content'] = row['content']
        # rating['pub_date'] = row['pub_date']
        ratings.append(rating)

    return ratings