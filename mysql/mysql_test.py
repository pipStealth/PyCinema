import pymysql

# Функция для чтения изображения в бинарном формате
def read_image(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

# Подключение к базе данных
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='2010Navolokov',
    database='root'
)

try:
    with connection.cursor() as cursor:
        # Подготовка данных для вставки
        code_value = 101  # Замените на нужное значение
        headline = "Matrix"
        description = "The concept of a matrix is fundamental in mathematics, particularly in linear algebra. A matrix is a rectangular array of numbers, symbols, or expressions, arranged in rows and columns. It can represent data, perform linear transformations, and solve systems of equations. Matrices can be added, subtracted, and multiplied, with various properties like determinants and eigenvalues revealing important information about the transformations they represent. In computer science, matrices are used in graphics, machine learning, and data analysis, highlighting their versatility and importance in numerous fields."
        image_data = read_image('text.jpg')  # Укажите путь к вашему изображению

        # Выполнение запроса на вставку
        sql_query = """
        INSERT INTO kinopoisk (code, headline, description, photo)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql_query, (code_value, headline, description, image_data))
        
        # Сохранение изменений
        connection.commit()

        print("Image inserted successfully")
finally:
    connection.close()
