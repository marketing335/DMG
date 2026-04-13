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

def clean_text(t):
    if not t: return ''
    t = unescape(t)
    t = re.sub(r'\[&#8230;\]|\[…\]', '…', t)
    t = re.sub(r'&#\d+;', lambda m: unescape(m.group(0)), t)
    return t.strip()

def render_comment(c, is_reply=False):
    author = clean_text(c.get('author', 'Anónimo'))
    author = re.sub(r'<[^>]+>', '', author)
    date_fmt = format_comment_date(c.get('date', ''))
    content = clean_text(c.get('content', ''))
    if not content.strip().startswith('<'):
        content = f'<p>{content}</p>'
    avatar_letter = author[0].upper() if author else '?'
    reply_class = ' is-reply' if is_reply else ''
    return f'''      <li class="comment-item{reply_class}">
        <div class="comment-avatar">{avatar_letter}</div>
        <div class="comment-body">
          <div class="comment-meta">
            <span class="comment-author">{author}</span>
            <span class="comment-date">{date_fmt}</span>
          </div>
          <div class="comment-content">{content}</div>
        </div>
      </li>\n'''

def make_comments_html(comments, post_slug):
    # Filter approved non-pingback comments
    clean = [c for c in comments 
             if c.get('approved') == '1' and c.get('type') not in ('pingback','trackback')]
    
    if not clean:
        form_only = True
    else:
        form_only = False
    
    if not form_only:
        # Sort by date ascending
        def parse_dt(c):
            try: return datetime.strptime(c.get('date','')[:19], '%Y-%m-%d %H:%M:%S')
            except: return datetime.min
        clean.sort(key=parse_dt)
        
        # Build id -> comment map and parent -> children map
        by_id = {c['id']: c for c in clean}
        children = {}  # parent_id -> [child comments]
        top_level = []
        for c in clean:
            pid = c.get('parent', '0')
            if pid == '0' or pid not in by_id:
                top_level.append(c)
            else:
                children.setdefault(pid, []).append(c)
        
        # Render threaded
        items = ''
        for c in top_level:
            items += render_comment(c, is_reply=False)
            # Add replies indented
            cid = c['id']
            for reply in children.get(cid, []):
                items += render_comment(reply, is_reply=True)
                # Support one more level
                rid = reply['id']
                for subreply in children.get(rid, []):
                    items += render_comment(subreply, is_reply=True)
        
        count = len(clean)
        plural = 'comentario' if count == 1 else 'comentarios'
        comments_list = f'''    <h2 class="comments-title">{count} {plural}</h2>
    <ul class="comment-list">
{items}    </ul>\n'''
    else:
        comments_list = '<h2 class="comments-title">Deja un comentario</h2>\n'
    
    form_html = f'''    <div class="comment-form-section">
      {'<h3 class="comment-form-title">Deja un comentario</h3>' if not form_only else ''}
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
    </div>'''
    
    return f'''
  <section class="comments-section">
{comments_list}
{form_html}
  </section>'''

# Parse XML
print("Parsing XML for comments...")
tree = ET.parse('esthermagarcorreccindeestiloyortotipografa.WordPress.2026-04-13.xml')
root = tree.getroot()

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
    link = link_el.text if link_el is not None else ''
    slug = link.rstrip('/').split('/')[-1] if link else title[:40]
    
    comments = []
    for c in item.findall('wp:comment', NS):
        approved = c.find('wp:comment_approved', NS)
        ctype = c.find('wp:comment_type', NS)
        author = c.find('wp:comment_author', NS)
        date = c.find('wp:comment_date', NS)
        content = c.find('wp:comment_content', NS)
        cid_el = c.find('wp:comment_id', NS)
        parent_el = c.find('wp:comment_parent', NS)
        comments.append({
            'id': cid_el.text if cid_el is not None else '0',
            'approved': approved.text if approved is not None else '0',
            'type': ctype.text if ctype is not None else 'comment',
            'author': author.text if author is not None else 'Anónimo',
            'date': date.text if date is not None else '',
            'content': content.text if content is not None else '',
            'parent': parent_el.text if parent_el is not None else '0',
        })
    
    title_to_comments[title.lower().strip()] = comments
    title_to_slug[title.lower().strip()] = slug

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
    best_score, best_key = 0, None
    for k in title_to_comments:
        k_words = set(re.sub(r'[¿?¡!:,«»"\'…]', '', k).split())
        overlap = len(q_words & k_words)
        if overlap > best_score and overlap >= min(3, len(q_words)):
            best_score = overlap; best_key = k
    if best_key:
        return title_to_comments[best_key], title_to_slug.get(best_key, '')
    return [], ''

with open('blog.html', 'r', encoding='utf-8') as f:
    blog_content = f.read()

blog_map = {}
for m in re.finditer(r'href="articulo-(\d+)\.html"[^>]*>([^<]+)</a>', blog_content):
    num = int(m.group(1))
    if num not in blog_map:
        blog_map[num] = m.group(2).strip()

updated = 0
for num, title in sorted(blog_map.items()):
    filepath = f'articulo-{num}.html'
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    comments, slug = find_comments(title)
    comments_html = make_comments_html(comments, slug)
    # Remove existing comments section
    html = re.sub(r'\s*<section class="comments-section">.*?</section>', '', html, flags=re.DOTALL)
    # Also remove extra article-container div we added before
    html = re.sub(r'\s*<div class="article-container">\s*\n\s*<section class="comments-section">', 
                  '\n    <div class="article-container">\n  <section class="comments-section">', html, flags=re.DOTALL)
    if '</main>' in html:
        html = html.replace('</main>', f'\n    <div class="article-container">{comments_html}\n    </div>\n  </main>', 1)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        updated += 1

print(f"Updated {updated} articles")
