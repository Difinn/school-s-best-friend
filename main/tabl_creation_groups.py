import sqlite3
db = sqlite3.connect("groupstable.db")

c = db.cursor()

c.execute("""CREATE TABLE articles (
    id text,
    name text,
    participants text,
    otchim text,
    events text
)""")

#otchim - это классрук (или декан)
#бляяя нужно по row id как-то использовать для получения группы из имени

db.commit()
db.close()