import sqlite3

conn = sqlite3.connect("kitchenbrain.db")

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS food(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
expiry TEXT
)
""")

conn.commit()
conn.close()

print("Database created")