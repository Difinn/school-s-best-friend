import sqlite3
db = sqlite3.connect("groupstable.db")

c = db.cursor()

c.execute("""CREATE TABLE articles (
    id text,
    name text,
    participants text,
    dean text,
    events text
)""")

#dean - это классрук (или декан)

db.commit()
db.close()