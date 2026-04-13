import xml.etree.ElementTree as ET
import re
from datetime import datetime
from html import unescape
import os

NS = {
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'wp': 'http://wordpress.org/export/1.2/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/'
}

MONTHS_ES = {1:'ene',2:'feb',3:'mar',4:'abr',5:'may',6:'jun',
             7:'jul',8:'ago',9:'sep',10:'oct',11:'nov',12:'dic'}

def format_comment_date(date_str):
    try:
        dt = datetime.strptime(date_str[:19], '%Y-%m-%d %H:%M:%S')
        return f"{dt.day} {MONTHS_ES[dt.month]} {dt.year}"
    except:
        return date_str[:10]

def make_comments_html(comments, post_slug):
    """Generate comments section HTML"""
    
    # Filter approved comments (not spam, not pingbacks)
    clean = []
    for c in comments:
        approved = c.get('approved', '0')
        ctype = c.get('type', 'comment')
        if approved == '1' and ctype not in ('pingback', 'trackback'):
            clean.append(c)
    
    # Comments list
    comments_html = ''
    if clean:
        items = ''
        for c in clean:
            author = c.get('author', 'Anónimo')
            # Strip HTML entities
            author = unescape(re.sub(r'<[^>]+>', '', author))
            date_fmt = format_comment_date(c.get('date', ''))
            content = c.get('content', '')
            content = unescape(content).strip()
            # Clean content
            content = re.sub(r'\[&#8230;\]', '…', content)
            content = re.sub(r'&#8217;', "'", content)
            content = re.sub(r'&#8220;|&#8221;', '"', content)
            content = re.sub(r'&#8211;', '–', content)
            content = re.sub(r'&#8212;', '—', content)
            # Wrap plain text in <p>
            if not content.startswith('<'):
                content = f'<p>{content}</p>'
            # Avatar letter
            avatar_letter = author[0].upper() if author else '?'
            items += f'''      <li class="comment-item">
        <div class="comment-avatar">{avatar_letter}</div>
        <div class="comment-body">
          <div class="comment-meta">
            <span class="comment-author">{author}</span>
            <span class="comment-date">{date_fmt}</span>
          </div>
          <div class="comment-content">{content}</div>
        </div>
      </li>\n'''
        
        count = len(clean)
        plural = 'comentario' if count == 1 else 'comentarios'
        comments_html = f'''
  <section class="comments-section">
    <h2 class="comments-title">{count} {plural}</h2>
    <ul class="comment-list">
{items}    </ul>

    <div class="comment-form-section">
      <h3 class="comment-form-title">Deja un comentario</h3>
      <form class="comment-form" action="https://formspree.io/f/contacto" method="POST">
        <input type="hidden" name="_subject" value="Comentario en: {post_slug}" />
        <div class="comment-form-row">
          <div class="comment-field">
            <label for="comment-name">Nombre *</label>
            <input type="text" id="comment-name" name="nombre" required />
          </div>
          <div class="comment-field">
            <label for="comment-email">Correo electrónico *</label>
            <input type="email" id="comment-email" name="email" required />
          </div>
        </div>
        <div class="comment-field">
          <label for="comment-text">Comentario *</label>
          <textarea id="comment-text" name="comentario" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary comment-submit">Publicar comentario</button>
      </form>
    </div>
  </section>'''
    else:
        comments_html = f'''
  <section class="comments-section">
    <h2 class="comments-title">Deja un comentario</h2>
    <div class="comment-form-section">
      <form class="comment-form" action="https://formspree.io/f/contacto" method="POST">
        <input type="hidden" name="_subject" value="Comentario en: {post_slug}" />
        <div class="comment-form-row">
          <div class="comment-field">
            <label for="comment-name">Nombre *</label>
            <input type="text" id="comment-name" name="nombre" required />
          </div>
          <div class="comment-field">
            <label for="comment-email">Correo electrónico *</label>
            <input type="email" id="comment-email" name="email" required />
          </div>
        </div>
        <div class="comment-field">
          <label for="comment-text">Comentario *</label>
          <textarea id="comment-text" name="comentario" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary comment-submit">Publicar comentario</button>
      </form>
    </div>
  </section>'''
    
    return comments_html

# Parse XML
print("Parsing XML for comments...")
tree = ET.parse('esthermagarcorreccindeestiloyortotipografa.WordPress.2026-04-13.xml')
root = tree.getroot()

# Build title -> comments map
title_to_comments = {}
title_to_slug = {}

for item in root.findall('.//item'):
    pt = item.find('wp:post_type', NS)
    status = item.find('wp:status', NS)
    if pt is None or pt.text != 'post': continue
    if status is None or status.text != 'publish': continue
    
    title_el = item.find('title')
    link_el = item.find('link')
    if title_el is None: continue
    title = title_el.text or ''
    
    # Extract slug from link
    link = link_el.text if link_el is not None else ''
    slug = link.rstrip('/').split('/')[-1] if link else title[:40]
    
    comments = []
    for c in item.findall('wp:comment', NS):
        approved = c.find('wp:comment_approved', NS)
        ctype = c.find('wp:comment_type', NS)
        author = c.find('wp:comment_author', NS)
        date = c.find('wp:comment_date', NS)
        content = c.find('wp:comment_content', NS)
        comments.append({
            'approved': approved.text if approved is not None else '0',
            'type': ctype.text if ctype is not None else 'comment',
            'author': author.text if author is not None else 'Anónimo',
            'date': date.text if date is not None else '',
            'content': content.text if content is not None else ''
        })
    
    title_to_comments[title.lower().strip()] = comments
    title_to_slug[title.lower().strip()] = slug

print(f"Loaded comments for {len(title_to_comments)} posts")

# Read blog.html to get articulo-N -> title mapping
with open('blog.html', 'r', encoding='utf-8') as f:
    blog_content = f.read()

pattern = re.compile(r'href="articulo-(\d+)\.html"[^>]*>([^<]+)</a>', re.DOTALL)
blog_map = {}
for m in pattern.finditer(blog_content):
    num = int(m.group(1))
    title = m.group(2).strip()
    if num not in blog_map:
        blog_map[num] = title

def find_comments(title_query):
    q = title_query.lower().strip()
    if q in title_to_comments:
        return title_to_comments[q], title_to_slug.get(q, '')
    q_clean = re.sub(r'[¿?¡!:,«»"\'…]', '', q).strip()
    for k, v in title_to_comments.items():
        k_clean = re.sub(r'[¿?¡!:,«»"\'…]', '', k).strip()
        if q_clean == k_clean:
            return v, title_to_slug.get(k, '')
    q_words = set(q_clean.split())
    best_score = 0
    best_key = None
    for k in title_to_comments:
        k_words = set(re.sub(r'[¿?¡!:,«»"\'…]', '', k).split())
        overlap = len(q_words & k_words)
        if overlap > best_score and overlap >= min(3, len(q_words)):
            best_score = overlap
            best_key = k
    if best_key:
        return title_to_comments[best_key], title_to_slug.get(best_key, '')
    return [], ''

# Update each article HTML to add comments section
SKIP = set()  # Don't skip any - add comments to all
updated = 0
skipped = 0

for num, title in sorted(blog_map.items()):
    filepath = f'articulo-{num}.html'
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Get comments for this post
    comments, slug = find_comments(title)
    comments_html = make_comments_html(comments, slug)
    
    # Remove any existing comments section first
    html = re.sub(r'\s*<section class="comments-section">.*?</section>', '', html, flags=re.DOTALL)
    
    # Insert comments before </main>
    if '</main>' in html:
        html = html.replace('</main>', f'\n    <div class="article-container">{comments_html}\n    </div>\n  </main>', 1)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        updated += 1
    else:
        skipped += 1

print(f"Updated {updated} articles with comments, skipped {skipped}")
