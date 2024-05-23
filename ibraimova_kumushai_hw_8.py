import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS countries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL
                )''')

cursor.executemany('''INSERT INTO countries (title) VALUES (?)''',
                    [('Киргизия',), ('Германия',), ('Китай',)])

cursor.execute('''CREATE TABLE IF NOT EXISTS cities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    area REAL DEFAULT 0,
                    country_id INTEGER,
                    FOREIGN KEY (country_id) REFERENCES countries(id)
                )''')

cursor.executemany('''INSERT INTO cities (title, country_id) VALUES (?, ?)''',
                    [('Бишкек', 1), ('Ош', 1), ('Берлин', 2), ('Пекин', 3), ('Москва', 3), ('Лондон', 2), ('Париж', 2)])

cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    city_id INTEGER,
                    FOREIGN KEY (city_id) REFERENCES cities(id)
                )''')

cursor.executemany('''INSERT INTO students (first_name, last_name, city_id) VALUES (?, ?, ?)''',
                    [('Иван', 'Иванов', 1), ('Петр', 'Петров', 1), ('Анна', 'Иванова', 2), ('Мария', 'Петрова', 3),
                     ('Алексей', 'Сидоров', 4), ('Елена', 'Смирнова', 5), ('Дмитрий', 'Козлов', 6),
                     ('Ольга', 'Новикова', 7), ('Игорь', 'Морозов', 1), ('Татьяна', 'Павлова', 2),
                     ('Сергей', 'Соколов', 3), ('Екатерина', 'Кузнецова', 4), ('Александра', 'Ильина', 5),
                     ('Артем', 'Королев', 6), ('Наталья', 'Галкина', 7)])

conn.commit()

cursor.execute('''SELECT id, title FROM cities''')
cities = cursor.fetchall()
print("Вы можете отобразить список учеников по выбранному id города из перечня городов ниже, для выхода из программы введите 0:")
for city in cities:
    print(f"{city[0]}. {city[1]}")

city_id = int(input("Введите id города: "))

if city_id == 0:
    exit()

cursor.execute('''SELECT students.first_name, students.last_name, countries.title, cities.title, cities.area 
                  FROM students 
                  JOIN cities ON students.city_id = cities.id 
                  JOIN countries ON cities.country_id = countries.id 
                  WHERE cities.id = ?''', (city_id,))
students = cursor.fetchall()

print("\nУченики из выбранного города:")
for student in students:
    print(f"Имя: {student[0]}, Фамилия: {student[1]}, Страна: {student[2]}, Город: {student[3]}, Площадь города: {student[4]}")

conn.close()
