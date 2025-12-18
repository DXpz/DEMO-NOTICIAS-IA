#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Actualizador automático del index.html
Lee noticias.json y genera el index.html con todas las noticias
Autor: Trickzz.sh
"""

import json
from datetime import datetime
from pathlib import Path


# Plantilla HTML del index.html
PLANTILLA_INDEX = """<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <meta name="version" content="2.0-IA-NOTICIAS">
    <title>RED Noticias - Tu fuente confiable de información</title>
    <!-- Importamos fuentes elegantes de Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Roboto:wght@300;400;500;700&display=swap"
        rel="stylesheet">

    <style>
        /* VARIABLES Y CONFIGURACIÓN BASE */
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
            cursor: pointer;
        }}

        a:hover {{
            color: var(--brand-red);
        }}

        /* LAYOUT GENERAL */
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
            cursor: pointer;
            /* Para volver al home */
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

        /* LOGO TEXTO */
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


        /* GRID PRINCIPAL DE NOTICIAS (HOME) */
        .news-grid {{
            display: grid;
            grid-template-columns: 1.5fr 1fr;
            gap: 40px;
            margin-top: 30px;
            margin-bottom: 50px;
            max-width: 1400px;
            margin-left: auto;
            margin-right: auto;
        }}

        /* ESTILOS DE ARTÍCULOS (PREVIEW) */
        .article {{
            margin-bottom: 30px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 20px;
        }}

        .article:last-child {{
            border-bottom: none;
        }}

        .article-kicker {{
            color: var(--brand-red);
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
            display: block;
        }}

        .article-title {{
            font-family: var(--sans-font);
            font-weight: 700;
            line-height: 1.1;
            color: var(--brand-dark);
            margin-bottom: 10px;
        }}

        .article-title:hover {{
            color: var(--brand-red);
            cursor: pointer;
        }}

        .article-summary {{
            font-size: 15px;
            color: #555;
            margin-bottom: 15px;
        }}

        .article-author {{
            font-size: 12px;
            color: #888;
            text-transform: uppercase;
        }}

        .article-author strong {{
            color: var(--brand-dark);
        }}

        .article-img {{
            width: 100%;
            height: auto;
            display: block;
            margin-bottom: 15px;
            filter: brightness(0.95);
            transition: filter 0.3s;
            cursor: pointer;
        }}

        .article-img:hover {{
            filter: brightness(1);
        }}

        .hero-article .article-title {{
            font-size: 42px;
        }}

        .hero-article .article-summary {{
            font-size: 18px;
            line-height: 1.6;
        }}

        .list-article .article-title {{
            font-size: 20px;
        }}

        .list-article .article-img {{
            aspect-ratio: 16/9;
            object-fit: cover;
        }}

        /* SIDEBAR Y ANUNCIO */
        .sidebar-title {{
            font-size: 14px;
            font-weight: 900;
            text-transform: uppercase;
            border-bottom: 2px solid var(--brand-dark);
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}


        .opinion-item {{
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            border-bottom: 1px dotted #ccc;
            padding-bottom: 15px;
        }}

        .opinion-img {{
            width: 50px;
            height: 50px;
            border-radius: 50%;
            margin-right: 15px;
            object-fit: cover;
        }}

        .opinion-content h4 {{
            font-family: var(--sans-font);
            font-size: 16px;
            margin-bottom: 4px;
        }}

        .opinion-author {{
            font-size: 11px;
            text-transform: uppercase;
            color: var(--brand-red);
            font-weight: bold;
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
            .news-grid {{
                grid-template-columns: 1fr;
            }}

            .sidebar-col {{
                display: none;
            }}

            /* Simplificado para tablet */
        }}

        @media (max-width: 768px) {{
            .sidebar-col {{
                display: block;
                margin-top: 40px;
            }}

            /* Sidebar vuelve abajo en móvil */
        }}
    </style>
</head>

<body>

    <!-- HEADER LOGO -->
    <header class="header-main">
        <div class="container">
            <a href="index.html">
                <div class="logo-text">
                    <span class="logo-red">RED</span><span class="logo-noticias"> Noticias</span>
                </div>
            </a>
            <div class="date-line">
                {fecha_actualizacion}
            </div>
        </div>
    </header>


    <!-- CONTENIDO PRINCIPAL -->
    <main class="container">

        <!-- ======================= NUEVAS NOTICIAS DE IA ======================= -->
        <div id="home-view">
            <h2 style="font-family: var(--sans-font); font-size: 28px; margin: 30px 0 30px 0; color: var(--text-grey); font-weight: 400;">
                Las últimas noticias sobre el impacto de la IA en deportes, logística, sanidad, educación y economía
            </h2>

            <div class="news-grid">

                <!-- COLUMNA 1: PRINCIPAL -->
                <section class="main-col">
{noticia_principal}

{noticias_secundarias_main}
                </section>

                <!-- COLUMNA 2: SECUNDARIAS -->
                <section class="center-col">
                    <div class="sidebar-title">Más Noticias de IA</div>

{noticias_secundarias_center}

{noticias_lo_ultimo}
                </section>

            </div>
        </div>

    </main>

    <!-- FOOTER -->
    <footer>
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col">
                    <div class="logo-text" style="font-size: 36px;">
                        <span class="logo-red">RED</span><span class="logo-noticias"> Noticias</span>
                    </div>
                    <p style="font-size: 13px; color: #999; margin-top: 10px;">Tu fuente confiable de noticias e información.</p>
                </div>
                <div class="footer-col">
                    <h4>Información</h4>
                    <ul>
                        <li><a href="index.html">Inicio</a></li>
                        <li><a href="#">Acerca de</a></li>
                        <li><a href="#">Contacto</a></li>
                        <li><a href="#">Términos y Condiciones</a></li>
                    </ul>
                </div>
                <!-- ... -->
            </div>
            <div
                style="text-align: center; border-top: 1px solid #333; padding-top: 20px; font-size: 14px; color: #999;">
                2025 RED Noticias
            </div>
        </div>
    </footer>


</body>

</html>"""


def generar_articulo_principal(noticia):
    """Genera el HTML para la noticia principal"""
    return f"""                    <article class="article hero-article">
                        <span class="article-kicker">{noticia.get('categoria', 'Actualidad')}</span>
                        <a href="noticias/{noticia['id']}.html">
                            <img src="{noticia['imagen']}"
                                alt="{noticia['titulo']}" class="article-img">
                        </a>
                        <h1 class="article-title"><a href="noticias/{noticia['id']}.html">{noticia['titulo']}</a></h1>
                        <p class="article-summary">
                            {noticia['resumen']}
                        </p>
                        <div class="article-author">
                            Por <strong>Redacción RED Noticias</strong> | San Salvador
                        </div>
                    </article>"""


def generar_articulo_secundario_main(noticia):
    """Genera el HTML para una noticia secundaria en la columna principal"""
    return f"""                    <article class="article" style="margin-top: 30px;">
                        <a href="noticias/{noticia['id']}.html">
                            <img src="{noticia['imagen']}" alt="{noticia['titulo']}"
                                class="article-img">
                        </a>
                        <span class="article-kicker">{noticia.get('categoria', 'Actualidad')}</span>
                        <h2 class="article-title" style="font-size: 28px;"><a
                                href="noticias/{noticia['id']}.html">{noticia['titulo']}</a></h2>
                        <p class="article-summary" style="font-size: 16px;">
                            {noticia['resumen']}
                        </p>
                        <div class="article-author">
                            Por <strong>Redacción RED Noticias</strong> | San Salvador
                        </div>
                    </article>"""


def generar_articulo_lista(noticia):
    """Genera el HTML para una noticia en lista (columna central)"""
    return f"""                    <article class="article list-article">
                        <a href="noticias/{noticia['id']}.html">
                            <img src="{noticia['imagen']}"
                                alt="{noticia['titulo']}" class="article-img">
                        </a>
                        <span class="article-kicker">{noticia.get('categoria', 'Actualidad')}</span>
                        <h3 class="article-title"><a href="noticias/{noticia['id']}.html">{noticia['titulo']}</a></h3>
                        <p class="article-summary" style="font-size: 14px; margin-top: 8px;">
                            {noticia['resumen']}
                        </p>
                    </article>"""


def main():
    """Función principal que actualiza el index.html"""
    print("🔄 Actualizador de Index.html - RED Noticias")
    print("=" * 50)
    
    # Cargar JSON de noticias
    try:
        with open('noticias.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✅ JSON de noticias cargado correctamente")
    except Exception as e:
        print(f"❌ Error al cargar noticias.json: {e}")
        return
    
    config = data.get('config', {})
    
    # Preparar variables de la plantilla
    edicion = config.get('edicion', 'Edición El Salvador')
    fecha_actualizacion = config.get('fecha_actualizacion', datetime.now().strftime('%A, %d de %B de %Y'))
    
    # Extraer fecha corta para el sidebar
    try:
        # Intentar extraer una fecha corta del formato
        fecha_corta = datetime.now().strftime('%d/%m/%Y')
    except:
        fecha_corta = '17/12/2025'
    
    # Generar HTML de las noticias
    noticia_principal_html = ""
    noticias_secundarias_main_html = ""
    noticias_secundarias_center_html = ""
    noticias_lo_ultimo_html = ""
    
    total_noticias = 0
    
    # Noticia principal
    if 'noticia_principal' in data:
        noticia_principal_html = generar_articulo_principal(data['noticia_principal'])
        total_noticias += 1
        print("✅ Noticia principal procesada")
    
    # Noticias secundarias (repartidas entre main y center)
    if 'noticias_secundarias' in data:
        secundarias = data['noticias_secundarias']
        # Primera noticia secundaria va a main-col
        if len(secundarias) > 0:
            noticias_secundarias_main_html = generar_articulo_secundario_main(secundarias[0])
            total_noticias += 1
        
        # El resto van a center-col
        for noticia in secundarias[1:]:
            noticias_secundarias_center_html += generar_articulo_lista(noticia) + "\n"
            total_noticias += 1
        
        print(f"✅ {len(secundarias)} noticias secundarias procesadas")
    
    # Noticias de "lo último"
    if 'noticias_lo_ultimo' in data:
        for noticia in data['noticias_lo_ultimo']:
            noticias_lo_ultimo_html += generar_articulo_lista(noticia) + "\n"
            total_noticias += 1
        print(f"✅ {len(data['noticias_lo_ultimo'])} noticias de 'Lo último' procesadas")
    
    # Generar HTML completo
    html_final = PLANTILLA_INDEX.format(
        edicion=edicion,
        fecha_actualizacion=fecha_actualizacion,
        noticia_principal=noticia_principal_html,
        noticias_secundarias_main=noticias_secundarias_main_html,
        noticias_secundarias_center=noticias_secundarias_center_html,
        noticias_lo_ultimo=noticias_lo_ultimo_html,
        total_noticias=total_noticias,
        fecha_corta=fecha_corta
    )
    
    # Guardar index.html
    try:
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_final)
        print("\n✅ index.html actualizado correctamente")
        print(f"📊 Total de noticias: {total_noticias}")
        print("💡 El archivo está listo para ser usado")
    except Exception as e:
        print(f"❌ Error al guardar index.html: {e}")


if __name__ == "__main__":
    main()

