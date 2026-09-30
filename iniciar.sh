set -euo pipefail 
cd "$(dirname "$0")"

if [ -z "${REGISTRO_CLAVE:-}"]; then 
   echo "falta REGISTRO_CLAVE. se define asi : export REGISTRO_CLAVE = tu_clave">&2 
   exit1
fi

export TZ="America/Bogota"

.venv/bin/python app.py