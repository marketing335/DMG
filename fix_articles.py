#!/usr/bin/env python3
"""Fix WordPress markup issues in all article HTML files."""
import os
import re
import glob

def fix_article(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    # 1. Bump CSS version v=3 -> v=4
    html = html.replace('magar.css?v=3', 'magar.css?v=4')
    html = html.replace('articulo.css?v=3', 'articulo.css?v=4')

    # 2. Inside <article class="article-body">, convert h1 -> h2
    #    (the real page title h1 is inside <header class="article-header">, not here)
    def downgrade_h1(m):
        body = m.group(0)
        # Replace opening <h1 ...> with <h2 ...>
        body = re.sub(r'<h1(\s[^>]*)?>', lambda x: '<h2' + (x.group(1) or '') + '>', body)
        # Replace closing </h1> with </h2>
        body = body.replace('</h1>', '</h2>')
        return body

    html = re.sub(
        r'<article class="article-body">.*?</article>',
        downgrade_h1,
        html,
        flags=re.DOTALL
    )

    # 3. Remove inline color styles from h2/h3/h4 opening tags (CSS will handle color)
    #    But keep other styles like text-align
    def clean_heading_style(m):
        tag = m.group(1)   # e.g. 'h2' or 'h3'
        attrs = m.group(2)  # everything inside the tag after tag name
        if not attrs:
            return f'<{tag}>'
        # Remove color from style attribute, keep text-align etc.
        def remove_color_from_style(sm):
            style = sm.group(1)
            # Remove color:... declarations
            style = re.sub(r'color\s*:\s*[^;"}]+;?\s*', '', style)
            style = style.strip().rstrip(';').strip()
            if style:
                return f' style="{style}"'
            return ''
        attrs = re.sub(r'\s*style="([^"]*)"', remove_color_from_style, attrs)
        return f'<{tag}{attrs}>'

    html = re.sub(
        r'<(h2|h3|h4)(\s[^>]*)?>',
        clean_heading_style,
        html
    )

    # 4. Remove empty <p></p> and <p> </p> (only plain whitespace/nbsp)
    html = re.sub(r'<p[^>]*>\s*(&nbsp;)?\s*</p>\n?', '', html)

    # 5. Remove inline style from blockquotes that already have our style
    #    (they have style="border-left:3px solid #094588;..." which is fine, keep them)
    #    Actually keep blockquote styles as-is, they're correct.

    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False

files = sorted(glob.glob('/home/user/DMG/articulo-*.html'))
changed = 0
for path in files:
    if fix_article(path):
        changed += 1
        print(f'Fixed: {os.path.basename(path)}')

print(f'\nDone. {changed}/{len(files)} files updated.')
