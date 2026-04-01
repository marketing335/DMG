#!/usr/bin/env python3
"""
Generador de artículos estáticos desde WordPress
Uso: python3 generar_articulos.py
Requiere: pip install requests
"""

import requests, json, os, re, math
from datetime import datetime

# ── CONFIGURACIÓN ──────────────────────────────────────────
WP_URL  = "https://relatosmagar.com"
WP_USER = "Digital Mastery Group"
WP_PASS = "a#lsBumnw^M#b60Y0)Iro39n"
OUTPUT  = "."          # carpeta donde se generan los HTML
# ───────────────────────────────────────────────────────────

LOGO = "https://i.ibb.co/xtBTCFC4/LA-BOMBA-ESPA-OLA-2.png"
AUTHOR_IMG = "https://i.ibb.co/zH7DxvJS/dame-esta-mujercon-202603241403.jpg"
HERO_IMG_DEFAULT = "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1200&h=500&fit=crop&q=80"

NAVBAR = f"""  <header class="navbar" id="navbar">
    <div class="nav-inner">
      <a href="relatosmagar.html" class="nav-logo">
        <img src="{LOGO}" alt="Magar" class="nav-logo-img" />
      </a>
      <nav class="nav-links" id="navLinks">
        <a href="relatosmagar.html">Servicios</a>
        <a href="relatosmagar.html">Blog</a>
        <a href="suscripcion.html">Newsletter</a>
        <a href="contacto.html" class="nav-cta">Solicitar presupuesto</a>
      </nav>
      <button class="hamburger" id="hamburger" aria-label="Menú"><span></span><span></span><span></span></button>
    </div>
  </header>"""

FOOTER = """  <footer class="footer">
    <div class="container">
      <div class="footer-bottom" style="border-top:1px solid rgba(255,255,255,.06);padding-top:24px;">
        <p>© 2025 Magar · Corrección y edición profesional</p>
        <a href="relatosmagar.html" style="color:rgba(255,255,255,.5);font-size:13px;">← Volver al blog</a>
      </div>
    </div>
  </footer>"""

def slug_to_filename(slug, index):
    return f"wp-{index:04d}-{slug[:60]}.html"

def format_date(date_str):
    try:
        dt = datetime.fromisoformat(date_str)
        meses = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"]
        return f"{dt.day} {meses[dt.month-1]} {dt.year}"
    except:
        return date_str[:10]

def estimate_read_time(content):
    words = len(re.sub(r'<[^>]+>', '', content).split())
    return max(1, math.ceil(words / 200))

def generate_article_html(post, index, prev_slug=None, next_slug=None):
    title     = post.get("title", {}).get("rendered", "Sin título")
    content   = post.get("content", {}).get("rendered", "")
    excerpt   = re.sub(r'<[^>]+>', '', post.get("excerpt", {}).get("rendered", ""))[:200]
    date      = format_date(post.get("date", ""))
    slug      = post.get("slug", f"post-{index}")
    filename  = slug_to_filename(slug, index)
    read_time = estimate_read_time(content)

    # imagen destacada
    hero_img = post.get("_embedded", {}).get("wp:featuredmedia", [{}])[0].get("source_url", HERO_IMG_DEFAULT)
    if not hero_img:
        hero_img = HERO_IMG_DEFAULT

    nav_links = ""
    if prev_slug:
        nav_links += f'<a href="{prev_slug}" class="btn btn-ghost btn-sm">← Anterior</a>'
    if next_slug:
        nav_links += f'<a href="{next_slug}" class="btn btn-ghost btn-sm">Siguiente →</a>'

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | Magar</title>
  <meta name="description" content="{excerpt}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,900;1,400;1,600&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="magar.css" />
  <link rel="stylesheet" href="articulo.css" />
</head>
<body>

{NAVBAR}

  <main class="article-main">
    <div class="article-container">

      <nav class="breadcrumb">
        <a href="relatosmagar.html">Inicio</a>
        <span>›</span>
        <a href="blog.html">Blog</a>
        <span>›</span>
        <span>{title[:60]}</span>
      </nav>

      <header class="article-header">
        <h1 class="article-title">{title}</h1>
        <div class="article-meta">
          <span>{date}</span>
          <span class="meta-dot">·</span>
          <span>{read_time} min lectura</span>
          <span class="meta-dot">·</span>
          <span>por <strong>Esther Magar</strong></span>
        </div>
      </header>

      <figure class="article-hero-img">
        <img src="{hero_img}" alt="{title}" />
      </figure>

      <div class="article-layout">
        <article class="article-body">
          {content}
          <div style="display:flex;gap:12px;margin-top:40px;flex-wrap:wrap;">
            {nav_links}
          </div>
          <div class="article-cta-box" style="margin-top:40px;">
            <p>¿Tu texto necesita una revisión profesional?</p>
            <a href="contacto.html" class="btn btn-primary">Solicitar corrección gratuita</a>
          </div>
        </article>

        <aside class="article-sidebar">
          <div class="sidebar-widget">
            <h4>Sobre la autora</h4>
            <img src="{AUTHOR_IMG}" alt="Esther Magar" class="sidebar-avatar" />
            <p><strong>Esther Magar</strong> es correctora y editora de textos con más de diez años de experiencia.</p>
            <a href="sobre-mi.html" class="sidebar-link">Conocer más →</a>
          </div>
          <div class="sidebar-widget">
            <h4>¿Tu texto necesita corrección?</h4>
            <p>Primera muestra gratuita. Presupuesto sin compromiso.</p>
            <a href="contacto.html" class="btn btn-primary btn-sm" style="width:100%;margin-top:8px;">Pedir presupuesto</a>
          </div>
        </aside>
      </div>

    </div>
  </main>

{FOOTER}

  <script src="magar.js"></script>
</body>
</html>
"""

def fetch_all_posts():
    print("🔄 Conectando a WordPress...")
    session = requests.Session()
    session.auth = (WP_USER, WP_PASS)
    session.headers.update({"User-Agent": "Mozilla/5.0"})

    all_posts = []
    page = 1
    while True:
        url = f"{WP_URL}/wp-json/wp/v2/posts?per_page=100&page={page}&_embed=wp:featuredmedia&_fields=id,slug,title,date,excerpt,content,_links,_embedded"
        r = session.get(url, timeout=30)
        if r.status_code == 400:
            break
        if r.status_code != 200:
            print(f"❌ Error {r.status_code} en página {page}: {r.text[:200]}")
            break
        posts = r.json()
        if not posts:
            break
        all_posts.extend(posts)
        total = int(r.headers.get("X-WP-TotalPages", 1))
        print(f"   Página {page}/{total} — {len(posts)} artículos")
        if page >= total:
            break
        page += 1

    return all_posts

def generate_blog_index(posts):
    """Genera blog.html con todos los artículos"""
    cards = ""
    images = [
        "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=600&h=380&fit=crop&q=80",
        "https://images.unsplash.com/photo-1471107340929-a87cd0f5b5f3?w=600&h=380&fit=crop&q=80",
        "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=600&h=380&fit=crop&q=80",
        "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=600&h=380&fit=crop&q=80",
    ]
    for i, post in enumerate(posts):
        title    = post.get("title", {}).get("rendered", "Sin título")
        excerpt  = re.sub(r'<[^>]+>', '', post.get("excerpt", {}).get("rendered", ""))[:120]
        date     = format_date(post.get("date", ""))
        slug     = post.get("slug", f"post-{i}")
        filename = slug_to_filename(slug, i+1)
        hero_img = post.get("_embedded", {}).get("wp:featuredmedia", [{}])[0].get("source_url") or images[i % 4]
        cards += f"""
      <article class="bp-card">
        <img src="{hero_img}" alt="{title}" />
        <div class="bp-card-body">
          <h3><a href="{filename}">{title}</a></h3>
          <p>{excerpt}...</p>
          <div class="bp-meta"><span>{date}</span></div>
        </div>
      </article>"""

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Blog | Magar</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,900;1,400;1,600&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="magar.css" />
  <style>
    .blog-page-hero{{background:var(--navy,#0f1b2d);padding:140px 0 64px;text-align:center;}}
    .blog-page-hero h1{{font-family:'Playfair Display',serif;font-size:clamp(2rem,4vw,3rem);color:#fff;margin:0 0 16px;}}
    .blog-page-hero p{{color:rgba(255,255,255,.6);font-size:1.05rem;max-width:520px;margin:0 auto;}}
    .blog-page-section{{padding:72px 0 96px;background:#faf9f7;}}
    .blog-page-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:32px;max-width:1100px;margin:0 auto;padding:0 24px;}}
    @media(max-width:900px){{.blog-page-grid{{grid-template-columns:repeat(2,1fr);}}}}
    @media(max-width:580px){{.blog-page-grid{{grid-template-columns:1fr;}}}}
    .bp-card{{background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.06);display:flex;flex-direction:column;transition:transform .2s;}}
    .bp-card:hover{{transform:translateY(-4px);}}
    .bp-card img{{width:100%;height:190px;object-fit:cover;}}
    .bp-card-body{{padding:20px 22px 24px;display:flex;flex-direction:column;flex:1;}}
    .bp-card-body h3{{font-family:'Playfair Display',serif;font-size:1.05rem;line-height:1.45;margin:0 0 10px;color:#0f1b2d;}}
    .bp-card-body h3 a{{color:inherit;text-decoration:none;}}
    .bp-card-body p{{font-size:.88rem;color:#666;line-height:1.6;margin:0 0 16px;flex:1;}}
    .bp-meta{{font-size:.8rem;color:#999;}}
  </style>
</head>
<body>
{NAVBAR}
  <section class="blog-page-hero">
    <div class="container">
      <h1>Artículos sobre escritura<br/>y corrección</h1>
      <p>Todos los artículos de Esther Magar sobre escritura, corrección literaria y el mundo editorial.</p>
    </div>
  </section>
  <section class="blog-page-section">
    <div class="blog-page-grid">
      {cards}
    </div>
  </section>
{FOOTER}
  <script src="magar.js"></script>
</body>
</html>"""

def main():
    posts = fetch_all_posts()
    if not posts:
        print("❌ No se pudieron obtener artículos. Verifica usuario/contraseña.")
        return

    print(f"\n✅ {len(posts)} artículos encontrados. Generando HTML...")

    filenames = [slug_to_filename(p.get("slug", f"post-{i}"), i+1) for i, p in enumerate(posts)]

    generated = 0
    for i, post in enumerate(posts):
        prev_fn = filenames[i-1] if i > 0 else None
        next_fn = filenames[i+1] if i < len(posts)-1 else None
        html = generate_article_html(post, i+1, prev_fn, next_fn)
        filepath = os.path.join(OUTPUT, filenames[i])
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        generated += 1
        if generated % 20 == 0:
            print(f"   {generated}/{len(posts)} generados...")

    # Generar blog.html
    blog_html = generate_blog_index(posts)
    with open(os.path.join(OUTPUT, "blog.html"), "w", encoding="utf-8") as f:
        f.write(blog_html)

    print(f"\n🎉 ¡Listo! {generated} artículos generados + blog.html actualizado.")
    print(f"\nAhora ejecuta en la carpeta DMG:")
    print(f"  git add .")
    print(f"  git commit -m 'Añadir {generated} artículos del blog'")
    print(f"  git push -u origin claude/create-new-repo-9iGFT")

if __name__ == "__main__":
    main()
