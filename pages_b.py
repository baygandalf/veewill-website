import json, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
from data import EMAIL, APP, APP_START
from layout import path_of, rel

EN = json.load(open(os.path.join(HERE, "en.json")))
FR = json.load(open(os.path.join(HERE, "fr.json")))
def S(lang): return EN if lang == "en" else FR
def link(here, key, lang): return rel(here, path_of(key, lang))
def mail(subject=None):
    q = f"?subject={subject.replace(' ', '%20')}" if subject else ""
    return f'<a href="mailto:{EMAIL}{q}">{EMAIL}</a>'

# ---------------------------------------------------------------- FAQ
def faq(lang):
    here = path_of("faq", lang)
    h = S(lang)["help"]
    if lang == "en":
        extra_start = [
          ("Can I start for free?", "Yes. Drafting your will is free, and you don't need an account to start. Create a free account to save your progress and pick up on another device. You pay once when you choose a plan."),
          ("Which provinces does VeeWill cover?", "All 10 provinces and 3 territories: Wills, powers of attorney and health care directives everywhere in Canada, written for each province's and territory's rules. Nunavut has no law for health care directives, so there VeeWill prepares Health Care Wishes: your care wishes and who you want to speak for you, which doctors and family can rely on as guidance, though it isn't legally binding. If you live outside Canada but own property here, an Expat Will covers that property."),
          ("What language is my will in?", "You can use VeeWill in English, French, Turkish, Polish or German, and talk to VeeWill AI in any language. Your will is prepared in English (or French in Québec), the languages Canadian courts and banks work with. That's the version you sign, so make sure you understand it fully: if English isn't your first language, ask someone you trust or a professional to go through it with you."),
        ]
        security = ("Is my personal information secure?", "Your information and documents are encrypted in transit and at rest, and they're released only to the people you choose in Release Settings. We never sell your data. We share it only with the service providers needed to run VeeWill, as our Privacy Policy explains.")
        c = dict(title="Help & FAQ | VeeWill", desc="Answers to common questions about VeeWill, making a valid will in Canada, plans, executors and privacy.",
                 still="Still have a question?", stillP=f"Email us at {mail('VeeWill Support Request')}. We typically respond within 24 hours on business days.")
    else:
        extra_start = [
          ("Puis-je commencer gratuitement ?", "Oui. La rédaction de votre testament est gratuite, et aucun compte n'est requis pour commencer. Créez un compte gratuit pour enregistrer votre progression et la reprendre sur un autre appareil. Vous payez une seule fois quand vous choisissez un forfait."),
          ("Quelles provinces VeeWill couvre-t-il ?", "Les 10 provinces et les 3 territoires : testaments, procurations et directives de soins de santé partout au Canada, rédigés selon les règles de chaque province et territoire. Le Nunavut n'a pas de loi sur les directives de soins de santé; VeeWill y prépare donc des volontés en matière de soins de santé : vos souhaits de soins et la personne que vous voulez voir parler en votre nom, dont les médecins et la famille peuvent s'inspirer, mais qui n'ont pas force obligatoire. Si vous habitez à l'étranger mais possédez des biens ici, un testament d'expatrié couvre ces biens."),
          ("En quelle langue est rédigé mon testament ?", "Vous pouvez utiliser VeeWill en français, en anglais, en turc, en polonais ou en allemand, et discuter avec VeeWill AI dans la langue de votre choix. Votre testament est rédigé en anglais (ou en français au Québec), les langues avec lesquelles travaillent les tribunaux et les banques au Canada. C'est cette version que vous signez : assurez-vous de bien la comprendre et, si l'anglais n'est pas votre langue première, demandez à une personne de confiance ou à un professionnel de la relire avec vous."),
        ]
        security = ("Mes renseignements personnels sont-ils protégés ?", "Vos renseignements et vos documents sont chiffrés en transit et au repos, et ils ne sont transmis qu'aux personnes que vous choisissez dans les paramètres de transmission. Nous ne vendons jamais vos données. Nous les partageons uniquement avec les fournisseurs de services nécessaires au fonctionnement de VeeWill, comme l'explique notre politique de confidentialité.")
        c = dict(title="Aide et FAQ | VeeWill", desc="Réponses aux questions courantes sur VeeWill, la validité d'un testament au Canada, les forfaits, les liquidateurs et la confidentialité.",
                 still="Vous avez encore une question ?", stillP=f"Écrivez-nous à {mail('Demande de soutien VeeWill')}. Nous répondons habituellement dans les 24 heures, les jours ouvrables.")
    groups = [
      (h["catGettingStarted"], [(h["startQ1"], h["startA1"]), (h["startQ2"], h["startA2"]), (h["startQ3"], h["startA3"])] + extra_start),
      (h["catPlansBilling"], [(h["billingQ1"], h["billingA1"]), (h["billingQ2"], h["billingA2"]), (h["billingQ4"], h["billingA4"]), (h["billingQ3"], h["billingA3"])]),
      (h["catExecutors"], [(h["executorQ1"], h["executorA1"]), (h["executorQ2"], h["executorA2"])]),
      (h["catSecurity"], [security, (h["securityQ2"], h["legalAdviceNote"])]),
    ]
    blocks, ld = "", []
    for i, (title, qs) in enumerate(groups):
        items = "".join(f'<details class="qa"><summary>{q}</summary><p>{a}</p></details>' for q, a in qs)
        blocks += f'<section class="qa-group" aria-labelledby="g{i}"><h2 id="g{i}">{title}</h2><div class="qas">{items}</div></section>'
        ld += [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]
    toc = "".join(f'<a href="#g{i}">{t}</a>' for i, (t, _) in enumerate(groups))
    schema = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ld}, ensure_ascii=False) + "</script>"
    body = f'''
  <section class="page-hero">
    <div class="wrap">
      <h1>{h["heroTitle"]}</h1>
      <p class="lede">{h["heroSubtitle"]}</p>
      <nav class="chips-nav" aria-label="{h["heroTitle"]}">{toc}</nav>
    </div>
  </section>
  <section class="paper">
    <div class="wrap narrow">
      {blocks}
      <div class="still"><h2>{c["still"]}</h2><p>{c["stillP"]}</p></div>
    </div>
  </section>'''
    return c["title"], c["desc"], body, schema

# ---------------------------------------------------------------- About
def about(lang):
    here = path_of("about", lang)
    note = S(lang)["help"]["legalAdviceNote"]
    if lang == "en":
        c = dict(title="About VeeWill | VeeWill", desc="VeeWill helps Canadians make a real will online, in plain language, for their province.",
          h1="About VeeWill", lede="VeeWill helps Canadians make a real will without the appointment, the legal jargon or the big bill.",
          sec=[("Why VeeWill", "Most people know they should have a will, and many keep putting it off. Appointments, fees and legal language make it feel bigger than it is. VeeWill turns it into plain questions you can answer at your own pace, on your phone or computer, and stop and pick up whenever you like."),
               ("What VeeWill does", "VeeWill asks about your family, your wishes and the people you trust, then prepares a will worded for your province, including Québec civil law. You can answer the questions yourself or describe things in your own words to VeeWill AI. When you're done, you print your will and sign it with two witnesses. VeeWill also keeps your signed copy in a private Vault and lets you choose who can reach your documents, and when."),
               ("Built for Canada", "VeeWill works in English, French, Turkish, Polish and German, covers every province and territory, and uses the right terms where you live: executors in common-law provinces, liquidators in Québec. Your will is prepared in English, or French in Québec, the languages Canadian courts and banks work with. Prices are in Canadian dollars, with one payment and nothing that renews by itself."),
               ("What VeeWill isn't", note)],
          start="Start my will", contact="Contact us")
    else:
        c = dict(title="À propos de VeeWill | VeeWill", desc="VeeWill aide les Canadiens à rédiger un vrai testament en ligne, en mots simples, adapté à leur province.",
          h1="À propos de VeeWill", lede="VeeWill aide les Canadiens à rédiger un vrai testament, sans rendez-vous, sans jargon juridique et sans grosse facture.",
          sec=[("Pourquoi VeeWill", "La plupart des gens savent qu'ils devraient avoir un testament, et beaucoup remettent ça à plus tard. Les rendez-vous, les frais et le langage juridique donnent l'impression que c'est plus compliqué que ça ne l'est. VeeWill en fait des questions simples, auxquelles vous répondez à votre rythme, sur votre téléphone ou votre ordinateur, en vous arrêtant et en reprenant quand vous voulez."),
               ("Ce que fait VeeWill", "VeeWill vous pose des questions sur votre famille, vos volontés et les personnes en qui vous avez confiance, puis prépare un testament rédigé pour votre province, y compris selon le droit civil du Québec. Vous pouvez répondre vous-même aux questions ou tout expliquer dans vos mots à VeeWill AI. Une fois terminé, vous imprimez votre testament et le signez devant deux témoins. VeeWill garde aussi votre copie signée dans un coffre-fort privé et vous laisse choisir qui peut consulter vos documents, et quand."),
               ("Conçu pour le Canada", "VeeWill fonctionne en français, en anglais, en turc, en polonais et en allemand, couvre toutes les provinces et tous les territoires et emploie les bons termes selon l'endroit où vous habitez : liquidateur au Québec, exécuteur testamentaire ailleurs. Votre testament est rédigé en anglais, ou en français au Québec, les langues avec lesquelles travaillent les tribunaux et les banques au Canada. Les prix sont en dollars canadiens, avec un seul paiement et rien qui se renouvelle tout seul."),
               ("Ce que VeeWill n'est pas", note)],
          start="Commencer mon testament", contact="Nous joindre")
    secs = "".join(f"<h2>{a}</h2><p>{b}</p>" for a, b in c["sec"])
    body = f'''
  <section class="page-hero">
    <div class="wrap">
      <h1>{c["h1"]}</h1>
      <p class="lede">{c["lede"]}</p>
    </div>
  </section>
  <section class="paper">
    <div class="wrap narrow prose">{secs}
      <p class="prose-ctas"><a class="btn btn-night" href="{APP_START}">{c["start"]}</a> <a class="btn btn-line" href="{link(here,'contact',lang)}">{c["contact"]}</a></p>
    </div>
  </section>'''
    return c["title"], c["desc"], body, ""

# ---------------------------------------------------------------- Contact
def contact(lang):
    here = path_of("contact", lang)
    k = S(lang)["contactSupport"]
    note = S(lang)["help"]["legalAdviceNote"]
    helps = "".join(f"<li>{k['helpItem'+str(i)]}</li>" for i in [1, 2, 3, 4, 6])
    if lang == "en":
        c = dict(title="Contact VeeWill | VeeWill", desc="Email VeeWill support. We typically respond within 24 hours on business days.",
                 h1="Contact us", privT="Privacy requests",
                 priv="To see, correct or delete the information we hold about you, or to delete your account and everything in it, email us from the address on your account and tell us what you'd like done.")
    else:
        c = dict(title="Nous joindre | VeeWill", desc="Écrivez au soutien VeeWill. Nous répondons habituellement dans les 24 heures, les jours ouvrables.",
                 h1="Nous joindre", privT="Demandes liées à vos renseignements",
                 priv="Pour consulter, corriger ou supprimer les renseignements que nous détenons à votre sujet, ou pour supprimer votre compte et tout son contenu, écrivez-nous depuis l'adresse de votre compte en précisant votre demande.")
    hours = k["businessHoursBody"].replace("\n", "<br>")
    body = f'''
  <section class="page-hero">
    <div class="wrap">
      <h1>{c["h1"]}</h1>
      <p class="lede">{k["heroSubtitle"]}.</p>
    </div>
  </section>
  <section class="band band-top0">
    <div class="wrap">
      <div class="contact-grid">
        <div class="mail-card">
          <h2>{k["emailSupport"]}</h2>
          <p class="mail-big">{mail(k["emailSubject"])}</p>
          <p>{k["responseTimeBody"]}.</p>
        </div>
        <div class="tile"><h3>{k["businessHoursTitle"]}</h3><p>{hours}</p></div>
        <div class="tile"><h3>{k["beforeContactTitle"]}</h3><p>{k["beforeContactBody"]}</p><p><a href="{link(here,'faq',lang)}">{k["viewFaq"]}</a></p></div>
      </div>
    </div>
  </section>
  <section class="paper">
    <div class="wrap split">
      <div class="prose">
        <h2>{k["whatWeHelpTitle"]}</h2>
        <ul>{helps}</ul>
        <h2>{c["privT"]}</h2>
        <p>{c["priv"]}</p>
      </div>
      <aside class="checklist"><h3>{k["importantNoteTitle"]}</h3><p>{note}</p></aside>
    </div>
  </section>'''
    return c["title"], c["desc"], body, ""

# ---------------------------------------------------------------- Legal pages (app text, word for word)
def legal(kind, lang):
    s = S(lang)[kind]
    parts = []
    i = 1
    while f"s{i}Title" in s:
        parts.append(f"<h2>{s[f's{i}Title']}</h2>")
        parts.append(f"<p>{s[f's{i}Body'].replace('{{email}}', mail())}</p>")
        bullets = [s[f"s{i}Bullet{j}"] for j in range(1, 10) if f"s{i}Bullet{j}" in s]
        if bullets:
            parts.append("<ul>" + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>")
        i += 1
    eff = s["effectiveDate"].replace("[Launch Date]", '<mark class="todo">[Launch Date]</mark>')
    body = f'''
  <section class="page-hero">
    <div class="wrap">
      <h1>{s["title"]}</h1>
      <p class="lede">{s["reassurance"]}</p>
    </div>
  </section>
  <section class="paper">
    <div class="wrap narrow prose legal">
      <p class="eff">{eff}</p>
      <p>{s["intro"]}</p>
      {"".join(parts)}
    </div>
  </section>'''
    desc = s["intro"]
    return f'{s["title"]} | VeeWill', desc, body, ""

def privacy(lang): return legal("privacy", lang)
def terms(lang): return legal("terms", lang)


# ---------------------------------------------------------------- Delete your account
# Linked from Google Play's Data safety form ("Delete account URL"), which asks
# for the app's name, the steps to request deletion, and what is deleted or
# kept and for how long. Mirrors supabase/functions/delete-account in the app.
def deleteAccount(lang):
    here = path_of("deleteAccount", lang)
    if lang == "en":
        c = dict(title="Delete your VeeWill account | VeeWill",
          desc="How to delete your VeeWill account and everything stored with it, in the app or by email.",
          h1="Delete your VeeWill account",
          lede="You can delete your VeeWill account, and everything stored with it, at any time.",
          appT="In the VeeWill app (fastest)",
          app=["Open the VeeWill app or app.veewill.ca and sign in.", "Go to <strong>Settings</strong>, then <strong>Your data</strong>.",
               "Tap <strong>Delete my account</strong> and confirm with your account's email address.",
               "Your account and data are deleted right away."],
          guest="Using VeeWill without an account? Your answers are saved only on that device: go to <strong>Settings → Your data → Delete my data</strong> to erase them.",
          mailT="Without the app",
          mail=f"Email us at {mail('Delete my VeeWill account')} <strong>from the email address on your account</strong>, with the subject \"Delete my VeeWill account\". We'll confirm it's you, delete your account and data, and reply to let you know, within 30 days.",
          goneT="What's deleted",
          gone=["Your account and sign-in", "Every version of your Will, your Power of Attorney and Health Care Directive, and your drafts",
                "Notes for loved ones, funeral wishes and your executor file", "Files in your Vault, including your signed Will",
                "Your trusted access and release settings, and your link with a partner"],
          keptT="What's kept, and for how long",
          kept=["Records of payments, kept by our payment providers (Stripe, Apple or Google) for tax and legal reasons, for as long as the law requires.",
                "Anything you added to someone else's account stays with that person, for example a report you made about another person's Will.",
                "Short-lived usage counts for VeeWill AI, which are deleted automatically within two days.",
                "Copies in our backups, which are erased as those backups expire."],
          note="Deleting your account can't be undone. If you've printed and signed your Will, the paper copy is still valid: deleting your account doesn't cancel it.",
          partT="Delete some of your data and keep your account",
          partApp="In the app, you can remove items yourself at any time: change or clear any answer in your Will or documents, and use <strong>Remove</strong> on notes for loved ones and their attachments, people, gifts and entries in your asset list.",
          partMail=f"For anything else, such as your signed Will in the Vault, a whole document or an earlier version of your Will, email {mail('Delete some of my VeeWill data')} from the email address on your account and tell us what to delete. We'll delete it and reply, within 30 days. Your account stays open.",
          partKept="What's kept is the same as above.")
    else:
        c = dict(title="Supprimer votre compte VeeWill | VeeWill",
          desc="Comment supprimer votre compte VeeWill et tout ce qui y est enregistré, dans l'application ou par courriel.",
          h1="Supprimer votre compte VeeWill",
          lede="Vous pouvez supprimer votre compte VeeWill, et tout ce qui y est enregistré, en tout temps.",
          appT="Dans l'application VeeWill (le plus rapide)",
          app=["Ouvrez l'application VeeWill ou app.veewill.ca et connectez-vous.", "Allez dans <strong>Réglages</strong>, puis <strong>Vos données</strong>.",
               "Touchez <strong>Supprimer mon compte</strong> et confirmez avec l'adresse courriel de votre compte.",
               "Votre compte et vos données sont supprimés immédiatement."],
          guest="Vous utilisez VeeWill sans compte ? Vos réponses sont enregistrées uniquement sur cet appareil : allez dans <strong>Réglages → Vos données → Supprimer mes données</strong> pour les effacer.",
          mailT="Sans l'application",
          mail=f"Écrivez-nous à {mail('Supprimer mon compte VeeWill')} <strong>depuis l'adresse courriel de votre compte</strong>, avec l'objet « Supprimer mon compte VeeWill ». Nous confirmerons qu'il s'agit bien de vous, supprimerons votre compte et vos données, et vous répondrons, dans un délai de 30 jours.",
          goneT="Ce qui est supprimé",
          gone=["Votre compte et votre connexion", "Toutes les versions de votre testament, votre procuration et votre directive de soins de santé, ainsi que vos brouillons",
                "Vos notes pour vos proches, vos volontés funéraires et votre dossier du liquidateur", "Les fichiers de votre coffre-fort, y compris votre testament signé",
                "Vos paramètres d'accès de confiance et de transmission, et votre lien avec un partenaire"],
          keptT="Ce qui est conservé, et pendant combien de temps",
          kept=["Les relevés de paiement, conservés par nos fournisseurs de paiement (Stripe, Apple ou Google) pour des raisons fiscales et légales, aussi longtemps que la loi l'exige.",
                "Ce que vous avez ajouté au compte d'une autre personne reste avec elle, par exemple un signalement fait au sujet du testament de quelqu'un d'autre.",
                "Les compteurs d'utilisation de VeeWill AI, effacés automatiquement en deux jours.",
                "Les copies dans nos sauvegardes, effacées à mesure que ces sauvegardes expirent."],
          note="La suppression de votre compte est définitive. Si vous avez imprimé et signé votre testament, la copie papier reste valide : supprimer votre compte ne l'annule pas.",
          partT="Supprimer une partie de vos données et garder votre compte",
          partApp="Dans l'application, vous pouvez retirer des éléments vous-même en tout temps : modifiez ou effacez n'importe quelle réponse de votre testament ou de vos documents, et utilisez <strong>Retirer</strong> sur les notes pour vos proches et leurs pièces jointes, les personnes, les dons et les éléments de votre liste de biens.",
          partMail=f"Pour tout le reste, comme votre testament signé dans le coffre-fort, un document entier ou une version antérieure de votre testament, écrivez à {mail('Supprimer une partie de mes données VeeWill')} depuis l'adresse courriel de votre compte en précisant ce qu'il faut supprimer. Nous le supprimerons et vous répondrons, dans un délai de 30 jours. Votre compte reste ouvert.",
          partKept="Ce qui est conservé est le même que ci-dessus.")
    steps = "".join(f"<li>{x}</li>" for x in c["app"])
    gone = "".join(f"<li>{x}</li>" for x in c["gone"])
    kept = "".join(f"<li>{x}</li>" for x in c["kept"])
    body = f'''
  <section class="page-hero">
    <div class="wrap">
      <h1>{c["h1"]}</h1>
      <p class="lede">{c["lede"]}</p>
    </div>
  </section>
  <section class="paper">
    <div class="wrap narrow prose">
      <h2>{c["appT"]}</h2>
      <ol>{steps}</ol>
      <p>{c["guest"]}</p>
      <h2>{c["mailT"]}</h2>
      <p>{c["mail"]}</p>
      <h2>{c["goneT"]}</h2>
      <ul>{gone}</ul>
      <h2>{c["keptT"]}</h2>
      <ul>{kept}</ul>
      <p><strong>{c["note"]}</strong></p>
      <h2 id="delete-some-data">{c["partT"]}</h2>
      <p>{c["partApp"]}</p>
      <p>{c["partMail"]}</p>
      <p>{c["partKept"]}</p>
    </div>
  </section>'''
    return c["title"], c["desc"], body, ""

# ---------------------------------------------------------------- 404 (bilingual)
def notfound():
    body = '''
  <section class="page-hero nf">
    <div class="wrap">
      <h1>Page not found</h1>
      <p class="lede">This page doesn't exist or has moved.</p>
      <div class="hero-ctas"><a class="btn btn-gold" href="/">Go to the homepage</a></div>
      <h2 lang="fr-CA" class="nf-fr">Page introuvable</h2>
      <p class="lede" lang="fr-CA">Cette page n'existe pas ou a été déplacée.</p>
      <div class="hero-ctas" lang="fr-CA"><a class="btn btn-ghost" href="/fr/">Aller à l'accueil</a></div>
    </div>
  </section>'''
    return "Page not found | VeeWill", "This page doesn't exist.", body, '<meta name="robots" content="noindex">'
