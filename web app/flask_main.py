from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, g, jsonify
import sys
import requests
from flask_config import SECRET_KEY, API_KEY_OMBDB, DEBUG_STATUS
import base64
sys.path.append('D:/Kinopoisk project')
from mysql.mysql_main import add_db, take_db 
from mysql.mysql_command import get_poster_by_code, get_all_codes, get_last_code

# =============================================================================
# Configuration
# =============================================================================

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = SECRET_KEY

def get_movie_info_omdb(title, api_key=API_KEY_OMBDB):
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['Response'] == 'True':
            return {
                'genre': data.get('Genre').split(",")[0],
                'rating': data.get('imdbRating')
            }
        else:
            return f"Movie not found: {data['Error']}"
    else:
        return f"Error: {response.status_code}"

# def movies():
#     list = []
#     for i in range(100, take_db(get_last_code(), 0)["code"]+1):
#         image_data = take_db(get_poster_by_code(i), 0)["photo"]
#         list.append(
#             {"code": take_db(get_poster_by_code(i), 0)["code"],
#             "headline": take_db(get_poster_by_code(i), 0)["headline"],
#             "description": take_db(get_poster_by_code(i), 0)["description"],
#             "encoded_image": base64.b64encode(image_data).decode('utf-8'),
#             "rating": get_movie_info_omdb(take_db(get_poster_by_code(i), 0)["headline"])["rating"],
#             "ganere": get_movie_info_omdb(take_db(get_poster_by_code(i), 0)["headline"])["genre"]}
#             )
#     return list
    

# =============================================================================

@app.route('/')
def home():
    movies = []
    for i in range(100, take_db(get_last_code(), 0)["code"]+1):
        image_data = take_db(get_poster_by_code(i), 0)["photo"]
        movies.append(
            {"code": take_db(get_poster_by_code(i), 0)["code"],
            "headline": take_db(get_poster_by_code(i), 0)["headline"],
            "description": take_db(get_poster_by_code(i), 0)["description"],
            "encoded_image": base64.b64encode(image_data).decode('utf-8'),
}
            )
        
    return render_template("index.html", movies=movies)

@app.route('/search', methods=['POST'])
def search():
    movies = []
    for i in range(100, take_db(get_last_code(), 0)["code"]+1):
        image_data = take_db(get_poster_by_code(i), 0)["photo"]
        movies.append(
            {"code": take_db(get_poster_by_code(i), 0)["code"],
            "headline": take_db(get_poster_by_code(i), 0)["headline"],
            "description": take_db(get_poster_by_code(i), 0)["description"],
            "encoded_image": base64.b64encode(image_data).decode('utf-8'),
}
            )
    query = request.form.get('query', '').lower()
    try:
        filtered_movies = [movie for movie in movies if query in str(movie['code']).lower()]
        return jsonify({"movies": filtered_movies})
    except Exception as e:
        print(f"Error: {e}")  # Вывод ошибки в консоль
        return jsonify({"error": "An error occurred during search."}), 500

if __name__ == "__main__":
    app.run(debug=DEBUG_STATUS)