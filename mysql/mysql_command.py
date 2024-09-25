

def get_poster_by_code(code_value):
    return f"SELECT * FROM kinopoisk WHERE code = {code_value}"

def get_all_codes():
    return "SELECT code, headline FROM kinopoisk;"

def get_last_code():
    return "SELECT code FROM kinopoisk ORDER BY id DESC LIMIT 1;"

def add_film(code, headline, description, photo):
    return "INSERT INTO kinopoisk (code, headline, description, photo) VALUES (%s, %s, %s, %s)", (code, headline, description, photo)
