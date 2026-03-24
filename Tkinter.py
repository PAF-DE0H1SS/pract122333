import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

DB_NAME = "my_database.db"


class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление базой данных SQLite")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')

        self.init_database()
        self.create_widgets()
        self.refresh_table()

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
            ("борис", "boris@example.com", 32, 1),
            ("чарли", "charlie@example.com", 25, 0),
            ("диана", "diana@example.com", 35, 1),
            ("евгений", "evgeniy@example.com", 29, 1),
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

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.manage_frame = ttk.Frame(notebook)
        self.query_frame = ttk.Frame(notebook)
        self.stats_frame = ttk.Frame(notebook)
        self.advanced_frame = ttk.Frame(notebook)

        notebook.add(self.manage_frame, text="Управление пользователями")
        notebook.add(self.query_frame, text="SQL запросы")
        notebook.add(self.stats_frame, text="Статистика")
        notebook.add(self.advanced_frame, text="Расширенные функции")

        self.create_manage_tab()
        self.create_query_tab()
        self.create_stats_tab()
        self.create_advanced_tab()

    def create_manage_tab(self):
        input_frame = ttk.LabelFrame(self.manage_frame, text="Ввод данных", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(input_frame, text="Имя пользователя:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.username_entry = ttk.Entry(input_frame, width=30)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Email:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.email_entry = ttk.Entry(input_frame, width=30)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Возраст:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.age_entry = ttk.Entry(input_frame, width=30)
        self.age_entry.grid(row=2, column=1, padx=5, pady=5)

        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Добавить", command=self.add_user).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Обновить", command=self.update_user).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Удалить", command=self.delete_user).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Обновить список", command=self.refresh_table).pack(side='left', padx=5)

        table_frame = ttk.LabelFrame(self.manage_frame, text="Список пользователей", padding=10)
        table_frame.pack(fill='both', expand=True, padx=10, pady=5)

        columns = ('id', 'username', 'email', 'age', 'is_active', 'created_at')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)

        self.tree.heading('id', text='ID')
        self.tree.heading('username', text='Имя')
        self.tree.heading('email', text='Email')
        self.tree.heading('age', text='Возраст')
        self.tree.heading('is_active', text='Активен')
        self.tree.heading('created_at', text='Дата создания')

        self.tree.column('id', width=50)
        self.tree.column('username', width=120)
        self.tree.column('email', width=200)
        self.tree.column('age', width=70)
        self.tree.column('is_active', width=70)
        self.tree.column('created_at', width=150)

        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def create_query_tab(self):
        query_frame = ttk.LabelFrame(self.query_frame, text="Пользовательский SQL запрос", padding=10)
        query_frame.pack(fill='both', expand=True, padx=10, pady=5)

        ttk.Label(query_frame, text="SQL запрос:").pack(anchor='w', pady=5)
        self.query_text = scrolledtext.ScrolledText(query_frame, height=8, width=80)
        self.query_text.pack(fill='x', pady=5)
        self.query_text.insert('1.0', 'SELECT * FROM Users WHERE age > 25')

        btn_frame = ttk.Frame(query_frame)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Выполнить", command=self.execute_query).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Очистить", command=self.clear_results).pack(side='left', padx=5)

        result_frame = ttk.LabelFrame(query_frame, text="Результаты запроса", padding=10)
        result_frame.pack(fill='both', expand=True, pady=5)

        self.result_text = scrolledtext.ScrolledText(result_frame, height=15, width=80)
        self.result_text.pack(fill='both', expand=True)

    def create_stats_tab(self):
        stats_frame = ttk.LabelFrame(self.stats_frame, text="Статистика базы данных", padding=10)
        stats_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=20, width=80)
        self.stats_text.pack(fill='both', expand=True)

        ttk.Button(stats_frame, text="Обновить статистику", command=self.refresh_stats).pack(pady=10)
        self.refresh_stats()

    def create_advanced_tab(self):
        advanced_frame = ttk.LabelFrame(self.advanced_frame, text="Расширенные операции", padding=10)
        advanced_frame.pack(fill='both', expand=True, padx=10, pady=5)

        ttk.Label(advanced_frame, text="Демонстрация транзакций:").pack(anchor='w', pady=5)
        ttk.Button(advanced_frame, text="Выполнить транзакцию", command=self.run_transaction).pack(anchor='w', pady=5)

        ttk.Label(advanced_frame, text="Демонстрация подготовленных запросов:").pack(anchor='w', pady=5)
        ttk.Button(advanced_frame, text="Выполнить подготовленный запрос", command=self.run_prepared).pack(anchor='w',
                                                                                                           pady=5)

        ttk.Label(advanced_frame, text="Агрегатные функции:").pack(anchor='w', pady=5)
        ttk.Button(advanced_frame, text="Показать агрегаты", command=self.show_aggregates).pack(anchor='w', pady=5)

        ttk.Label(advanced_frame, text="Представление активных пользователей:").pack(anchor='w', pady=5)
        ttk.Button(advanced_frame, text="Показать активных", command=self.show_active_users).pack(anchor='w', pady=5)

        ttk.Label(advanced_frame, text="NULL значения:").pack(anchor='w', pady=5)
        ttk.Button(advanced_frame, text="Показать NULL значения", command=self.show_null_values).pack(anchor='w',
                                                                                                      pady=5)

        self.advanced_result = scrolledtext.ScrolledText(advanced_frame, height=12, width=80)
        self.advanced_result.pack(fill='both', expand=True, pady=10)

    def add_user(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        age = self.age_entry.get()

        if not username or not email:
            messagebox.showerror("Ошибка", "Имя пользователя и email обязательны")
            return

        try:
            age_val = int(age) if age else None
            self.cursor.execute(
                "INSERT INTO Users (username, email, age, is_active) VALUES (?, ?, ?, 1)",
                (username, email, age_val)
            )
            self.conn.commit()
            self.refresh_table()
            self.clear_inputs()
            messagebox.showinfo("Успех", "Пользователь успешно добавлен")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def update_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите пользователя для обновления")
            return

        user_id = self.tree.item(selected[0])['values'][0]
        username = self.username_entry.get()
        email = self.email_entry.get()
        age = self.age_entry.get()

        try:
            age_val = int(age) if age else None
            self.cursor.execute(
                "UPDATE Users SET username=?, email=?, age=? WHERE id=?",
                (username, email, age_val, user_id)
            )
            self.conn.commit()
            self.refresh_table()
            self.clear_inputs()
            messagebox.showinfo("Успех", "Пользователь успешно обновлен")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def delete_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите пользователя для удаления")
            return

        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этого пользователя?"):
            user_id = self.tree.item(selected[0])['values'][0]
            self.cursor.execute("DELETE FROM Users WHERE id=?", (user_id,))
            self.conn.commit()
            self.refresh_table()
            self.clear_inputs()
            messagebox.showinfo("Успех", "Пользователь успешно удален")

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.cursor.execute("SELECT id, username, email, age, is_active, created_at FROM Users")
        for row in self.cursor.fetchall():
            active_status = "Да" if row[4] == 1 else "Нет"
            self.tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], active_status, row[5]))

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, values[1])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, values[2])
            self.age_entry.delete(0, tk.END)
            if values[3]:
                self.age_entry.insert(0, values[3])

    def clear_inputs(self):
        self.username_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)

    def execute_query(self):
        query = self.query_text.get('1.0', tk.END).strip()
        if not query:
            return

        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            self.result_text.delete('1.0', tk.END)
            if results:
                col_names = [description[0] for description in self.cursor.description]
                self.result_text.insert('1.0', ' | '.join(col_names) + '\n')
                self.result_text.insert('2.0', '-' * 50 + '\n')

                for row in results:
                    self.result_text.insert(tk.END, ' | '.join(str(val) for val in row) + '\n')
                self.result_text.insert(tk.END, f"\nВсего строк: {len(results)}")
            else:
                self.result_text.insert('1.0', "Запрос выполнен успешно. Результатов не найдено.")
        except Exception as e:
            messagebox.showerror("Ошибка запроса", str(e))

    def clear_results(self):
        self.result_text.delete('1.0', tk.END)

    def refresh_stats(self):
        self.stats_text.delete('1.0', tk.END)

        self.cursor.execute("SELECT COUNT(*) FROM Users")
        total = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT AVG(age) FROM Users WHERE age IS NOT NULL")
        avg_age = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT MIN(age) FROM Users")
        min_age = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT MAX(age) FROM Users")
        max_age = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT SUM(age) FROM Users")
        sum_age = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM Users WHERE is_active = 1")
        active = self.cursor.fetchone()[0]

        self.stats_text.insert('1.0', "=== СТАТИСТИКА БАЗЫ ДАННЫХ ===\n\n")
        self.stats_text.insert(tk.END, f"Всего пользователей: {total}\n")
        self.stats_text.insert(tk.END, f"Активных пользователей: {active}\n")
        self.stats_text.insert(tk.END, f"Неактивных пользователей: {total - active}\n\n")
        self.stats_text.insert(tk.END, "=== СТАТИСТИКА ВОЗРАСТА ===\n\n")
        self.stats_text.insert(tk.END, f"Средний возраст: {avg_age:.2f}\n" if avg_age else "Средний возраст: Н/Д\n")
        self.stats_text.insert(tk.END, f"Минимальный возраст: {min_age}\n" if min_age else "Минимальный возраст: Н/Д\n")
        self.stats_text.insert(tk.END,
                               f"Максимальный возраст: {max_age}\n" if max_age else "Максимальный возраст: Н/Д\n")
        self.stats_text.insert(tk.END, f"Сумма возрастов: {sum_age}\n" if sum_age else "Сумма возрастов: Н/Д\n")

    def run_transaction(self):
        self.advanced_result.delete('1.0', tk.END)
        try:
            self.cursor.execute("BEGIN")
            self.cursor.execute("INSERT INTO Users (username, email, age) VALUES (?, ?, ?)",
                                ("транзакция_пользователь", "trans@example.com", 99))
            self.cursor.execute("INSERT INTO Users (username, email, age) VALUES (?, ?, ?)",
                                ("транзакция_пользователь2", "trans2@example.com", 100))
            self.cursor.execute("COMMIT")
            self.advanced_result.insert('1.0', "Транзакция успешно выполнена!\n")
            self.advanced_result.insert(tk.END, "Добавлено 2 пользователя через транзакцию\n")
            self.refresh_table()
        except Exception as e:
            self.cursor.execute("ROLLBACK")
            self.advanced_result.insert('1.0', f"Транзакция отменена: {e}\n")

    def run_prepared(self):
        self.advanced_result.delete('1.0', tk.END)
        query = "SELECT * FROM Users WHERE age > ?"
        ages = [20, 25, 30]

        for age in ages:
            self.cursor.execute(query, (age,))
            results = self.cursor.fetchall()
            self.advanced_result.insert(tk.END, f"Пользователи старше {age} лет: найдено {len(results)}\n")
            for user in results:
                self.advanced_result.insert(tk.END, f"  - {user[1]} ({user[3]} лет)\n")
            self.advanced_result.insert(tk.END, "\n")

    def show_aggregates(self):
        self.advanced_result.delete('1.0', tk.END)

        self.cursor.execute("SELECT COUNT(*), AVG(age), MIN(age), MAX(age), SUM(age) FROM Users")
        count, avg, min_age, max_age, sum_age = self.cursor.fetchone()

        self.advanced_result.insert('1.0', "=== АГРЕГАТНЫЕ ФУНКЦИИ ===\n\n")
        self.advanced_result.insert(tk.END, f"COUNT (количество): {count}\n")
        self.advanced_result.insert(tk.END,
                                    f"AVG (средний возраст): {avg:.2f}\n" if avg else "AVG (средний возраст): Н/Д\n")
        self.advanced_result.insert(tk.END,
                                    f"MIN (минимальный возраст): {min_age}\n" if min_age else "MIN (минимальный возраст): Н/Д\n")
        self.advanced_result.insert(tk.END,
                                    f"MAX (максимальный возраст): {max_age}\n" if max_age else "MAX (максимальный возраст): Н/Д\n")
        self.advanced_result.insert(tk.END,
                                    f"SUM (сумма возрастов): {sum_age}\n" if sum_age else "SUM (сумма возрастов): Н/Д\n")

        self.cursor.execute("SELECT is_active, COUNT(*) FROM Users GROUP BY is_active")
        self.advanced_result.insert(tk.END, "\n=== ГРУППИРОВКА ПО СТАТУСУ ===\n\n")
        for active, count in self.cursor.fetchall():
            status = "Активен" if active == 1 else "Неактивен"
            self.advanced_result.insert(tk.END, f"{status}: {count} пользователей\n")

    def show_active_users(self):
        self.advanced_result.delete('1.0', tk.END)
        self.cursor.execute("SELECT * FROM ActiveUsers")
        users = self.cursor.fetchall()

        self.advanced_result.insert('1.0', "=== АКТИВНЫЕ ПОЛЬЗОВАТЕЛИ (Представление) ===\n\n")
        for user in users:
            self.advanced_result.insert(tk.END,
                                        f"ID: {user[0]}, Имя: {user[1]}, Email: {user[2]}, Возраст: {user[3]}\n")

    def show_null_values(self):
        self.advanced_result.delete('1.0', tk.END)

        self.cursor.execute("INSERT INTO Users (username, email, age) VALUES (?, ?, ?)",
                            ("пользователь_null", "null@example.com", None))
        self.conn.commit()

        self.cursor.execute("SELECT * FROM Users WHERE age IS NULL")
        null_users = self.cursor.fetchall()

        self.advanced_result.insert('1.0', "=== ПОЛЬЗОВАТЕЛИ С NULL ЗНАЧЕНИЯМИ В ВОЗРАСТЕ ===\n\n")
        for user in null_users:
            self.advanced_result.insert(tk.END,
                                        f"ID: {user[0]}, Имя: {user[1]}, Email: {user[2]}, Возраст: {user[3]}\n")

        self.advanced_result.insert(tk.END, f"\nВсего найдено: {len(null_users)} пользователей\n")
        self.advanced_result.insert(tk.END, "\nCOALESCE пример:\n")

        self.cursor.execute("SELECT username, COALESCE(age, 0) as age FROM Users WHERE username = ?",
                            ("пользователь_null",))
        result = self.cursor.fetchone()
        if result:
            self.advanced_result.insert(tk.END, f"  - {result[0]}: возраст = {result[1]} (NULL заменен на 0)\n")

        self.refresh_table()

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()


def main():
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()