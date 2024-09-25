import pymysql
import pymysql.cursors
from .mysql_config import host, user, password, db_name

def add_db(code, headline, description, photo):
    try:
        conn = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Connected to the database successfully...")
        with conn.cursor() as cur:
            cur.execute("INSERT INTO kinopoisk (code, headline, description, photo) VALUES (%s, %s, %s, %s)", (code, headline, description, photo))  # Извлекаем запрос и параметры из кортежа
        conn.commit()
        return True  # Возвращаем True, если все прошло успешно
    except Exception as e:
        print("Error in connection...")
        print(e)
        return False
    finally:
        conn.close()

def take_db(task, func):
    try:
        conn = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Connected to the database successfully...")
        with conn.cursor() as cur:
            if isinstance(task, tuple):
                cur.execute(task[0], task[1])
            else:
                cur.execute(task)
                result = cur.fetchall() if func == 1 else cur.fetchone()
        conn.commit()
        return result
    except Exception as e:
        print("Error in connection...")
        print(e)
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    add_db(

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
