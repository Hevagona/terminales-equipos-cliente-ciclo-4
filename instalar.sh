set -euo pipefail
cd "$(dirname "$0")"

python3 -m venv .venv

.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python crear_db.py
echo "Intalación lista. para iniciar: bash iniciar.sh"
