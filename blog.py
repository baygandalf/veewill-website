"""Blog engine: article pages, the blog index and their sitemap entries.

Articles live in articles/*.py, each defining ARTICLE = dict(...):
  slug_en / slug_fr      URL slugs (fr optional: no French page if missing)
  title / desc           per language: {"en": ..., "fr": ...} (search title, meta description)
  h1, intro              per language
  published, updated     ISO dates ("2026-10-20")
  reviewed_by            "" until a lawyer has reviewed it (then shown on the page)
  sections               per language: list of (heading, html)
  sources                list of (label, url): official sources the article relies on
  related                list of other article slugs (en)
Nothing is published until an article exists; the blog index appears with the first one.
"""
import glob, importlib.util, json, os, re
from data import SITE, APP_START

BLOG = {"en": "blog/", "fr": "fr/blogue/"}
L = {
 "en": dict(blog="Blog", home="Home", updated="Updated", published="Published", reviewed="Reviewed by", contents="On this page",
            sources="Sources", related="Keep reading", ctaTitle="Ready to make your will?", ctaBody="Make a valid will online in about 20 minutes, written for your province's rules.",
            cta="Start my will", note="This article is general information, not legal advice. Laws change and every situation is different.",
            indexTitle="VeeWill blog: wills and estate planning in Canada", indexDesc="Plain-language guides to wills, executors, probate and estate planning in every Canadian province and territory.",
            indexH1="Wills and estates, explained", indexLede="Plain-language guides for Canadians, checked against official sources.", read="min read"),
 "fr": dict(blog="Blogue", home="Accueil", updated="Mis à jour", published="Publié", reviewed="Révisé par", contents="Sur cette page",
            sources="Sources", related="À lire aussi", ctaTitle="Prêt à faire votre testament ?", ctaBody="Faites un testament valide en ligne en environ 20 minutes, selon les règles de votre province.",
            cta="Commencer mon testament", note="Cet article fournit de l'information générale et non un conseil juridique. Les lois changent et chaque situation est unique.",
            indexTitle="Blogue VeeWill : testaments et planification successorale au Canada", indexDesc="Des guides clairs sur les testaments, les liquidateurs, l'homologation et la planification successorale dans chaque province et territoire.",
            indexH1="Testaments et successions, expliqués", indexLede="Des guides clairs pour les Canadiens, vérifiés auprès des sources officielles.", read="min de lecture"),
}

def load_articles():
    out = []
    for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__), "articles", "*.py"))):
        spec = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f)
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        out.append(mod.ARTICLE)
    return sorted(out, key=lambda a: a["published"], reverse=True)

def path(a, lang):
    slug = a.get("slug_" + lang)
    return f"{BLOG[lang]}{slug}/" if slug else None

def minutes(sections):
    words = len(re.sub(r"<[^>]+>", " ", " ".join(h for _, h in sections)).split())
    return max(2, round(words / 220))

def article_page(a, lang, by_slug):
    l = L[lang]; here = path(a, lang)
    secs = a["sections"][lang]
    toc = "".join(f'<a href="#s{i}">{h}</a>' for i, (h, _) in enumerate(secs))
    body_secs = "".join(f'<section aria-labelledby="s{i}"><h2 id="s{i}">{h}</h2>{html}</section>' for i, (h, html) in enumerate(secs))
    srcs = "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{t}</a></li>' for t, u in a.get("sources", []))
    rel = ""
    for s in a.get("related", []):
        r = by_slug.get(s)
        if r and path(r, lang):
            rel += f'<li><a href="/{path(r, lang)}">{r["h1"][lang]}</a></li>'
    reviewed = f' · {l["reviewed"]} {a["reviewed_by"]}' if a.get("reviewed_by") else ""
    meta = f'{l["published"]} {a["published"]} · {l["updated"]} {a["updated"]}{reviewed} · {minutes(secs)} {l["read"]}'
    schema = [
      {"@context": "https://schema.org", "@type": "Article", "headline": a["h1"][lang], "description": a["desc"][lang],
       "datePublished": a["published"], "dateModified": a["updated"], "inLanguage": f"{lang}-CA",
       "author": {"@type": "Organization", "name": "VeeWill", "url": SITE},
       "publisher": {"@type": "Organization", "name": "VeeWill", "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/veewill-mark.png"}},
       "mainEntityOfPage": f"{SITE}/{here}"},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": l["home"], "item": f"{SITE}/{'' if lang == 'en' else 'fr/'}"},
        {"@type": "ListItem", "position": 2, "name": l["blog"], "item": f"{SITE}/{BLOG[lang]}"},
        {"@type": "ListItem", "position": 3, "name": a["h1"][lang], "item": f"{SITE}/{here}"}]},
    ]
    head = "".join('<script type="application/ld+json">' + json.dumps(s, ensure_ascii=False) + "</script>" for s in schema)
    body = f'''
  <section class="page-hero"><div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/{'' if lang == 'en' else 'fr/'}">{l["home"]}</a> › <a href="/{BLOG[lang]}">{l["blog"]}</a></nav>
    <h1>{a["h1"][lang]}</h1><p class="lede">{a["intro"][lang]}</p><p class="article-meta">{meta}</p>
  </div></section>
  <section class="paper"><div class="wrap narrow article">
    <nav class="article-toc" aria-label="{l["contents"]}"><p>{l["contents"]}</p>{toc}</nav>
    {body_secs}
    <p class="article-note">{l["note"]}</p>
    {f'<h2>{l["sources"]}</h2><ul class="article-sources">{srcs}</ul>' if srcs else ''}
    {f'<h2>{l["related"]}</h2><ul class="article-related">{rel}</ul>' if rel else ''}
    <div class="still"><h2>{l["ctaTitle"]}</h2><p>{l["ctaBody"]}</p><p><a class="btn btn-gold" href="{APP_START}">{l["cta"]}</a></p></div>
  </div></section>'''
    return a["title"][lang], a["desc"][lang], body, head

def index_page(articles, lang):
    l = L[lang]
    cards = "".join(
        f'<article class="post-card"><h2><a href="/{path(a, lang)}">{a["h1"][lang]}</a></h2><p>{a["desc"][lang]}</p>'
        f'<p class="article-meta">{l["updated"]} {a["updated"]} · {minutes(a["sections"][lang])} {l["read"]}</p></article>'
        for a in articles if path(a, lang))
    body = f'''
  <section class="page-hero"><div class="wrap"><h1>{l["indexH1"]}</h1><p class="lede">{l["indexLede"]}</p></div></section>
  <section class="paper"><div class="wrap narrow"><div class="post-list">{cards}</div></div></section>'''
    return l["indexTitle"], l["indexDesc"], body, ""
