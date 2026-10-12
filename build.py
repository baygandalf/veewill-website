import os, shutil
from layout import render
from data import PAGES, SITE
import pages_a, pages_b, pages_c

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "veewill-site")
if os.path.exists(OUT):
    for d in os.listdir(OUT):
        if d not in ("assets", "README.md"):
            p = os.path.join(OUT, d)
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
os.makedirs(OUT, exist_ok=True)

# Copy the site's CSS, scripts and images (the "assets" folder in this repo) into the built site.
ASSETS_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
if os.path.isdir(ASSETS_SRC):
    shutil.copytree(ASSETS_SRC, os.path.join(OUT, "assets"), dirs_exist_ok=True)

# The blog is registered first, so every page's footer can link to it.
import blog
ARTICLES = blog.load_articles()
has_fr = any(blog.path(a, "fr") for a in ARTICLES)
if ARTICLES:
    # The French index only exists once there's a French article.
    PAGES["blog"] = (blog.BLOG["en"], blog.BLOG["fr"] if has_fr else blog.BLOG["en"])

FN = {"home": pages_a.home, "how": pages_a.how, "pricing": pages_a.pricing,
      "faq": pages_b.faq, "about": pages_b.about, "contact": pages_b.contact,
      "privacy": pages_b.privacy, "terms": pages_b.terms,
      "deleteAccount": pages_b.deleteAccount, "probate": pages_c.probate}

for key, fn in FN.items():
    for lang in ("en", "fr"):
        title, desc, body, head = fn(lang)
        html, here = render(key, lang, title, desc, body, head)
        path = os.path.join(OUT, here, "index.html")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").write(html)
        print("wrote", "/" + here)

# Blog: article pages and the index (only once there's at least one article).
BY_SLUG = {a["slug_en"]: a for a in ARTICLES}
blog_urls = []
for a in ARTICLES:
    for lang in ("en", "fr"):
        p = blog.path(a, lang)
        if not p:
            continue
        title, desc, body, head = blog.article_page(a, lang, BY_SLUG)
        PAGES["_a_" + a["slug_en"]] = (blog.path(a, "en"), blog.path(a, "fr") or blog.path(a, "en"))
        html, here = render("_a_" + a["slug_en"], lang, title, desc, body, head)
        out = os.path.join(OUT, p, "index.html"); os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w").write(html); print("wrote", "/" + p)
if ARTICLES:
    for lang in (("en", "fr") if has_fr else ("en",)):
        title, desc, body, head = blog.index_page(ARTICLES, lang)
        html, here = render("blog", lang, title, desc, body, head)
        out = os.path.join(OUT, blog.BLOG[lang], "index.html"); os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w").write(html); print("wrote", "/" + blog.BLOG[lang])

t, d, b, h = pages_b.notfound()
html, _ = render("404", "en", t, d, b, h, with_closing=False)
open(os.path.join(OUT, "404.html"), "w").write(html)

urls = ""
for key, (en, fr) in PAGES.items():
    for p in (en, fr):
        urls += (f"  <url><loc>{SITE}/{p}</loc>"
                 f'<xhtml:link rel="alternate" hreflang="en-CA" href="{SITE}/{en}"/>'
                 f'<xhtml:link rel="alternate" hreflang="fr-CA" href="{SITE}/{fr}"/></url>\n')
open(os.path.join(OUT, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
    'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + "</urlset>\n")
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
print("done")
