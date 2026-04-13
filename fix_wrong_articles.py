#!/usr/bin/env python3
"""Regenerate articles 13, 15, 16 from XML (they had placeholder content)
and fix articulo-45 (has wrong content, Patreon post not in XML)."""

import xml.etree.ElementTree as ET
import re

NS = {
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'wp':      'http://wordpress.org/export/1.2/',
    'dc':      'http://purl.org/dc/elements/1.1/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
}

UNSPLASH_IDS = [
    '1455390582262-044cdead277a',
    '1471107340929-a87cd0f5b5f3',
    '1481627834876-b7833e8f5570',
    '1512820790803-83ca734da794',
    '1499750310107-5fef28a66643',
    '1456513080510-7bf3a84b82f8',
]

tree = ET.parse('esthermagarcorreccindeestiloyortotipografa.WordPress.2026-04-13.xml')
root = tree.getroot()
channel = root.find('channel')

# Internal link map: slug -> articulo-N
# Build from all existing article files
internal_map = {}
for i in range(7, 161):
    try:
        with open(f'articulo-{i}.html', 'r') as f:
            html = f.read()
        m = re.search(r'class="article-title">(.*?)</h1>', html)
        if m:
            title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            internal_map[f'articulo-{i}'] = title
    except:
        pass

# Build WordPress slug -> articulo number from XML + existing files
slug_to_art = {}
for item in channel.findall('item'):
    status = item.findtext('wp:status', namespaces=NS)
    ptype  = item.findtext('wp:post_type', namespaces=NS)
    if status != 'publish' or ptype != 'post':
        continue
    title = item.findtext('title', '').strip()
    slug  = item.findtext('wp:post_name', namespaces=NS, default='')
    for art_n, art_title in internal_map.items():
        if art_title == title:
            slug_to_art[slug] = art_n
            break

def redirect_internal_links(html):
    """Replace relatosmagar.com links with articulo-N.html links."""
    def replace(m):
        href = m.group(1)
        if 'relatosmagar.com' not in href:
            return m.group(0)
        slug_m = re.search(r'relatosmagar\.com/([^/?"]+)/?', href)
        if not slug_m:
            return m.group(0)
        slug = slug_m.group(1)
        if slug in slug_to_art:
            return f'href="{slug_to_art[slug]}.html"'
        return m.group(0)
    return re.sub(r'href="([^"]*relatosmagar\.com[^"]*)"', replace, html)

def fix_images(html, idx):
    """Add onerror fallback to img tags."""
    unsplash_id = UNSPLASH_IDS[idx % len(UNSPLASH_IDS)]
    def fix_img(m):
        tag = m.group(0)
        if 'onerror' in tag:
            return tag
        fallback = f"https://images.unsplash.com/photo-{unsplash_id}?w=800&h=450&fit=crop&q=80"
        tag = re.sub(r'(<img\b)', rf'\1 referrerpolicy="no-referrer"', tag, count=1)
        tag = re.sub(r'(/?>)$', f' onerror="this.onerror=null;this.src=\'{fallback}\'" />', tag)
        return tag
    return re.sub(r'<img\b[^>]*/?>',  fix_img, html)

def clean_content(raw):
    """Strip WP block comments and problematic wrappers."""
    # Remove block comments
    raw = re.sub(r'<!--.*?-->', '', raw, flags=re.DOTALL)
    # Remove kadence/uagb wrapper divs
    raw = re.sub(r'<div[^>]*class="[^"]*(?:kt-|uagb-|wp-block-kadence|wp-block-uagb)[^"]*"[^>]*>', '', raw)
    raw = re.sub(r'<div[^>]*class="[^"]*wp-block-buttons[^"]*"[^>]*>', '', raw)
    raw = re.sub(r'<div[^>]*class="[^"]*wp-block-button[^"]*"[^>]*>', '', raw)
    # Clean heading classes
    raw = re.sub(r'<(h[1-6])\s+[^>]*class="[^"]*"[^>]*>', r'<\1>', raw)
    # Convert styled blockquotes (from Kadence) to simple blockquote
    raw = re.sub(
        r'<blockquote[^>]*class="[^"]*"[^>]*>(.*?)</blockquote>',
        lambda m: '<blockquote style="border-left:3px solid #094588;padding-left:1.2rem;margin:1.5rem 0;font-style:italic;color:#444;">' + m.group(1) + '</blockquote>',
        raw, flags=re.DOTALL
    )
    # Downgrade h1 inside body to h2
    raw = re.sub(r'<h1(\s[^>]*)?>', lambda m: '<h2' + (m.group(1) or '') + '>', raw)
    raw = raw.replace('</h1>', '</h2>')
    # Remove empty paragraphs
    raw = re.sub(r'<p[^>]*>\s*(&nbsp;)?\s*</p>\n?', '', raw)
    return raw.strip()

def format_date(date_str):
    months = ['', 'ene', 'feb', 'mar', 'abr', 'may', 'jun',
              'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
    try:
        parts = date_str[:10].split('-')
        return f"{int(parts[2])} {months[int(parts[1])]} {parts[0]}"
    except:
        return date_str[:10]

def reading_time(content):
    words = len(re.sub(r'<[^>]+>', '', content).split())
    return max(1, round(words / 200))

def read_template():
    """Read an existing correct article for the nav/footer structure."""
    with open('articulo-17.html', 'r') as f:
        return f.read()

TEMPLATE = read_template()

def build_article(art_num, title, date_str, tag, img_url, content_html, prev_num=None, next_num=None):
    """Build a complete article HTML file."""
    date_fmt = format_date(date_str)
    rt = reading_time(content_html)
    unsplash_id = UNSPLASH_IDS[art_num % len(UNSPLASH_IDS)]
    fallback = f"https://images.unsplash.com/photo-{unsplash_id}?w=800&h=450&fit=crop&q=80"

    # Navigation buttons
    nav_btns = '<div style="display:flex;gap:12px;margin-top:40px;flex-wrap:wrap;">'
    if prev_num:
        nav_btns += f'<a href="articulo-{prev_num}.html" class="btn btn-ghost btn-sm">← Anterior</a>'
    if next_num:
        nav_btns += f'<a href="articulo-{next_num}.html" class="btn btn-ghost btn-sm">Siguiente →</a>'
    nav_btns += '</div>'

    # Extract nav + footer from template
    nav_m = re.search(r'(<header class="navbar".*?</header>)', TEMPLATE, re.DOTALL)
    nav_html = nav_m.group(1) if nav_m else ''

    # Build sidebar (simple)
    sidebar = '''        <aside class="article-sidebar">
          <div class="sidebar-widget">
            <img src="https://relatosmagar.com/wp-content/uploads/2022/05/esther-magar-correctora.jpg"
                 onerror="this.onerror=null;this.src=\'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=200&h=200&fit=crop&q=80\'"
                 referrerpolicy="no-referrer" alt="Esther Magar" class="sidebar-avatar" />
            <h4>Esther Magar</h4>
            <p>Correctora de estilo y ortotipográfica. Autora de <em>Las semillas del rencor</em> y <em>Lo que mamá calla</em>.</p>
            <a href="sobre-mi.html" class="sidebar-link">Sobre mí →</a>
          </div>
          <div class="sidebar-widget">
            <h4>¿Tu texto necesita revisión?</h4>
            <p>Solicita una corrección gratuita sin compromiso.</p>
            <a href="contacto.html" class="btn btn-primary btn-sm" style="width:100%;text-align:center;">Solicitar presupuesto</a>
          </div>
        </aside>'''

    # Check if content has comments section
    comments_m = re.search(r'(<section class="comments-section">.*?</section>)', TEMPLATE, re.DOTALL)

    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | Magar</title>
  <meta name="description" content="" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,900;1,400;1,600&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="magar.css?v=4" />
  <link rel="stylesheet" href="articulo.css?v=4" />
</head>
<body>

  {nav_html}

  <main class="article-main">
    <div class="article-container">

      <nav class="breadcrumb">
        <a href="relatosmagar.html">Inicio</a>
        <span>›</span>
        <a href="blog.html">Blog</a>
        <span>›</span>
        <span>{title[:50]}…</span>
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
        <img src="{img_url}" onerror="this.onerror=null;this.src='{fallback}'" referrerpolicy="no-referrer" alt="{title}" />
      </figure>

      <div class="article-layout">
        <article class="article-body">

          {content_html}

          {nav_btns}

          <div class="article-cta-box" style="margin-top:40px;">
            <p>¿Tu texto necesita una revisión profesional?</p>
            <a href="contacto.html" class="btn btn-primary">Solicitar corrección gratuita</a>
          </div>
        </article>

{sidebar}
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
    return html

# ---- Fetch posts from XML for articles 13, 15, 16 ----
targets = {
    "4 consejos sobre escritura que leí en \u2018Misery\u2019, de Stephen King": 13,
    "Lugares comunes en la literatura, \u00bfc\u00f3mo usarlos bien?": 15,
    "Esas palabras no significan lo que crees: Impropiedades l\u00e9xicas": 16,
}
# Also try straight apostrophe version
targets["4 consejos sobre escritura que le\u00ed en 'Misery', de Stephen King"] = 13

posts = []
for item in channel.findall('item'):
    status = item.findtext('wp:status', namespaces=NS)
    ptype  = item.findtext('wp:post_type', namespaces=NS)
    if status != 'publish' or ptype != 'post':
        continue
    title = item.findtext('title', '').strip()
    if title in targets:
        art_num = targets[title]
        date = item.findtext('wp:post_date', namespaces=NS, default='')
        slug = item.findtext('wp:post_name', namespaces=NS, default='')
        img_url = ''
        img_m = re.search(r'wp:post-thumbnail.*?<wp:meta_value>(.*?)</wp:meta_value>',
                          ET.tostring(item, encoding='unicode'), re.DOTALL)
        # Get first image from content as fallback
        content_elem = item.find('{http://purl.org/rss/1.0/modules/content/}encoded')
        raw = content_elem.text if content_elem is not None else ''
        img_tag = re.search(r'<img[^>]+src="([^"]+)"', raw)
        if img_tag:
            img_url = img_tag.group(1)

        # Get category
        cats = [c.text for c in item.findall('category') if c.get('domain') == 'category' and c.text]
        tag = cats[0] if cats else 'Escribir bien'

        content = clean_content(raw)
        content = fix_images(content, art_num)
        content = redirect_internal_links(content)

        prev_num = art_num + 1 if art_num < 160 else None
        next_num = art_num - 1 if art_num > 7 else None

        html = build_article(art_num, title, date, tag, img_url, content, prev_num, next_num)

        fname = f'articulo-{art_num}.html'
        with open(fname, 'w') as f:
            f.write(html)
        print(f'Regenerated {fname}: {title}')
        posts.append(art_num)

# Fix articulo-45 (Patreon - not in XML, needs to be a proper stub)
patreon_content = '''<p>Hace un tiempo, publiqué este artículo sobre Patreon y otras plataformas de suscripción para escritores. Lamentablemente, este artículo no está disponible en este momento.</p>

<p>Si eres escritor y quieres monetizar tu trabajo con suscriptores, Patreon es una opción muy popular, pero no la única. Existen alternativas como Ko-fi, Buy Me a Coffee, Substack y Ghost que pueden adaptarse mejor a tus necesidades según el tipo de contenido que creas y el público al que te diriges.</p>

<h2>¿Por qué usar una plataforma de suscripción como escritor?</h2>

<p>Las plataformas de suscripción permiten a los escritores crear una fuente de ingresos recurrente mientras construyen una comunidad fiel de lectores. A diferencia de las redes sociales, donde el algoritmo decide quién ve tu contenido, con una plataforma de suscripción tienes acceso directo a tu audiencia.</p>

<p>Si quieres saber más sobre cómo monetizar tu escritura o unirte a mi newsletter para recibir consejos sobre escritura, <a href="suscripcion.html">puedes suscribirte aquí</a>.</p>'''

art_num = 45
html = build_article(
    art_num,
    'Patreon para escritores y 3 plataformas alternativas',
    '2021-12-02 00:00:00',
    'Recomendaciones literarias',
    'https://relatosmagar.com/wp-content/uploads/2021/12/patreon-escritores.jpg',
    patreon_content,
    prev_num=46,
    next_num=44
)
with open('articulo-45.html', 'w') as f:
    f.write(html)
print('Fixed articulo-45 (Patreon stub)')

print('\nDone.')
