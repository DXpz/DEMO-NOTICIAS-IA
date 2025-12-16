# 📰 EL MUNDO - Sistema de Noticias con Páginas Individuales

## 📋 Descripción

Sistema de página web de noticias que genera automáticamente una página HTML individual para cada noticia desde un archivo JSON. 

**Archivos principales:**
- `index.html` - Portada del periódico
- `noticias.json` - Base de datos con todas las noticias
- `generar_paginas.py` - Script generador de páginas HTML
- `noticias/` - Carpeta con las páginas individuales generadas
- `INSTRUCCIONES.md` - Este archivo

---

## 🚀 Cómo usar

### Flujo de trabajo:

1. **Editar noticias**: Modifica el archivo `noticias.json`
2. **Generar páginas**: Ejecuta `python generar_paginas.py`
3. **Abrir portada**: Abre `index.html` en tu navegador
4. **Cada noticia tiene su propia URL** en la carpeta `noticias/`

### Comando rápido:

```bash
python generar_paginas.py
```

---

## ✅ Ventajas del nuevo sistema

🔗 **Cada noticia tiene su propia URL**
- `noticias/hero.html`
- `noticias/tribunales.html`
- `noticias/sanidad.html`
- etc.

✨ **Beneficios:**
- ✅ Puedes **compartir enlaces** específicos
- ✅ El **botón "Atrás"** del navegador funciona correctamente
- ✅ **SEO mejorado** - Google puede indexar cada noticia
- ✅ Se pueden **guardar como favoritos**
- ✅ **URLs permanentes** para cada artículo

---

## 📊 Estructura del JSON

### 1️⃣ **Configuración General** (`config`)
```json
"config": {
  "titulo_sitio": "EL MUNDO - Diario Online Líder",
  "edicion": "Edición España",
  "fecha_actualizacion": "Miércoles, 11 de Diciembre de 2025 • Actualizado a las 10:30",
  "logo_url": "URL_DEL_LOGO"
}
```

### 2️⃣ **Noticia Principal** (`noticia_principal`)
**1 espacio disponible** - Se muestra grande con imagen destacada

```json
"noticia_principal": {
  "id": "identificador-unico",
  "categoria": "Política Nacional",
  "titulo": "Título de la noticia principal",
  "resumen": "Resumen breve que aparece en portada",
  "autor": "Nombre Autor",
  "coautor": "Nombre Coautor (opcional)",
  "ciudad": "Madrid",
  "imagen": "URL_DE_LA_IMAGEN",
  "imagen_alt": "Descripción de la imagen",
  "imagen_caption": "Pie de foto | Agencia",
  "subtitulo": "Subtítulo del artículo completo",
  "contenido_completo": [
    "Párrafo 1 del contenido completo",
    "Párrafo 2 del contenido completo",
    "Párrafo 3..."
  ],
  "citas": [
    "Cita destacada que aparece en el artículo"
  ],
  "puntos_clave": [
    "Punto clave 1",
    "Punto clave 2",
    "Punto clave 3"
  ]
}
```

### 3️⃣ **Noticias Secundarias** (`noticias_secundarias`)
**2 espacios disponibles** - Aparecen debajo de la noticia principal **SIN IMAGEN**

```json
"noticias_secundarias": [
  {
    "id": "tribunales",
    "categoria": "Tribunales",
    "titulo": "Título de la noticia",
    "resumen": null,
    "autor": "Nombre Autor",
    "coautor": null,
    "ciudad": "Madrid",
    "imagen": "URL_IMAGEN",
    "imagen_alt": "Descripción",
    "imagen_caption": "Pie de foto",
    "subtitulo": "Subtítulo",
    "contenido_completo": [ "párrafos..." ],
    "citas": [ "citas..." ],
    "puntos_clave": [ "puntos..." ]
  }
]
```

### 4️⃣ **Lo Último** (`noticias_lo_ultimo`)
**3 espacios disponibles** - Las primeras 2 CON IMAGEN, la 3ª SIN IMAGEN

```json
"noticias_lo_ultimo": [
  {
    "id": "guerra",
    "categoria": "Internacional",
    "titulo": "Título",
    "imagen": "URL_IMAGEN (o null si no tiene)",
    ...
  }
]
```

### 5️⃣ **Artículos de Opinión** (`articulos_opinion`)
**3 espacios disponibles** - Con foto circular del autor

```json
"articulos_opinion": [
  {
    "id": "opinion1",
    "autor": "Jorge Plaza",
    "titulo": "El silencio de los corderos políticos",
    "categoria": "Opinión",
    "imagen_autor": "URL_FOTO_CIRCULAR",
    "contenido_completo": [
      "Párrafo de opinión..."
    ]
  }
]
```

---

## 🎨 Espacios Disponibles - Resumen

| Sección | Cantidad | Imagen |
|---------|----------|--------|
| **Noticia Principal** | 1 | ✅ Grande (800x450) |
| **Noticias Secundarias** | 2 | ❌ Sin imagen |
| **Lo Último** | 3 | ✅ 2 con imagen (400x225), ❌ 1 sin imagen |
| **Opinión** | 3 | ✅ Foto circular (50x50) |
| **TOTAL NOTICIAS** | **6 noticias** | 4 con imagen |

---

## 🔧 Cómo Agregar/Editar Noticias

### ✏️ **Editar una noticia existente:**
1. Abre `noticias.json`
2. Busca el artículo por su `id`
3. Modifica los campos que necesites
4. Guarda el archivo
5. Recarga la página

### ➕ **Agregar una nueva noticia:**
1. Decide en qué sección va (principal, secundarias, lo último)
2. Copia la estructura de una noticia similar
3. Cambia el `id` a uno único
4. Rellena todos los campos
5. Guarda y recarga

### 🖼️ **Sobre las imágenes:**
- Puedes usar URLs externas: `https://ejemplo.com/imagen.jpg`
- O imágenes locales: `./imagenes/foto.jpg`
- Usa `null` si no hay imagen
- Tamaños recomendados:
  - Noticia principal: 800x450 px
  - Lo último: 400x225 px (16:9)
  - Opinión: 50x50 px (circular)

---

## 🎯 Ejemplo Rápido: Cambiar Noticia Principal

**Antes:**
```json
"titulo": "El Gobierno aprueba la reforma histórica del sistema energético"
```

**Después:**
```json
"titulo": "Nueva crisis diplomática con países vecinos"
```

Guarda → Recarga → ¡Listo!

---

## 📝 Notas Importantes

✅ **Siempre usa comillas dobles** en JSON: `"texto"`  
✅ **No olvides las comas** entre elementos (excepto el último)  
✅ **Los arrays usan corchetes** `[ ]`  
✅ **Los objetos usan llaves** `{ }`  
✅ **null sin comillas** para campos vacíos  

❌ **Evita errores comunes:**
- No dejes comas al final: `"campo": "valor",]` ❌
- Cierra todos los corchetes y llaves
- Respeta las comillas en URLs

---

## 🛠️ Solución de Problemas

**¿La página no carga noticias?**
1. Abre la consola del navegador (F12)
2. Busca errores en rojo
3. Verifica que `noticias.json` esté en la misma carpeta que `index.html`
4. Valida tu JSON en: https://jsonlint.com/

**¿Las imágenes no aparecen?**
- Verifica que las URLs sean correctas
- Si son locales, comprueba la ruta
- Revisa permisos de archivos

---

## 📞 Campos Obligatorios vs Opcionales

### ✅ Obligatorios (no pueden ser null):
- `id`
- `categoria`
- `titulo`
- `autor`
- `contenido_completo`

### 🔘 Opcionales (pueden ser null):
- `resumen`
- `coautor`
- `imagen`
- `imagen_alt`
- `imagen_caption`
- `citas`
- `puntos_clave`

---

## 💡 Consejos Pro

1. **Mantén IDs únicos** - Usa nombres descriptivos: `energia-2025`, `ibex-diciembre`
2. **Optimiza imágenes** - Comprime antes de subir para carga rápida
3. **Contenido claro** - Párrafos cortos (3-4 líneas) son más legibles
4. **Backup regular** - Guarda copias de `noticias.json` antes de editar

---

## 🔄 El Script Generador

### ¿Qué hace `generar_paginas.py`?

1. **Lee** el archivo `noticias.json`
2. **Genera** una página HTML individual para cada noticia
3. **Guarda** los archivos en la carpeta `noticias/`
4. **Reporta** cuántas páginas se crearon exitosamente

### Ejemplo de salida:

```
🚀 Generador de Páginas HTML - EL MUNDO
==================================================
✅ JSON cargado correctamente
✅ Carpeta 'noticias/' verificada

📝 Generando 6 páginas...
--------------------------------------------------
✅ noticias/hero.html - El Gobierno aprueba...
✅ noticias/tribunales.html - El Supremo admite...
✅ noticias/sanidad.html - Nuevo plan de choque...
--------------------------------------------------

🎉 ¡Listo! 6 páginas generadas correctamente
```

### ¿Cuándo ejecutarlo?

⚡ **Cada vez que edites `noticias.json`** y quieras ver los cambios

### Estructura generada:

```
DEMO ELMUNDOSV/
├── index.html              ← Portada (http://localhost/index.html)
├── noticias/
│   ├── hero.html          ← http://localhost/noticias/hero.html
│   ├── tribunales.html    ← http://localhost/noticias/tribunales.html
│   ├── sanidad.html
│   ├── guerra.html
│   ├── bolsa.html
│   └── tecnologia.html
├── noticias.json
└── generar_paginas.py
```

---

¡Listo! Ahora puedes gestionar todo el contenido del periódico editando solo el archivo JSON y generando las páginas con un comando. 🎉

