import sqlite3

def create_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT, password TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (username TEXT, social INT, screen INT, sleep INT, study INT, result TEXT)''')

    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    data = c.fetchone()
    conn.close()
    return data

def save_history(username, social, screen, sleep, study, result):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO history VALUES (?, ?, ?, ?, ?, ?)",
              (username, social, screen, sleep, study, result))
    conn.commit()
    conn.close()

def get_history(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM history WHERE username=?", (username,))
    data = c.fetchall()
    conn.close()
    return data
