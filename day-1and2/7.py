import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS Users")

cursor.execute("""
    CREATE TABLE Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

cursor.execute('CREATE INDEX IF NOT EXISTS idx_username ON Users (username)')

cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS update_created_at
    AFTER INSERT ON Users
    BEGIN
        UPDATE Users SET created_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END
""")

cursor.execute("INSERT INTO Users (username, email, age, is_active) VALUES (?, ?, ?, ?)",
               ("alice", "alice@example.com", 30, 1))
cursor.execute("INSERT INTO Users (username, email, age, is_active) VALUES (?, ?, ?, ?)",
               ("bob", "bob@example.com", 20, 1))
cursor.execute("INSERT INTO Users (username, email, age, is_active) VALUES (?, ?, ?, ?)",
               ("charlie", "charlie@example.com", 35, 0))

connection.commit()

query = 'SELECT * FROM Users WHERE age > ?'
cursor.execute(query, (25,))
users = cursor.fetchall()
print("Users with age > 25:")
for user in users:
    print(user)

cursor.execute('DROP VIEW IF EXISTS ActiveUsers')
cursor.execute('CREATE VIEW ActiveUsers AS SELECT * FROM Users WHERE is_active = 1')
cursor.execute('SELECT * FROM ActiveUsers')
active_users = cursor.fetchall()
print("\nActive users:")
for user in active_users:
    print(user)

connection.close()