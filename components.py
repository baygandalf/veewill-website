from data import price, saving, APP

# Wording from the app's `pricing` namespace (en.ts / fr.ts).
T = {
 "en": dict(
   willName="Will", cpName="Complete Protection", recommended="Recommended",
   willShort="Your Will, notes for your loved ones and your funeral wishes.",
   cpShort="Your Will, plus the documents that speak for you if you can't.",
   oneTime="one payment", couple="for two, one payment", updates="Includes 1 year of updates",
   saving="{} less than buying two",
   itemWill="Your Will", itemWillCouple="A Will for each of you", notes="Notes for loved ones",
   funeral="Funeral wishes", pdf="Print-ready PDF",
   trusted="Trusted access: who can reach your documents, and when",
   poa="Financial Power of Attorney", hcd="Health Care Directive (living will)", vault="Secure Vault",
   execFile="Executor file: what you own and where to find it",
   versions="Up to 5 Will versions", versionsCouple="Up to 5 Will versions each",
   execTools="Executor tools", guided="Guided, step-by-step questions",
   province="Guidance for your province", email="Email support",
   chooseWill="Choose Will", chooseCp="Choose Complete Protection",
   who="Who is this for?", me="Just me", two="For two",
   head="Pick your plan", headSub="Prices in Canadian dollars. One payment. Nothing renews by itself.",
   refund="Because VeeWill generates personalized legal documents instantly, plans are non-refundable once documents are created.",
 ),
 "fr": dict(
   willName="Testament", cpName="Protection complète", recommended="Recommandé",
   willShort="Votre testament, des notes pour vos proches et vos volontés funéraires.",
   cpShort="Votre testament, et les documents qui parlent pour vous si vous ne le pouvez plus.",
   oneTime="un seul paiement", couple="pour deux, un seul paiement", updates="Comprend 1 an de mises à jour",
   saving="{} de moins qu'en achetant deux",
   itemWill="Votre testament", itemWillCouple="Un testament pour chacun de vous", notes="Notes pour vos proches",
   funeral="Volontés funéraires", pdf="PDF prêt à imprimer",
   trusted="Accès de confiance : qui peut consulter vos documents, et quand",
   poa="Procuration financière", hcd="Directive de soins de santé (testament de vie)", vault="Coffre-fort sécurisé",
   execFile="Dossier du liquidateur : vos biens et où les trouver",
   versions="Jusqu'à 5 versions de testament", versionsCouple="Jusqu'à 5 versions de testament chacun",
   execTools="Outils pour le liquidateur", guided="Questions guidées, étape par étape",
   province="Conseils propres à votre province", email="Soutien par courriel",
   chooseWill="Choisir le forfait Testament", chooseCp="Choisir la Protection complète",
   who="Pour qui ?", me="Juste pour moi", two="Pour deux",
   head="Choisissez votre forfait", headSub="Prix en dollars canadiens. Un seul paiement. Rien ne se renouvelle tout seul.",
   refund="Comme VeeWill génère instantanément des documents juridiques personnalisés, les forfaits ne sont pas remboursables une fois les documents créés.",
 ),
}

def both(single, couple):
    return f'<span data-for="single">{single}</span><span data-for="couple">{couple}</span>'

def toggle(lang):
    t = T[lang]
    return f'''<div class="audience" role="group" aria-label="{t["who"]}">
          <button type="button" data-audience="single" aria-pressed="true">{t["me"]}</button>
          <button type="button" data-audience="couple" aria-pressed="false">{t["two"]}</button>
        </div>'''

def plan_cards(lang):
    t = T[lang]
    def card(pid, name, short, items, cta, featured):
        badge = f'<span class="badge">{t["recommended"]}</span>' if featured else ""
        lis = "".join(f"<li>{i}</li>" for i in items)
        return f'''
        <article class="plan{' featured' if featured else ''}">
          <div class="plan-top"><h3>{name}</h3>{badge}</div>
          <p class="short">{short}</p>
          <p class="price">{price(pid)}</p>
          <p class="period">{both(t["oneTime"], t["couple"])}</p>
          <p class="period">{t["updates"]}</p>
          <p class="saving" data-for="couple">{t["saving"].format(saving(pid))}</p>
          <ul>{lis}</ul>
          <div class="plan-cta"><a class="btn {'btn-night' if featured else 'btn-ghost'}" data-plan-link href="{APP}subscription?plan={pid}">{cta}</a></div>
        </article>'''
    w = both(t["itemWill"], t["itemWillCouple"])
    return '<div class="plans">' + card("will", t["willName"], t["willShort"],
        [w, t["notes"], t["funeral"], t["pdf"], t["trusted"]], t["chooseWill"], False) + card(
        "completeProtection", t["cpName"], t["cpShort"],
        [w, t["poa"], t["hcd"], t["vault"], t["execFile"]], t["chooseCp"], True) + "\n      </div>"

def compare_rows(lang):
    """getPlanComparison(): Complete Protection's order, year-of-updates lines left out."""
    t = T[lang]
    rows = [
        (both(t["itemWill"], t["itemWillCouple"]), True, True),
        (t["poa"], False, True), (t["hcd"], False, True), (t["notes"], True, True),
        (t["funeral"], True, True), (t["vault"], False, True), (t["execFile"], False, True),
        (t["trusted"], True, True), (both(t["versions"], t["versionsCouple"]), False, True),
        (t["execTools"], False, True), (t["guided"], True, True), (t["pdf"], True, True),
        (t["province"], True, True), (t["email"], True, True),
    ]
    return rows
