#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de páginas HTML individuales para cada noticia
Lee noticias.json y crea un archivo HTML por cada noticia
Incluye funcionalidad de archivo de noticias antiguas
Autor: Trickzz.sh
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime

# Plantilla HTML para cada noticia
PLANTILLA_NOTICIA = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo} - RED Noticias</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    
    <style>
        :root {{
            --brand-red: #ce1126;
            --brand-dark: #111111;
            --text-grey: #333333;
            --light-grey: #f4f4f4;
            --border-color: #e5e5e5;
            --bg-color: #ffffff;
            --serif-font: 'Playfair Display', Georgia, serif;
            --sans-font: 'Roboto', Helvetica, Arial, sans-serif;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: var(--sans-font);
            background-color: var(--bg-color);
            color: var(--text-grey);
            line-height: 1.5;
        }}

        a {{
            text-decoration: none;
            color: inherit;
            transition: color 0.2s;
        }}

        a:hover {{
            color: var(--brand-red);
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}

        /* HEADER */
        .header-main {{
            padding: 25px 0;
            text-align: center;
            border-bottom: 4px solid var(--brand-red);
        }}

        .logo-text {{
            font-size: 72px;
            font-weight: 900;
            letter-spacing: -2px;
            line-height: 1;
            font-family: var(--sans-font);
        }}

        .logo-red {{
            color: #e4002b;
        }}

        .logo-noticias {{
            color: #000000;
        }}

        .date-line {{
            font-size: 13px;
            color: #666;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid var(--border-color);
            display: inline-block;
            padding-left: 20px;
            padding-right: 20px;
        }}


        /* ARTÍCULO */
        .article-layout {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 40px;
            margin-top: 30px;
        }}

        .full-article-header {{
            margin-bottom: 30px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 20px;
        }}

        .breadcrumbs {{
            font-size: 12px;
            text-transform: uppercase;
            color: var(--brand-red);
            font-weight: bold;
            margin-bottom: 15px;
            display: block;
        }}

        .full-headline {{
            font-family: var(--sans-font);
            font-size: 46px;
            line-height: 1.1;
            color: var(--brand-dark);
            margin-bottom: 20px;
        }}

        .full-lead {{
            font-family: var(--sans-font);
            font-size: 20px;
            line-height: 1.5;
            color: #444;
            margin-bottom: 20px;
        }}

        .full-meta {{
            font-size: 13px;
            color: #666;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .full-image-container {{
            margin-bottom: 30px;
        }}

        .full-image-container img {{
            width: 100%;
            height: auto;
            display: block;
        }}

        .full-image-caption {{
            font-size: 13px;
            color: #777;
            background: #f9f9f9;
            padding: 8px 15px;
            border-bottom: 1px solid #eee;
        }}

        .article-body {{
            font-family: var(--sans-font);
            font-size: 19px;
            line-height: 1.8;
            color: #222;
        }}

        .article-body p {{
            margin-bottom: 25px;
        }}
        
        .article-body h2 {{
            font-family: var(--sans-font);
            font-size: 24px;
            font-weight: 700;
            margin-top: 40px;
            margin-bottom: 20px;
            color: var(--brand-dark);
        }}

        .article-body ul {{
            margin-left: 30px;
            margin-bottom: 25px;
        }}

        .article-body li {{
            margin-bottom: 10px;
        }}

        .article-quote {{
            border-left: 4px solid var(--brand-red);
            padding-left: 25px;
            font-style: italic;
            font-size: 24px;
            color: #444;
            margin: 40px 0;
        }}

        .btn-back {{
            display: inline-block;
            margin-bottom: 20px;
            font-size: 12px;
            font-weight: bold;
            color: #666;
            cursor: pointer;
        }}
        .btn-back:hover {{
            color: var(--brand-red);
            text-decoration: underline;
        }}

        .sidebar-title {{
            font-size: 14px;
            font-weight: 900;
            text-transform: uppercase;
            border-bottom: 2px solid var(--brand-dark);
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}


        .related-item {{
            margin-bottom: 20px;
            border-bottom: 1px dotted #ccc;
            padding-bottom: 15px;
        }}

        .related-category {{
            font-size: 11px;
            text-transform: uppercase;
            color: var(--brand-red);
            font-weight: bold;
        }}

        .related-item h4 {{
            font-family: var(--sans-font);
            font-size: 16px;
            margin-top: 5px;
        }}

        /* FOOTER */
        footer {{
            background-color: var(--brand-dark);
            color: #fff;
            padding: 20px 0;
            margin-top: 50px;
            text-align: center;
            border-top: 1px solid #333;
        }}

        .footer-logo {{
            font-size: 24px;
            font-weight: 900;
            letter-spacing: -1px;
            font-family: var(--sans-font);
        }}

        .footer-logo .logo-noticias {{
            color: #ffffff;
        }}

        @media (max-width: 1024px) {{
            .article-layout {{
                grid-template-columns: 1fr;
            }}
            .article-sidebar {{
                display: none;
            }}
        }}

        @media (max-width: 768px) {{
            .full-headline {{
                font-size: 32px;
            }}
            .article-sidebar {{
                display: block;
                margin-top: 40px;
            }}
        }}
    </style>
</head>
<body>

    <!-- HEADER LOGO -->
    <header class="header-main">
        <div class="container">
            <a href="../index.html">
                <div class="logo-text">
                    <span class="logo-red">RED</span><span class="logo-noticias"> Noticias</span>
                </div>
            </a>
            <div class="date-line">
                {fecha_actualizacion}
            </div>
        </div>
    </header>

    <!-- CONTENIDO ARTÍCULO -->
    <main class="container">
        <a href="../index.html" class="btn-back">&larr; VOLVER A PORTADA</a>
        
        <div class="article-layout">
            <!-- CONTENIDO PRINCIPAL -->
            <div class="article-content">
                <header class="full-article-header">
                    <span class="breadcrumbs">{categoria}</span>
                    <h1 class="full-headline">{titulo}</h1>
                    <p class="full-lead">{lead}</p>
                    <div class="full-meta">
                        <span>{autor_completo}</span>
                        <span>{fecha_actualizacion}</span>
                    </div>
                </header>

                {imagen_html}

                <div class="article-body">
                    {contenido_html}
                </div>
            </div>

            <!-- SIDEBAR -->
            <aside class="article-sidebar">
                <div class="sidebar-title">Noticias Relacionadas</div>
                <div class="related-item">
                    <div class="related-category">Contexto</div>
                    <h4><a href="../index.html">Volver a la portada</a></h4>
                </div>
            </aside>
        </div>
    </main>

    <!-- FOOTER -->
    <footer>
        <div class="container">
            <div class="footer-logo">
                <span class="logo-red">RED</span><span class="logo-noticias"> Noticias</span>
            </div>
        </div>
    </footer>

    </body>
    </html>
"""


# Plantilla simple para páginas de redirección cuando una noticia
# se ha movido a la carpeta de archivo `noticias_ant/`
PLANTILLA_REDIRECCION = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>RED Noticias - Archivo</title>
    <meta http-equiv="refresh" content="0; url=../noticias_ant/{archivo}">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #fafafa;
            color: #333;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }}
        .card {{
            background: #fff;
            padding: 24px 28px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            max-width: 480px;
            text-align: center;
        }}
        h1 {{
            font-size: 20px;
            margin-bottom: 10px;
        }}
        p {{
            font-size: 14px;
            margin-bottom: 16px;
        }}
        a {{
            color: #ce1126;
            text-decoration: none;
            font-weight: 600;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="card">
        <h1>Esta noticia ha sido archivada</h1>
        <p>Estás siendo redirigido a la versión archivada de este artículo.</p>
        <p>Si la redirección no ocurre automáticamente, haz clic en el siguiente enlace:</p>
        <p><a href="../noticias_ant/{archivo}">Ver noticia archivada</a></p>
    </div>
</body>
</html>
"""


def generar_contenido_html(noticia):
    """Genera el HTML del contenido de la noticia"""
    html = ""
    
    # Añadir párrafos
    for parrafo in noticia.get('contenido_completo', []):
        html += f"<p>{parrafo}</p>\n"
    
    # Añadir cita si existe
    if noticia.get('citas') and len(noticia['citas']) > 0:
        html += f'<blockquote class="article-quote">"{noticia["citas"][0]}"</blockquote>\n'
    
    # Añadir puntos clave
    if noticia.get('puntos_clave') and len(noticia['puntos_clave']) > 0:
        html += '<h2>Puntos clave</h2>\n<ul>\n'
        for punto in noticia['puntos_clave']:
            html += f'<li>{punto}</li>\n'
        html += '</ul>\n'
    
    return html


def generar_autor_completo(noticia):
    """Genera el texto completo del autor"""
    autor = f"Por <strong>{noticia['autor']}</strong>"
    if noticia.get('coautor'):
        autor += f" y <strong>{noticia['coautor']}</strong>"
    autor += f" | {noticia.get('ciudad', 'Madrid')}"
    return autor


def generar_imagen_html(noticia):
    """Genera el HTML de la imagen si existe"""
    if noticia.get('imagen'):
        return f"""<div class="full-image-container">
                    <img src="{noticia['imagen']}" alt="{noticia.get('imagen_alt', '')}">
                    <div class="full-image-caption">{noticia.get('imagen_caption', '')}</div>
                </div>"""
    return ""


def generar_lead(noticia):
    """Genera el lead de la noticia"""
    if noticia.get('resumen'):
        return noticia['resumen']
    elif noticia.get('contenido_completo') and len(noticia['contenido_completo']) > 0:
        # Extraer texto del primer párrafo sin etiquetas HTML
        primer_parrafo = noticia['contenido_completo'][0]
        # Quitar etiquetas HTML básicas
        texto_limpio = primer_parrafo.replace('<strong>', '').replace('</strong>', '')
        texto_limpio = texto_limpio.replace('<em>', '').replace('</em>', '')
        return texto_limpio[:200] + '...'
    return ""


def generar_pagina_noticia(noticia, config):
    """Genera una página HTML individual para una noticia"""
    contenido_html = generar_contenido_html(noticia)
    autor_completo = generar_autor_completo(noticia)
    imagen_html = generar_imagen_html(noticia)
    lead = generar_lead(noticia)
    
    html = PLANTILLA_NOTICIA.format(
        titulo=noticia['titulo'],
        categoria=noticia['categoria'],
        lead=lead,
        autor_completo=autor_completo,
        fecha_actualizacion=config['fecha_actualizacion'],
        imagen_html=imagen_html,
        contenido_html=contenido_html
    )
    
    return html


def guardar_noticias_en_historial(noticias_actuales_json):
    """
    Guarda las noticias actuales en el historial completo
    Este historial se usa luego para el archivo
    """
    archivo_historial = 'historial_completo.json'
    historial = {}
    
    # Cargar historial existente
    if Path(archivo_historial).exists():
        try:
            with open(archivo_historial, 'r', encoding='utf-8') as f:
                historial = json.load(f)
        except:
            historial = {}
    
    # Recopilar todas las noticias actuales
    todas_noticias = []
    if 'noticia_principal' in noticias_actuales_json:
        todas_noticias.append(noticias_actuales_json['noticia_principal'])
    if 'noticias_secundarias' in noticias_actuales_json:
        todas_noticias.extend(noticias_actuales_json['noticias_secundarias'])
    if 'noticias_lo_ultimo' in noticias_actuales_json:
        todas_noticias.extend(noticias_actuales_json['noticias_lo_ultimo'])
    
    # Agregar al historial (clave: id, valor: datos completos de la noticia)
    for noticia in todas_noticias:
        if 'id' in noticia:
            # Agregar fecha de primera publicación si no existe
            if noticia['id'] not in historial:
                noticia_copia = noticia.copy()
                noticia_copia['fecha_primera_publicacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                historial[noticia['id']] = noticia_copia
    
    # Guardar historial actualizado
    with open(archivo_historial, 'w', encoding='utf-8') as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)


def archivar_noticias_antiguas(noticias_actuales_json):
    """
    Archiva las noticias antiguas de noticias/ a noticias_ant/
    y actualiza el JSON de noticias antiguas
    """
    print("\n📦 Archivando noticias antiguas...")
    print("-" * 50)
    
    # Crear carpeta de archivo si no existe
    Path('noticias_ant').mkdir(exist_ok=True)
    
    # Verificar si existe la carpeta de noticias actuales
    if not Path('noticias').exists():
        print("ℹ️  No hay noticias actuales para archivar")
        return
    
    # Cargar historial completo
    archivo_historial = 'historial_completo.json'
    historial = {}
    if Path(archivo_historial).exists():
        try:
            with open(archivo_historial, 'r', encoding='utf-8') as f:
                historial = json.load(f)
        except:
            historial = {}
    
    # Cargar JSON de noticias antiguas si existe
    archivo_json = 'noticias_antiguas.json'
    noticias_antiguas = []
    ids_ya_archivados = set()
    
    if Path(archivo_json).exists():
        try:
            with open(archivo_json, 'r', encoding='utf-8') as f:
                data_antiguas = json.load(f)
                noticias_antiguas = data_antiguas.get('noticias', [])
                # Obtener IDs ya archivados para no duplicar
                ids_ya_archivados = {n['id'] for n in noticias_antiguas if 'id' in n}
            print(f"✅ Cargadas {len(noticias_antiguas)} noticias antiguas existentes")
        except Exception as e:
            print(f"⚠️  Error al cargar {archivo_json}: {e}")
            noticias_antiguas = []
    
    # Obtener lista de archivos HTML en noticias/
    archivos_html = list(Path('noticias').glob('*.html'))
    
    if not archivos_html:
        print("ℹ️  No hay archivos HTML para archivar")
        return
    
    # Recopilar IDs de noticias actuales para no archivarlas
    ids_actuales = set()
    if 'noticia_principal' in noticias_actuales_json:
        ids_actuales.add(noticias_actuales_json['noticia_principal']['id'])
    if 'noticias_secundarias' in noticias_actuales_json:
        for noticia in noticias_actuales_json['noticias_secundarias']:
            ids_actuales.add(noticia['id'])
    if 'noticias_lo_ultimo' in noticias_actuales_json:
        for noticia in noticias_actuales_json['noticias_lo_ultimo']:
            ids_actuales.add(noticia['id'])
    
    # Construir conjunto de nombres ya archivados para evitar
    # re-mover o tocar páginas que ya fueron enviadas a noticias_ant
    nombres_ya_archivados = {p.name for p in Path('noticias_ant').glob('*.html')}

    # Mover archivos HTML antiguos y guardar sus datos
    archivados = 0
    for archivo in archivos_html:
        # Obtener el ID del archivo (nombre sin extensión)
        id_noticia = archivo.stem
        
        # Si este ID NO está en las noticias actuales, archivar
        if id_noticia not in ids_actuales:
            # Si ya existe una versión archivada con el mismo nombre,
            # asumimos que ya fue procesado y se mantiene su redirección.
            if archivo.name in nombres_ya_archivados:
                print(f"ℹ️  {archivo.name} ya está archivado, se mantiene su redirección.")
                continue

            # Buscar datos en el historial
            if id_noticia in historial and id_noticia not in ids_ya_archivados:
                noticia_datos = historial[id_noticia].copy()
                noticia_datos['fecha_archivo'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                noticias_antiguas.append(noticia_datos)
                print(f"📦 Archivado con datos: {archivo.name}")
            else:
                # Si no está en historial, guardar solo info básica
                if id_noticia not in ids_ya_archivados:
                    noticias_antiguas.append({
                        'id': id_noticia,
                        'fecha_archivo': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'nota': 'Archivado sin datos completos del historial'
                    })
                    print(f"📦 Archivado sin datos: {archivo.name}")
                else:
                    print(f"📦 Archivado (ya registrado): {archivo.name}")
            
            # Mover el archivo a noticias_ant
            destino = Path('noticias_ant') / archivo.name
            shutil.move(str(archivo), str(destino))
            archivados += 1

            # Crear una página de redirección en la ruta original
            # para que los enlaces antiguos (noticias/slug.html)
            # sigan funcionando y apunten al archivo en noticias_ant/.
            redireccion_path = Path('noticias') / archivo.name
            try:
                with open(redireccion_path, 'w', encoding='utf-8') as f:
                    f.write(PLANTILLA_REDIRECCION.format(archivo=archivo.name))
                print(f"🔁 Creada página de redirección: {redireccion_path}")
            except Exception as e:
                print(f"⚠️  No se pudo crear la página de redirección para {archivo.name}: {e}")
    
    if archivados > 0:
        print(f"\n✅ {archivados} archivos movidos a noticias_ant/")
        
        # Guardar JSON actualizado
        data_guardar = {
            'ultima_actualizacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_noticias': len(noticias_antiguas),
            'noticias': noticias_antiguas,
            'info': 'Este archivo contiene el historial de todas las noticias archivadas'
        }
        
        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(data_guardar, f, ensure_ascii=False, indent=2)
        
        print(f"✅ JSON actualizado: {archivo_json} ({len(noticias_antiguas)} noticias)")
    else:
        print("ℹ️  No hay noticias para archivar (todas son actuales)")


def main():
    """Función principal que genera todas las páginas"""
    print("🚀 Generador de Páginas HTML - RED Noticias")
    print("=" * 50)
    
    # Cargar JSON
    try:
        with open('noticias.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✅ JSON cargado correctamente")
    except Exception as e:
        print(f"❌ Error al cargar noticias.json: {e}")
        return
    
    # GUARDAR NOTICIAS ACTUALES EN EL HISTORIAL
    guardar_noticias_en_historial(data)
    
    # ARCHIVAR NOTICIAS ANTIGUAS ANTES DE GENERAR LAS NUEVAS
    archivar_noticias_antiguas(data)
    
    # Crear carpeta noticias si no existe
    Path('noticias').mkdir(exist_ok=True)
    print("\n📝 Preparando generación de noticias nuevas...")
    print("✅ Carpeta 'noticias/' verificada")
    
    config = data['config']
    noticias_generadas = 0
    
    # Recopilar todas las noticias
    todas_noticias = []
    
    # Noticia principal
    if 'noticia_principal' in data:
        todas_noticias.append(data['noticia_principal'])
    
    # Noticias secundarias
    if 'noticias_secundarias' in data:
        todas_noticias.extend(data['noticias_secundarias'])
    
    # Lo último
    if 'noticias_lo_ultimo' in data:
        todas_noticias.extend(data['noticias_lo_ultimo'])
    
    # Generar páginas
    print(f"\n📝 Generando {len(todas_noticias)} páginas...")
    print("-" * 50)
    
    for noticia in todas_noticias:
        try:
            html = generar_pagina_noticia(noticia, config)
            filename = f"noticias/{noticia['id']}.html"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
            
            print(f"✅ {filename} - {noticia['titulo'][:50]}...")
            noticias_generadas += 1
            
        except Exception as e:
            print(f"❌ Error al generar {noticia.get('id', 'unknown')}: {e}")
    
    print("-" * 50)
    print(f"\n🎉 ¡Listo! {noticias_generadas} páginas generadas correctamente")
    print(f"📁 Ubicación: ./noticias/")
    print("\n💡 Ahora puedes abrir index.html y hacer clic en las noticias")


if __name__ == "__main__":
    main()

