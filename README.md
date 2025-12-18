# 📰 RED Noticias - Sistema de Actualización Automática

## 🚀 ¿Qué hace este sistema?

Este sistema automatiza completamente la actualización del sitio web de noticias. Con solo editar el archivo `noticias.json` y ejecutar un comando, se actualizará todo el sitio web automáticamente.

---

## 📁 Archivos del Sistema

### Scripts Principales

1. **`generar_paginas.py`**
   - Archiva las noticias antiguas en `noticias_ant/`
   - Genera las páginas HTML individuales de cada noticia
   - Mantiene un registro JSON de noticias archivadas

2. **`actualizar_index.py`**
   - Lee `noticias.json`
   - Actualiza automáticamente el `index.html` con las noticias nuevas
   - Mantiene el diseño y estructura del sitio

3. **`actualizar_todo.py`** ⭐ (RECOMENDADO)
   - Script maestro que ejecuta todo el proceso completo
   - Ejecuta los dos scripts anteriores en el orden correcto
   - Muestra un resumen detallado del proceso

---

## 🎯 Uso Rápido (Recomendado)

### Método Simple: Un Solo Comando

```bash
# 1. Edita el archivo noticias.json con las nuevas noticias
# 2. Ejecuta el script maestro:
python3 actualizar_todo.py
```

¡Y listo! Todo se actualiza automáticamente.

---

## 📝 Flujo de Trabajo Completo

### Paso a Paso

1. **Editar `noticias.json`** con las noticias nuevas:
   ```json
   {
     "config": {
       "edicion": "Edición El Salvador",
       "fecha_actualizacion": "Miércoles, 18 de Diciembre de 2025 • Actualizado a las 09:00"
     },
     "noticia_principal": {
       "id": "nueva-noticia-1",
       "titulo": "Título de la noticia",
       "categoria": "Actualidad",
       "imagen": "URL_de_la_imagen",
       "resumen": "Resumen breve...",
       "contenido": [...]
     },
     "noticias_secundarias": [...],
     "noticias_lo_ultimo": [...]
   }
   ```

2. **Ejecutar el script de actualización**:
   ```bash
   python3 actualizar_todo.py
   ```

3. **Verificar los cambios**:
   - Abre `index.html` en tu navegador
   - Revisa que las noticias se vean correctamente
   - Verifica las páginas individuales en `noticias/`

4. **Publicar los cambios** (Git):
   ```bash
   git add .
   git commit -m "Actualización de noticias - $(date +%Y-%m-%d)"
   git push origin main
   ```

---

## 🗂️ Estructura de Carpetas

```
DEMO ELMUNDOSV/
├── noticias.json              # ← EDITA ESTE ARCHIVO (noticias actuales)
├── index.html                 # Generado automáticamente
│
├── noticias/                  # Páginas HTML de noticias actuales
│   ├── noticia-1.html
│   ├── noticia-2.html
│   └── ...
│
├── noticias_ant/              # Noticias archivadas (HTMLs antiguos)
│   ├── noticia-vieja-1.html
│   └── ...
│
├── historial_completo.json    # ⭐ HISTORIAL: Todas las noticias publicadas
├── noticias_antiguas.json     # ⭐ ARCHIVO: Noticias con datos completos
│
├── generar_paginas.py         # Script 1: Genera páginas + archivo
├── actualizar_index.py        # Script 2: Actualiza index
└── actualizar_todo.py         # Script maestro (USA ESTE)
```

---

## 🔄 ¿Qué Sucede al Ejecutar `actualizar_todo.py`?

### Proceso Automático:

1. **Guardado en Historial** 💾
   - Guarda todas las noticias actuales en `historial_completo.json`
   - Este historial NUNCA se borra, contiene TODAS las noticias publicadas
   - Incluye: título, categoría, resumen, contenido, imágenes, fechas, etc.

2. **Archivo de Noticias Antiguas** 📦
   - Identifica las noticias que ya no están en `noticias.json`
   - Busca sus datos completos en `historial_completo.json`
   - Las mueve de `noticias/` → `noticias_ant/` (archivos HTML)
   - Guarda los datos completos en `noticias_antiguas.json`:
     * ✅ Título, categoría, resumen
     * ✅ Autor, ciudad, imagen
     * ✅ Contenido completo
     * ✅ Citas y puntos clave
     * ✅ Fechas de publicación y archivo

3. **Generación de Páginas Nuevas** 📝
   - Lee las noticias de `noticias.json`
   - Genera un archivo HTML por cada noticia en `noticias/`
   - Aplica el diseño de "RED Noticias"

4. **Actualización del Index** 🏠
   - Lee `noticias.json`
   - Regenera completamente `index.html`
   - Organiza las noticias en el layout correcto

---

## 💡 Casos de Uso

### Actualizar Noticias Diariamente

```bash
# 1. Edita noticias.json con las noticias del día
# 2. Ejecuta:
python3 actualizar_todo.py
# 3. Publica:
git add . && git commit -m "Noticias del día" && git push
```

### Recuperar Noticias Antiguas

Las noticias archivadas están guardadas con **DATOS COMPLETOS**:
- **Archivos HTML**: Carpeta `noticias_ant/`
- **Datos Completos**: Archivo `noticias_antiguas.json`
- **Historial Total**: Archivo `historial_completo.json`

```bash
# Ver noticias archivadas (solo nombres)
ls noticias_ant/

# Ver datos completos de noticias archivadas
cat noticias_antiguas.json | python3 -m json.tool

# Ver historial completo de TODAS las noticias publicadas
cat historial_completo.json | python3 -m json.tool

# Buscar una noticia específica en el historial
python3 -c "
import json
with open('noticias_antiguas.json', 'r') as f:
    data = json.load(f)
    for n in data['noticias']:
        if 'robotica' in n.get('id', ''):
            print(f'{n[\"titulo\"]}')
            print(f'Archivada: {n[\"fecha_archivo\"]}')
"
```

**Datos que se guardan por cada noticia archivada:**
- ID, título, categoría, resumen
- Autor, coautor, ciudad
- Imagen (URL, alt, caption)
- Subtítulo
- Contenido completo (párrafos)
- Citas textuales
- Puntos clave
- Fecha de primera publicación
- Fecha de archivo

---

## 🛠️ Solución de Problemas

### Error: "No se encuentra noticias.json"
**Solución**: Asegúrate de ejecutar el script desde la carpeta `DEMO ELMUNDOSV`

```bash
cd /home/trickzz/Documents/TestINTELFON/DEMO\ ELMUNDOSV
python3 actualizar_todo.py
```

### Las noticias antiguas no se archivan
**Causa**: Las noticias actuales tienen los mismos IDs que las del JSON
**Solución**: El sistema solo archiva noticias que ya no están en `noticias.json`

### El index.html no se actualiza
**Solución**: Verifica que `noticias.json` tenga el formato correcto (JSON válido)

```bash
# Verificar JSON
python3 -m json.tool noticias.json
```

---

## 🎓 Scripts Individuales (Uso Avanzado)

Si necesitas ejecutar solo una parte del proceso:

### Solo generar páginas HTML:
```bash
python3 generar_paginas.py
```

### Solo actualizar index.html:
```bash
python3 actualizar_index.py
```

---

## ⚙️ Configuración

### Editar el diseño del sitio:
- **Páginas individuales**: Edita la plantilla en `generar_paginas.py` (línea 14)
- **Index.html**: Edita la plantilla en `actualizar_index.py` (línea 16)

### Personalizar el proceso:
Abre `actualizar_todo.py` y modifica la función `main()`

---

## 📊 Ejemplo Completo

```bash
# Situación: Tienes 5 noticias nuevas del día

# 1. Editar noticias.json (con tus 5 noticias nuevas)
nano noticias.json

# 2. Ejecutar actualización automática
python3 actualizar_todo.py

# Salida esperada:
# 🚀 ACTUALIZACIÓN COMPLETA DEL SITIO WEB
# ✅ Noticias antiguas archivadas
# ✅ 5 páginas generadas
# ✅ index.html actualizado

# 3. Verificar
firefox index.html  # o tu navegador preferido

# 4. Publicar
git add .
git commit -m "Actualización: Noticias del 18/12/2025"
git push origin main
```

---

## 🌟 Ventajas del Sistema

✅ **Automatización completa**: Solo editas JSON, todo lo demás es automático
✅ **Archivo automático**: Las noticias viejas se guardan sin perder nada
✅ **Sin errores manuales**: No necesitas editar HTML a mano
✅ **Historial completo**: Todas las noticias antiguas quedan registradas
✅ **Rápido**: Actualizar el sitio completo toma segundos

---

## 📞 Soporte

**Autor**: Trickzz.sh  
**Email**: antoniohector413@gmail.com  
**Repositorio**: https://github.com/DXpz/DEMO-NOTICIAS-IA.git

---

## 📅 Última Actualización

**Versión**: 2.0  
**Fecha**: 18 de Diciembre de 2025  
**Cambios**: Sistema de actualización automática completa

---

**¡Disfruta de tu sistema automatizado de noticias! 🎉**

