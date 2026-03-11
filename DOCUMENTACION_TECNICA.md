# Documentación Técnica: DEMO-NOTICIAS-IA

**Versión:** 3.0  
**Última actualización:** 10 de marzo de 2026  
**Repositorio:** https://github.com/DXpz/DEMO-NOTICIAS-IA.git

---

## 1. Resumen Ejecutivo

DEMO-NOTICIAS-IA es un **sitio web estático de noticias** generado a partir de un archivo JSON. El sistema automatiza la creación de páginas HTML, el archivo de noticias antiguas y la actualización de la portada. No existe base de datos: todo se gestiona mediante scripts Python que leen `noticias.json` y generan HTML estático servido por Nginx en un servidor privado.

A partir de la versión 3.0, el sitio ha sido migrado de Vercel a un servidor privado dedicado (Debian 12 sobre Proxmox) y cuenta con una **API FastAPI** que recibe el JSON de noticias desde Make y regenera el sitio automáticamente.

---

## 2. Funcionalidades Principales

| Funcionalidad | Descripción |
|---------------|-------------|
| **Edición manual de noticias** | El contenido se edita únicamente en `noticias.json`. No se toca HTML a mano. |
| **Generación automática de páginas** | Cada noticia en `noticias.json` genera un HTML en `noticias/{id}.html`. |
| **Archivo automático de noticias antiguas** | Las noticias que dejan de estar en `noticias.json` se mueven a `noticias_ant/` y sus datos se guardan en `noticias_antiguas.json`. |
| **Historial completo** | Todas las noticias publicadas se registran en `historial_completo.json` con `fecha_primera_publicacion`. |
| **Redirecciones para enlaces antiguos** | Al archivar una noticia, se crea en `noticias/` una página que redirige a `noticias_ant/{id}.html`, manteniendo los enlaces funcionales. |
| **Portada dinámica** | `index.html` se regenera con la noticia principal, secundarias y "Lo último" según `noticias.json`. |
| **Push automático a Git** | `actualizar_todo.py` hace `git add`, `commit` y `push` si hay cambios. |
| **API FastAPI** | `api.py` expone `POST /api/actualizar` que recibe el JSON de Make, lo guarda y ejecuta los scripts. |
| **Despliegue en servidor privado** | Nginx sirve el HTML estático directamente desde `/home/iakimi/noticias-ia`. |
| **Dependencias de API** | `api.py` requiere FastAPI y Uvicorn (instalados en `venv/`). Los scripts de generación siguen sin dependencias. |
| **Citas y puntos clave** | Soporte para bloques de cita (`blockquote`) y listas de puntos clave en cada artículo. |
| **Imágenes con caption** | Cada noticia puede tener imagen, `alt` y caption. |
| **Configuración centralizada** | Título del sitio, edición y fecha en `noticias.json` → `config`. |
| **Breadcrumbs por categoría** | Cada artículo muestra la categoría como breadcrumb en el header. |
| **Lead automático** | Si no hay `resumen`, se usa el primer párrafo de `contenido_completo` (200 caracteres). |
| **Coautor opcional** | Campo `coautor` para firmas compartidas. |
| **Artículos de opinión** | Estructura `articulos_opinion` en JSON (preparada para futura expansión). |
| **Cache deshabilitado** | Headers `Cache-Control` en Vercel para ver cambios al instante. |
| **Layout de portada** | Hero (noticia principal) + grid de secundarias + sección "Lo último". |
| **Botón "Volver a portada"** | Cada artículo incluye enlace de vuelta al `index.html`. |
| **Sidebar en artículos** | Bloque "Noticias Relacionadas" con enlace a la portada. |
| **Diseño responsive** | Grid adaptativo: una columna en tablet/móvil (`max-width: 1024px`). |
| **Favicon** | Logo IAKimi en pestaña del navegador. |
| **Branding "Diario El Mundo"** | Línea "En colaboración con Diario El Mundo" en el header. |
| **Historial vs archivadas** | `historial_completo.json` = todas las noticias publicadas (actuales + archivadas). `noticias_antiguas.json` = solo las que ya no están en portada. |
| **Slug como ID** | El `id` de cada noticia es el slug de la URL (ej. `google-reduce-comisiones-en-android-...`). Define el nombre del archivo y la ruta. |
| **Meta refresh para archivadas** | Las páginas de redirección usan `<meta http-equiv="refresh">` para enviar al usuario a `noticias_ant/{id}.html` automáticamente. |
| **Scripts ejecutables por separado** | Se puede ejecutar solo `generar_paginas.py` o solo `actualizar_index.py` si no se quiere el flujo completo. |

---

## 3. Sistema de Noticias Antiguas (Archivadas)

**Resumen:** Las noticias antiguas quedan en **tres sitios**: (1) `noticias_ant/{id}.html` — HTML del artículo; (2) `noticias/{id}.html` — página de redirección; (3) `noticias_antiguas.json` — datos completos en JSON.

### 3.1 ¿Qué son y cuándo se archivan?

Una noticia se considera **antigua** cuando su `id` ya **no aparece** en `noticias.json` (ni en `noticia_principal`, ni en `noticias_secundarias`, ni en `noticias_lo_ultimo`). Al ejecutar `generar_paginas.py`, el sistema:

1. Compara los archivos HTML en `noticias/` con los IDs actuales.
2. Los que ya no están en `noticias.json` se archivan.

### 3.2 ¿Dónde quedan las noticias antiguas?

| Ubicación | Contenido |
|-----------|-----------|
| **`noticias_ant/{id}.html`** | El HTML completo del artículo (el mismo que estaba en `noticias/`). Se **mueve** aquí. |
| **`noticias/{id}.html`** | Una página de **redirección** que envía al usuario a `../noticias_ant/{id}.html` (meta refresh + enlace manual). |
| **`noticias_antiguas.json`** | Array con los **datos completos** de cada noticia archivada: título, categoría, resumen, autor, imagen, `contenido_completo`, citas, puntos clave, `fecha_primera_publicacion`, `fecha_archivo`. |

### 3.3 Flujo de archivo (paso a paso)

```
Noticia "X" estaba en noticias.json → noticias/x.html existe
         │
         │  Usuario edita noticias.json y quita la noticia "X"
         │
         ▼
Ejecuta: python3 actualizar_todo.py
         │
         ├─► guardar_noticias_en_historial() → historial_completo.json
         │
         ├─► archivar_noticias_antiguas():
         │       │
         │       ├─ Mueve noticias/x.html → noticias_ant/x.html
         │       ├─ Crea noticias/x.html (redirección a noticias_ant/x.html)
         │       └─ Añade datos de "X" a noticias_antiguas.json
         │
         └─► Genera HTML de noticias actuales
```

### 3.4 URLs y acceso

| Tipo | URL | Comportamiento |
|------|-----|----------------|
| Noticia actual | `/noticias/google-reduce-comisiones-....html` | Muestra el artículo completo. |
| Noticia archivada (enlace antiguo) | `/noticias/robotica-ia-almacenes-hogares.html` | Redirige automáticamente a la versión archivada. |
| Noticia archivada (directa) | `/noticias_ant/robotica-ia-almacenes-hogares.html` | Muestra el artículo archivado. |

### 3.5 Recuperar o consultar noticias archivadas

- **HTML:** `ls noticias_ant/` o abrir `/noticias_ant/{id}.html` en el navegador.
- **Datos JSON:** `noticias_antiguas.json` (array `noticias`) y `historial_completo.json` (objeto por `id`).

---

## 4. Estructura del Proyecto

```
DEMO-NOTICIAS-IA/
├── index.html                    # Portada del sitio (generada automáticamente)
├── noticias.json                 # Fuente de datos principal
├── historial_completo.json       # Historial de todas las noticias publicadas
├── noticias_antiguas.json        # Noticias archivadas con datos completos
├── vercel.json                   # Configuración legacy Vercel (ya no se usa)
├── api.py                        # API FastAPI — recibe JSON de Make y regenera el sitio
├── README_SCRIPTS.md             # Documentación de uso de scripts
├── DOCUMENTACION_TECNICA.md      # Este documento
├── DOCUMENTACION_SERVIDOR.md     # Documentación de infraestructura del servidor
│
├── generar_paginas.py            # Script 1: genera páginas HTML + archivo de antiguas
├── actualizar_index.py           # Script 2: regenera index.html
├── actualizar_todo.py            # Script maestro (uso manual)
│
├── noticias/                     # Páginas HTML de noticias actuales
│   ├── {id}.html                 # Una por noticia
│   └── ...                       # + páginas de redirección para archivadas
│
├── noticias_ant/                 # Noticias archivadas (HTML movidos aquí)
│   └── {id}.html
│
├── IMG/                          # Assets estáticos
│   ├── Logo IAKimi - Sin Fondo.png
│   ├── Logo IAKimi - Negativo.png
│   └── Logo IAKimi - Positivo.png
│
└── venv/                         # Entorno virtual Python (solo en servidor)
    └── ...
```

---

## 5. Stack Tecnológico

| Categoría | Tecnología |
|-----------|------------|
| **Lenguaje** | Python 3 |
| **Frontend** | HTML5 + CSS3 (sin JavaScript) |
| **Datos** | JSON |
| **API** | FastAPI + Uvicorn |
| **Servidor web** | Nginx 1.22 |
| **Hosting** | Servidor privado Debian 12 (Proxmox) |
| **Automatización** | Make (envía JSON vía POST) |
| **Control de versiones** | Git |

### Dependencias Python

**Scripts de generación** — solo módulos estándar:

- `json` — lectura/escritura de JSON
- `os`, `shutil`, `pathlib` — manipulación de archivos y rutas
- `datetime` — fechas
- `subprocess` — ejecución de scripts hijos
- `sys` — argumentos y salida

**API (`api.py`)** — requiere entorno virtual (`venv/`):

- `fastapi` — framework API REST
- `uvicorn` — servidor ASGI

---

## 6. Scripts

### 6.1 `generar_paginas.py`

**Función:** Generar páginas HTML individuales por noticia y archivar las antiguas.

**Flujo:**

1. Cargar `noticias.json`.
2. **Guardar en historial:** Añadir todas las noticias actuales a `historial_completo.json` (clave: `id`). Si una noticia es nueva, se añade `fecha_primera_publicacion`.
3. **Archivar noticias antiguas:**
   - Identificar archivos HTML en `noticias/` cuyo `id` (nombre sin extensión) ya no está en `noticias.json`.
   - Mover esos HTML a `noticias_ant/`.
   - Crear en `noticias/` una página de redirección (meta refresh) a `../noticias_ant/{archivo}`.
   - Actualizar `noticias_antiguas.json` con los datos completos de las archivadas.
4. Generar un HTML por cada noticia actual en `noticias/{id}.html`.

**Plantillas:**

- `PLANTILLA_NOTICIA`: Página completa de artículo (header, contenido, sidebar, footer).
- `PLANTILLA_REDIRECCION`: Página de redirección para noticias archivadas.

**Funciones principales:**

| Función | Descripción |
|---------|-------------|
| `generar_contenido_html(noticia)` | Convierte `contenido_completo`, `citas` y `puntos_clave` en HTML |
| `generar_autor_completo(noticia)` | Formatea autor, coautor y ciudad |
| `generar_imagen_html(noticia)` | Genera bloque HTML de imagen con caption |
| `generar_lead(noticia)` | Extrae lead desde `resumen` o primer párrafo |
| `guardar_noticias_en_historial(data)` | Actualiza `historial_completo.json` |
| `archivar_noticias_antiguas(data)` | Mueve HTML antiguos y actualiza `noticias_antiguas.json` |
| `generar_pagina_noticia(noticia, config)` | Genera el HTML completo de una noticia |

---

### 6.2 `actualizar_index.py`

**Función:** Regenerar `index.html` a partir de `noticias.json`.

**Flujo:**

1. Cargar `noticias.json`.
2. Generar HTML para:
   - `noticia_principal` → hero principal (imagen grande, título destacado).
   - Primera `noticias_secundarias` → columna principal.
   - Resto de secundarias → columna central.
   - `noticias_lo_ultimo` → columna central.
3. Aplicar `PLANTILLA_INDEX` y guardar `index.html`.

**Layout:**

- Grid CSS: `grid-template-columns: 1.5fr 1fr`.
- Responsive: una columna en tablet/móvil (`max-width: 1024px`).

---

### 6.3 `actualizar_todo.py`

**Función:** Orquestar la actualización completa del sitio.

**Flujo:**

1. Comprobar que existe `noticias.json`.
2. Ejecutar `generar_paginas.py`.
3. Ejecutar `actualizar_index.py`.
4. Si hay cambios: `git add -A`, `git commit`, `git push origin main`.

**Uso recomendado:**

```bash
python3 actualizar_todo.py
```

---

## 7. Almacenamiento de Noticias

### 7.1 Archivos y roles

| Archivo | Ubicación | Rol |
|---------|-----------|-----|
| `noticias.json` | Raíz | Noticias actuales (fuente de verdad) |
| `historial_completo.json` | Raíz | Historial por `id` (objeto clave-valor) |
| `noticias_antiguas.json` | Raíz | Lista de noticias archivadas con datos completos |
| Páginas actuales | `noticias/{id}.html` | HTML generado |
| Páginas archivadas | `noticias_ant/{id}.html` | HTML movido al archivo |

### 7.2 Estructura de `noticias.json`

```json
{
  "config": {
    "titulo_sitio": "string",
    "edicion": "string",
    "fecha_actualizacion": "string",
    "logo_url": "string"
  },
  "noticia_principal": { /* objeto noticia */ },
  "noticias_secundarias": [ /* array de noticias */ ],
  "noticias_lo_ultimo": [ /* array de noticias */ ],
  "articulos_opinion": [ /* array, opcional */ ]
}
```

### 7.3 Objeto noticia

```json
{
  "id": "slug-url-amigable",
  "url": "https://...",
  "categoria": "string",
  "titulo": "string",
  "resumen": "string",
  "autor": "string",
  "coautor": "string | null",
  "ciudad": "string",
  "imagen": "URL",
  "imagen_alt": "string",
  "imagen_caption": "string",
  "subtitulo": "string",
  "contenido_completo": ["<p>...</p>", "<h2>...</h2>", "texto plano", ...],
  "citas": ["string"],
  "puntos_clave": ["string"]
}
```

### 7.4 `historial_completo.json`

```json
{
  "id-noticia-1": { /* objeto noticia completo */ },
  "id-noticia-2": { /* ... */ }
}
```

Se añade `fecha_primera_publicacion` al guardar por primera vez.

### 7.5 `noticias_antiguas.json`

```json
{
  "ultima_actualizacion": "YYYY-MM-DD HH:MM:SS",
  "total_noticias": 279,
  "noticias": [
    {
      "id": "...",
      /* objeto noticia completo */
      "fecha_primera_publicacion": "...",
      "fecha_archivo": "..."
    }
  ],
  "info": "Este archivo contiene el historial de todas las noticias archivadas"
}
```

---

## 8. Flujo de la Aplicación

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. Edición manual de noticias.json                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. Ejecución: python3 actualizar_todo.py                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
         ┌───────────────────┴───────────────────┐
         ▼                                       ▼
┌─────────────────────┐               ┌─────────────────────────────┐
│ generar_paginas.py   │               │ actualizar_index.py         │
│ - Historial          │               │ - Regenera index.html       │
│ - Archivo antiguas   │               │ - Layout: principal +       │
│ - Genera HTML       │               │   secundarias + lo último    │
└─────────────────────┘               └─────────────────────────────┘
         │                                       │
         └───────────────────┬───────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. Git: add, commit, push (si hay cambios)                         │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. Nginx sirve el HTML actualizado directamente desde el servidor │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9. Configuración

### 9.1 Variables de entorno

No hay `.env` ni variables de entorno. Todo se configura en `noticias.json` (sección `config`).

### 9.2 `vercel.json`

```json
{
  "version": 2,
  "headers": [
    {
      "source": "/(.*)",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=0, must-revalidate" }]
    },
    {
      "source": "/noticias/(.*)",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=0, must-revalidate" }]
    }
  ]
}
```

Se fuerza revalidación para que los cambios se reflejen de inmediato.

### 9.3 Metadatos en HTML

- `Cache-Control: no-cache, no-store, must-revalidate`
- `Pragma: no-cache`
- `Expires: 0`
- `version: 2.0-IA-NOTICIAS`

---

## 10. APIs y Endpoints

No existe backend ni API REST. Es un sitio estático:

- `index.html` → portada
- `noticias/{id}.html` → artículo o redirección al archivo

---

## 11. Componentes de UI

### 11.1 Diseño

| Elemento | Valor |
|----------|-------|
| **Fuentes** | Playfair Display (serif), Roboto (sans-serif) |
| **Colores** | `#000000`, `#f34b26`, `#333333`, `#f4f4f4` |
| **Layout** | Grid CSS, responsive |

### 11.2 Bloques principales

| Componente | Ubicación | Descripción |
|------------|-----------|-------------|
| Header | Todas las páginas | Logo IAKimi, "En colaboración con Diario El Mundo", fecha |
| Hero article | `index.html` | Noticia principal con imagen grande |
| List articles | `index.html` | Noticias secundarias y "Lo último" |
| Article layout | Páginas de noticia | Grid 2fr + 1fr (contenido + sidebar) |
| Sidebar | Páginas de noticia | "Noticias Relacionadas" (enlace a portada) |
| Footer | Todas | Logo IAKimi en negativo |
| Redirección | `noticias/` | Página "archivada" con meta refresh |

### 11.3 Rutas de assets

- Logo header: `IMG/Logo IAKimi - Sin Fondo.png`
- Logo footer: `IMG/Logo IAKimi - Negativo.png`
- Imágenes de noticias: URLs externas (ej. ibb.co)

---

## 12. Base de Datos y Persistencia

No hay base de datos. Todo se guarda en JSON y HTML:

| Tipo | Ubicación | Formato |
|------|-----------|---------|
| Noticias actuales | `noticias.json` | JSON |
| Historial | `historial_completo.json` | JSON (objeto por id) |
| Archivadas | `noticias_antiguas.json` | JSON (array) |
| Páginas | `noticias/`, `noticias_ant/` | HTML estático |

---

## 13. Detalles Técnicos Adicionales

### 13.1 Redirecciones para archivadas

Cuando una noticia pasa a archivo:

1. Se mueve `noticias/{id}.html` → `noticias_ant/{id}.html`.
2. Se crea `noticias/{id}.html` con meta refresh a `../noticias_ant/{id}.html`.
3. Los enlaces antiguos siguen funcionando.

### 13.2 ID de noticia

El `id` es un slug (ej. `google-reduce-comisiones-en-android-y-reordena-el-negocio-de-las-apps`) y define:

- Nombre del archivo: `{id}.html`
- URL: `/noticias/{id}.html`

### 13.3 Despliegue

- Hosting: Servidor privado Debian 12 sobre Proxmox
- IP privada: `172.17.3.43` (red interna)
- IP pública: `200.35.189.154` (requiere NAT en Proxmox para acceso externo)
- Nginx sirve los archivos estáticos desde `/home/iakimi/noticias-ia`
- FastAPI corre en `127.0.0.1:8000` gestionado por systemd (`noticias-api.service`)
- Ver `DOCUMENTACION_SERVIDOR.md` para detalles completos de infraestructura

---

## 14. Consideraciones 

### 14.1 Contenido HTML en `contenido_completo`

En `generar_paginas.py`, cada elemento de `contenido_completo` se envuelve en `<p>`:

```python
for parrafo in noticia.get('contenido_completo', []):
    html += f"<p>{parrafo}</p>\n"
```

Si el elemento ya es `<h2>...</h2>` o `<p>...</p>`, se genera `<p><h2>...</h2></p>`, que es HTML inválido. Sería recomendable detectar si el fragmento es un bloque HTML y no envolverlo en `<p>`.

### 14.2 Citas

La condición `if noticia.get('citas') and len(noticia['citas']) > 0` es correcta, pero usar `noticia.get('citas', [])` sería más consistente para evitar posibles errores si la estructura cambia.

---

## 15. Comandos de Referencia

```bash
# Actualización completa (recomendado)
python3 actualizar_todo.py

# Solo generar páginas
python3 generar_paginas.py

# Solo actualizar index
python3 actualizar_index.py

# Verificar JSON
python3 -m json.tool noticias.json
```

---

## 16.Repositorio

- **Repositorio:** https://github.com/DXpz/DEMO-NOTICIAS-IA.git

---

## 17. Migración a servidor dedicado (implementada en v3.0)

### 17.1 Estado actual

A partir del 10 de marzo de 2026, el sistema ha sido completamente migrado a un servidor privado dedicado. Lo que antes era una propuesta teórica está ahora en producción. `noticias.json` ya no se edita manualmente: Make envía el JSON automáticamente a la API FastAPI que regenera el sitio.

### 17.2 Flujo propuesto con servidor dedicado

1. **Generación externa del JSON**
   - Un sistema externo (por ejemplo, una herramienta editorial o un servicio de IA) genera un nuevo `noticias.json` con la misma estructura actual.
   - En lugar de que una persona copie/pegue el contenido, este sistema envía el JSON al servidor dedicado (por HTTP, webhook o procesando automáticamente el JSON adjunto en un correo).

2. **Recepción del JSON en el servidor**
   - El servidor dedicado expone un endpoint (por ejemplo `POST /actualizar-noticias`) que recibe el JSON.
   - Opcionalmente valida:
     - Estructura (`config`, `noticia_principal`, `noticias_secundarias`, `noticias_lo_ultimo`, etc.).
     - Tipos básicos (strings, arrays, campos obligatorios como `id`, `titulo`, `categoria`, etc.).

3. **Actualización del `noticias.json` local**
   - El servidor escribe el JSON recibido en el `noticias.json` del proyecto (reemplazo completo o merge controlado, según la política que se defina).
   - Opcionalmente puede hacer copias de seguridad del `noticias.json` anterior (por ejemplo `noticias_backup_YYYYMMDD.json`).

4. **Ejecución automática de los scripts**
   - Una vez actualizado el archivo, el servidor ejecuta en el directorio del proyecto:
     - `python3 generar_paginas.py`
     - `python3 actualizar_index.py`
     - o directamente `python3 actualizar_todo.py` si se quiere mantener el mismo flujo actual.
   - Esto dispara todo el pipeline existente:
     - Actualización de `historial_completo.json`.
     - Archivo de noticias antiguas (`noticias_ant/` + `noticias_antiguas.json`).
     - Regeneración de `index.html` y de todas las páginas en `noticias/`.

5. **Integración con control de versiones y despliegue**
   - El servidor podría, igual que hace actualmente `actualizar_todo.py`, ejecutar:
     - `git add -A`
     - `git commit -m "Actualización automática desde servidor dedicado"`
     - `git push origin main`
   - El push a `main` mantendría el comportamiento actual: Vercel detecta el cambio y despliega la nueva versión del sitio.

### 17.3 Ventajas de este enfoque

- **Cero intervención manual** en la etapa de copiado de JSON y ejecución de scripts.
- **Menos errores humanos** (olvidar un script, dejar una noticia duplicada, etc.).
- **Integración fácil** con herramientas externas (IA generativa, CMS, back-office corporativo).
- **Escalabilidad**: se pueden programar múltiples actualizaciones al día sin carga operativa.

### 17.4 Consideraciones técnicas para la implementación

- **Seguridad del endpoint**
  - Autenticación (token, API key, firma HMAC o similar).
  - Validación estricta del JSON de entrada para evitar inyección de contenido malicioso.
- **Gestión de errores**
  - Log de errores cuando el JSON no es válido o los scripts fallan.
  - Notificación (correo, Slack, etc.) si una actualización automática no se completa.
- **Entornos separados**
  - Posible uso de entorno de staging (por ejemplo, rama `staging`) para probar cambios antes de desplegar a `main`.
- **Sincronización con el repositorio**
  - El servidor debería trabajar siempre sobre una copia actualizada del repositorio (`git pull` previo) para evitar conflictos.

### 17.5 Cambio de despliegue y hosting (sin Vercel)

En este escenario el **servidor dedicado también actúa como servidor web** del sitio estático, sustituyendo a Vercel. El flujo quedaría así:

- El bot de Make (u otro sistema) **ya genera un `noticias.json` estructurado** y lo envía directamente al endpoint del servidor (en lugar de mandarlo por correo para copiarlo a mano).
- El servidor **solo hace dos cosas**:
  1. Actualiza el archivo `noticias.json` local con el JSON recibido.
  2. Ejecuta los scripts Python (`generar_paginas.py` y `actualizar_index.py`, o `actualizar_todo.py` ajustado) para regenerar los HTML.
- Los archivos generados (`index.html`, carpeta `noticias/`, carpeta `noticias_ant/`, JSON auxiliares) se sirven directamente desde el propio servidor web (por ejemplo Nginx/Apache que apunta al directorio del proyecto).
- Vercel ya **no es necesario**: el despliegue pasa a ser puramente local en el servidor dedicado.

Para este modelo suele ser conveniente **ajustar los scripts**:

- Hacer opcional (o eliminar) la parte de `git add/commit/push` en `actualizar_todo.py` si el servidor no va a usar Git para desplegar.
- Mantener Git solo como control de versiones manual del código y de la estructura, no como paso obligatorio del despliegue.

Este apartado describe una **extensión posible** del sistema actual: no cambia el diseño base (scripts + JSON + HTML estático), sino que añade una capa de automatización alrededor de `noticias.json`, de la ejecución de los scripts existentes y del propio despliegue en un servidor dedicado.
