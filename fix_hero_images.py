#!/usr/bin/env python3
"""Corrige las imágenes de portada (hero) de los 10 artículos más recientes
usando la imagen destacada real del XML de WordPress (_thumbnail_id)."""

import xml.etree.ElementTree as ET
import re

NS = {
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'wp': 'http://wordpress.org/export/1.2/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
}

tree = ET.parse('esthermagarcorreccindeestiloyortotipografa.WordPress.2026-04-13.xml')
root = tree.getroot()
channel = root.find('channel')

# Mapa attachment_id -> URL
attachments = {}
for item in channel.findall('item'):
    ptype = item.findtext('wp:post_type', namespaces=NS)
    if ptype == 'attachment':
        post_id = item.findtext('wp:post_id', namespaces=NS, default='')
        att_url = item.findtext('wp:attachment_url', namespaces=NS, default='')
        if post_id and att_url:
            attachments[post_id] = att_url

UNSPLASH = [
    '1455390582262-044cdead277a',
    '1471107340929-a87cd0f5b5f3',
    '1481627834876-b7833e8f5570',
    '1512820790803-83ca734da794',
    '1499750310107-5fef28a66643',
    '1456513080510-7bf3a84b82f8',
]

TOP10_ORDER = [14, 8, 9, 10, 11, 12, 13, 15, 16, 7]

# Obtener top 10 posts con sus imágenes destacadas
posts = []
for item in channel.findall('item'):
    status = item.findtext('wp:status', namespaces=NS)
    ptype = item.findtext('wp:post_type', namespaces=NS)
    if status != 'publish' or ptype != 'post':
        continue
    title = item.findtext('title', '').strip()
    date = item.findtext('wp:post_date', namespaces=NS, default='')

    thumb_id = None
    for pm in item.findall('wp:postmeta', NS):
        key = pm.findtext('wp:meta_key', namespaces=NS)
        if key == '_thumbnail_id':
            thumb_id = pm.findtext('wp:meta_value', namespaces=NS)
            break

    thumb_url = attachments.get(thumb_id, '') if thumb_id else ''
    posts.append((date, title, thumb_url))

posts.sort(key=lambda x: x[0], reverse=True)

# Aplicar imagen correcta a cada artículo
for i, (date, title, thumb_url) in enumerate(posts[:10]):
    art_num = TOP10_ORDER[i]
    fname = f'articulo-{art_num}.html'

    with open(fname, 'r') as f:
        html = f.read()

    if not thumb_url:
        print(f"  WARNING articulo-{art_num}: no featured image in XML")
        continue

    uns = UNSPLASH[art_num % len(UNSPLASH)]
    fallback = f"https://images.unsplash.com/photo-{uns}?w=800&h=450&fit=crop&q=80"

    # Reemplazar src de la imagen hero
    new_hero = f'<figure class="article-hero-img">\n        <img src="{thumb_url}" onerror="this.onerror=null;this.src=\'{fallback}\'" referrerpolicy="no-referrer" alt="{title}" />\n      </figure>'

    html = re.sub(
        r'<figure class="article-hero-img">.*?</figure>',
        new_hero,
        html,
        count=1,
        flags=re.DOTALL
    )

    with open(fname, 'w') as f:
        f.write(html)

    print(f"  articulo-{art_num}: {thumb_url.split('/')[-1]}")

print("\nDone.")
