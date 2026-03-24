import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

cursor.execute('SELECT COUNT(*) FROM Users')
total_users = cursor.fetchone()[0]
print('Общее количество пользователей:', total_users)

cursor.execute('SELECT SUM(age) FROM Users')
total_age = cursor.fetchone()[0]
print('Общая сумма возрастов пользователей:', total_age)

cursor.execute('SELECT AVG(age) FROM Users')
average_age = cursor.fetchone()[0]
print('Средний возраст пользователей:', average_age)

cursor.execute('SELECT MIN(age) FROM Users')
min_age = cursor.fetchone()[0]
print('Минимальный возраст среди пользователей:', min_age)

cursor.execute('SELECT MAX(age) FROM Users')
max_age = cursor.fetchone()[0]
print('Максимальный возраст среди пользователей:', max_age)

connection.close()