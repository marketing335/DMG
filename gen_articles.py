import xml.etree.ElementTree as ET
import re
from datetime import datetime
from math import ceil
import os

NS = {
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'wp': 'http://wordpress.org/export/1.2/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/'
}

UNSPLASH = [
    '1455390582262-044cdead277a',
    '1471107340929-a87cd0f5b5f3',
    '1481627834876-b7833e8f5570',
    '1512820790803-83ca734da794',
    '1499750310107-5fef28a66643',
    '1456513080510-7bf3a84b82f8',
]

MONTHS_ES = {1:'ene',2:'feb',3:'mar',4:'abr',5:'may',6:'jun',
             7:'jul',8:'ago',9:'sep',10:'oct',11:'nov',12:'dic'}

def format_date(dt):
    return f"{dt.day} {MONTHS_ES[dt.month]} {dt.year}"

def reading_time(text):
    words = len(re.findall(r'\w+', text))
    return max(1, ceil(words / 200))

def clean_content(raw):
    if not raw:
        return ''
    # Remove block comments
    text = re.sub(r'<!--\s*/?\s*wp:[^>]*-->', '', raw)
    # Remove Kadence/UAGB wrapper divs but keep inner content
    # Remove uagb-columns wrappers completely (they hold sidebar CTAs)
    text = re.sub(r'<section[^>]*uagb[^>]*>.*?</section>', '', text, flags=re.DOTALL)
    # Remove wp-block-kadence-infobox blocks
    text = re.sub(r'<div[^>]*kt-info-box[^>]*>.*?</div>\s*</div>', '', text, flags=re.DOTALL)
    # Remove wp-block-kadence-advancedbtn (standalone buttons outside article)
    # Keep wp-block-buttons (buy buttons) - handle separately
    # Remove wp-block-group wrappers but keep content
    text = re.sub(r'<div[^>]*wp-block-group[^>]*>', '', text)
    text = re.sub(r'<div[^>]*wp-block-group__inner[^>]*>', '', text)
    # Remove wp-block-columns wrappers
    text = re.sub(r'<div[^>]*wp-block-columns[^>]*>', '', text)
    text = re.sub(r'<div[^>]*wp-block-column[^>]*>', '', text)
    # Remove wp-block-uagb-image wrappers
    text = re.sub(r'<div[^>]*wp-block-uagb-image[^>]*>', '', text)
    text = re.sub(r'<figure[^>]*wp-block-uagb-image[^>]*>', '<figure>', text)
    # Style blockquotes
    text = re.sub(
        r'<blockquote[^>]*>',
        '<blockquote style="border-left:3px solid #094588;padding-left:1.2rem;margin:1.5rem 0;font-style:italic;color:#444;">',
        text
    )
    # Remove blockquote class from wp-block-quote
    # Handle Kadence headings - preserve color
    def fix_heading(m):
        tag = m.group(1)
        attrs = m.group(2)
        color_match = re.search(r'color\s*:\s*(#[0-9a-fA-F]+)', attrs)
        align_match = re.search(r'text-align\s*:\s*(\w+)', attrs)
        style_parts = []
        if color_match:
            style_parts.append(f'color:{color_match.group(1)}')
        if align_match:
            style_parts.append(f'text-align:{align_match.group(1)}')
        style_str = ';'.join(style_parts)
        if style_str:
            return f'<{tag} style="{style_str}">'
        return f'<{tag}>'
    text = re.sub(r'<(h[1-6])\s+([^>]*)>', fix_heading, text)
    # Handle images - add onerror and referrerpolicy
    idx = [0]
    def fix_img(m):
        attrs = m.group(1)
        src_match = re.search(r'src=["\']([^"\']+)["\']', attrs)
        if not src_match:
            return m.group(0)
        src = src_match.group(1)
        if 'unsplash' in src or 'gravatar' in src:
            return m.group(0)
        fb = UNSPLASH[idx[0] % len(UNSPLASH)]
        idx[0] += 1
        # Clean attrs - keep src, alt, style, width, height
        alt_match = re.search(r'alt=["\']([^"\']*)["\']', attrs)
        style_match = re.search(r'style=["\']([^"\']*)["\']', attrs)
        alt = alt_match.group(1) if alt_match else ''
        style = style_match.group(1) if style_match else ''
        style_attr = f' style="{style}"' if style else ''
        return (f'<img src="{src}" '
                f'onerror="this.onerror=null;this.src=\'https://images.unsplash.com/photo-{fb}?w=800&h=450&fit=crop&q=80\'" '
                f'referrerpolicy="no-referrer" alt="{alt}"{style_attr} />')
    text = re.sub(r'<img\s+([^>]+)/?>', fix_img, text)
    # Convert wp-block-button links to btn btn-primary
    def fix_button(m):
        href_match = re.search(r'href=["\']([^"\']+)["\']', m.group(0))
        text_match = re.search(r'<a[^>]*>([^<]+)</a>', m.group(0))
        if href_match and text_match:
            href = href_match.group(1)
            btn_text = text_match.group(1).strip()
            return f'<div style="text-align:center;margin:1.5rem 0;"><a href="{href}" target="_blank" rel="noopener" class="btn btn-primary">{btn_text}</a></div>'
        return ''
    text = re.sub(r'<div[^>]*wp-block-button[^>]*>.*?</div>', fix_button, text, flags=re.DOTALL)
    text = re.sub(r'<div[^>]*wp-block-buttons[^>]*>(.*?)</div>', r'\1', text, flags=re.DOTALL)
    # Remove remaining class/id heavy divs that are just wrappers
    text = re.sub(r'<div[^>]*class="[^"]*uagb[^"]*"[^>]*>', '', text)
    text = re.sub(r'<div[^>]*class="[^"]*kt-[^"]*"[^>]*>', '', text)
    text = re.sub(r'<div[^>]*class="[^"]*kadence[^"]*"[^>]*>', '', text)
    # Remove wp-block-spacer
    text = re.sub(r'<div[^>]*wp-block-spacer[^>]*[^/]*/>', '', text)
    text = re.sub(r'<div[^>]*aria-hidden[^>]*/>', '', text)
    # Clean up extra closing divs and empty lines
    text = re.sub(r'</div>\s*</div>\s*</div>', '', text)
    text = re.sub(r'</div>', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()
    return text

def get_category_label(cat_slug):
    mapping = {
        'escribir-bien': 'Escribir bien',
        'realismo-magico': 'Realismo Mágico',
        'recomendaciones-literarias': 'Recomendaciones literarias',
        'imagen': 'Blog',
        'correctores': 'Corrección',
        'concursos': 'Blog',
    }
    return mapping.get(cat_slug.lower(), cat_slug.replace('-', ' ').title())

def get_featured_img_url(item, attachment_map):
    for meta in item.findall('wp:postmeta', NS):
        key = meta.find('wp:meta_key', NS)
        if key is not None and key.text == '_thumbnail_id':
            val = meta.find('wp:meta_value', NS)
            if val is not None and val.text in attachment_map:
                return attachment_map[val.text]
    # Try to find first image in content
    content_el = item.find('content:encoded', NS)
    if content_el is not None and content_el.text:
        m = re.search(r'src=["\']([^"\']*relatosmagar\.com[^"\']+\.(?:jpg|jpeg|png|gif|webp))["\']', 
                      content_el.text, re.IGNORECASE)
        if m:
            return m.group(1)
    return ''

# ---- Parse XML ----
print("Parsing XML...")
tree = ET.parse('esthermagarcorreccindeestiloyortotipografa.WordPress.2026-04-13.xml')
root = tree.getroot()

# Build attachment map: post_id -> url
attachment_map = {}
for item in root.findall('.//item'):
    pt = item.find('wp:post_type', NS)
    if pt is not None and pt.text == 'attachment':
        pid = item.find('wp:post_id', NS)
        link = item.find('link')
        # Get actual file URL from guid or attachment_url meta
        guid = item.find('guid')
        if pid is not None and guid is not None:
            attachment_map[pid.text] = guid.text

# Get all published posts
posts = []
for item in root.findall('.//item'):
    post_type = item.find('wp:post_type', NS)
    status = item.find('wp:status', NS)
    if post_type is not None and post_type.text == 'post' and status is not None and status.text == 'publish':
        title_el = item.find('title')
        pub_date_el = item.find('pubDate')
        content_el = item.find('content:encoded', NS)
        excerpt_el = item.find('excerpt:encoded', NS)
        link_el = item.find('link')
        
        # Get all categories
        cats = []
        for cat_el in item.findall('category'):
            domain = cat_el.get('domain', '')
            if domain == 'category':
                cats.append(cat_el.text or '')
        
        # Get category slugs
        cat_slugs = []
        for cat_el in item.findall('category'):
            domain = cat_el.get('domain', '')
            nicename = cat_el.get('nicename', '')
            if domain == 'category' and nicename:
                cat_slugs.append(nicename)
        
        date_str = pub_date_el.text if pub_date_el is not None else ''
        try:
            dt = datetime.strptime(date_str[:25], '%a, %d %b %Y %H:%M:%S')
        except:
            dt = datetime.min
        
        featured_img = get_featured_img_url(item, attachment_map)
        
        posts.append({
            'title': title_el.text if title_el is not None else '',
            'date': dt,
            'date_fmt': format_date(dt) if dt != datetime.min else '',
            'link': link_el.text if link_el is not None else '',
            'cats': cats,
            'cat_slugs': cat_slugs,
            'content': content_el.text if content_el is not None else '',
            'excerpt': excerpt_el.text if excerpt_el is not None else '',
            'featured_img': featured_img,
        })

posts.sort(key=lambda x: x['date'], reverse=True)
print(f"Total posts: {len(posts)}")

# ---- Build title -> post mapping ----
title_to_post = {}
for p in posts:
    title_to_post[p['title'].lower().strip()] = p

# ---- Read blog.html mapping ----
with open('blog.html', 'r', encoding='utf-8') as f:
    blog_content = f.read()

# Extract all articulo-N -> title mappings from blog.html
blog_map = {}  # articulo_num -> {title, img_src, date, tag, excerpt}
pattern = re.compile(
    r'<article[^>]*>.*?href="articulo-(\d+)\.html"[^>]*>([^<]+)</a>',
    re.DOTALL
)
for m in pattern.finditer(blog_content):
    num = int(m.group(1))
    title = m.group(2).strip()
    blog_map[num] = title

print(f"Blog.html maps {len(blog_map)} articles")

# Also get all articulo numbers in order they appear in blog.html
articulo_order = []
for m in re.finditer(r'href="articulo-(\d+)\.html"', blog_content):
    n = int(m.group(1))
    if n not in articulo_order:
        articulo_order.append(n)

print(f"Articulo order (first 10): {articulo_order[:10]}")


# ---- HTML Template ----
def make_article_html(num, post, prev_num, next_num, related_nums, blog_map):
    title = post['title']
    date_fmt = post['date_fmt']
    content_raw = post['content']
    featured_img = post['featured_img']
    
    # Category label
    cat_label = 'Blog'
    if post['cat_slugs']:
        cat_label = get_category_label(post['cat_slugs'][0])
    elif post['cats']:
        cat_label = post['cats'][0]
    
    # Reading time
    rt = reading_time(content_raw)
    
    # Hero image
    if not featured_img:
        fb_idx = num % len(UNSPLASH)
        hero_src = f'https://images.unsplash.com/photo-{UNSPLASH[fb_idx]}?w=800&h=450&fit=crop&q=80'
        hero_img = f'<img src="{hero_src}" alt="{title}" />'
    else:
        fb_idx = num % len(UNSPLASH)
        fb = UNSPLASH[fb_idx]
        hero_img = (f'<img src="{featured_img}" '
                   f'onerror="this.onerror=null;this.src=\'https://images.unsplash.com/photo-{fb}?w=800&h=450&fit=crop&q=80\'" '
                   f'referrerpolicy="no-referrer" alt="{title}" />')
    
    # Clean content
    body_html = clean_content(content_raw)
    
    # Breadcrumb short title
    short_title = title[:50] + ('…' if len(title) > 50 else '')
    
    # Navigation
    prev_link = f'<a href="articulo-{prev_num}.html" class="btn btn-ghost btn-sm">← Anterior</a>' if prev_num else ''
    next_link = f'<a href="articulo-{next_num}.html" class="btn btn-ghost btn-sm">Siguiente →</a>' if next_num else ''
    nav_html = f'<div style="display:flex;gap:12px;margin-top:40px;flex-wrap:wrap;">{prev_link}{next_link}</div>'
    
    # Related articles
    related_html = ''
    for rn in related_nums[:3]:
        rtitle = blog_map.get(rn, f'Artículo {rn}')
        related_html += f'<li><a href="articulo-{rn}.html">{rtitle}</a></li>\n'
    
    # Meta description
    excerpt = post.get('excerpt', '') or ''
    excerpt_clean = re.sub(r'<[^>]+>', '', excerpt).strip()[:160]
    if not excerpt_clean:
        excerpt_clean = re.sub(r'<[^>]+>', '', content_raw).strip()[:160]
    
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | Magar</title>
  <meta name="description" content="{excerpt_clean}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,900;1,400;1,600&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="magar.css" />
  <link rel="stylesheet" href="articulo.css" />
</head>
<body>

  <header class="navbar" id="navbar">
    <div class="nav-inner">
      <a href="relatosmagar.html" class="nav-logo">
        <img src="https://i.ibb.co/xtBTCFC4/LA-BOMBA-ESPA-OLA-2.png" alt="Magar" class="nav-logo-img" />
      </a>
      <nav class="nav-links" id="navLinks">
        <a href="relatosmagar.html">Servicios</a>
        <a href="relatosmagar.html">Cómo funciona</a>
        <a href="relatosmagar.html">Cursos</a>
        <a href="relatosmagar.html">Opiniones</a>
        <a href="relatosmagar.html">Novelas</a>
        <a href="blog.html">Blog</a>
        <a href="suscripcion.html">Newsletter</a>
        <a href="contacto.html" class="nav-cta">Solicitar presupuesto</a>
      </nav>
      <button class="hamburger" id="hamburger" aria-label="Menú"><span></span><span></span><span></span></button>
    </div>
  </header>

  <main class="article-main">
    <div class="article-container">

      <nav class="breadcrumb">
        <a href="relatosmagar.html">Inicio</a>
        <span>›</span>
        <a href="blog.html">Blog</a>
        <span>›</span>
        <span>{short_title}</span>
      </nav>

      <header class="article-header">
        <div class="article-tag">{cat_label}</div>
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
        {hero_img}
      </figure>

      <div class="article-layout">
        <article class="article-body">

          {body_html}

          {nav_html}

          <div class="article-cta-box" style="margin-top:40px;">
            <p>¿Tu texto necesita una revisión profesional?</p>
            <a href="contacto.html" class="btn btn-primary">Solicitar corrección gratuita</a>
          </div>
        </article>

        <aside class="article-sidebar">
          <div class="sidebar-widget">
            <h4>Sobre la autora</h4>
            <img src="https://i.ibb.co/zH7DxvJS/dame-esta-mujercon-202603241403.jpg" alt="Esther Magar" class="sidebar-avatar" />
            <p><strong>Esther Magar</strong> es correctora y editora de textos con más de diez años de experiencia.</p>
            <a href="sobre-mi.html" class="sidebar-link">Conocer más →</a>
          </div>
          <div class="sidebar-widget">
            <h4>Artículos relacionados</h4>
            <ul class="sidebar-related">
              {related_html}
            </ul>
          </div>
          <div class="sidebar-widget" style="display:grid;grid-template-columns:1fr 1fr;gap:10px;background:none;box-shadow:none;padding:0;">
            <div style="background:#fff;border-radius:12px;padding:16px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.08);">
              <div style="width:46px;height:46px;background:#094588;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 10px;">
                <svg width="22" height="22" fill="#fff" viewBox="0 0 8 8"><path d="M6 0l-1 1 2 2 1-1-2-2zm-2 2l-4 4v2h2l4-4-2-2z"/></svg>
              </div>
              <h4 style="font-size:.82rem;margin-bottom:6px;">¿Buscas corrector de textos?</h4>
              <p style="font-size:.78rem;color:#666;margin-bottom:10px;">Pídeme presupuesto sin compromiso, te responderé lo antes posible.</p>
              <a href="contacto.html" class="btn btn-primary btn-sm" style="width:100%;">Quiero presupuesto</a>
            </div>
            <div style="background:#fff;border-radius:12px;padding:16px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.08);">
              <div style="width:46px;height:46px;background:#094588;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 10px;">
                <svg width="22" height="22" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
              </div>
              <h4 style="font-size:.82rem;margin-bottom:6px;">¿Te parece interesante?</h4>
              <p style="font-size:.78rem;color:#666;margin-bottom:10px;">Para no perderte ningún artículo y acceder a contenido exclusivo, suscríbete a mi lista.</p>
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
        </aside>
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
    return html


# ---- Match blog.html articles to XML posts ----
def find_post(title_query, title_to_post):
    """Find post by title, trying exact then fuzzy match"""
    q = title_query.lower().strip()
    # Exact
    if q in title_to_post:
        return title_to_post[q]
    # Remove punctuation and try again
    q_clean = re.sub(r'[¿?¡!:,«»"\'…]', '', q).strip()
    for k, v in title_to_post.items():
        k_clean = re.sub(r'[¿?¡!:,«»"\'…]', '', k).strip()
        if q_clean == k_clean:
            return v
    # Partial match - title starts with query
    for k, v in title_to_post.items():
        if k.startswith(q[:30]):
            return v
    # Word overlap
    q_words = set(q_clean.split())
    best_score = 0
    best_post = None
    for k, v in title_to_post.items():
        k_words = set(re.sub(r'[¿?¡!:,«»"\'…]', '', k).split())
        overlap = len(q_words & k_words)
        if overlap > best_score and overlap >= min(3, len(q_words)):
            best_score = overlap
            best_post = v
    return best_post

# Build articulo_num -> post mapping
SKIP = {14, 15, 16}  # already have real content

articulo_to_post = {}
matched = []
unmatched = []

for num, title in blog_map.items():
    post = find_post(title, title_to_post)
    if post:
        articulo_to_post[num] = post
        matched.append((num, title, post['title']))
    else:
        unmatched.append((num, title))

print(f"\nMatched: {len(matched)}, Unmatched: {len(unmatched)}")
if unmatched:
    print("Unmatched:")
    for num, title in unmatched[:10]:
        print(f"  articulo-{num}: {title}")

# For unmatched, use posts by order (the posts not yet assigned)
used_posts = set(id(p) for p in articulo_to_post.values())
unused_posts = [p for p in posts if id(p) not in used_posts]

# Assign unmatched articulos to unused posts in order
for i, (num, title) in enumerate(unmatched):
    if i < len(unused_posts):
        articulo_to_post[num] = unused_posts[i]

# ---- Generate existing articulos (7-87 in blog.html) ----
generated = []
skipped = []

for num in sorted(blog_map.keys()):
    if num in SKIP:
        skipped.append(num)
        continue
    if num not in articulo_to_post:
        continue
    
    post = articulo_to_post[num]
    
    # Find prev/next in articulo_order
    try:
        idx = articulo_order.index(num)
        prev_num = articulo_order[idx + 1] if idx + 1 < len(articulo_order) else None
        next_num = articulo_order[idx - 1] if idx > 0 else None
    except ValueError:
        prev_num = None
        next_num = None
    
    # Related: nearby articles
    try:
        idx = articulo_order.index(num)
        candidates = articulo_order[max(0,idx-2):idx] + articulo_order[idx+1:idx+3]
        related_nums = [n for n in candidates if n != num][:3]
    except ValueError:
        related_nums = []
    
    html = make_article_html(num, post, prev_num, next_num, related_nums, blog_map)
    
    filepath = f'articulo-{num}.html'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    generated.append(num)

print(f"\nGenerated {len(generated)} articles: {sorted(generated)[:10]}...")
print(f"Skipped (already have real content): {skipped}")


# ---- Generate new articles 88-160 ----
print("\nGenerating articles 88-160...")

# Find posts not yet used in blog.html
used_post_titles = set(p['title'].lower() for p in articulo_to_post.values())
remaining_posts = [p for p in posts if p['title'].lower() not in used_post_titles]
print(f"Remaining posts available: {len(remaining_posts)}")

# Unsplash fallback for blog cards
UNSPLASH_CARD = [
    '1481627834876-b7833e8f5570',
    '1455390582262-044cdead277a',
    '1471107340929-a87cd0f5b5f3',
    '1512820790803-83ca734da794',
    '1499750310107-5fef28a66643',
    '1456513080510-7bf3a84b82f8',
]

# Blog card template
def make_blog_card(num, post, fallback_idx):
    title = post['title']
    date_fmt = post['date_fmt']
    featured = post['featured_img']
    fb = UNSPLASH_CARD[fallback_idx % len(UNSPLASH_CARD)]
    
    cat_label = 'Blog'
    if post['cat_slugs']:
        cat_label = get_category_label(post['cat_slugs'][0])
    elif post['cats']:
        cat_label = post['cats'][0]
    
    rt = reading_time(post['content'])
    
    excerpt = post.get('excerpt', '') or ''
    excerpt_clean = re.sub(r'<[^>]+>', '', excerpt).strip()[:120]
    if not excerpt_clean:
        text = re.sub(r'<[^>]+>', '', post['content']).strip()
        excerpt_clean = text[:120] + ('…' if len(text) > 120 else '')
    
    if featured:
        img_html = (f'<img src="{featured}" '
                   f'onerror="this.onerror=null;this.src=\'https://images.unsplash.com/photo-{fb}?w=600&h=380&fit=crop&q=80\'" '
                   f'referrerpolicy="no-referrer" alt="{title}" />')
    else:
        img_html = f'<img src="https://images.unsplash.com/photo-{fb}?w=600&h=380&fit=crop&q=80" alt="{title}" />'
    
    return f'''        <article class="bp-card">
          {img_html}
          <div class="bp-card-body">
            <div class="blog-tag">{cat_label}</div>
            <h3><a href="articulo-{num}.html">{title}</a></h3>
            <p>{excerpt_clean}</p>
            <div class="bp-meta"><span>{date_fmt}</span><span>·</span><span>{rt} min</span></div>
          </div>
        </article>'''

new_cards = []
new_articulo_order = list(articulo_order)

for i, post in enumerate(remaining_posts[:73]):  # 73 to reach 160
    num = 88 + i
    
    # Prev/next
    prev_num = num + 1 if i + 1 < len(remaining_posts[:73]) else None
    next_num = num - 1 if num > 88 else articulo_order[-1] if articulo_order else None
    
    # Related
    related_nums = []
    if num > 88: related_nums.append(num - 1)
    if num > 89: related_nums.append(num - 2)
    if prev_num: related_nums.append(prev_num)
    
    # Update blog_map for related titles
    blog_map[num] = post['title']
    
    html = make_article_html(num, post, prev_num, next_num, related_nums, blog_map)
    filepath = f'articulo-{num}.html'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    card = make_blog_card(num, post, i)
    new_cards.append(card)
    new_articulo_order.append(num)

print(f"Generated articles 88-{87+len(new_cards)}")

# ---- Update blog.html ----
print("\nUpdating blog.html...")

with open('blog.html', 'r', encoding='utf-8') as f:
    blog_html = f.read()

# Find the end of the last article card and insert new ones before closing grid
cards_html = '\n'.join(new_cards)

# Find closing tag of the blog grid
insert_marker = '</div>\n      </section>'
if insert_marker not in blog_html:
    # Try alternative
    insert_marker = '      </div>\n    </section>'

if insert_marker in blog_html:
    # Insert before the last closing div of the grid
    new_blog = blog_html.replace(insert_marker, f'\n{cards_html}\n{insert_marker}', 1)
    with open('blog.html', 'w', encoding='utf-8') as f:
        f.write(new_blog)
    print(f"blog.html updated with {len(new_cards)} new cards")
else:
    print("Could not find insert marker in blog.html - trying alternative...")
    # Just append before </main>
    new_blog = blog_html.replace('</main>', f'\n<!-- NEW CARDS -->\n{cards_html}\n</main>', 1)
    with open('blog.html', 'w', encoding='utf-8') as f:
        f.write(new_blog)
    print("Inserted before </main>")

print("\nDone!")
