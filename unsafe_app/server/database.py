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
        create_transfers_table(cursor=cursor, conn=conn)
        create_officials_table(cursor=cursor, conn=conn)


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
    print('=====DATABASE: Table users already created!=====')


def create_transfers_table(cursor, conn):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transfers'")
    table_exists = cursor.fetchone()
    if not table_exists:
        cursor.execute("""
            CREATE TABLE transfers (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                account_number TEXT NOT NULL,
                amount TEXT NOT NULL,
                reciever_info TEXT NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.commit()
        print('=====DATABASE: Table transfers created successfully!=====')
    print('=====DATABASE: Table transfers already created!=====')


def create_officials_table(cursor, conn):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='officials'")
    table_exists = cursor.fetchone()
    if not table_exists:
        cursor.execute("""
            CREATE TABLE officials (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                user_email TEXT NOT NULL,
                user_first_name TEXT NOT NULL,
                user_last_name TEXT NOT NULL,
                description TEXT NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (user_email) REFERENCES users(email)
            )
        """)
        conn.commit()
        print('=====DATABASE: Table officials created successfully!=====')
    print('=====DATABASE: Table officials already created!=====')
