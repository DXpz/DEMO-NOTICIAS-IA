# Documentación de Servidor — IAKimi Noticias

**Versión:** 2.0  
**Fecha:** 11 de marzo de 2026  
**Servidor:** `srv-noticias`

---

## 1. Arquitectura General

```
[Make]
  │
  │  POST /api/actualizar
  │  Header: X-API-Key
  │  Body: JSON de noticias
  ▼
[FastAPI — puerto 8000 (interno)]
  │
  │  Guarda noticias.json
  │  Ejecuta actualizar_index.py
  │  Ejecuta generar_paginas.py
  ▼
[Nginx — puerto 80 (público)]
  │
  │  Sirve archivos HTML estáticos
  ▼
[Usuario final en el navegador]
```

---

## 2. Especificaciones del Servidor

| Campo | Valor |
|---|---|
| Hostname | `srv-noticias` |
| Sistema Operativo | Debian 12 (Bookworm) |
| Kernel | `6.1.0-43-amd64` |
| Infraestructura | VM sobre Proxmox |
| vCPU | 2 |
| RAM | 2 GB |
| Almacenamiento | 40 GB SSD |
| IP Privada | `172.17.3.43` |
| IP Pública | `200.35.189.130` |
| Usuario SSH | `iakimi` |

---

## 3. Software Instalado

| Paquete | Versión | Uso |
|---|---|---|
| Nginx | 1.22.1 | Servidor web |
| Python 3 | 3.11 | Ejecución de scripts |
| FastAPI | 0.135.1 | API REST |
| Uvicorn | 0.41.0 | Servidor ASGI para FastAPI |
| rsync | — | Sincronización de archivos |
| curl | — | Diagnóstico de red |

---

## 4. Estructura de Archivos en el Servidor

```
/home/iakimi/noticias-ia/
├── api.py                      ← API FastAPI
├── actualizar_index.py         ← Genera index.html
├── generar_paginas.py          ← Genera páginas individuales
├── actualizar_todo.py          ← Script auxiliar
├── noticias.json               ← Base de datos de noticias activas
├── noticias_antiguas.json      ← Historial de noticias archivadas
├── historial_completo.json     ← Historial completo
├── index.html                  ← Portada generada
├── noticias/                   ← Páginas HTML individuales
├── noticias_ant/               ← Páginas archivadas
├── IMG/                        ← Imágenes del sitio
├── venv/                       ← Entorno virtual Python
├── .api_key                    ← Clave secreta de la API (no compartir)
└── api.log                     ← Log de actividad de la API
```

---

## 5. Configuración de Nginx

**Archivo:** `/etc/nginx/sites-available/noticias-ia`  
**Enlace activo:** `/etc/nginx/sites-enabled/noticias-ia`

```nginx
server {
    listen 80;
    server_name _;

    root /home/iakimi/noticias-ia;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /health {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }
}
```

**Comandos de gestión:**

```bash
sudo nginx -t                    # Verificar configuración
sudo systemctl reload nginx      # Aplicar cambios
sudo systemctl status nginx      # Ver estado
```

---

## 6. Servicio FastAPI (systemd)

**Archivo:** `/etc/systemd/system/noticias-api.service`

```ini
[Unit]
Description=IAKimi Noticias FastAPI
After=network.target

[Service]
User=iakimi
WorkingDirectory=/home/iakimi/noticias-ia
ExecStart=/home/iakimi/noticias-ia/venv/bin/uvicorn api:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

**Comandos de gestión:**

```bash
sudo systemctl status noticias-api     # Ver estado
sudo systemctl restart noticias-api    # Reiniciar
sudo systemctl stop noticias-api       # Detener
sudo systemctl start noticias-api      # Iniciar
journalctl -u noticias-api -f          # Ver logs en tiempo real
```

---

## 7. API FastAPI

### URL base

```
https://noticias.iakimi.com
```

### Endpoints disponibles

#### `GET /health`
Comprueba que la API está activa. No requiere autenticación.

**Respuesta:**
```json
{
  "status": "ok",
  "timestamp": "2026-03-10T13:24:40.532239"
}
```

---

#### `POST /api/actualizar`
Recibe el JSON de noticias, lo guarda y regenera el sitio web completo.

**Headers requeridos:**

| Header | Valor |
|---|---|
| `X-API-Key` | Clave secreta almacenada en `.api_key` |
| `Content-Type` | `application/json` |

**Body:** JSON con la estructura completa de noticias (mismo formato que `noticias.json`)

**Respuesta exitosa:**
```json
{
  "status": "ok",
  "mensaje": "Sitio actualizado correctamente",
  "timestamp": "2026-03-11T13:25:40.906092"
}
```

**Respuesta con error parcial (código 207):**
```json
{
  "status": "parcial",
  "mensaje": "noticias.json guardado pero hubo errores en los scripts",
  "errores": ["Error en actualizar_todo.py: ..."]
}
```

**Respuesta con API key inválida (código 403):**
```json
{
  "detail": "API key inválida"
}
```

---

#### `GET /api/noticias`
Devuelve el contenido actual de `noticias.json`. Requiere autenticación.

**Headers requeridos:**

| Header | Valor |
|---|---|
| `X-API-Key` | Clave secreta almacenada en `.api_key` |

**Respuesta:** JSON completo con la estructura actual de `noticias.json`.

**Uso en Make:**
- Method: `GET`
- URL: `https://noticias.iakimi.com/api/noticias`
- Header: `X-API-Key: tu_clave`

---

### Webhooks de notificación

Al completar `/api/actualizar` la API llama automáticamente a dos webhooks de Make:

| Webhook | Cuándo | Payload |
|---|---|---|
| `smnd3366zz9hv9t0s5lf93x18rwut2q8` | Inmediatamente al terminar | `{"success": true/false, "mensaje": "...", "timestamp": "..."}` |
| `fu7d7r70mrhqvcxdqo79yfhuyeqas7jn` | 5 minutos después (solo si éxito) | `{"status": "ok", "timestamp": "..."}` |

El segundo webhook se ejecuta en segundo plano — la API responde a Make sin esperar los 5 minutos.

---

### URL de noticias individuales

```
https://noticias.iakimi.com/noticias/{id}.html
```

Ejemplo:
```
https://noticias.iakimi.com/noticias/nvidia-consolida-su-dominio.html
```

En Make: `https://noticias.iakimi.com/noticias/{{id}}.html`

---

### Prueba manual desde terminal

```bash
# Verificar estado
curl -s https://noticias.iakimi.com/health

# Enviar noticias y regenerar sitio
curl -s -X POST https://noticias.iakimi.com/api/actualizar \
  -H "X-API-Key: TU_API_KEY" \
  -H "Content-Type: application/json" \
  -d @/ruta/local/noticias.json
```

---

## 8. Configuración en Make

Para enviar el JSON de noticias automáticamente desde Make:

1. Añadir módulo **HTTP → Make a request**
2. Configurar:

| Campo | Valor |
|---|---|
| URL | `https://noticias.iakimi.com/api/actualizar` |
| Method | `POST` |
| Headers | `X-API-Key: tu_clave_secreta` |
| Body type | `Raw` |
| Content type | `application/json` |
| Body | JSON de noticias generado en el escenario |

---

## 9. API Key

La API key se almacena en `/home/iakimi/noticias-ia/.api_key`.

**Para regenerar una nueva API key:**

```bash
python3 -c "import secrets; print(secrets.token_hex(32))" > /home/iakimi/noticias-ia/.api_key
sudo systemctl restart noticias-api
```

> Tras regenerarla, actualiza también el valor en Make.

---

## 10. Logs

La API registra toda la actividad en `/home/iakimi/noticias-ia/api.log`.

```bash
# Ver logs completos
cat /home/iakimi/noticias-ia/api.log

# Ver logs en tiempo real
tail -f /home/iakimi/noticias-ia/api.log

# Ver logs del servicio systemd
journalctl -u noticias-api -f
```

---

## 11. Sincronizar archivos desde la máquina local

Para subir cambios del proyecto al servidor:

```bash
sudo rsync -avz --progress \
  /home/sstar/Documents/TESTRED/ADOPTIA/DEMO-NOTICIAS-IA/ \
  iakimi@172.17.3.43:/home/iakimi/noticias-ia/
```

Para subir solo un archivo concreto:

```bash
sudo rsync -avz \
  /home/sstar/Documents/TESTRED/ADOPTIA/DEMO-NOTICIAS-IA/api.py \
  iakimi@172.17.3.43:/home/iakimi/noticias-ia/
```

---

## 12. Acceso externo

El sitio es accesible públicamente desde internet.

- **Dominio:** `noticias.iakimi.com`
- **IP pública:** `200.35.189.130`
- **HTTP:** redirige automáticamente a HTTPS
- **HTTPS:** certificado SSL de Let's Encrypt gestionado por Certbot

### Renovación automática del certificado SSL

Certbot renueva el certificado automáticamente cada 90 días. Para verificar:

```bash
sudo certbot renew --dry-run
```

---

## 13. Flujo completo de actualización

```
1. Make genera el JSON de noticias
2. Make hace POST a /api/actualizar con X-API-Key
3. FastAPI valida la API key
4. FastAPI guarda el JSON en noticias.json
5. FastAPI ejecuta actualizar_index.py → regenera index.html
6. FastAPI ejecuta generar_paginas.py → regenera páginas individuales
7. Nginx sirve el HTML actualizado al usuario
```
