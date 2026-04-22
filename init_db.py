import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'hw13.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'schema.sql')

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

with open(SCHEMA_PATH, 'r') as f:
    conn.executescript(f.read())

cur.execute("""
    INSERT INTO students (first_name, last_name)
    VALUES (?, ?)
""", ('John', 'Smith'))

cur.execute("""
    INSERT INTO quizzes (subject, num_questions, quiz_date)
    VALUES (?, ?, ?)
""", ('Python Basics', 5, '2015-02-05'))

cur.execute("""
    INSERT INTO results (student_id, quiz_id, score)
    VALUES (?, ?, ?)
""", (1, 1, 85))

conn.commit()
conn.close()

print('Database created successfully.')
print('Database path:', DB_PATH)