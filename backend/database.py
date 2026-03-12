import sqlite3

# connect database

conn = sqlite3.connect("kitchenbrain.db")

cur = conn.cursor()

# create table

cur.execute("""
CREATE TABLE IF NOT EXISTS food(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
expiry TEXT NOT NULL,
notified INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()

print("KitchenBrain database ready")
