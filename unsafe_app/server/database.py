import os
import sqlite3


def get_db():
    db = sqlite3.connect("unsafe_sqlite.db")
    try:
        yield db
    finally:
        db.close()


def initialize_database():
    if not os.path.exists("unsafe_sqlite.db"):
        open("unsafe_sqlite.db", "w").close()

    print('=====DATABASE connected successfully!=====')

    with sqlite3.connect("unsafe_sqlite.db") as conn:
        cursor = conn.cursor()
        create_users_table(cursor=cursor, conn=conn)


def create_users_table(cursor, conn):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table_exists = cursor.fetchone()
    if not table_exists:
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                pesel TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL
            )
        """)
        conn.commit()
        print('=====DATABASE: Table users created successfully!=====')
