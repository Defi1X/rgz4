import sqlite3
from datetime import datetime, timedelta

DATABASE = 'reports.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports (hash TEXT PRIMARY KEY, report TEXT, date TIMESTAMP)''')
    conn.commit()
    conn.close()

def save_report(file_hash, report):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO reports (hash, report, date) VALUES (?, ?, ?)',
              (file_hash, str(report), datetime.now()))
    conn.commit()
    conn.close()

def get_report(file_hash):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT report FROM reports WHERE hash=?', (file_hash,))
    row = c.fetchone()
    conn.close()
    return eval(row[0]) if row else None

def get_statistics():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT COUNT(*), AVG(julianday(date) - julianday("now")) FROM reports')
    count, avg_age = c.fetchone()
    conn.close()
    return {
        'total_scans': count,
        'average_report_age_days': -avg_age if avg_age else None
    }

def clean_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM reports')

    conn.commit()
    conn.close()

clean_database()
init_db()
