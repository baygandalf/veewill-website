import os, re
from data import PAGES, APP, APP_LOGIN, APP_START, SITE

UI = {
 "en": dict(skip="Skip to content", home="VeeWill home", main="Main", how="How it works", pricing="Pricing",
            faq="FAQ", login="Log in", start="Get started", menu="Menu", other="FR", other_full="Français",
            other_label="Français", disclaimer="VeeWill is not a law firm and does not provide legal advice.",
            about="About", contact="Contact", privacy="Privacy", terms="Terms", deleteAccount="Delete your account", probate="Probate fee calculator", blog="Blog", foot="Footer",
            g1="VeeWill", g2="Company", g3="Legal", closing="A little time today. Peace of mind for good.",
            cta="Start my will", copy="© 2026 VeeWill"),
 "fr": dict(skip="Aller au contenu", home="Accueil VeeWill", main="Menu principal", how="Comment ça fonctionne",
            pricing="Forfaits", faq="FAQ", login="Se connecter", start="Commencer", menu="Menu", other="EN",
            other_full="English", other_label="English",
            disclaimer="VeeWill n'est pas un cabinet d'avocats et ne donne pas de conseils juridiques.",
            about="À propos", contact="Nous joindre", privacy="Confidentialité", terms="Conditions", deleteAccount="Supprimer votre compte", probate="Calculateur des frais d'homologation", blog="Blogue", foot="Pied de page",
            g1="VeeWill", g2="L'entreprise", g3="Mentions légales",
            closing="Un peu de temps aujourd'hui. L'esprit tranquille pour de bon.",
            cta="Commencer mon testament", copy="© 2026 VeeWill"),
}

def path_of(key, lang):
    return PAGES[key][0 if lang == "en" else 1]

def rel(from_path, to_path):
    """Relative link between two page folders ('' is the site root)."""
    depth = from_path.count("/")
    return ("../" * depth) + to_path if (("../" * depth) + to_path) else "./"

def fr_typo(html):
    # French spacing: a non-breaking space before ? ! : ; » and after «, in text.
    nb = "\u00a0"
    html = re.sub(r" ([?!:;»])", nb + r"\1", html)
    html = html.replace("« ", "«" + nb)
    html = re.sub(r"(\d) h\b", r"\1" + nb + "h", html)
    # Undo inside URLs and code-like attributes (none use " :" but be safe).
    return html

def closing(lang):
    u = UI[lang]
    return f'''
  <section class="closing" aria-labelledby="closing-title">
    <div class="closing-inner">
      <img src="{{ROOT}}assets/veewill-mark-on-dark.png" alt="" width="420" height="261">
      <h2 id="closing-title">{u["closing"]}</h2>
      <a class="btn btn-gold" href="{APP_START}">{u["cta"]}</a>
    </div>
  </section>'''

def render(key, lang, title, desc, body, head_extra="", with_closing=True, main_id=None):
    u = UI[lang]
    here = path_of(key, lang) if key != "404" else ""
    other = "fr" if lang == "en" else "en"
    root = rel(here, "")
    root = "" if root == "./" else root
    L = lambda k: rel(here, path_of(k, lang))
    other_link = rel(here, path_of(key, other)) if key != "404" else rel(here, path_of("home", other))
    if key == "404":
        root = "/"
        L = lambda k: "/" + path_of(k, lang)
        other_link = "/" + path_of("home", other)
    cur = lambda k: ' aria-current="page"' if k == key else ""
    canonical = f"{SITE}/{here}" if key != "404" else ""
    alts = ""
    if key != "404":
        fr_alt = (f'<link rel="alternate" hreflang="fr-CA" href="{SITE}/{path_of(key,"fr")}">\n'
                  if path_of(key, "fr") != path_of(key, "en") else "")
        alts = (f'<link rel="canonical" href="{canonical}">\n'
                f'<link rel="alternate" hreflang="en-CA" href="{SITE}/{path_of(key,"en")}">\n'
                + fr_alt +
                f'<link rel="alternate" hreflang="x-default" href="{SITE}/{path_of(key,"en")}">\n'
                f'<meta property="og:url" content="{canonical}">')
    # Footer link to the blog, once it has articles (build.py adds PAGES['blog']).
    blog_link = f'<a href="{L("blog")}">{u["blog"]}</a>' if "blog" in PAGES else ""
    html = f'''<!doctype html>
<html lang="{lang}-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{alts}
<meta property="og:type" content="website">
<meta property="og:site_name" content="VeeWill">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:locale" content="{lang}_CA">
<meta property="og:image" content="{SITE}/assets/{'og-image-fr.png' if lang == 'fr' else 'og-image.png'}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{'VeeWill : votre testament, en toute simplicité.' if lang == 'fr' else 'VeeWill: your will, made simple.'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/assets/{'og-image-fr.png' if lang == 'fr' else 'og-image.png'}">
<meta name="theme-color" content="#141C3D">
<link rel="icon" type="image/png" href="{root}assets/favicon.png">
<link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/styles.css">
{head_extra}
</head>
<body>
<a class="skip" href="#main">{u["skip"]}</a>

<div id="promo-bar" class="promo-bar" hidden aria-live="polite">
  <span id="promo-msg"></span>
  <span class="promo-countdown" id="promo-countdown" aria-label="Time remaining"></span>
  <button class="promo-dismiss" id="promo-dismiss" aria-label="Dismiss">&times;</button>
</div>

<header class="site-header">
  <div class="wrap">
    <a class="logo" href="{L("home")}" aria-label="{u["home"]}"><img src="{root}assets/veewill-logo-on-dark.png" alt="VeeWill" width="127" height="32"></a>
    <nav class="nav" aria-label="{u["main"]}">
      <a href="{L("how")}"{cur("how")}>{u["how"]}</a>
      <a href="{L("pricing")}"{cur("pricing")}>{u["pricing"]}</a>
      <a href="{L("faq")}"{cur("faq")}>{u["faq"]}</a>
    </nav>
    <div class="header-actions">
      <a class="lang-toggle" href="{other_link}" hreflang="{other}-CA" lang="{other}-CA" aria-label="{u["other_label"]}">{u["other"]}</a>
      <a class="link-login" href="{APP_LOGIN}">{u["login"]}</a>
      <a class="btn btn-gold btn-sm" href="{APP}">{u["start"]}</a>
      <details class="menu">
        <summary aria-label="{u["menu"]}"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></summary>
        <div class="menu-panel">
          <a href="{L("how")}">{u["how"]}</a>
          <a href="{L("pricing")}">{u["pricing"]}</a>
          <a href="{L("faq")}">{u["faq"]}</a>
          <a href="{L("about")}">{u["about"]}</a>
          <a href="{L("contact")}">{u["contact"]}</a>
          <a href="{APP_LOGIN}">{u["login"]}</a>
          <a href="{other_link}" hreflang="{other}-CA" lang="{other}-CA">{u["other_full"]}</a>
        </div>
      </details>
    </div>
  </div>
</header>

<main id="main"{f' class="{main_id}"' if main_id else ""}>
{body}
{closing(lang) if with_closing else ""}
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="foot-brand">
      <img class="foot-mark" src="{root}assets/veewill-mark-on-dark.png" alt="VeeWill" width="64" height="40">
      <p>{u["disclaimer"]}</p>
      <p>{u["copy"]}</p>
    </div>
    <nav class="foot-links" aria-label="{u["foot"]}">
      <div><h2>{u["g1"]}</h2><a href="{L("how")}">{u["how"]}</a><a href="{L("pricing")}">{u["pricing"]}</a><a href="{L("faq")}">{u["faq"]}</a><a href="{L("probate")}">{u["probate"]}</a>{blog_link}</div>
      <div><h2>{u["g2"]}</h2><a href="{L("about")}">{u["about"]}</a><a href="{L("contact")}">{u["contact"]}</a><a href="{other_link}" hreflang="{other}-CA" lang="{other}-CA">{u["other_full"]}</a></div>
      <div><h2>{u["g3"]}</h2><a href="{L("privacy")}">{u["privacy"]}</a><a href="{L("terms")}">{u["terms"]}</a><a href="{L("deleteAccount")}">{u["deleteAccount"]}</a></div>
    </nav>
  </div>
</footer>

<script>window.VW_LANG="{lang}";</script>
<script src="{root}assets/promo.js" defer></script>
<script src="{root}assets/site.js" defer></script>
</body>
</html>
'''
    html = html.replace("{ROOT}", root)
    if lang == "fr":
        html = fr_typo(html)
    return html, here
