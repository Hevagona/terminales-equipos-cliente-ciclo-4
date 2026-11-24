#!/usr/bin/env bash
# Mira cómo está el servidor de pruebas. No cambia nada.
 

#!/usr/bin/env bash
# Mira cómo está el servidor de pruebas. No cambia nada.

echo "== 1. Programa sqlite3"
command -v sqlite3 || echo "NO está instalado"

echo "== 2. Usuario registro"
id registro 2>&1

echo "== 3. Carpeta /opt/registro"
ls -la /opt/registro 2>&1

echo "== 4. Visitas en la base"
python3 -c "
import sqlite3
for fila in sqlite3.connect('file:/opt/registro/registro.db?mode=ro', uri=True).execute('SELECT id, nombre, momento FROM visitas'):
    print(fila)
" 2>&1

echo "== 5. Configuración (registro.env)"
cat /opt/registro/registro.env 2>&1
echo "(líneas: $(wc -l 2>/dev/null < /opt/registro/registro.env || echo 0))"

echo "== 7. Avisos en .bashrc"
grep -c "SERVIDOR DE PRUEBAS" ~/.bashrc

