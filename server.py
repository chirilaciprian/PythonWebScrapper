from flask import Flask, request, jsonify
import requests
from youtubesearchpython import VideosSearch
from bs4 import BeautifulSoup
import MoviesDB

def get_trailer(movie_name):
    search = VideosSearch(f"{movie_name} trailer"  , limit = 1)
    result = search.result()
    trailer = result['result'][0]['link']
    return trailer

def get_rating_and_reviews_from_rotten_tomatoes(movie_name):
    html = requests.get(f"https://www.rottentomatoes.com/search?search={movie_name}")
    soup = BeautifulSoup(html.text, 'html.parser')
    tmp_link = soup.findAll('search-page-media-row')
    cast = tmp_link[0].get('cast')
    year = tmp_link[0].get('releaseyear')
    movie_name = tmp_link[0].findAll('a')[1].text.strip()
    result = tmp_link[0].find('a')
    html = requests.get(result.get('href'))
    soup = BeautifulSoup(html.text, 'html.parser')
    # print(soup.find('score-board-deprecated').find('h1').text)
    rating = soup.find('score-board-deprecated').get('audiencescore')
    mdb.insert_into_db(movie_name, rating, year,cast)
    reviews = soup.findAll('review-speech-balloon-deprecated')[:5]
    reviews_dict = {}
    for review in reviews:
        quote =  review.get('reviewquote')
        critic_name = review.findAll('a')[1].text.strip()
        reviews_dict[critic_name] = quote
    return reviews_dict,rating,movie_name
    
mdb = MoviesDB.MovieDb()
app = Flask(__name__)

@app.route("/movies/<movie_name>", methods=["GET"])
def get_movie(movie_name):
    rating = mdb.find_rating_by_title(movie_name)
    if rating is None:
        _,rating,movie_name = get_rating_and_reviews_from_rotten_tomatoes(movie_name)
    movie_data={
        "trailer": get_trailer(movie_name),
        "Movie Name": movie_name,
        "rating": rating,
    }
    return jsonify(movie_data),200

@app.route("/actors/<actor_name>", methods=["GET"])
def get_actor(actor_name):
    actor_data=mdb.find_title_by_actor(actor_name)
    return jsonify(actor_data),200

@app.route("/reviews/<movie_name>", methods=["GET"])
def get_reviews(movie_name):
    reviews,_,name = get_rating_and_reviews_from_rotten_tomatoes(movie_name)
    return jsonify(reviews,name),200

if __name__ == '__main__':
    app.run(debug=True)