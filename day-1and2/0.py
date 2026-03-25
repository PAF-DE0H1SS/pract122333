import sqlite3
import os
from datetime import datetime

DB_NAME = "practice.db"


def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS tasks")

    cursor.execute("""
                   CREATE TABLE users
                   (
                       id         INTEGER PRIMARY KEY AUTOINCREMENT,
                       username   TEXT NOT NULL UNIQUE,
                       email      TEXT NOT NULL,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )
                   """)

    cursor.execute("""
                   CREATE TABLE tasks
                   (
                       id          INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id     INTEGER NOT NULL,
                       title       TEXT    NOT NULL,
                       description TEXT,
                       status      TEXT      DEFAULT 'pending',
                       priority    INTEGER   DEFAULT 1,
                       created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY (user_id) REFERENCES users (id)
                   )
                   """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")

    conn.commit()
    conn.close()
    print("Database and tables created successfully")


def insert_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    users_data = [
        ("alice", "alice@example.com"),
        ("bob", "bob@example.com"),
        ("charlie", "charlie@example.com"),
    ]

    cursor.executemany("INSERT INTO users (username, email) VALUES (?, ?)", users_data)

    tasks_data = [
        (1, "Complete SQLite practice", "Finish all exercises", "pending", 3),
        (1, "Write documentation", "Document the project", "in_progress", 2),
        (2, "Review code", "Check pull requests", "pending", 1),
        (2, "Fix bugs", "Resolve issues in main branch", "completed", 3),
        (3, "Deploy application", "Deploy to production server", "pending", 3),
        (1, "Test features", "Run unit tests", "completed", 2),
    ]

    cursor.executemany(
        "INSERT INTO tasks (user_id, title, description, status, priority) VALUES (?, ?, ?, ?, ?)",
        tasks_data
    )

    conn.commit()
    conn.close()
    print("Sample data inserted successfully")


def update_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("UPDATE tasks SET status = ? WHERE title = ?", ("in_progress", "Complete SQLite practice"))
    print(f"Updated {cursor.rowcount} row(s)")

    cursor.execute("UPDATE users SET email = ? WHERE username = ?", ("alice.new@example.com", "alice"))
    print(f"Updated {cursor.rowcount} row(s)")

    conn.commit()
    conn.close()


def delete_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE status = ?", ("completed",))
    print(f"Deleted {cursor.rowcount} task(s)")

    conn.commit()
    conn.close()


def select_queries():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print("\n=== All users ===")
    cursor.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        print(row)

    print("\n=== Tasks with high priority ===")
    cursor.execute("SELECT * FROM tasks WHERE priority >= ? ORDER BY priority DESC", (3,))
    for row in cursor.fetchall():
        print(row)

    print("\n=== Users and their tasks (JOIN) ===")
    cursor.execute("""
                   SELECT u.username, t.title, t.status, t.priority
                   FROM users u
                            JOIN tasks t ON u.id = t.user_id
                   ORDER BY u.username, t.priority DESC
                   """)
    for row in cursor.fetchall():
        print(row)

    print("\n=== Task statistics by user ===")
    cursor.execute("""
                   SELECT u.username, COUNT(t.id) as task_count, AVG(t.priority) as avg_priority
                   FROM users u
                            LEFT JOIN tasks t ON u.id = t.user_id
                   GROUP BY u.id
                   HAVING COUNT(t.id) > 0
                   """)
    for row in cursor.fetchall():
        print(row)

    conn.close()


def advanced_queries():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DROP VIEW IF EXISTS user_task_summary")
    cursor.execute("""
                   CREATE VIEW user_task_summary AS
                   SELECT u.id,
                          u.username,
                          COUNT(t.id)                                               as total_tasks,
                          SUM(CASE WHEN t.status = 'pending' THEN 1 ELSE 0 END)     as pending_tasks,
                          SUM(CASE WHEN t.status = 'in_progress' THEN 1 ELSE 0 END) as in_progress_tasks,
                          AVG(t.priority)                                           as avg_priority
                   FROM users u
                            LEFT JOIN tasks t ON u.id = t.user_id
                   GROUP BY u.id
                   """)

    print("\n=== User task summary view ===")
    cursor.execute("SELECT * FROM user_task_summary")
    for row in cursor.fetchall():
        print(row)

    cursor.execute("""
                   SELECT username, total_tasks, pending_tasks
                   FROM user_task_summary
                   WHERE total_tasks > 1
                   ORDER BY total_tasks DESC
                   """)
    results = cursor.fetchall()
    print("\n=== Users with more than 1 task ===")
    for row in results:
        print(row)

    conn.close()


def transactions_demo():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print("\n=== Transaction demo ===")
    try:
        cursor.execute("BEGIN")

        cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", ("dave", "dave@example.com"))
        user_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO tasks (user_id, title, status, priority) VALUES (?, ?, ?, ?)",
            (user_id, "New user task", "pending", 2)
        )

        cursor.execute("COMMIT")
        print("Transaction committed successfully")

    except Exception as e:
        cursor.execute("ROLLBACK")
        print(f"Transaction rolled back: {e}")

    with conn:
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"Total users after transaction: {count}")

    conn.close()


def prepared_statements():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print("\n=== Prepared statements demo ===")

    cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", ("eve", "eve@example.com"))
    user_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO tasks (user_id, title, priority) VALUES (?, ?, ?)",
        (user_id, "Prepared statement task", 3)
    )

    cursor.execute("SELECT * FROM users WHERE username = ?", ("eve",))
    user = cursor.fetchone()
    print(f"User inserted: {user}")

    conn.commit()
    conn.close()


def null_handling():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tasks (user_id, title, description, priority) VALUES (?, ?, ?, ?)",
                   (1, "Task with null description", None, 2))

    cursor.execute("SELECT * FROM tasks WHERE description IS NULL")
    null_results = cursor.fetchall()
    print(f"\nTasks with NULL description: {len(null_results)}")

    cursor.execute("SELECT title, COALESCE(description, 'No description') as desc FROM tasks WHERE id = ?",
                   (cursor.lastrowid,))
    row = cursor.fetchone()
    print(f"Task with coalesced description: {row[0]} - {row[1]}")

    conn.commit()
    conn.close()


def task_manager_app():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    def add_task(username, title, description, priority):
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user:
            cursor.execute(
                "INSERT INTO tasks (user_id, title, description, priority, status) VALUES (?, ?, ?, ?, ?)",
                (user[0], title, description, priority, "pending")
            )
            conn.commit()
            print(f"Task '{title}' added for {username}")
        else:
            print(f"User {username} not found")

    def list_tasks(username=None):
        if username:
            cursor.execute("""
                           SELECT t.title, t.description, t.status, t.priority
                           FROM tasks t
                                    JOIN users u ON t.user_id = u.id
                           WHERE u.username = ?
                           ORDER BY t.priority DESC, t.created_at
                           """, (username,))
        else:
            cursor.execute("""
                           SELECT u.username, t.title, t.status, t.priority
                           FROM tasks t
                                    JOIN users u ON t.user_id = u.id
                           ORDER BY t.priority DESC
                           """)

        tasks = cursor.fetchall()
        if tasks:
            for task in tasks:
                print(task)
        else:
            print("No tasks found")

    def update_task_status(username, title, new_status):
        cursor.execute("""
                       UPDATE tasks
                       SET status = ?
                       WHERE title = ?
                         AND user_id = (SELECT id FROM users WHERE username = ?)
                       """, (new_status, title, username))
        conn.commit()
        print(f"Updated {cursor.rowcount} task(s)")

    def delete_completed_tasks():
        cursor.execute("DELETE FROM tasks WHERE status = 'completed'")
        conn.commit()
        print(f"Deleted {cursor.rowcount} completed task(s)")

    print("\n=== Task Manager Application ===")
    add_task("alice", "Learn SQLite", "Complete all exercises", 3)
    add_task("bob", "Write report", "Monthly report", 2)

    print("\nAll tasks:")
    list_tasks()

    print("\nAlice's tasks:")
    list_tasks("alice")

    update_task_status("alice", "Learn SQLite", "in_progress")

    delete_completed_tasks()

    conn.close()


def main():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

    setup_database()
    insert_data()
    update_data()
    select_queries()
    advanced_queries()
    transactions_demo()
    prepared_statements()
    null_handling()
    delete_data()
    task_manager_app()

#123
if __name__ == "__main__":
    main()