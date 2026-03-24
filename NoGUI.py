import sqlite3
from datetime import datetime

DB_NAME = "my_database.db"


class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.init_database()

    def init_database(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()

        self.cursor.execute("DROP TABLE IF EXISTS Users")
        self.cursor.execute("""
                            CREATE TABLE Users
                            (
                                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                                username   TEXT NOT NULL,
                                email      TEXT NOT NULL,
                                age        INTEGER,
                                is_active  INTEGER   DEFAULT 1,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
                            """)

        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_username ON Users (username)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users (email)")

        self.cursor.execute("""
                            CREATE TRIGGER IF NOT EXISTS update_created_at
            AFTER INSERT ON Users
                            BEGIN
                            UPDATE Users
                            SET created_at = CURRENT_TIMESTAMP
                            WHERE id = NEW.id;
                            END
                            """)

        sample_data = [
            ("алиса", "alisa@example.com", 28, 1),
            ("боб", "bob@example.com", 32, 1),
            ("чарли", "charlie@example.com", 25, 0),
            ("диана", "diana@example.com", 35, 1),
            ("ева", "eva@example.com", 29, 1),
        ]

        self.cursor.executemany("INSERT INTO Users (username, email, age, is_active) VALUES (?, ?, ?, ?)", sample_data)
        self.conn.commit()

        self.cursor.execute("""
                            CREATE VIEW IF NOT EXISTS ActiveUsers AS
                            SELECT *
                            FROM Users
                            WHERE is_active = 1
                            """)
        self.conn.commit()

        print("База данных успешно инициализирована")

    def add_user(self, username, email, age=None):
        try:
            self.cursor.execute(
                "INSERT INTO Users (username, email, age, is_active) VALUES (?, ?, ?, 1)",
                (username, email, age)
            )
            self.conn.commit()
            print(f"Пользователь '{username}' успешно добавлен")
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Ошибка при добавлении пользователя: {e}")
            return None

    def update_user(self, user_id, username=None, email=None, age=None):
        try:
            updates = []
            params = []

            if username:
                updates.append("username = ?")
                params.append(username)
            if email:
                updates.append("email = ?")
                params.append(email)
            if age is not None:
                updates.append("age = ?")
                params.append(age)

            if updates:
                params.append(user_id)
                query = f"UPDATE Users SET {', '.join(updates)} WHERE id = ?"
                self.cursor.execute(query, params)
                self.conn.commit()
                print(f"Пользователь с ID {user_id} успешно обновлен")
        except Exception as e:
            print(f"Ошибка при обновлении пользователя: {e}")

    def delete_user(self, user_id):
        try:
            self.cursor.execute("DELETE FROM Users WHERE id = ?", (user_id,))
            self.conn.commit()
            print(f"Пользователь с ID {user_id} успешно удален")
        except Exception as e:
            print(f"Ошибка при удалении пользователя: {e}")

    def get_all_users(self):
        self.cursor.execute("SELECT id, username, email, age, is_active, created_at FROM Users")
        return self.cursor.fetchall()

    def get_user_by_id(self, user_id):
        self.cursor.execute("SELECT * FROM Users WHERE id = ?", (user_id,))
        return self.cursor.fetchone()

    def get_users_by_age(self, min_age=None, max_age=None):
        if min_age and max_age:
            self.cursor.execute("SELECT * FROM Users WHERE age BETWEEN ? AND ?", (min_age, max_age))
        elif min_age:
            self.cursor.execute("SELECT * FROM Users WHERE age >= ?", (min_age,))
        elif max_age:
            self.cursor.execute("SELECT * FROM Users WHERE age <= ?", (max_age,))
        else:
            return self.get_all_users()
        return self.cursor.fetchall()

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                self.conn.commit()
                print("Запрос выполнен успешно")
                return None
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None

    def run_transaction(self):
        print("\n=== Демонстрация транзакции ===")
        try:
            self.cursor.execute("BEGIN")

            self.cursor.execute("INSERT INTO Users (username, email, age) VALUES (?, ?, ?)",
                                ("транзакция_пользователь", "trans@example.com", 99))
            self.cursor.execute("INSERT INTO Users (username, email, age) VALUES (?, ?, ?)",
                                ("транзакция_пользователь2", "trans2@example.com", 100))

            self.cursor.execute("COMMIT")
            print("Транзакция успешно выполнена! Добавлено 2 пользователя")
        except Exception as e:
            self.cursor.execute("ROLLBACK")
            print(f"Транзакция отменена: {e}")

    def show_aggregates(self):
        print("\n=== Агрегатные функции ===")

        self.cursor.execute("SELECT COUNT(*) FROM Users")
        count = self.cursor.fetchone()[0]
        print(f"Всего пользователей: {count}")

        self.cursor.execute("SELECT AVG(age) FROM Users WHERE age IS NOT NULL")
        avg_age = self.cursor.fetchone()[0]
        print(f"Средний возраст: {avg_age:.2f}" if avg_age else "Средний возраст: Нет данных")

        self.cursor.execute("SELECT MIN(age) FROM Users")
        min_age = self.cursor.fetchone()[0]
        print(f"Минимальный возраст: {min_age}" if min_age else "Минимальный возраст: Нет данных")

        self.cursor.execute("SELECT MAX(age) FROM Users")
        max_age = self.cursor.fetchone()[0]
        print(f"Максимальный возраст: {max_age}" if max_age else "Максимальный возраст: Нет данных")

        self.cursor.execute("SELECT SUM(age) FROM Users")
        sum_age = self.cursor.fetchone()[0]
        print(f"Сумма возрастов: {sum_age}" if sum_age else "Сумма возрастов: Нет данных")

    def show_group_by(self):
        print("\n=== Группировка по статусу активности ===")
        self.cursor.execute("SELECT is_active, COUNT(*) FROM Users GROUP BY is_active")
        for active, count in self.cursor.fetchall():
            status = "Активные" if active == 1 else "Неактивные"
            print(f"{status}: {count} пользователей")

    def show_active_users(self):
        print("\n=== Активные пользователи (используя представление) ===")
        self.cursor.execute("SELECT * FROM ActiveUsers")
        users = self.cursor.fetchall()
        for user in users:
            print(f"ID: {user[0]}, Имя: {user[1]}, Email: {user[2]}, Возраст: {user[3]}")

    def prepared_statements_demo(self):
        print("\n=== Демонстрация подготовленных запросов ===")
        query = "SELECT * FROM Users WHERE age > ?"
        ages = [20, 25, 30]

        for age in ages:
            self.cursor.execute(query, (age,))
            results = self.cursor.fetchall()
            print(f"Пользователи старше {age} лет: {len(results)} найдено")
            for user in results:
                print(f"  - {user[1]} ({user[3]} лет)")

    def null_handling_demo(self):
        print("\n=== Демонстрация обработки NULL ===")

        self.cursor.execute("INSERT INTO Users (username, email, age) VALUES (?, ?, ?)",
                            ("null_тест", "null@example.com", None))
        self.conn.commit()
        print("Добавлен пользователь с NULL возрастом")

        self.cursor.execute("SELECT * FROM Users WHERE age IS NULL")
        null_users = self.cursor.fetchall()
        print(f"Пользователи с NULL возрастом: {len(null_users)}")

        for user in null_users:
            print(f"  ID: {user[0]}, Имя: {user[1]}, Возраст: {user[3] or 'Не указан'}")

    def complex_query_demo(self):
        print("\n=== Сложный запрос с подзапросом ===")

        self.cursor.execute("""
                            SELECT username, age
                            FROM Users
                            WHERE age = (SELECT MAX(age) FROM Users)
                            """)
        oldest_users = self.cursor.fetchall()
        print("Пользователи с максимальным возрастом:")
        for user in oldest_users:
            print(f"  {user[0]}: {user[1]} лет")

        print("\n=== Запрос с JOIN, GROUP BY и HAVING ===")

        self.cursor.execute("""
                            SELECT CASE WHEN is_active = 1 THEN 'Активные' ELSE 'Неактивные' END as status,
                                   COUNT(*) as count,
                AVG(age) as avg_age,
                MIN(age) as min_age,
                MAX(age) as max_age
                            FROM Users
                            GROUP BY is_active
                            HAVING COUNT (*) > 0
                            """)

        for row in self.cursor.fetchall():
            print(f"Статус: {row[0]}")
            print(f"  Количество: {row[1]}")
            print(f"  Средний возраст: {row[2]:.2f}" if row[2] else f"  Средний возраст: Нет данных")
            print(f"  Мин. возраст: {row[3]}" if row[3] else f"  Мин. возраст: Нет данных")
            print(f"  Макс. возраст: {row[4]}" if row[4] else f"  Макс. возраст: Нет данных")

    def print_users(self, users):
        print("\n" + "=" * 80)
        print(f"{'ID':<5} {'Имя':<15} {'Email':<25} {'Возраст':<8} {'Активен':<8} {'Дата создания'}")
        print("-" * 80)
        for user in users:
            active = "Да" if user[4] == 1 else "Нет"
            age = user[3] if user[3] else "Не указан"
            print(f"{user[0]:<5} {user[1]:<15} {user[2]:<25} {age:<8} {active:<8} {user[5]}")
        print("=" * 80)

    def close(self):
        if self.conn:
            self.conn.close()
            print("\nСоединение с базой данных закрыто")


def main():
    db = DatabaseManager()

    print("\n" + "=" * 60)
    print("ПРОГРАММА УПРАВЛЕНИЯ БАЗОЙ ДАННЫХ SQLITE")
    print("=" * 60)

    print("\n1. Вывод всех пользователей:")
    all_users = db.get_all_users()
    db.print_users(all_users)

    print("\n2. Добавление нового пользователя:")
    db.add_user("иван", "ivan@example.com", 27)
    db.add_user("мария", "maria@example.com", 31)

    print("\n3. Обновление пользователя:")
    db.update_user(1, age=29)

    print("\n4. Пользователи старше 28 лет:")
    users_old = db.get_users_by_age(min_age=28)
    db.print_users(users_old)

    print("\n5. Пользователи в возрасте от 25 до 30 лет:")
    users_range = db.get_users_by_age(min_age=25, max_age=30)
    db.print_users(users_range)

    db.show_aggregates()

    db.show_group_by()

    db.prepared_statements_demo()

    db.null_handling_demo()

    db.complex_query_demo()

    db.show_active_users()

    db.run_transaction()

    print("\n6. Удаление пользователя:")
    db.delete_user(6)

    print("\n7. Выполнение произвольного SQL запроса:")
    results = db.execute_query("SELECT username, email FROM Users WHERE is_active = 1")
    if results:
        print("Активные пользователи:")
        for row in results:
            print(f"  {row[0]} - {row[1]}")

    print("\n8. Итоговый список всех пользователей:")
    final_users = db.get_all_users()
    db.print_users(final_users)

    db.close()


if __name__ == "__main__":
    main()