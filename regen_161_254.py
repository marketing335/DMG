#!/usr/bin/env python3
"""Genera articulo-161 a articulo-254 desde los posts del XML no cubiertos por articulos 7-160."""

import xml.etree.ElementTree as ET, re, os

NS = {
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'wp':      'http://wordpress.org/export/1.2/',
}

UNSPLASH = [
    '1455390582262-044cdead277a', '1471107340929-a87cd0f5b5f3',
    '1481627834876-b7833e8f5570', '1512820790803-83ca734da794',
    '1499750310107-5fef28a66643', '1456513080510-7bf3a84b82f8',
]

tree = ET.parse('esthermagarcorreccindeestiloyortotipografa.WordPress.2026-04-13.xml')
root = tree.getroot()
channel = root.find('channel')

# --- Mapa attachment_id -> URL ---
attachments = {}
for item in channel.findall('item'):
    if item.findtext('wp:post_type', namespaces=NS) == 'attachment':
        pid = item.findtext('wp:post_id', namespaces=NS)
        url = item.findtext('wp:attachment_url', namespaces=NS, default='')
        if not url:
            url = item.findtext('guid', '').strip()
        if pid and url and 'wp-content/uploads' in url:
            attachments[pid] = url

# --- Títulos ya generados (articulo-7 a 160) ---
used_titles = set()
for n in range(7, 161):
    f = f'articulo-{n}.html'
    if not os.path.exists(f):
        continue
    with open(f) as fh:
        h = fh.read()
    m = re.search(r'class="article-title">(.*?)</h1>', h)
    if m:
        used_titles.add(re.sub(r'<[^>]+>', '', m.group(1)).strip())

# --- Posts pendientes (ordenados newest→oldest → numeración 161, 162…) ---
pending = []
for item in channel.findall('item'):
    if item.findtext('wp:status', namespaces=NS) != 'publish':
        continue
    if item.findtext('wp:post_type', namespaces=NS) != 'post':
        continue
    title = (item.findtext('title') or '').strip()
    if title in used_titles:
        continue
    date = item.findtext('wp:post_date', namespaces=NS) or ''
    content_el = item.find('{http://purl.org/rss/1.0/modules/content/}encoded')
    raw = content_el.text if content_el is not None else ''
    pending.append((date, title, raw, item))

pending.sort(key=lambda x: x[0], reverse=True)   # newest first → lowest article number
print(f'Posts pendientes: {len(pending)} → articulo-161 a articulo-{160 + len(pending)}')

# --- Navbar desde plantilla ---
with open('articulo-17.html') as f:
    TEMPLATE = f.read()
nav_m = re.search(r'(<header class="navbar".*?</header>)', TEMPLATE, re.DOTALL)
NAV_HTML = nav_m.group(1) if nav_m else ''

# --- Artículos relacionados para el sidebar ---
RELATED_POOL = [
    (14, 'No es lo mismo folk horror que gótico rural'),
    (7,  'Guía para solucionar las dudas de escritores noveles'),
    (17, '9 libros sobre escritura que quizá no conozcas'),
    (8,  '¿Miedo a publicar tu segunda novela? No eres el único'),
    (9,  'Narrador en primera persona: pros y contras'),
    (18, '10 tipos de trama que necesitas conocer para no atascarte'),
    (19, 'El mejor consejo de escritura del mundo'),
]


def make_sidebar(art_num):
    related = [(n, t) for n, t in RELATED_POOL if n != art_num][:3]
    related_items = ''.join(
        f'              <li><a href="articulo-{n}.html">{t}</a></li>\n'
        for n, t in related
    )
    return f'''        <aside class="article-sidebar">
          <div class="sidebar-widget">
            <h4>Sobre la autora</h4>
            <img src="https://i.ibb.co/zH7DxvJS/dame-esta-mujercon-202603241403.jpg"
                 onerror="this.onerror=null;this.src=\'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=200&h=200&fit=crop&q=80\'"
                 alt="Esther Magar" class="sidebar-avatar" />
            <p><strong>Esther Magar</strong> es correctora y editora de textos con más de diez años de experiencia.</p>
            <a href="sobre-mi.html" class="sidebar-link">Conocer más →</a>
          </div>
          <div class="sidebar-widget">
            <h4>Artículos relacionados</h4>
            <ul class="sidebar-related">
{related_items}            </ul>
          </div>
          <div class="sidebar-widget" style="display:grid;grid-template-columns:1fr 1fr;gap:10px;background:none;box-shadow:none;padding:0;">
            <div style="background:#fff;border-radius:12px;padding:16px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.08);">
              <div style="width:46px;height:46px;background:#094588;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 10px;">
                <svg width="22" height="22" fill="#fff" viewBox="0 0 8 8"><path d="M6 0l-1 1 2 2 1-1-2-2zm-2 2l-4 4v2h2l4-4-2-2z"/></svg>
              </div>
              <h4 style="font-size:.82rem;margin-bottom:6px">¿Buscas corrector de textos?</h4>
              <p style="font-size:.78rem;color:#666;margin-bottom:10px;">Pídeme presupuesto sin compromiso, te responderé lo antes posible.</p>
              <a href="contacto.html" class="btn btn-primary btn-sm" style="width:100%;">Quiero presupuesto</a>
            </div>
            <div style="background:#fff;border-radius:12px;padding:16px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.08);">
              <div style="width:46px;height:46px;background:#094588;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 10px;">
                <svg width="22" height="22" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
              </div>
              <h4 style="font-size:.82rem;margin-bottom:6px">¿Te parece interesante?</h4>
              <p style="font-size:.78rem;color:#666;margin-bottom:10px;">Para no perderte ningún artículo, suscríbete a mi lista.</p>
              <a href="suscripcion.html" class="btn btn-primary btn-sm" style="width:100%;">Me suscribo</a>
            </div>
          </div>
          <div class="sidebar-widget" style="text-align:center;border:1px solid #e8e4df;border-radius:12px;padding:20px;">
            <p style="font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;color:#094588;font-weight:700;margin-bottom:14px;">Conoce mi universo literario</p>
            <div style="display:flex;justify-content:center;gap:10px;margin-bottom:14px;">
              <img src="https://m.media-amazon.com/images/P/B093Z7T8HV.01._SCLZZZZZZZ_SX500_.jpg" alt="Las semillas del rencor" style="width:70px;border-radius:4px;box-shadow:0 2px 6px rgba(0,0,0,.15);" />
              <img src="https://m.media-amazon.com/images/P/B0GQ3JZ7M1.01._SCLZZZZZZZ_SX500_.jpg" alt="Lo que mamá calla" style="width:70px;border-radius:4px;box-shadow:0 2px 6px rgba(0,0,0,.15);" />
            </div>
            <div style="display:flex;gap:8px;justify-content:center;">
              <a href="https://amzn.to/3Yrt4oo" target="_blank" rel="noopener" class="btn btn-primary btn-sm" style="font-size:.72rem;padding:8px 10px;">Las semillas del…</a>
              <a href="http://amzn.to/4aRt4TY" target="_blank" rel="noopener" class="btn btn-primary btn-sm" style="font-size:.72rem;padding:8px 10px;">Lo que mamá calla</a>
            </div>
          </div>
        </aside>'''


def unwrap_div_by_class(html, class_pattern):
    result = []
    pos = 0
    while pos < len(html):
        div_start = html.find('<div', pos)
        if div_start == -1:
            result.append(html[pos:])
            break
        tag_end = html.find('>', div_start)
        if tag_end == -1:
            result.append(html[pos:])
            break
        tag = html[div_start:tag_end+1]
        if tag.endswith('/>'):
            result.append(html[pos:tag_end+1])
            pos = tag_end + 1
            continue
        if re.search(class_pattern, tag):
            result.append(html[pos:div_start])
            depth = 1
            scan_pos = tag_end + 1
            inner_start = scan_pos
            while scan_pos < len(html) and depth > 0:
                next_open = html.find('<div', scan_pos)
                next_close = html.find('</div>', scan_pos)
                if next_close == -1:
                    result.append(html[inner_start:])
                    scan_pos = len(html)
                    break
                if next_open != -1 and next_open < next_close:
                    depth += 1
                    oe = html.find('>', next_open)
                    scan_pos = (oe + 1) if oe != -1 else (next_open + 4)
                else:
                    depth -= 1
                    if depth == 0:
                        result.append(html[inner_start:next_close])
                        scan_pos = next_close + 6
                        break
                    scan_pos = next_close + 6
            pos = scan_pos
        else:
            result.append(html[pos:tag_end+1])
            pos = tag_end + 1
    return ''.join(result)


def clean_content(raw):
    c = re.sub(r'<!--.*?-->', '', raw, flags=re.DOTALL)
    def clean_heading(m):
        t = re.sub(r'\s*class="[^"]*(?:kt-|uagb-|wp-block-)[^"]*"', '', m.group(0))
        t = re.sub(r'\s*id="kt-adv-heading[^"]*"', '', t)
        return t
    c = re.sub(r'(<h[1-6]\b[^>]*>)', clean_heading, c)
    c = re.sub(r'<h1(\s[^>]*)?>', lambda m: '<h2' + (m.group(1) or '') + '>', c)
    c = c.replace('</h1>', '</h2>')
    c = re.sub(r'<div[^>]*class="[^"]*(?:wp-block-kadence|wp-block-uagb)[^"]*"[^>]*>', '<div>', c)
    c = unwrap_div_by_class(c, r'class="[^"]*wp-block-buttons[^"]*"')
    c = unwrap_div_by_class(c, r'class="[^"]*wp-block-button\b[^"]*"')
    c = re.sub(r'<figure[^>]*class="[^"]*wp-block-pullquote[^"]*"[^>]*>(.*?)</figure>',
               lambda m: '<blockquote class="wp-pullquote">' + re.sub(r'</?figure[^>]*>', '', m.group(1)) + '</blockquote>',
               c, flags=re.DOTALL)
    c = re.sub(r'<blockquote[^>]*class="wp-block-quote"[^>]*>', '<blockquote>', c)
    def clean_figure(m):
        return re.sub(r'class="[^"]*wp-block-image[^"]*"', 'class="wp-block-image"', m.group(0))
    c = re.sub(r'<figure[^>]*class="[^"]*wp-block-image[^"]*"[^>]*>', clean_figure, c)
    def clean_para(m):
        keep = [cl for cl in re.findall(r'class="([^"]*)"', m.group(0))[0:1] and
                re.findall(r'class="([^"]*)"', m.group(0))[0].split()
                if cl.startswith('has-') or cl in ['aligncenter', 'alignleft', 'alignright']] \
               if re.search(r'class="', m.group(0)) else []
        tag = m.group(0)
        if keep:
            tag = re.sub(r'class="[^"]*"', f'class="{" ".join(keep)}"', tag)
        else:
            tag = re.sub(r'\s*class="[^"]*"', '', tag)
        return tag
    c = re.sub(r'<p\b[^>]*>', clean_para, c)
    c = re.sub(r'<p[^>]*>\s*(&nbsp;)?\s*</p>\n?', '', c)
    c = re.sub(r'\s*data-type="[^"]*"', '', c)
    c = re.sub(r'\s*data-id="[^"]*"', '', c)
    return c.strip()


def format_date(d):
    months = ['', 'ene', 'feb', 'mar', 'abr', 'may', 'jun',
              'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
    try:
        p = d[:10].split('-')
        return f"{int(p[2])} {months[int(p[1])]} {p[0]}"
    except:
        return d[:10]


def reading_time(text):
    return max(1, round(len(re.sub(r'<[^>]+>', '', text).split()) / 200))


def get_hero_image(item, content_raw):
    for pm in item.findall('wp:postmeta', NS):
        if pm.findtext('wp:meta_key', namespaces=NS) == '_thumbnail_id':
            tid = pm.findtext('wp:meta_value', namespaces=NS)
            if tid and tid in attachments:
                return attachments[tid]
    for img in re.findall(r'src="(https?://[^"]*wp-content/uploads/[^"]+\.(?:jpg|jpeg|png|webp|gif))"',
                           content_raw, re.IGNORECASE):
        if not re.search(r'-\d+x\d+\.', img):
            return img
    return ''


def add_img_fallback(html, idx):
    uns = UNSPLASH[idx % len(UNSPLASH)]
    fb = f"https://images.unsplash.com/photo-{uns}?w=800&h=450&fit=crop&q=80"
    def fix(m):
        t = m.group(0)
        if 'onerror' in t:
            return t
        if 'referrerpolicy' not in t:
            t = re.sub(r'<img\b', '<img referrerpolicy="no-referrer"', t, count=1)
        t = t.rstrip('/>').rstrip()
        return t + f' onerror="this.onerror=null;this.src=\'{fb}\'" />'
    return re.sub(r'<img\b[^>]*/?>',  fix, html)


# --- Generar articulos ---
for i, (date, title, raw, item) in enumerate(pending):
    art_num = 161 + i
    cats = [c.text for c in item.findall('category') if c.get('domain') == 'category' and c.text]
    tag = cats[0] if cats else 'Blog'
    hero_img = get_hero_image(item, raw)
    uns = UNSPLASH[art_num % len(UNSPLASH)]
    fallback = f"https://images.unsplash.com/photo-{uns}?w=800&h=450&fit=crop&q=80"
    if not hero_img:
        hero_img = fallback
    body = clean_content(raw)
    body = add_img_fallback(body, art_num)
    date_fmt = format_date(date)
    rt = reading_time(body)
    prev_n = art_num + 1 if art_num < 160 + len(pending) else None
    next_n = art_num - 1 if art_num > 161 else 160

    nav_btns = '<div style="display:flex;gap:12px;margin-top:40px;flex-wrap:wrap;">'
    if next_n:
        nav_btns += f'<a href="articulo-{next_n}.html" class="btn btn-ghost btn-sm">← Anterior</a>'
    if prev_n:
        nav_btns += f'<a href="articulo-{prev_n}.html" class="btn btn-ghost btn-sm">Siguiente →</a>'
    nav_btns += '</div>'

    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | Magar</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,900;1,400;1,600&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="magar.css?v=5" />
  <link rel="stylesheet" href="articulo.css?v=5" />
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

{body}

          {nav_btns}

          <div style="background:#0f1b2d;border-radius:12px;padding:36px;margin:40px 0;text-align:center;">
            <p style="color:#ffffff;font-size:16px;margin-bottom:20px;">¿Tu texto necesita una revisión profesional?</p>
            <a href="contacto.html" style="display:inline-block;background:#1a3a8f;color:#ffffff;padding:14px 28px;border-radius:8px;font-weight:600;font-size:15px;text-decoration:none;">Solicitar corrección gratuita</a>
          </div>
        </article>

{make_sidebar(art_num)}
      </div>

    </div>
  </main>

  <footer class="footer">
    <div class="container">
      <div class="footer-bottom" style="border-top:1px solid rgba(255,255,255,.06);padding-top:24px;">
        <p>© 2025 Magar · Corrección y edición profesional</p>
        <a href="blog.html" style="color:rgba(255,255,255,.5);font-size:13px;">← Volver al blog</a>
      </div>
    </div>
  </footer>

  <script src="magar.js"></script>
</body>
</html>'''

    fname = f'articulo-{art_num}.html'
    with open(fname, 'w') as f:
        f.write(html)
    print(f'  articulo-{art_num}: {title[:55]}')

print(f'\nDone. {len(pending)} articulos generados (161-{160+len(pending)}).')
