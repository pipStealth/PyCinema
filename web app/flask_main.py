from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, g, jsonify
import sys
import requests
from flask_config import SECRET_KEY, API_KEY_OMBDB, DEBUG_STATUS
import base64
sys.path.append('D:/Kinopoisk project')
from mysql.mysql_main import add_db, take_db 
from mysql.mysql_command import get_poster_by_code, get_all_codes, get_last_code, get_preview

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
            return False
    else:
        return False


# =============================================================================
# Routers
# =============================================================================

@app.route('/')
def home():
    try:
        movies = take_db(get_preview(), 1); 
        for i in range(0, 8):
            movies[i]["photo"] = base64.b64encode(movies[i]["photo"]).decode('utf-8')
        return render_template("index.html", movies=movies)
    except Exception as e:
        print(f"Some error: {e}")
        abort(501)

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '').lower()
    try:
        if (not query) or (len(query) <= 2):
            movies = take_db(get_preview(), 1)
            for i in range(0, 8):
                movies[i]["photo"] = base64.b64encode(movies[i]["photo"]).decode('utf-8')
            return jsonify({"movies": movies})
        movies = take_db(get_poster_by_code(query), 1)
        movies[0]["photo"] = base64.b64encode(movies[0]["photo"]).decode('utf-8')
        return jsonify({"movies": movies})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred during search."}), 500

if __name__ == "__main__":
    app.run(debug=DEBUG_STATUS)