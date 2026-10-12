# Mirrors lib/pricing.ts (October 2026). Cents, per audience.
P = {
 "will": (6999, 11999), "completeProtection": (12999, 20999),
 "financialPoa": (3499, 5499), "healthDirective": (2499, 3999),
 "expatCanada": (5999, 9999), "expatQuebec": (6999, 10999),
 "expatAddon": (3999, 6499), "vaultAddon": (1999, 2999), "executorFileAddon": (2999, 4499),
 "membership": (2499, 3999),
}
def fmt(c):
    d, r = divmod(c, 100)
    return f"${d}" if r == 0 else f"${d}.{r:02d}"
def price(pid):
    s, c = P[pid]
    return f'<span data-for="single">{fmt(s)}</span><span data-for="couple">{fmt(c)}</span>'
def saving(pid):
    s, c = P[pid]
    return fmt(2 * s - c)

APP = "https://app.veewill.ca/"
# Where the website's buttons go in the web app.
APP_LOGIN = APP + "login"                              # "Log in"
APP_START = APP + "will/wizard/province-selection"     # "Start my will": the Will's first step
EMAIL = "support@veewill.ca"
SITE = "https://veewill.ca"

# Page slugs per language. Key -> (en path, fr path)
PAGES = {
 "home": ("", "fr/"),
 "how": ("how-it-works/", "fr/comment-ca-fonctionne/"),
 "pricing": ("pricing/", "fr/forfaits/"),
 "faq": ("faq/", "fr/faq/"),
 "about": ("about/", "fr/a-propos/"),
 "contact": ("contact/", "fr/contact/"),
 "privacy": ("privacy/", "fr/confidentialite/"),
 "terms": ("terms/", "fr/conditions/"),
 "deleteAccount": ("delete-account/", "fr/supprimer-mon-compte/"),
 "probate": ("probate-fee-calculator/", "fr/calculateur-frais-homologation/"),
}

# App store pages for the hero's store buttons. Leave empty until the apps are
# published: the buttons then say "Coming soon" and aren't clickable. Paste the
# full store links here and rebuild once the listings are live.
APP_STORE_URL = ""
PLAY_STORE_URL = ""
