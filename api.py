#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API FastAPI para recibir el JSON de noticias desde Make
y regenerar automáticamente el sitio web.
"""

import json
import subprocess
import logging
import urllib.request
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, Security, Request
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import JSONResponse

# ── Configuración ──────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
NOTICIAS_JSON = BASE_DIR / "noticias.json"
LOG_FILE = BASE_DIR / "api.log"
API_KEY_FILE = BASE_DIR / ".api_key"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ── Cargar API key desde archivo ───────────────────────────────────────────────
if not API_KEY_FILE.exists():
    raise RuntimeError(f"Falta el archivo de API key: {API_KEY_FILE}")

API_KEY = API_KEY_FILE.read_text().strip()

MAKE_WEBHOOK = "https://hook.eu2.make.com/smnd3366zz9hv9t0s5lf93x18rwut2q8"


def notificar_make(exito: bool, mensaje: str, timestamp: str):
    """Envía notificación al webhook de Make al finalizar la actualización."""
    payload = json.dumps({
        "success": exito,
        "mensaje": mensaje,
        "timestamp": timestamp,
    }).encode("utf-8")
    try:
        req = urllib.request.Request(
            MAKE_WEBHOOK,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            logging.info(f"Webhook Make notificado — status {resp.status}")
    except Exception as e:
        logging.warning(f"No se pudo notificar al webhook de Make: {e}")


# ── App ────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="IAKimi Noticias API",
    description="Recibe el JSON de noticias y regenera el sitio web.",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verificar_api_key(key: str = Security(api_key_header)):
    if key != API_KEY:
        logging.warning("Intento de acceso con API key inválida")
        raise HTTPException(status_code=403, detail="API key inválida")
    return key


# ── Endpoints ──────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    """Comprueba que la API está activa."""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.post("/api/actualizar")
async def actualizar_noticias(request: Request, key: str = Security(verificar_api_key)):
    """
    Recibe el JSON de noticias desde Make, lo guarda y regenera el sitio.
    Header requerido: X-API-Key
    Body: JSON con la lista de noticias
    """
    try:
        datos = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="El body no es JSON válido")

    # Guardar noticias.json
    try:
        NOTICIAS_JSON.write_text(json.dumps(datos, ensure_ascii=False, indent=2))
        logging.info(f"noticias.json actualizado — {len(datos) if isinstance(datos, list) else '?'} entradas")
    except Exception as e:
        logging.error(f"Error al guardar noticias.json: {e}")
        raise HTTPException(status_code=500, detail=f"Error al guardar noticias.json: {e}")

    # Ejecutar script maestro
    errores = []
    resultado = subprocess.run(
        ["python3", str(BASE_DIR / "actualizar_todo.py")],
        capture_output=True,
        text=True,
        cwd=str(BASE_DIR),
    )
    if resultado.returncode != 0:
        msg = f"Error en actualizar_todo.py: {resultado.stderr.strip()}"
        logging.error(msg)
        errores.append(msg)
    else:
        logging.info("actualizar_todo.py ejecutado correctamente")

    timestamp = datetime.now().isoformat()

    if errores:
        notificar_make(False, f"Errores en scripts: {'; '.join(errores)}", timestamp)
        return JSONResponse(status_code=207, content={
            "status": "parcial",
            "mensaje": "noticias.json guardado pero hubo errores en los scripts",
            "errores": errores,
        })

    logging.info("Sitio regenerado correctamente")
    notificar_make(True, "Sitio actualizado correctamente", timestamp)
    return {"status": "ok", "mensaje": "Sitio actualizado correctamente", "timestamp": timestamp}
