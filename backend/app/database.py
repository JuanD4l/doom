"""
CAPA DE BASE DE DATOS Y CONEXIÓN
Soporta SQLAlchemy con fallback transparente al driver nativo sqlite3.
"""

import os
import sqlite3
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cyberdoom.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            wave INTEGER NOT NULL,
            kills INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    # Insertar datos semilla si la tabla está vacía
    cursor.execute("SELECT COUNT(*) as cnt FROM scores")
    count = cursor.fetchone()[0]
    if count == 0:
        seed_data = [
            ("CYBER_SLAYER", 15400, 7, 28),
            ("NEO_V", 12100, 5, 21),
            ("NIGHT_HAWK", 9800, 4, 17),
            ("GLITCH_RUNNER", 7600, 3, 13),
            ("GHOST_SHELL", 5200, 2, 9),
            ("CYBER_MARINE", 3400, 2, 6),
            ("ZERO_COOL", 2100, 1, 4),
        ]
        cursor.executemany("""
            INSERT INTO scores (player_name, score, wave, kills)
            VALUES (?, ?, ?, ?)
        """, seed_data)
        conn.commit()

    conn.close()

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# Inicializar esquema al arrancar
init_db()
