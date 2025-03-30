import sqlite3
connection = sqlite3.connect('userstable.db')
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARU KEY, name TEXT NOT NULL, birth date TEXT NOT NULL, role TEXT NOT NULL)')
connection.commit()
connection.close()