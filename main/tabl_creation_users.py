import sqlite3
db = sqlite3.connect("userstable.db")

c = db.cursor()

c.execute("""CREATE TABLE articles (
    id text,
    name text,
    groups text,
    birth_date text,
    role text
)""")

db.commit()
db.close()