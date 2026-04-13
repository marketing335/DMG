#!/usr/bin/env python3
"""Replace article-body content in articulo-13, 15, 16 with real XML content.
Preserves the HTML structure (nav, header, sidebar, comments)."""

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

# Build slug -> articulo-N map from existing files
slug_to_art = {}
for item in channel.findall('item'):
    status = item.findtext('wp:status', namespaces=NS)
    ptype  = item.findtext('wp:post_type', namespaces=NS)
    if status != 'publish' or ptype != 'post':
        continue
    title = item.findtext('title', '').strip()
    slug  = item.findtext('wp:post_name', namespaces=NS, default='')
    # Match to known article files by reading their h1
    for i in range(7, 161):
        try:
            with open(f'articulo-{i}.html', 'r') as f:
                html = f.read()
            m = re.search(r'class="article-title">(.*?)</h1>', html)
            if m:
                htitle = re.sub(r'<[^>]+>', '', m.group(1)).strip()
                if htitle == title:
                    slug_to_art[slug] = i
                    break
        except:
            pass

def redirect_links(html):
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

def fix_images(html, idx):
    unsplash = UNSPLASH_IDS[idx % len(UNSPLASH_IDS)]
    def fix_img(m):
        tag = m.group(0)
        if 'onerror' in tag:
            return tag
        fallback = f"https://images.unsplash.com/photo-{unsplash}?w=800&h=450&fit=crop&q=80"
        if 'referrerpolicy' not in tag:
            tag = re.sub(r'(<img\b)', r'\1 referrerpolicy="no-referrer"', tag, count=1)
        tag = tag.rstrip('>')
        tag = tag.rstrip('/')
        tag = tag.rstrip()
        tag += f' onerror="this.onerror=null;this.src=\'{fallback}\'" />'
        return tag
    return re.sub(r'<img\b[^>]*/?>',  fix_img, html)

def clean_content(raw):
    raw = re.sub(r'<!--.*?-->', '', raw, flags=re.DOTALL)
    raw = re.sub(r'<div[^>]*class="[^"]*(?:kt-|uagb-|wp-block-kadence|wp-block-uagb|wp-block-buttons|wp-block-button)[^"]*"[^>]*>', '', raw)
    raw = re.sub(r'<(h[1-6])\s+[^>]*class="[^"]*"[^>]*>', r'<\1>', raw)
    # Convert h1 in body to h2
    raw = re.sub(r'<h1(\s[^>]*)?>', lambda m: '<h2' + (m.group(1) or '') + '>', raw)
    raw = raw.replace('</h1>', '</h2>')
    # Remove color from heading styles
    def clean_heading_style(m):
        tag, attrs = m.group(1), m.group(2) or ''
        def rm_color(sm):
            style = sm.group(1)
            style = re.sub(r'color\s*:\s*[^;"}]+;?\s*', '', style).strip().rstrip(';').strip()
            return f' style="{style}"' if style else ''
        attrs = re.sub(r'\s*style="([^"]*)"', rm_color, attrs)
        return f'<{tag}{attrs}>'
    raw = re.sub(r'<(h[2-4])(\s[^>]*)?>', clean_heading_style, raw)
    # Empty paragraphs
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

# Targets: XML title -> article number
TARGETS = {
    "4 consejos sobre escritura que leí en \u2018Misery\u2019, de Stephen King": 13,
    "4 consejos sobre escritura que le\u00ed en 'Misery', de Stephen King": 13,
    "Lugares comunes en la literatura, \u00bfc\u00f3mo usarlos bien?": 15,
    "Esas palabras no significan lo que crees: Impropiedades l\u00e9xicas": 16,
}

for item in channel.findall('item'):
    status = item.findtext('wp:status', namespaces=NS)
    ptype  = item.findtext('wp:post_type', namespaces=NS)
    if status != 'publish' or ptype != 'post':
        continue
    title = item.findtext('title', '').strip()
    if title not in TARGETS:
        continue

    art_num = TARGETS[title]
    date_str = item.findtext('wp:post_date', namespaces=NS, default='')
    cats = [c.text for c in item.findall('category') if c.get('domain') == 'category' and c.text]
    tag = cats[0] if cats else 'Escribir bien'

    content_elem = item.find('{http://purl.org/rss/1.0/modules/content/}encoded')
    raw = content_elem.text if content_elem is not None else ''

    # Get first image for hero
    img_url = ''
    img_m = re.search(r'<img[^>]+src="([^"]+)"', raw)
    if img_m:
        img_url = img_m.group(1)

    cleaned = clean_content(raw)
    cleaned = fix_images(cleaned, art_num)
    cleaned = redirect_links(cleaned)

    rt = reading_time(cleaned)
    date_fmt = format_date(date_str)
    unsplash = UNSPLASH_IDS[art_num % len(UNSPLASH_IDS)]
    fallback = f"https://images.unsplash.com/photo-{unsplash}?w=800&h=450&fit=crop&q=80"

    # Read existing file
    fname = f'articulo-{art_num}.html'
    with open(fname, 'r') as f:
        html = f.read()

    # 1. Replace article-body content
    html = re.sub(
        r'(<article class="article-body">)(.*?)(</article>)',
        lambda m: m.group(1) + '\n\n          ' + cleaned + '\n\n          ' +
                  f'<div style="display:flex;gap:12px;margin-top:40px;flex-wrap:wrap;">'
                  f'<a href="articulo-{art_num+1}.html" class="btn btn-ghost btn-sm">← Anterior</a>'
                  f'<a href="articulo-{art_num-1}.html" class="btn btn-ghost btn-sm">Siguiente →</a>'
                  f'</div>\n\n          '
                  f'<div class="article-cta-box" style="margin-top:40px;">\n'
                  f'            <p>¿Tu texto necesita una revisión profesional?</p>\n'
                  f'            <a href="contacto.html" class="btn btn-primary">Solicitar corrección gratuita</a>\n'
                  f'          </div>\n        ' + m.group(3),
        html, flags=re.DOTALL
    )

    # 2. Update hero image
    if img_url:
        html = re.sub(
            r'(<figure class="article-hero-img">.*?<img\s+src=")[^"]*(")',
            lambda m: m.group(1) + img_url + m.group(2),
            html, flags=re.DOTALL
        )
        html = re.sub(
            r'(onerror="this\.onerror=null;this\.src=\')[^\']*(\'")',
            lambda m: m.group(1) + fallback + m.group(2),
            html, count=1
        )

    # 3. Update article-tag
    html = re.sub(r'(<div class="article-tag">)[^<]*(</div>)', rf'\g<1>{tag}\g<2>', html, count=1)

    # 4. Update meta date and reading time
    html = re.sub(
        r'(<div class="article-meta">.*?<span>)\d{1,2} \w+ \d{4}(</span>)',
        lambda m: m.group(1) + date_fmt + m.group(2),
        html, flags=re.DOTALL, count=1
    )
    html = re.sub(
        r'(<span>)\d+ min lectura(</span>)',
        lambda m: m.group(1) + f'{rt} min lectura' + m.group(2),
        html, count=1
    )

    with open(fname, 'w') as f:
        f.write(html)
    print(f'Fixed {fname}: {title!r}')

# Fix articulo-45 (Patreon - not in XML)
with open('articulo-45.html', 'r') as f:
    html45 = f.read()

patreon_body = '''<p>Si eres escritor y quieres monetizar tu trabajo con suscriptores, Patreon es una opción muy popular, pero no la única. En este artículo te explico las diferencias entre las principales plataformas de mecenazgo para escritores y cuál se adapta mejor a cada situación.</p>

<h2>¿Qué es Patreon y cómo funciona para escritores?</h2>

<p>Patreon es una plataforma que permite a los creadores recibir pagos recurrentes de sus suscriptores a cambio de contenido exclusivo. Como escritor, puedes ofrecer acceso anticipado a tus relatos, borradores de novelas, tutoriales de escritura o consultas personalizadas.</p>

<h2>3 alternativas a Patreon para escritores</h2>

<h3>Ko-fi</h3>
<p>Ko-fi es más sencillo que Patreon y permite tanto pagos únicos como suscripciones. Ideal si quieres empezar sin comprometerte con publicaciones regulares.</p>

<h3>Substack</h3>
<p>Substack es una plataforma orientada específicamente a newsletters. Si ya tienes una lista de suscriptores o quieres crear una, Substack facilita tanto el envío de correos como la versión de pago.</p>

<h3>Buy Me a Coffee</h3>
<p>Muy similar a Ko-fi, con una interfaz amigable. Puedes recibir donaciones puntuales o configurar membresías mensuales con contenido exclusivo para tus mecenas.</p>

<h2>¿Cuál elegir?</h2>
<p>Si ya tienes una audiencia consolidada y publicas contenido de forma regular, Patreon puede ser la mejor opción. Si estás empezando, Ko-fi o Buy Me a Coffee son más accesibles. Y si tu contenido principal es una newsletter, Substack es la elección natural.</p>'''

html45 = re.sub(
    r'(<article class="article-body">)(.*?)(</article>)',
    lambda m: m.group(1) + '\n\n          ' + patreon_body + '\n\n          ' +
              '<div style="display:flex;gap:12px;margin-top:40px;flex-wrap:wrap;">'
              '<a href="articulo-46.html" class="btn btn-ghost btn-sm">← Anterior</a>'
              '<a href="articulo-44.html" class="btn btn-ghost btn-sm">Siguiente →</a>'
              '</div>\n\n          '
              '<div class="article-cta-box" style="margin-top:40px;">\n'
              '            <p>¿Tu texto necesita una revisión profesional?</p>\n'
              '            <a href="contacto.html" class="btn btn-primary">Solicitar corrección gratuita</a>\n'
              '          </div>\n        ' + m.group(3),
    html45, flags=re.DOTALL
)
# Fix title
html45 = re.sub(r'(<h1 class="article-title">).*?(</h1>)',
                r'\1Patreon para escritores y 3 plataformas alternativas\2', html45, count=1)
# Fix date
html45 = re.sub(r'(<div class="article-meta">.*?<span>)\d{1,2} \w+ \d{4}(</span>)',
                lambda m: m.group(1) + '2 dic 2021' + m.group(2),
                html45, flags=re.DOTALL, count=1)

with open('articulo-45.html', 'w') as f:
    f.write(html45)
print('Fixed articulo-45 (Patreon)')

print('\nAll done.')
