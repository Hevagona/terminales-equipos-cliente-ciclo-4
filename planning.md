# Plan de Trabajo — Finalización del Kit de Despliegue Reproducible

**Proyecto:** Registro de Visitas (Flask + Ansible)  
**Entrega final:** Jueves 3 de diciembre, 11:59 pm  
**Regla de oro:** *La IA escribe y explica. El Codespace nuevo es el juez.*

---

## 1. Contexto y Objetivos

El objetivo de este proyecto es construir un **kit de despliegue reproducible** para una aplicación web pequeña en Flask. Cualquier persona debe poder clonar el repositorio en un GitHub Codespace nuevo (Ubuntu 24), seguir únicamente las instrucciones del `README.md` y levantar:
1. **Ambiente de Pruebas:** Bajo el usuario del sistema `registro`, en `/opt/registro`, con su clave `REGISTRO_CLAVE`, virtualenv y base de datos de pruebas con visita de verificación.
2. **Ambiente de Producción:** En la misma máquina pero completamente segmentado y aislado, bajo el usuario `registro-prod`, en `/opt/registro-prod`, con permisos restrictivos (`0750` y `0600`), su clave independiente `REGISTRO_CLAVE_PROD` y sin datos de prueba.

---

## 2. Arquitectura y Uso de Ansible

Ansible es la herramienta central de automatización de este proyecto. Su función es garantizar que cualquier servidor pueda ser aprovisionado de forma **reproducible** y **declarativa**:
- **Declarativo vs Imperativo:** En lugar de ejecutar una lista de pasos (`bash provisionar.sh`), Ansible describe el **estado final deseado** del sistema (p. ej. "el usuario debe existir", "el archivo debe tener permisos 0600"). Si ya está en ese estado, no hace nada.
- **Idempotencia (`changed=0`):** Una corrida sobre un sistema ya configurado debe dar `ok` en todas las tareas y `changed=0`. Esto asegura que correr el playbook múltiples veces sea completamente seguro.
- **Módulos nativos (`ansible.builtin.*`):**
  - `ansible.builtin.assert`: Detiene la ejecución si falta una variable obligatoria.
  - `ansible.builtin.user` / `group`: Administra usuarios y grupos del sistema sin shell de login (`/usr/sbin/nologin`).
  - `ansible.builtin.file`: Crea carpetas y asegura permisos (`0750`).
  - `ansible.builtin.copy`: Despliega archivos de código y configuración sensible (`0600`).
  - `ansible.builtin.pip`: Gestiona el entorno virtual de Python (`venv`) y sus dependencias.
  - `ansible.builtin.command`: Ejecuta scripts de inicialización (`crear_db.py`).
- **Seguridad en Ansible:**
  - `lookup('ansible.builtin.env', 'REGISTRO_CLAVE')`: Extrae el secreto de la memoria del entorno en tiempo de ejecución.
  - `no_log: true`: Evita que Ansible imprima en consola o logs el contenido de tareas que manipulan secretos.
- **Comandos de ejecución en el Codespace:**
  - Instalar: `pip install -r requirements-infra.txt` y `export PATH="$HOME/.local/bin:$PATH"`
  - Pruebas: `ansible-playbook provisionar.yml`
  - Producción: `ansible-playbook produccion.yml`

---

## 3. Reglas de Trabajo No Negociables

1. **Explicar antes de cambiar:** En español sencillo, conceptos antes del código.
2. **Un solo cambio a la vez:** Paso a paso, sin tocar múltiples archivos no relacionados.
3. **Cero secretos en el código:** Nunca escribir claves reales en archivos ni pegarlas en el chat. Se toman del entorno (`REGISTRO_CLAVE` y `REGISTRO_CLAVE_PROD`).
4. **Versiones fijadas (`==`):** Nada de versiones flotantes o inventadas.
5. **No sudo local ni git push automático:** Todo se prueba en el Codespace. En este computador no se ejecuta `sudo` ni se hace `git push` sin permiso explícito.
6. **La evidencia es tuya:** Las salidas de terminal (`changed=0`, `Permission denied`, conteos) se obtienen de corridas reales en el Codespace; no se inventan.

---

## 3. Ciclo de Trabajo por Cada Paso

```text
Antigravity (explica y edita) 
       ↓ 
Tú revisas la explicación y el cambio
       ↓ 
git add, commit y push hacia GitHub
       ↓ 
En Codespace nuevo: git pull (o git clone)
       ↓ 
Ejecutas los comandos de prueba indicados
       ↓ 
¿Salió el resultado esperado?
    ├── SÍ → Marcar paso en planning.md y pasar al siguiente
    └── NO → Traer el error exacto (sin claves) al chat para analizarlo
```

---

## 4. Estado Actual del Repositorio (Diagnóstico)

| Componente | Estado | Detalle |
| :--- | :---: | :--- |
| `requirements-infra.txt` | **Falta** | No existe; se requiere fijar Ansible. |
| `provisionar.yml` (Pruebas) | **A medias** | Crea usuario y carpeta, maneja secreto con `assert`/`no_log`, pero falta copiar la app, crear el virtualenv, instalar dependencias e inicializar la base de datos con verificación idempotente. |
| `produccion.yml` (Producción) | **Falta** | No existe; debe aislar `/opt/registro-prod`, usuario `registro-prod`, clave `REGISTRO_CLAVE_PROD` y base de datos limpia. |
| `inspeccionar.sh` | **Listo** | Enmascara la clave correctamente (solo requiere limpiar un encabezado duplicado). |
| `README.md` | **A medias** | Falta la guía paso a paso completa para que un tercero reconstruya ambos ambientes sin intervención manual. |
| `PROVISION.md` | **Falta** | Falta documentar punto de partida, idempotencia, tabla de alcance, manejo de secretos y sección de uso de IA. |
| `VERIFICACION_AMBIENTES.md` | **Falta** | Falta evidencia real de intento de acceso cruzado, equivalencia Factor X, diferencia no prevista y análisis de costos/aislamiento. |
| Repositorio sin secretos | **Listo** | Verificado; no hay claves reales en el código actual. |

---

## 5. Fases de Ejecución Paso a Paso

### Fase 1: Base de Infraestructura (Prompt 2 - Parte 1)
- [x] **Paso 1.1:** Crear `requirements-infra.txt` fijando `ansible-core` con una versión estable verificada (`ansible-core==2.17.6`).
  - *Prueba en Codespace:* `pip install -r requirements-infra.txt` y `ansible --version`.

### Fase 2: Completar Ambiente de Pruebas (Prompt 2 - Parte 2)
- [ ] **Paso 2.1:** Extender `provisionar.yml` para:
  - Copiar los archivos de la app (`app.py`, `requirements.txt`, `crear_db.py`).
  - Crear el entorno virtual (`venv`) en `/opt/registro/venv`.
  - Instalar `requirements.txt` en ese venv.
  - Ejecutar `crear_db.py` para crear `registro.db`.
  - Crear una visita inicial de verificación de manera idempotente (`register` + `when`).
- [ ] **Paso 2.2:** Probar en Codespace nuevo:
  - 1.ª corrida: instala todo.
  - 2.ª corrida: verifica idempotencia (`changed=0`).
  - 3.ª corrida sin variable: verifica que falle en el `assert`.
  - Comprobar permisos: `cat /opt/registro/registro.env` da `Permission denied`.
  - Levantar la app de pruebas en puerto 5000 y registrar visita.

### Fase 3: Ambiente de Producción Segmentado (Prompt 3)
- [ ] **Paso 3.1:** Crear `produccion.yml`:
  - Usuario propio: `registro-prod` (dueño de `/opt/registro-prod`).
  - Carpeta en modo `0750` y `registro.env` en `0600` con `no_log: true`.
  - Clave tomada de `REGISTRO_CLAVE_PROD`.
  - `assert` que verifique que existe y que es distinta a `REGISTRO_CLAVE`.
  - Sin datos ni visitas de prueba.
- [ ] **Paso 3.2:** Probar en Codespace:
  - 2.ª corrida con `changed=0`.
  - Validación con claves iguales para ver que el `assert` detenga el despliegue.

### Fase 4: Pruebas de Seguridad y Factor X (Prompts 4 y 5)
- [ ] **Paso 4.1:** Ejecutar el intento controlado de acceso desde `registro` hacia `/opt/registro-prod`:
  - Intentar leer `registro.env`.
  - Intentar leer visitas en SQLite.
  - Intentar borrar visitas en SQLite.
  - Copiar la evidencia real a `VERIFICACION_AMBIENTES.md`.
- [ ] **Paso 4.2:** Ejecutar comandos de equivalencia entre pruebas y producción:
  - Comparar `pip freeze`, versiones de Python, esquema de base de datos y zona horaria.
  - Registrar la diferencia no prevista y argumentar la decisión en `VERIFICACION_AMBIENTES.md`.
  - Redactar la decisión económica sobre aislamiento para una tienda pequeña.

### Fase 5: Documentación de Aprovisionamiento (Prompts 2 y 8)
- [ ] **Paso 5.1:** Crear `PROVISION.md`:
  - Punto de partida del playbook.
  - Explicación de tareas e idempotencia (`changed=0`).
  - Tabla de alcance (lo que se asume del ambiente base).
  - Tratamiento de datos sensibles.
  - Sección "Uso de IA" con los tres apartados obligatorios y los `[COMPLETAR]` del estudiante.

### Fase 6: Manual de Reconstrucción y Auditoría Final (Prompts 6 y 7)
- [ ] **Paso 6.1:** Redactar `README.md` completo:
  - Pasos exactos desde cero (variables, instalación de Ansible, playbooks, arranque en puertos 5000 y 5001, y verificación de aislamiento).
- [ ] **Paso 6.2:** Auditoría de "compañero ciego":
  - Revisar si el `README.md` deja alguna duda o paso tácito.
- [ ] **Paso 6.3:** Limpieza menor de `inspeccionar.sh` y verificación final de que no existan credenciales en Git (`git grep`).
