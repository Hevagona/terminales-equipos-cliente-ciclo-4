
import os
import sqlite3
from datetime import datetime

from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)

DB_PATH = os.environ.get("REGISTRO_DB", "registro.db")

CLAVE = os.environ.get("REGISTRO_CLAVE")
if not CLAVE:
    raise RuntimeError(
        "Falta la variable de entorno REGISTRO_CLAVE. "
        "La aplicacion no arranca sin ella."
    )

app.secret_key = CLAVE

PLANTILLA = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Registro de Visitas</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 640px; margin: 3rem auto; padding: 0 1rem; }
    h1 { font-size: 1.5rem; }
    form { display: flex; gap: .5rem; margin-bottom: 2rem; }
    input { flex: 1; padding: .5rem; font-size: 1rem; }
    button { padding: .5rem 1rem; font-size: 1rem; cursor: pointer; }
    li { margin-bottom: .35rem; }
    .vacio { color: #666; font-style: italic; }
  </style>
</head>
<body>
  <h1>Registro de Visitas</h1>
  <form method="post" action="/registrar">
    <input name="nombre" placeholder="Nombre del visitante" required>
    <button type="submit">Registrar</button>
  </form>
  {% if visitas %}
    <ul>
    {% for nombre, momento in visitas %}
      <li><strong>{{ nombre }}</strong> — {{ momento }}</li>
    {% endfor %}
    </ul>
  {% else %}
    <p class="vacio">Todavia no hay visitas registradas.</p>
  {% endif %}
</body>
</html>
"""


def conectar():
    if not os.path.exists(DB_PATH):
        raise RuntimeError(
            f"No existe la base de datos '{DB_PATH}'. "
            "Hay que crearla antes de arrancar la aplicacion."
        )
    return sqlite3.connect(DB_PATH)


@app.route("/")
def inicio():
    con = conectar()
    filas = con.execute(
        "SELECT nombre, momento FROM visitas ORDER BY id DESC"
    ).fetchall()
    con.close()
    return render_template_string(PLANTILLA, visitas=filas)


@app.route("/registrar", methods=["POST"])
def registrar():
    nombre = request.form["nombre"]
    momento = datetime.now().strftime("%Y-%m-%d %H:%M")
    con = conectar()
    con.execute(
        "INSERT INTO visitas (nombre, momento) VALUES (?, ?)", (nombre, momento)
    )
    con.commit()
    con.close()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
