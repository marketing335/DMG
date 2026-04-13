#!/usr/bin/env python3
"""
1. Remove orphaned full-width CTA+books block from ALL 154 articles
2. Upgrade simple sidebar (articles 7-16) to full sidebar with CTAs + books
"""
import re, os

# ── Full sidebar replacement (replaces the simple "¿Tu texto necesita revisión?" widget) ──
FULL_SIDEBAR_WIDGETS = '''          <div class="sidebar-widget" style="display:grid;grid-template-columns:1fr 1fr;gap:10px;background:none;box-shadow:none;padding:0;">
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
        </aside>'''

# The simple sidebar widget to replace (articles 7-16 only)
SIMPLE_SIDEBAR_PATTERN = r'          <div class="sidebar-widget">\n            <h4>¿Tu texto necesita revisión\?</h4>.*?          </div>\n        </aside>'

orphan_cleaned = 0
sidebar_upgraded = 0
no_orphan = 0

for n in range(7, 161):
    fname = f'articulo-{n}.html'
    if not os.path.exists(fname):
        continue

    with open(fname) as f:
        html = f.read()

    changed = False

    # ── Step 1: Remove orphaned content between article-layout and comments ──
    # Pattern: </aside>..article-layout close..first-container close..ORPHAN..<div class="article-container">
    cleaned, count = re.subn(
        r'(</aside>\n      </div>\n\n    </div>)(.*?)(    <div class="article-container">)',
        r'\1\n  \n\3',
        html,
        count=1,
        flags=re.DOTALL
    )
    if count:
        html = cleaned
        orphan_cleaned += 1
        changed = True
    else:
        # Also try for articulo-13 style (ends with </main> not a 2nd container)
        cleaned2, count2 = re.subn(
            r'(</aside>\n      </div>\n\n    </div>)(.*?)(\n  </main>)',
            r'\1\n  \n\3',
            html,
            count=1,
            flags=re.DOTALL
        )
        if count2:
            html = cleaned2
            orphan_cleaned += 1
            changed = True
        else:
            no_orphan += 1

    # ── Step 2: Upgrade simple sidebar for articles 7-16 ──
    if n <= 16:
        upgraded, count2 = re.subn(
            SIMPLE_SIDEBAR_PATTERN,
            FULL_SIDEBAR_WIDGETS,
            html,
            count=1,
            flags=re.DOTALL
        )
        if count2:
            html = upgraded
            sidebar_upgraded += 1
            changed = True

    if changed:
        with open(fname, 'w') as f:
            f.write(html)

print(f'Orphaned content removed: {orphan_cleaned}')
print(f'Sidebars upgraded (7-16): {sidebar_upgraded}')
print(f'No orphan found (already clean): {no_orphan}')
