import sqlite3

DB_NAME = "smc_bot.db"


def get_connection():

    return sqlite3.connect(
        DB_NAME,
        check_same_thread=False
    )


def init_db():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS signals (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        symbol TEXT NOT NULL,

        side TEXT NOT NULL,

        zone_start REAL NOT NULL,

        zone_end REAL NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
