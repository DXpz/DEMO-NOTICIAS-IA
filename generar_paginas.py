#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de páginas HTML individuales para cada noticia
Lee noticias.json y crea un archivo HTML por cada noticia
"""

import json
import os
from pathlib import Path

# Plantilla HTML para cada noticia
PLANTILLA_NOTICIA = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo} - EL MUNDO</title>
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
        .top-bar {{
            background-color: var(--light-grey);
            font-size: 12px;
            padding: 8px 0;
            border-bottom: 1px solid var(--border-color);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .top-bar .container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .header-main {{
            padding: 25px 0;
            text-align: center;
            border-bottom: 4px solid var(--brand-red);
        }}

        .logo {{
            max-width: 300px;
            height: auto;
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

        /* NAVEGACIÓN */
        .main-nav {{
            position: sticky;
            top: 0;
            background: white;
            z-index: 100;
            border-bottom: 1px solid var(--border-color);
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}

        .nav-list {{
            display: flex;
            justify-content: center;
            list-style: none;
            overflow-x: auto;
        }}

        .nav-item {{
            padding: 15px 20px;
            font-weight: 700;
            font-size: 14px;
            text-transform: uppercase;
            white-space: nowrap;
        }}

        .nav-item:hover {{
            color: var(--brand-red);
            border-bottom: 3px solid var(--brand-red);
            margin-bottom: -1px;
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
            font-family: var(--serif-font);
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
            font-family: var(--serif-font);
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

        .ad-box {{
            border: 2px solid var(--brand-red);
            background-color: #fdfdfd;
            padding: 25px;
            text-align: center;
            margin-bottom: 30px;
            position: relative;
        }}

        .ad-label {{
            position: absolute;
            top: 0; left: 50%;
            transform: translateX(-50%) translateY(-50%);
            background: var(--brand-red); color: white;
            font-size: 10px; padding: 2px 8px;
            text-transform: uppercase; font-weight: bold;
        }}

        .ad-box h3 {{
            font-family: var(--sans-font); font-weight: 900;
            color: var(--brand-red); font-size: 24px; margin-bottom: 10px;
            text-transform: uppercase;
        }}

        .btn-subscribe {{
            display: inline-block; background-color: var(--brand-red); color: white;
            padding: 12px 25px; font-weight: 700; text-transform: uppercase;
            font-size: 13px; transition: background 0.3s;
        }}
        .btn-subscribe:hover {{
            background-color: #a30e1e;
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
            font-family: var(--serif-font);
            font-size: 16px;
            margin-top: 5px;
        }}

        /* FOOTER */
        footer {{
            background-color: var(--brand-dark);
            color: #fff;
            padding: 50px 0;
            margin-top: 50px;
        }}

        .footer-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 30px;
            margin-bottom: 40px;
        }}

        .footer-col h4 {{
            color: #fff;
            text-transform: uppercase;
            margin-bottom: 20px;
            font-size: 14px;
            letter-spacing: 1px;
        }}

        .footer-col ul {{
            list-style: none;
        }}

        .footer-col li {{
            margin-bottom: 10px;
        }}

        .footer-col a {{
            color: #999;
            font-size: 13px;
        }}

        .footer-col a:hover {{
            color: #fff;
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

    <!-- BARRA SUPERIOR -->
    <div class="top-bar">
        <div class="container">
            <span>Edición España | <a href="#">Cambiar</a></span>
            <div>
                <a href="#" style="margin-right: 15px;">Iniciar Sesión</a>
                <a href="#" style="font-weight: bold;">Suscríbete</a>
            </div>
        </div>
    </div>

    <!-- HEADER LOGO -->
    <header class="header-main">
        <div class="container">
            <a href="../index.html">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/El_Mundo_logo.svg/1200px-El_Mundo_logo.svg.png" alt="El Mundo" class="logo">
            </a>
            <div class="date-line">
                {fecha_actualizacion}
            </div>
        </div>
    </header>

    <!-- NAVEGACIÓN -->
    <nav class="main-nav">
        <div class="container">
            <ul class="nav-list">
                <li class="nav-item"><a href="../index.html">Portada</a></li>
                <li class="nav-item"><a href="#">España</a></li>
                <li class="nav-item"><a href="#">Opinión</a></li>
                <li class="nav-item"><a href="#">Economía</a></li>
                <li class="nav-item"><a href="#">Internacional</a></li>
                <li class="nav-item"><a href="#">Deportes</a></li>
            </ul>
        </div>
    </nav>

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
                <div class="ad-box">
                    <span class="ad-label">Para ti</span>
                    <h3>No te pierdas nada</h3>
                    <p>La mejor información, sin límites.</p>
                    <a href="#" class="btn-subscribe">Suscribirme</a>
                </div>

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
            <div class="footer-grid">
                <div class="footer-col">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/El_Mundo_logo.svg/1200px-El_Mundo_logo.svg.png" alt="Logo Footer" width="150" style="filter: brightness(0) invert(1); margin-bottom: 20px;">
                    <p style="font-size: 13px; color: #999;">El diario líder en información general en español.</p>
                </div>
                <div class="footer-col">
                    <h4>Secciones</h4>
                    <ul>
                        <li><a href="../index.html">Portada</a></li>
                        <li><a href="#">España</a></li>
                        <li><a href="#">Economía</a></li>
                        <li><a href="#">Internacional</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Servicios</h4>
                    <ul>
                        <li><a href="#">Guía TV</a></li>
                        <li><a href="#">Tráfico</a></li>
                        <li><a href="#">El Tiempo</a></li>
                        <li><a href="#">Traductor</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Corporativo</h4>
                    <ul>
                        <li><a href="#">Aviso Legal</a></li>
                        <li><a href="#">Política de Privacidad</a></li>
                        <li><a href="#">Publicidad</a></li>
                        <li><a href="#">Contacto</a></li>
                    </ul>
                </div>
            </div>
            <div style="text-align: center; border-top: 1px solid #333; padding-top: 20px; font-size: 12px; color: #666;">
                &copy; 2025 Unidad Editorial Información General, S.L.U. Todos los derechos reservados.
            </div>
        </div>
    </footer>

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


def main():
    """Función principal que genera todas las páginas"""
    print("🚀 Generador de Páginas HTML - EL MUNDO")
    print("=" * 50)
    
    # Cargar JSON
    try:
        with open('noticias.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✅ JSON cargado correctamente")
    except Exception as e:
        print(f"❌ Error al cargar noticias.json: {e}")
        return
    
    # Crear carpeta noticias si no existe
    Path('noticias').mkdir(exist_ok=True)
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

