import pymysql
import pymysql.cursors
from .mysql_config import host, user, password, db_name

def execute_db(task):
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
            cur.execute(task)
        conn.commit()
    except Exception as e:
        print("Error in connection...")
        print(e)
        return False
    finally:
        conn.close()


if __name__ == "__main__":
    execute_db(

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
