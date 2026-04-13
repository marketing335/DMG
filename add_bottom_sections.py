#!/usr/bin/env python3
"""Add full-width CTA + Books sections to ALL 154 articles.
Inserts between the article-layout container and the comments container."""

import re

CTA_BOOKS_HTML = '''    <!-- CTAs + Books (full-width, below article) -->
    <div class="article-container" style="padding-top:0;padding-bottom:0;">
      <div style="display:flex;flex-wrap:wrap;gap:24px;margin:40px 0 24px;">
        <div style="flex:1;min-width:260px;background:#fff;border-radius:14px;padding:32px 24px;text-align:center;box-shadow:0 2px 16px rgba(0,0,0,.08);border:1px solid #e8e4df;">
          <div style="width:52px;height:52px;background:#094588;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 16px;">
            <svg width="24" height="24" fill="#fff" viewBox="0 0 8 8"><path d="M6 0l-1 1 2 2 1-1-2-2zm-2 2l-4 4v2h2l4-4-2-2z"/></svg>
          </div>
          <h3 style="font-family:\'Playfair Display\',serif;font-size:1.2rem;color:#0a1628;margin-bottom:10px;">¿Buscas corrector de textos?</h3>
          <p style="font-size:.9rem;color:#666;line-height:1.6;margin-bottom:20px;">Pídeme presupuesto sin compromiso, te responderé lo antes posible.</p>
          <a href="contacto.html" class="btn btn-primary">Quiero presupuesto</a>
        </div>
        <div style="flex:1;min-width:260px;background:#fff;border-radius:14px;padding:32px 24px;text-align:center;box-shadow:0 2px 16px rgba(0,0,0,.08);border:1px solid #e8e4df;">
          <div style="width:52px;height:52px;background:#094588;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 16px;">
            <svg width="24" height="24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
          </div>
          <h3 style="font-family:\'Playfair Display\',serif;font-size:1.2rem;color:#0a1628;margin-bottom:10px;">¿Te parece interesante?</h3>
          <p style="font-size:.9rem;color:#666;line-height:1.6;margin-bottom:20px;">Para no perderte ningún artículo y acceder a contenido exclusivo, suscríbete a mi lista.</p>
          <a href="suscripcion.html" class="btn btn-primary">Me suscribo</a>
        </div>
      </div>
      <div style="background:#0a1628;border-radius:16px;padding:40px 32px;margin-bottom:48px;text-align:center;">
        <p style="font-size:.72rem;text-transform:uppercase;letter-spacing:.15em;color:#c9a84c;font-weight:700;margin-bottom:20px;">Conoce mi universo literario</p>
        <div style="display:flex;justify-content:center;gap:24px;margin-bottom:20px;">
          <img src="https://m.media-amazon.com/images/P/B093Z7T8HV.01._SCLZZZZZZZ_SX500_.jpg" alt="Las semillas del rencor" style="width:110px;border-radius:6px;box-shadow:0 4px 20px rgba(0,0,0,.5);" />
          <img src="https://m.media-amazon.com/images/P/B0GQ3JZ7M1.01._SCLZZZZZZZ_SX500_.jpg" alt="Lo que mamá calla" style="width:110px;border-radius:6px;box-shadow:0 4px 20px rgba(0,0,0,.5);" />
        </div>
        <p style="font-size:.95rem;color:rgba(255,255,255,.8);line-height:1.7;max-width:520px;margin:0 auto 28px;font-style:italic;">Lugares opresivos, personajes crudos y el lirismo de los cuentos clásicos.</p>
        <div style="display:flex;justify-content:center;gap:14px;flex-wrap:wrap;">
          <a href="https://amzn.to/3Yrt4oo" target="_blank" rel="noopener" class="btn btn-primary">Las semillas del rencor</a>
          <a href="http://amzn.to/4aRt4TY" target="_blank" rel="noopener" class="btn btn-primary">Lo que mamá calla</a>
        </div>
      </div>
    </div>
'''

def make_comments_html(slug):
    return f'''    <div class="article-container">
  <section class="comments-section">
<h2 class="comments-title">Deja un comentario</h2>

    <div class="comment-form-section">
      <form class="comment-form" action="https://formspree.io/f/contacto" method="POST">
        <input type="hidden" name="_subject" value="Comentario en: {slug}" />
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
  </section>
    </div>'''

MARKER = 'padding-top:0;padding-bottom:0;'  # unique string in our injected section

fixed = 0
skipped = 0
no_match = []

for n in range(7, 161):
    fname = f'articulo-{n}.html'
    try:
        with open(fname, 'r') as f:
            html = f.read()
    except FileNotFoundError:
        continue

    # Already injected?
    if MARKER in html:
        skipped += 1
        continue

    # Case 1: article has 2nd container (comments section)
    # Pattern: \n    </div>\n  \n    <div class="article-container">\n
    m = re.search(r'(\n    </div>\n  \n)(    <div class="article-container">\n)', html)
    if m:
        insert_pos = m.start(2)
        html = html[:insert_pos] + CTA_BOOKS_HTML + '\n' + html[insert_pos:]
        with open(fname, 'w') as f:
            f.write(html)
        fixed += 1
        continue

    # Case 2: article has no comments section (articulo-13)
    # Pattern: \n    </div>\n  </main>
    m = re.search(r'(\n    </div>\n  </main>)', html)
    if m:
        # Get title for slug
        title_m = re.search(r'class="article-title">(.*?)</h1>', html)
        title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else ''
        slug = f'articulo-{n}'
        comments_html = make_comments_html(slug)

        insert_pos = m.start(1) + 1  # after the first \n
        # Replace \n    </div>\n  </main> with \n    </div>\n[CTA]\n[COMMENTS]\n  </main>
        old = '    </div>\n  </main>'
        new = '    </div>\n\n' + CTA_BOOKS_HTML + '\n' + comments_html + '\n  </main>'
        html = html[:m.start()+1] + new + html[m.end():]
        with open(fname, 'w') as f:
            f.write(html)
        fixed += 1
        print(f'  articulo-{n}: added CTAs + comments (was missing)')
        continue

    no_match.append(n)

print(f'\nFixed: {fixed}')
print(f'Skipped (already done): {skipped}')
if no_match:
    print(f'No match found: {no_match}')
else:
    print('All articles processed successfully.')
