#!/usr/bin/env python3
"""Regenera los 10 artículos más recientes con contenido IDÉNTICO al XML de WordPress.
Preserva TODO el contenido original: imágenes, estilos, citas, versos, etc."""

import xml.etree.ElementTree as ET
import re
import os

NS = {
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'wp':      'http://wordpress.org/export/1.2/',
    'dc':      'http://purl.org/dc/elements/1.1/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
}

UNSPLASH = [
    '1455390582262-044cdead277a',
    '1471107340929-a87cd0f5b5f3',
    '1481627834876-b7833e8f5570',
    '1512820790803-83ca734da794',
    '1499750310107-5fef28a66643',
    '1456513080510-7bf3a84b82f8',
]

# Artículos top 10 por fecha (número de artículo -> datos)
# blog.html order: 14, 8, 9, 10, 11, 12, 13, 15, 16, 7
TOP10_ORDER = [14, 8, 9, 10, 11, 12, 13, 15, 16, 7]

tree = ET.parse('esthermagarcorreccindeestiloyortotipografa.WordPress.2026-04-13.xml')
root = tree.getroot()
channel = root.find('channel')

# --- Mapa slug -> articulo-N (para redirigir enlaces internos) ---
slug_to_art = {}
for i in range(7, 161):
    fname = f'articulo-{i}.html'
    if not os.path.exists(fname):
        continue
    with open(fname, 'r') as f:
        html = f.read()
    m = re.search(r'class="article-title">(.*?)</h1>', html)
    if m:
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        slug_to_art[f'__title__{title}'] = i

# Mapa por slug de WordPress
for item in channel.findall('item'):
    status = item.findtext('wp:status', namespaces=NS)
    ptype  = item.findtext('wp:post_type', namespaces=NS)
    if status != 'publish' or ptype != 'post':
        continue
    title = item.findtext('title', '').strip()
    slug  = item.findtext('wp:post_name', namespaces=NS, default='')
    key = f'__title__{title}'
    if key in slug_to_art:
        slug_to_art[slug] = slug_to_art[key]

def redirect_links(html):
    """Redirige enlaces de relatosmagar.com a articulo-N.html."""
    def replace(m):
        href = m.group(1)
        if 'relatosmagar.com' not in href:
            return m.group(0)
        slug_m = re.search(r'relatosmagar\.com/([^/?"#]+)/?', href)
        if not slug_m:
            return m.group(0)
        slug = slug_m.group(1)
        if slug in slug_to_art:
            return f'href="articulo-{slug_to_art[slug]}.html"'
        return m.group(0)
    return re.sub(r'href="([^"]*relatosmagar\.com[^"]*)"', replace, html)

def add_img_fallback(html, idx):
    """Añade onerror fallback a imágenes de WordPress."""
    unsplash = UNSPLASH[idx % len(UNSPLASH)]
    fallback = f"https://images.unsplash.com/photo-{unsplash}?w=800&h=450&fit=crop&q=80"
    def fix_img(m):
        tag = m.group(0)
        if 'onerror' in tag:
            return tag
        if 'referrerpolicy' not in tag:
            tag = re.sub(r'<img\b', '<img referrerpolicy="no-referrer"', tag, count=1)
        tag = tag.rstrip('/>').rstrip()
        tag += f' onerror="this.onerror=null;this.src=\'{fallback}\'" />'
        return tag
    return re.sub(r'<img\b[^>]*/?>',  fix_img, html)

def clean_content(raw):
    """Limpia el contenido WordPress preservando TODO el contenido semántico."""
    # 1. Eliminar SOLO los comentarios de bloque WordPress
    cleaned = re.sub(r'<!--.*?-->', '', raw, flags=re.DOTALL)

    # 2. Limpiar clases Kadence/UAGB de los headings pero PRESERVAR inline styles e id
    def clean_heading(m):
        full_tag = m.group(0)
        tag = m.group(1)
        # Eliminar solo class attribute (contiene clases Kadence largas)
        full_tag = re.sub(r'\s*class="[^"]*(?:kt-|uagb-|wp-block-kadence|wp-block-)[^"]*"', '', full_tag)
        # Eliminar id de Kadence (kt-adv-heading_...)
        full_tag = re.sub(r'\s*id="kt-adv-heading[^"]*"', '', full_tag)
        return full_tag
    cleaned = re.sub(r'(<h[1-6]\b[^>]*>)', clean_heading, cleaned)

    # 3. Convertir h1 dentro del cuerpo en h2 (excepto el title que está fuera)
    cleaned = re.sub(r'<h1(\s[^>]*)?>', lambda m: '<h2' + (m.group(1) or '') + '>', cleaned)
    cleaned = cleaned.replace('</h1>', '</h2>')

    # 4. Limpiar class de Kadence en divs wrapper pero MANTENER el contenido
    cleaned = re.sub(r'<div[^>]*class="[^"]*(?:wp-block-kadence|wp-block-uagb)[^"]*"[^>]*>', '<div>', cleaned)

    # 5. Limpiar class de wp-block-buttons/button wrapper pero mantener el enlace
    cleaned = re.sub(r'<div[^>]*class="[^"]*wp-block-buttons[^"]*"[^>]*>', '', cleaned)
    cleaned = re.sub(r'<div[^>]*class="[^"]*wp-block-button[^"]*"[^>]*>', '', cleaned)

    # 6. Convertir pullquote en blockquote estilizado
    cleaned = re.sub(
        r'<figure[^>]*class="[^"]*wp-block-pullquote[^"]*"[^>]*>(.*?)</figure>',
        lambda m: '<blockquote class="wp-pullquote">' + re.sub(r'</?figure[^>]*>', '', m.group(1)) + '</blockquote>',
        cleaned, flags=re.DOTALL
    )

    # 7. Limpiar class de wp-block-quote
    cleaned = re.sub(r'<blockquote[^>]*class="wp-block-quote"[^>]*>', '<blockquote>', cleaned)

    # 8. Limpiar class de figuras wp-block-image (mantener figura pero limpiar clases largas)
    def clean_figure(m):
        tag = m.group(0)
        # Keep simple classes only
        tag = re.sub(r'class="[^"]*wp-block-image[^"]*"', 'class="wp-block-image"', tag)
        return tag
    cleaned = re.sub(r'<figure[^>]*class="[^"]*wp-block-image[^"]*"[^>]*>', clean_figure, cleaned)

    # 9. Limpiar párrafos con clases Gutenberg largas pero mantener has-background
    def clean_para(m):
        tag = m.group(0)
        # Keep has-background and has-text-align-center classes
        keep_classes = []
        classes_m = re.search(r'class="([^"]*)"', tag)
        if classes_m:
            for cls in classes_m.group(1).split():
                if cls.startswith('has-') or cls in ['aligncenter', 'alignleft', 'alignright']:
                    keep_classes.append(cls)
            if keep_classes:
                tag = re.sub(r'class="[^"]*"', f'class="{" ".join(keep_classes)}"', tag)
            else:
                tag = re.sub(r'\s*class="[^"]*"', '', tag)
        return tag
    cleaned = re.sub(r'<p\b[^>]*>', clean_para, cleaned)

    # 10. Eliminar párrafos vacíos
    cleaned = re.sub(r'<p[^>]*>\s*(&nbsp;)?\s*</p>\n?', '', cleaned)

    # 11. Limpiar data-type y data-id de enlaces (no necesario)
    cleaned = re.sub(r'\s*data-type="[^"]*"', '', cleaned)
    cleaned = re.sub(r'\s*data-id="[^"]*"', '', cleaned)

    return cleaned.strip()

def format_date(date_str):
    months = ['', 'ene', 'feb', 'mar', 'abr', 'may', 'jun',
              'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
    try:
        parts = date_str[:10].split('-')
        return f"{int(parts[2])} {months[int(parts[1])]} {parts[0]}"
    except:
        return date_str[:10]

def reading_time(text):
    words = len(re.sub(r'<[^>]+>', '', text).split())
    return max(1, round(words / 200))

def get_hero_image(item, content_raw):
    """Obtiene la imagen de portada del post."""
    # Try featured image attachment URL from XML meta
    raw_xml = ET.tostring(item, encoding='unicode')
    # Look for _thumbnail_id in postmeta
    thumb_id = None
    for pm in item.findall('wp:postmeta', NS):
        key = pm.findtext('wp:meta_key', namespaces=NS)
        if key == '_thumbnail_id':
            thumb_id = pm.findtext('wp:meta_value', namespaces=NS)

    # If no thumbnail, get first meaningful image from content
    imgs = re.findall(r'<img[^>]+src="([^"]+)"', content_raw)
    for img in imgs:
        if 'wp-content/uploads' in img:
            return img

    return ''

# Leer la plantilla de navegación de un artículo existente
with open('articulo-17.html', 'r') as f:
    TEMPLATE = f.read()

nav_m = re.search(r'(<header class="navbar".*?</header>)', TEMPLATE, re.DOTALL)
NAV_HTML = nav_m.group(1) if nav_m else ''

SIDEBAR = '''        <aside class="article-sidebar">
          <div class="sidebar-widget">
            <img src="https://relatosmagar.com/wp-content/uploads/2022/05/esther-magar-correctora.jpg"
                 onerror="this.onerror=null;this.src=\'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=200&h=200&fit=crop&q=80\'"
                 referrerpolicy="no-referrer"
                 alt="Esther Magar" class="sidebar-avatar" />
            <h4>Esther Magar</h4>
            <p>Correctora de estilo y ortotipográfica. Autora de <em>Las semillas del rencor</em> y <em>Lo que mamá calla</em>.</p>
            <a href="sobre-mi.html" class="sidebar-link">Sobre mí →</a>
          </div>
          <div class="sidebar-widget" style="display:grid;grid-template-columns:1fr 1fr;gap:10px;background:none;box-shadow:none;padding:0;">
            <div style="background:#fff;border-radius:12px;padding:16px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.08);">
              <div style="width:46px;height:46px;background:#094588;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 10px;">
                <svg width="22" height="22" fill="#fff" viewBox="0 0 8 8"><path d="M6 0l-1 1 2 2 1-1-2-2zm-2 2l-4 4v2h2l4-4-2-2z"/></svg>
              </div>
              <h4 style="font-size:.82rem;margin-bottom:6px">¿Buscas corrector de textos?</h4>
              <p style="font-size:.78rem;color:#666;margin-bottom:10px;">Pídeme presupuesto sin compromiso, te responderé lo antes posible.</p>
              <a href="contacto.html" style="display:block;background:#094588;color:#ffffff;padding:8px 10px;border-radius:6px;font-weight:600;font-size:.72rem;text-decoration:none;text-align:center;">Quiero presupuesto</a>
            </div>
            <div style="background:#fff;border-radius:12px;padding:16px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.08);">
              <div style="width:46px;height:46px;background:#094588;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 10px;">
                <svg width="22" height="22" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
              </div>
              <h4 style="font-size:.82rem;margin-bottom:6px">¿Te parece interesante?</h4>
              <p style="font-size:.78rem;color:#666;margin-bottom:10px;">Para no perderte ningún artículo y acceder a contenido exclusivo, suscríbete a mi lista.</p>
              <a href="suscripcion.html" style="display:block;background:#094588;color:#ffffff;padding:8px 10px;border-radius:6px;font-weight:600;font-size:.72rem;text-decoration:none;text-align:center;">Me suscribo</a>
            </div>
          </div>
          <div class="sidebar-widget" style="text-align:center;border:1px solid #e8e4df;border-radius:12px;padding:20px;">
            <p style="font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;color:#094588;font-weight:700;margin-bottom:14px;">Conoce mi universo literario</p>
            <div style="display:flex;justify-content:center;gap:10px;margin-bottom:14px;">
              <img src="https://m.media-amazon.com/images/P/B093Z7T8HV.01._SCLZZZZZZZ_SX500_.jpg" alt="Las semillas del rencor" style="width:70px;border-radius:4px;box-shadow:0 2px 6px rgba(0,0,0,.15);" />
              <img src="https://m.media-amazon.com/images/P/B0GQ3JZ7M1.01._SCLZZZZZZZ_SX500_.jpg" alt="Lo que mamá calla" style="width:70px;border-radius:4px;box-shadow:0 2px 6px rgba(0,0,0,.15);" />
            </div>
            <div style="display:flex;gap:8px;justify-content:center;">
              <a href="https://amzn.to/3Yrt4oo" target="_blank" rel="noopener" style="display:inline-block;background:#094588;color:#ffffff;padding:8px 10px;border-radius:6px;font-weight:600;font-size:.72rem;text-decoration:none;">Las semillas del…</a>
              <a href="http://amzn.to/4aRt4TY" target="_blank" rel="noopener" style="display:inline-block;background:#094588;color:#ffffff;padding:8px 10px;border-radius:6px;font-weight:600;font-size:.72rem;text-decoration:none;">Lo que mamá calla</a>
            </div>
          </div>
        </aside>'''

def build_html(art_num, title, date_str, tag, hero_img, body_html, prev_n, next_n):
    date_fmt = format_date(date_str)
    rt = reading_time(body_html)
    uns = UNSPLASH[art_num % len(UNSPLASH)]
    fallback = f"https://images.unsplash.com/photo-{uns}?w=800&h=450&fit=crop&q=80"

    nav_btns = '<div style="display:flex;gap:12px;margin-top:40px;flex-wrap:wrap;">'
    if prev_n:
        nav_btns += f'<a href="articulo-{prev_n}.html" class="btn btn-ghost btn-sm">← Anterior</a>'
    if next_n:
        nav_btns += f'<a href="articulo-{next_n}.html" class="btn btn-ghost btn-sm">Siguiente →</a>'
    nav_btns += '</div>'

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | Magar</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,900;1,400;1,600&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="magar.css?v=4" />
  <link rel="stylesheet" href="articulo.css?v=4" />
</head>
<body>

  {NAV_HTML}

  <main class="article-main">
    <div class="article-container">

      <nav class="breadcrumb">
        <a href="relatosmagar.html">Inicio</a>
        <span>›</span>
        <a href="blog.html">Blog</a>
        <span>›</span>
        <span>{title[:55]}…</span>
      </nav>

      <header class="article-header">
        <div class="article-tag">{tag}</div>
        <h1 class="article-title">{title}</h1>
        <div class="article-meta">
          <span>{date_fmt}</span>
          <span class="meta-dot">·</span>
          <span>{rt} min lectura</span>
          <span class="meta-dot">·</span>
          <span>por <strong>Esther Magar</strong></span>
        </div>
      </header>

      <figure class="article-hero-img">
        <img src="{hero_img}" onerror="this.onerror=null;this.src=\'{fallback}\'" referrerpolicy="no-referrer" alt="{title}" />
      </figure>

      <div class="article-layout">
        <article class="article-body">

{body_html}

          {nav_btns}

          <div style="background:#0f1b2d;border-radius:12px;padding:36px;margin:40px 0;text-align:center;">
            <p style="color:#ffffff;font-size:16px;margin-bottom:20px;">¿Tu texto necesita una revisión profesional?</p>
            <a href="contacto.html" style="display:inline-block;background:#1a3a8f;color:#ffffff;padding:14px 28px;border-radius:8px;font-weight:600;font-size:15px;text-decoration:none;">Solicitar corrección gratuita</a>
          </div>
        </article>

{SIDEBAR}
      </div>

    </div>
  </main>

  <script>
    const nav = document.getElementById('navbar');
    window.addEventListener('scroll', () => nav.classList.toggle('scrolled', window.scrollY > 40));
    document.getElementById('hamburger').addEventListener('click', () => {{
      document.getElementById('navLinks').classList.toggle('open');
    }});
  </script>
</body>
</html>'''

# --- Procesar los 10 artículos más recientes ---
posts = []
for item in channel.findall('item'):
    status = item.findtext('wp:status', namespaces=NS)
    ptype  = item.findtext('wp:post_type', namespaces=NS)
    if status != 'publish' or ptype != 'post':
        continue
    title = item.findtext('title', '').strip()
    date  = item.findtext('wp:post_date', namespaces=NS, default='')
    content_elem = item.find('{http://purl.org/rss/1.0/modules/content/}encoded')
    raw = content_elem.text if content_elem is not None else ''
    cats = [c.text for c in item.findall('category') if c.get('domain') == 'category' and c.text]
    tag = cats[0] if cats else 'Escribir bien'
    posts.append((date, title, raw, tag, item))

posts.sort(key=lambda x: x[0], reverse=True)

for i, (date, title, raw, tag, item) in enumerate(posts[:10]):
    art_num = TOP10_ORDER[i]

    # Imagen de portada
    hero_img = get_hero_image(item, raw)

    # Limpiar contenido
    body = clean_content(raw)
    body = add_img_fallback(body, art_num)
    body = redirect_links(body)

    # Determinar artículo anterior y siguiente
    prev_n = TOP10_ORDER[i + 1] if i + 1 < len(TOP10_ORDER) else None
    next_n = TOP10_ORDER[i - 1] if i > 0 else None

    # Leer el archivo existente para preservar la sección de comentarios
    fname = f'articulo-{art_num}.html'
    comments_section = ''
    if os.path.exists(fname):
        with open(fname, 'r') as f:
            existing = f.read()
        comments_m = re.search(r'(<section class="comments-section">.*?</section>)', existing, re.DOTALL)
        if comments_m:
            comments_section = comments_m.group(1)

    html = build_html(art_num, title, date, tag, hero_img, body, prev_n, next_n)

    # Reinsertar comentarios antes de </main>
    if comments_section:
        html = html.replace('</main>', f'\n    <div class="article-container">\n      {comments_section}\n    </div>\n  </main>', 1)

    with open(fname, 'w') as f:
        f.write(html)

    body_len = len(re.search(r'<article class="article-body">(.*?)</article>', html, re.DOTALL).group(1))
    print(f"  articulo-{art_num}: {title[:50]} ({body_len} chars)")

print(f"\nDone. {len(posts[:10])} articles regenerated.")
