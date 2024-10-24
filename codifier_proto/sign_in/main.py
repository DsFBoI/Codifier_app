import sqlite3

def initialize_db():
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()

    # Create table for storing usernames and encoded photo passwords
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    encoded_password TEXT NOT NULL)''')

    # Example: Inserting a new user (You can later use an admin interface to add users)
    # The 'encoded_password' should be the password stored from the image encoding.
    c.execute("INSERT OR IGNORE INTO users (username, encoded_password) VALUES (?, ?)",
              ('Dani', 'DaniElMejor'))  # 'mysecret' here is a placeholder
    conn.commit()
    conn.close()

# Run this once to initialize the database
initialize_db()
