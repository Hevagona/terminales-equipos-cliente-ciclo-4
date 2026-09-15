"""Crea la base de datos vacia que la aplicacion necesita."""

import os
import sqlite3

DB_PATH = os.environ.get("REGISTRO_DB", "registro.db")

con = sqlite3.connect(DB_PATH)
con.execute(
    """
    CREATE TABLE IF NOT EXISTS visitas (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre  TEXT NOT NULL,
        momento TEXT NOT NULL
    )
    """
)
con.commit()
con.close()

print(f"Listo. Base de datos creada en: {DB_PATH}")
