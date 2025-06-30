import sqlite3
import os

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/scammers.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS scammers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL,
            reason TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_scammer(phone, reason):
    conn = sqlite3.connect("data/scammers.db")
    c = conn.cursor()
    c.execute("INSERT INTO scammers (phone, reason) VALUES (?, ?)", (phone, reason))
    conn.commit()
    conn.close()

def get_all_scammers():
    conn = sqlite3.connect("data/scammers.db")
    c = conn.cursor()
    c.execute("SELECT phone, reason FROM scammers")
    scammers = c.fetchall()
    conn.close()
    return scammers
