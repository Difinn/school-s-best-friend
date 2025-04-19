import sqlite3
db = sqlite3.connect("userstable.db")

c = db.cursor()

c.execute("""CREATE TABLE articles (
    name text,
    description text,
    time text,
    notifications text
)""")

#id это по номеру (len + 1), хотя есть rowid, но это нюансы
#Я выбираю rowid

db.commit()
db.close()