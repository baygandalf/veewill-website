"""Resources: the probate fee calculator (verified October 12, 2026)."""
import json
from layout import path_of
from data import APP_START, SITE

CHECKED = {"en": "October 12, 2026", "fr": "12 octobre 2026"}

# code, en name, fr name, basis (gross/net/none), official source label, url
JUR = [
 ("ON", "Ontario", "Ontario", "gross", "Ontario Ministry of Finance, Estate Administration Tax", "https://www.ontario.ca/page/estate-administration-tax"),
 ("QC", "Québec", "Québec", "none", "Government of Québec, forms of will and probate", "https://www.quebec.ca/en/justice-and-civil-status/wills-estate/wills/forms-will/holograph-will"),
 ("BC", "British Columbia", "Colombie-Britannique", "gross", "Probate Fee Act, SBC 1999, c. 4, s. 2", "https://www.canlii.org/en/bc/laws/stat/sbc-1999-c-4/latest/sbc-1999-c-4.html"),
 ("AB", "Alberta", "Alberta", "net", "Government of Alberta, court fees (Surrogate matters)", "https://www.alberta.ca/court-fees"),
 ("SK", "Saskatchewan", "Saskatchewan", "gross", "Public Legal Education Association of Saskatchewan, estate costs", "https://plea.org/death-estates/estate/estate-costs"),
 ("MB", "Manitoba", "Manitoba", "none", "The Court Services Fees Act (probate charges eliminated Nov. 6, 2020)", "https://lawlibrary.ca/2020/11/11/probate-charges-eliminated/"),
 ("NB", "New Brunswick", "Nouveau-Brunswick", "gross", "Courts of New Brunswick, Probate Court (rates from June 12, 2026)", "https://www.courtsnb-coursnb.ca/content/cour/en/probate-court.html"),
 ("NS", "Nova Scotia", "Nouvelle-Écosse", "gross", "Probate Act (Nova Scotia), s. 87(2)", "https://nslegislature.ca/sites/default/files/legc/statutes/probate.pdf"),
 ("PE", "Prince Edward Island", "Île-du-Prince-Édouard", "gross", "Probate Act (Prince Edward Island), s. 119.1", "https://www.princeedwardisland.ca/sites/default/files/legislation/p-21-probate_act.pdf"),
 ("NL", "Newfoundland and Labrador", "Terre-Neuve-et-Labrador", "gross", "Services Charges Act, SNL 1998, c. S-13.2, s. 4", "https://www.assembly.nl.ca/Legislation/sr/statutes/s13-2.htm"),
 ("YT", "Yukon", "Yukon", "gross", "Supreme Court Rules (Yukon), Appendix C, Schedule 1, item 11", ""),
 ("NT", "Northwest Territories", "Territoires du Nord-Ouest", "net", "Court Services Fees Regulations (NWT), Schedule A, Part 2", "https://www.justice.gov.nt.ca/en/files/legislation/seizures/seizures.r2.pdf"),
 ("NU", "Nunavut", "Nunavut", "net", "Court Fees Regulations, R-042-2021, Schedule C (Nunavut)", "https://www.nunavutlegislation.ca/en/regulation/r-042-2021-court-fees-regulations"),
]

# Plain-language rule per jurisdiction (shown under the result).
RULE = {
 "en": {
  "ON": "No tax on estates of $50,000 or less. Above that, $15 for every $1,000 (or part) of the value over $50,000.",
  "QC": "Québec has no probate fee based on the value of the estate. A notarial will needs no verification. A holograph will or a will made before witnesses must be verified (probated) by the Superior Court or a notary after death, which has its own costs.",
  "BC": "No fee on estates of $25,000 or less. Then $6 per $1,000 (or part) from $25,000 to $50,000, and $14 per $1,000 (or part) above $50,000. A separate court filing fee also applies.",
  "AB": "A flat fee by the estate's net value: $35 up to $10,000; $135 up to $25,000; $275 up to $125,000; $400 up to $250,000; $525 above.",
  "SK": "$7 for every $1,000 (or part) of the estate's value (0.7%).",
  "MB": "Manitoba eliminated probate fees on November 6, 2020. Small court service fees may still apply.",
  "NB": "$200 on estates of $20,000 or less. Then $5 per $1,000 (or part) from $20,000 to $100,000, and $15 per $1,000 (or part) above $100,000 (rates in force since June 12, 2026).",
  "NS": "$85.60 up to $10,000; $215.20 up to $25,000; $358.15 up to $50,000; $1,002.65 up to $100,000; then $16.95 per $1,000 (or part) above $100,000.",
  "PE": "$50 up to $10,000; $100 up to $25,000; $200 up to $50,000; $400 up to $100,000; then $4 per $1,000 (or part) above $100,000.",
  "NL": "$60 on estates of $1,000 or less. Above that, $60 plus $0.60 for every additional $100.",
  "YT": "No fee on estates of $25,000 or less; $140 above that.",
  "NT": "A flat fee by the value after debts: $30 up to $10,000; $110 up to $25,000; $215 up to $125,000; $325 up to $250,000; $435 above.",
  "NU": "A flat fee by value: $30 up to $10,000; $110 up to $25,000; $215 up to $125,000; $325 up to $250,000; $425 above.",
 },
 "fr": {
  "ON": "Aucun impôt pour une succession de 50 000 $ ou moins. Au-delà, 15 $ par tranche de 1 000 $ (ou fraction) de la valeur qui dépasse 50 000 $.",
  "QC": "Le Québec n'impose aucun frais d'homologation selon la valeur de la succession. Le testament notarié n'a pas à être vérifié. Le testament olographe ou devant témoins doit être vérifié par la Cour supérieure ou un notaire après le décès, ce qui entraîne ses propres frais.",
  "BC": "Aucuns frais pour une succession de 25 000 $ ou moins. Ensuite, 6 $ par tranche de 1 000 $ (ou fraction) de 25 000 $ à 50 000 $, et 14 $ par tranche de 1 000 $ (ou fraction) au-delà de 50 000 $. Des frais de dépôt au tribunal s'ajoutent.",
  "AB": "Frais fixes selon la valeur nette de la succession : 35 $ jusqu'à 10 000 $; 135 $ jusqu'à 25 000 $; 275 $ jusqu'à 125 000 $; 400 $ jusqu'à 250 000 $; 525 $ au-delà.",
  "SK": "7 $ par tranche de 1 000 $ (ou fraction) de la valeur de la succession (0,7 %).",
  "MB": "Le Manitoba a aboli les frais d'homologation le 6 novembre 2020. De faibles frais de service judiciaire peuvent s'appliquer.",
  "NB": "200 $ pour une succession de 20 000 $ ou moins. Ensuite, 5 $ par tranche de 1 000 $ (ou fraction) de 20 000 $ à 100 000 $, et 15 $ par tranche de 1 000 $ (ou fraction) au-delà de 100 000 $ (taux en vigueur depuis le 12 juin 2026).",
  "NS": "85,60 $ jusqu'à 10 000 $; 215,20 $ jusqu'à 25 000 $; 358,15 $ jusqu'à 50 000 $; 1 002,65 $ jusqu'à 100 000 $; puis 16,95 $ par tranche de 1 000 $ (ou fraction) au-delà de 100 000 $.",
  "PE": "50 $ jusqu'à 10 000 $; 100 $ jusqu'à 25 000 $; 200 $ jusqu'à 50 000 $; 400 $ jusqu'à 100 000 $; puis 4 $ par tranche de 1 000 $ (ou fraction) au-delà de 100 000 $.",
  "NL": "60 $ pour une succession de 1 000 $ ou moins. Au-delà, 60 $ plus 0,60 $ par tranche additionnelle de 100 $.",
  "YT": "Aucuns frais pour une succession de 25 000 $ ou moins; 140 $ au-delà.",
  "NT": "Frais fixes selon la valeur après déduction des dettes : 30 $ jusqu'à 10 000 $; 110 $ jusqu'à 25 000 $; 215 $ jusqu'à 125 000 $; 325 $ jusqu'à 250 000 $; 435 $ au-delà.",
  "NU": "Frais fixes selon la valeur : 30 $ jusqu'à 10 000 $; 110 $ jusqu'à 25 000 $; 215 $ jusqu'à 125 000 $; 325 $ jusqu'à 250 000 $; 425 $ au-delà.",
 },
}

T = {
 "en": dict(
  title="Probate Fee Calculator for Canada (2026) | VeeWill",
  desc="Estimate probate fees in every Canadian province and territory, from official sources. Includes New Brunswick's June 2026 rates. Free, no sign-up.",
  h1="Probate fee calculator", lede="Estimate the probate fee (or estate administration tax) in any province or territory. Every rule comes from an official source, listed below.",
  prov="Province or territory", choose="Choose…", value="Estimated value of the estate", calc="Calculate",
  feeIs="Estimated probate fee", basis={"gross": "Based on the estate's gross value (before debts).", "net": "Based on the estate's net value (after debts).", "none": "No fee based on the estate's value."},
  needValue="Enter the estate's value, in Canadian dollars.", needProv="Choose a province or territory.",
  disclaimer=f"An estimate only, not legal or tax advice. Fees last checked against official sources on {CHECKED['en']}. Other court or filing fees may apply.",
  source="Official source",
  tableTitle="Probate fees across Canada", tableIntro="How each province and territory calculates its fee, with the official source.",
  colWhere="Province or territory", colRule="How the fee works", colSource="Source",
  ctaTitle="Make your executor's job easier", ctaBody="A clear, valid will is the first step. Make yours online in about 20 minutes, written for your province's rules.", cta="Start my will",
  faqTitle="Questions about probate",
  faq=[
   ("What is probate?", "Probate is the court process that confirms a will is valid and gives the executor the legal authority to deal with the estate. Banks and land registries often ask for it before they release or transfer assets."),
   ("Which assets count toward the fee?", "Generally, assets that pass through the will. Assets with a named beneficiary (such as life insurance, and in most provinces RRSPs, RRIFs and TFSAs) and property owned jointly with right of survivorship usually pass outside the estate and aren't counted. The rules differ by province, so check with a professional."),
   ("Gross value or net value?", "Most provinces use the gross value of the estate, before debts (some allow mortgages on real estate to be deducted). Alberta, the Northwest Territories and Nunavut base their fee on the net value. The calculator tells you which applies."),
   ("Who pays probate fees?", "The estate does, usually from its own funds, when the executor applies for probate. They're not paid by the beneficiaries personally."),
   ("Does every estate need probate?", "No. Small estates, or estates where everything passes outside the will, may not need it. In Québec, a notarial will needs no verification at all. Whether probate is needed depends on the assets and on what banks and registries ask for."),
   ("Why are some calculators different?", "Fees change. New Brunswick raised its probate tax on June 12, 2026, and Nunavut updated its court fees in 2021, so older calculators may show outdated amounts. Ours shows the date we last checked every rule against official sources."),
  ],
 ),
 "fr": dict(
  title="Calculateur des frais d'homologation au Canada (2026) | VeeWill",
  desc="Estimez les frais d'homologation dans chaque province et territoire, selon les sources officielles. Comprend les taux du Nouveau-Brunswick de juin 2026. Gratuit.",
  h1="Calculateur des frais d'homologation", lede="Estimez les frais d'homologation (ou impôt sur l'administration des successions) dans toute province ou tout territoire. Chaque règle provient d'une source officielle, indiquée ci-dessous.",
  prov="Province ou territoire", choose="Choisir…", value="Valeur estimée de la succession", calc="Calculer",
  feeIs="Frais d'homologation estimés", basis={"gross": "Selon la valeur brute de la succession (avant les dettes).", "net": "Selon la valeur nette de la succession (après les dettes).", "none": "Aucuns frais selon la valeur de la succession."},
  needValue="Entrez la valeur de la succession, en dollars canadiens.", needProv="Choisissez une province ou un territoire.",
  disclaimer=f"Une estimation seulement, et non un conseil juridique ou fiscal. Frais vérifiés auprès des sources officielles le {CHECKED['fr']}. D'autres frais judiciaires ou de dépôt peuvent s'appliquer.",
  source="Source officielle",
  tableTitle="Les frais d'homologation au Canada", tableIntro="Comment chaque province et territoire calcule ses frais, avec la source officielle.",
  colWhere="Province ou territoire", colRule="Calcul des frais", colSource="Source",
  ctaTitle="Facilitez la tâche de votre liquidateur", ctaBody="Un testament clair et valide est la première étape. Faites le vôtre en ligne en environ 20 minutes, selon les règles de votre province.", cta="Commencer mon testament",
  faqTitle="Questions sur l'homologation",
  faq=[
   ("Qu'est-ce que l'homologation ?", "L'homologation est la procédure judiciaire qui confirme la validité d'un testament et donne au liquidateur (ou exécuteur) le pouvoir légal d'administrer la succession. Les banques et les bureaux d'enregistrement l'exigent souvent avant de libérer ou de transférer des biens."),
   ("Quels biens sont pris en compte ?", "En général, les biens transmis par le testament. Les biens assortis d'un bénéficiaire désigné (comme l'assurance vie et, dans la plupart des provinces, les REER, FERR et CELI) et les biens détenus conjointement avec gain de survie sont habituellement transmis hors succession. Les règles varient selon la province : vérifiez auprès d'un professionnel."),
   ("Valeur brute ou valeur nette ?", "La plupart des provinces utilisent la valeur brute, avant les dettes (certaines permettent de déduire les hypothèques). L'Alberta, les Territoires du Nord-Ouest et le Nunavut se basent sur la valeur nette. Le calculateur indique laquelle s'applique."),
   ("Qui paie les frais d'homologation ?", "La succession, habituellement à même ses fonds, au moment où le liquidateur présente la demande. Les bénéficiaires ne les paient pas personnellement."),
   ("Toutes les successions doivent-elles être homologuées ?", "Non. Les petites successions, ou celles dont tous les biens sont transmis hors testament, n'en ont parfois pas besoin. Au Québec, le testament notarié n'a pas à être vérifié. Cela dépend des biens et de ce qu'exigent les banques et les bureaux d'enregistrement."),
   ("Pourquoi certains calculateurs donnent-ils d'autres montants ?", "Les frais changent. Le Nouveau-Brunswick a augmenté son impôt le 12 juin 2026 et le Nunavut a mis à jour ses frais judiciaires en 2021 : d'anciens calculateurs peuvent afficher des montants périmés. Le nôtre indique la date de notre dernière vérification auprès des sources officielles."),
  ],
 ),
}

JS = r"""
(function(){
  var C = function(x, s){ return Math.ceil(x / s); };
  var F = {
    ON: function(v){ return v <= 50000 ? 0 : 15 * C(v - 50000, 1000); },
    QC: function(){ return 0; },
    BC: function(v){ if (v <= 25000) return 0; return 6 * C(Math.min(v, 50000) - 25000, 1000) + (v > 50000 ? 14 * C(v - 50000, 1000) : 0); },
    AB: function(v){ return v <= 10000 ? 35 : v <= 25000 ? 135 : v <= 125000 ? 275 : v <= 250000 ? 400 : 525; },
    SK: function(v){ return v <= 0 ? 0 : 7 * C(v, 1000); },
    MB: function(){ return 0; },
    NB: function(v){ if (v <= 20000) return 200; return 200 + 5 * C(Math.min(v, 100000) - 20000, 1000) + (v > 100000 ? 15 * C(v - 100000, 1000) : 0); },
    NS: function(v){ return v <= 10000 ? 85.60 : v <= 25000 ? 215.20 : v <= 50000 ? 358.15 : v <= 100000 ? 1002.65 : 1002.65 + 16.95 * C(v - 100000, 1000); },
    PE: function(v){ return v <= 10000 ? 50 : v <= 25000 ? 100 : v <= 50000 ? 200 : v <= 100000 ? 400 : 400 + 4 * C(v - 100000, 1000); },
    NL: function(v){ return v <= 1000 ? 60 : 60 + 0.60 * C(v - 1000, 100); },
    YT: function(v){ return v <= 25000 ? 0 : 140; },
    NT: function(v){ return v <= 10000 ? 30 : v <= 25000 ? 110 : v <= 125000 ? 215 : v <= 250000 ? 325 : 435; },
    NU: function(v){ return v <= 10000 ? 30 : v <= 25000 ? 110 : v <= 125000 ? 215 : v <= 250000 ? 325 : 425; }
  };
  window.veewillProbateFee = function(code, v){ return Math.round(F[code](v) * 100) / 100; };
  var form = document.getElementById('probate-form');
  if (!form) return;
  var D = JSON.parse(document.getElementById('probate-data').textContent);
  var money = new Intl.NumberFormat(D.locale, { style: 'currency', currency: 'CAD' });
  var input = document.getElementById('estate-value'), sel = document.getElementById('estate-prov');
  var out = document.getElementById('probate-result'), err = document.getElementById('probate-error');
  input.addEventListener('input', function(){ err.textContent = ''; });
  sel.addEventListener('change', function(){ err.textContent = ''; });
  form.addEventListener('submit', function(e){
    e.preventDefault();
    var code = sel.value, v = parseFloat(String(input.value).replace(/[^0-9.]/g, ''));
    if (!code) { err.textContent = D.needProv; out.hidden = true; sel.focus(); return; }
    if (!(v >= 0)) { err.textContent = D.needValue; out.hidden = true; input.focus(); return; }
    var j = D.jur[code], fee = window.veewillProbateFee(code, v);
    out.innerHTML = '<p class="calc-label">' + D.feeIs + ' · ' + j.name + '</p>' +
      '<p class="calc-fee">' + money.format(fee) + '</p>' +
      '<p class="calc-basis">' + D.basis[j.basis] + '</p>' +
      '<p class="calc-rule">' + j.rule + '</p>' +
      '<p class="calc-source">' + D.source + ': ' + (j.url ? '<a href="' + j.url + '" rel="noopener" target="_blank">' + j.src + '</a>' : j.src) + '</p>';
    out.hidden = false; out.focus();
  });
})();
"""

def probate(lang):
    t = T[lang]
    here = path_of("probate", lang)
    name = (lambda r: r[1]) if lang == "en" else (lambda r: r[2])
    opts = "".join(f'<option value="{r[0]}">{name(r)}</option>' for r in sorted(JUR, key=lambda r: name(r)))
    data = {"locale": "en-CA" if lang == "en" else "fr-CA", "feeIs": t["feeIs"], "basis": t["basis"], "source": t["source"],
            "needValue": t["needValue"], "needProv": t["needProv"],
            "jur": {r[0]: {"name": name(r), "basis": r[3], "rule": RULE[lang][r[0]], "src": r[4], "url": r[5]} for r in JUR}}
    rows = "".join(
        f'<tr><th scope="row">{name(r)}</th><td>{RULE[lang][r[0]]}</td><td>'
        + (f'<a href="{r[5]}" rel="noopener" target="_blank">{r[4]}</a>' if r[5] else r[4]) + '</td></tr>'
        for r in JUR)
    faqs = "".join(f'<details class="qa"><summary>{q}</summary><p>{a}</p></details>' for q, a in t["faq"])
    schema = [
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]},
        {"@context": "https://schema.org", "@type": "WebApplication", "name": t["h1"], "url": f"{SITE}/{here}",
         "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "inLanguage": f"{lang}-CA",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "CAD"}, "dateModified": "2026-10-12"},
    ]
    head = "".join('<script type="application/ld+json">' + json.dumps(s, ensure_ascii=False) + "</script>" for s in schema)
    body = f'''
  <section class="page-hero">
    <div class="wrap">
      <h1>{t["h1"]}</h1>
      <p class="lede">{t["lede"]}</p>
    </div>
  </section>
  <section class="paper">
    <div class="wrap narrow">
      <form id="probate-form" class="calc" novalidate>
        <div class="calc-field"><label for="estate-prov">{t["prov"]}</label>
          <select id="estate-prov" required><option value="">{t["choose"]}</option>{opts}</select></div>
        <div class="calc-field"><label for="estate-value">{t["value"]}</label>
          <div class="calc-money"><span aria-hidden="true">$</span><input id="estate-value" inputmode="decimal" autocomplete="off" placeholder="500000" required></div></div>
        <button type="submit" class="btn btn-gold">{t["calc"]}</button>
        <p id="probate-error" class="calc-error" role="alert"></p>
        <div id="probate-result" class="calc-result" tabindex="-1" aria-live="polite" hidden></div>
        <p class="calc-note">{t["disclaimer"]}</p>
      </form>
      <h2 class="calc-h2">{t["tableTitle"]}</h2>
      <p>{t["tableIntro"]}</p>
      <div class="calc-table-wrap"><table class="calc-table"><thead><tr><th scope="col">{t["colWhere"]}</th><th scope="col">{t["colRule"]}</th><th scope="col">{t["colSource"]}</th></tr></thead><tbody>{rows}</tbody></table></div>
      <h2 class="calc-h2">{t["faqTitle"]}</h2>
      <div class="qas">{faqs}</div>
      <div class="still"><h2>{t["ctaTitle"]}</h2><p>{t["ctaBody"]}</p><p><a class="btn btn-gold" href="{APP_START}">{t["cta"]}</a></p></div>
    </div>
  </section>
  <script type="application/json" id="probate-data">{json.dumps(data, ensure_ascii=False)}</script>
  <script>{JS}</script>'''
    return t["title"], t["desc"], body, head
