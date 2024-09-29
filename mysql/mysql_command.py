

def get_poster_by_code(code_value):
    return f"SELECT * FROM kinopoisk WHERE code = {code_value}"

def get_all_codes():
    return "SELECT code, headline FROM kinopoisk;"

def get_last_code():
    return "SELECT code FROM kinopoisk ORDER BY id DESC LIMIT 1;"

def get_preview():
    return "SELECT * FROM kinopoisk WHERE code BETWEEN 100 AND 107;"