import pymysql
import pymysql.cursors
from .mysql_config import host, user, password, db_name
import base64

def connection_db(host=host, user=user, password=password, db_name=db_name):
    try:
        conn = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        print("Error in connection...")
        print(e)
        return False

def add_db(code, headline, description, photo):
    conn = connection_db()
    print("Connected to the database successfully...")
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO kinopoisk (code, headline, description, photo) VALUES (%s, %s, %s, %s)", (code, headline, description, photo))
        conn.commit()
        return True
    finally:
        conn.close()

def take_db(task, fetch):
    conn = connection_db()

    print(f"Connected to the database successfully... {task} to {fetch}")
    try:
        with conn.cursor() as cur:
            if isinstance(task, tuple):
                cur.execute(task[0], task[1])
            else:
                cur.execute(task)
            result = cur.fetchall() if fetch == 1 else cur.fetchone()

        return result
    finally:
        conn.close()

if __name__ == "__main__":
    conn = connection_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS kinopoisk (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    code INT NOT NULL,
                    headline VARCHAR(255) NOT NULL,
                    description TEXT,
                    photo BLOB
                );
                """
            )
        conn.commit()
    finally:
        conn.close()
