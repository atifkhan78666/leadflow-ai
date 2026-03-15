import sqlite3
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "leads.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        address TEXT,
        phone TEXT,
        website TEXT,
        email TEXT,
        whatsapp TEXT,
        rating REAL,
        reviews INTEGER,
        maps_url TEXT,
        industry TEXT,
        location TEXT,
        scraped_at TEXT,
        email_sent INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()


def insert_lead(lead, industry, location):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id FROM leads
    WHERE name=? AND address=?
    """, (lead["Name"], lead["Address"]))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return

    cursor.execute("""
    INSERT INTO leads (
        name,
        address,
        phone,
        website,
        email,
        rating,
        reviews,
        maps_url,
        industry,
        location,
        scraped_at
    )
    VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, (
        lead["Name"],
        lead["Address"],
        lead["Phone"],
        lead["Website"],
        lead["Email"],
        lead["Rating"],
        lead["Reviews"],
        lead["Google Maps"],
        industry,
        location,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

def get_all_leads():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads")
    rows = cursor.fetchall()
    conn.close()
    return rows

def mark_email_sent(lead_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE leads
    SET email_sent=1
    WHERE id=?
    """, (lead_id,))
    conn.commit()
    conn.close()

def get_unsent_leads():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM leads
    WHERE email_sent=0 AND email IS NOT NULL
    """)

    rows = cursor.fetchall()
    conn.close()

def get_all_leads():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM leads")

    rows = cursor.fetchall()

    conn.close()

    return rows