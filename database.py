import sqlite3

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    user_id TEXT,
    date TEXT,
    punch_in TEXT,
    punch_out TEXT
)
""")

conn.commit()
conn.close()
