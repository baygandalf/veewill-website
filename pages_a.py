from data import price, saving, fmt, P, APP, APP_START, APP_STORE_URL, PLAY_STORE_URL
from components import T, toggle, plan_cards, compare_rows, both
from layout import path_of, rel

def link(here, key, lang):
    return rel(here, path_of(key, lang))


def store_buttons(c):
    """The hero's App Store and Google Play buttons. Text-only on purpose: when
    the apps are published, Apple's and Google's official badge artwork can
    replace them (both require their own badges in marketing). Without a store
    link a button is greyed out and isn't a link, and one line under the
    buttons says the app is coming soon."""
    out = ""
    any_soon = False
    for platform, url, top, name in (
        ("ios", APP_STORE_URL, c["iosTop"], c["iosName"]),
        ("android", PLAY_STORE_URL, c["andTop"], c["andName"]),
    ):
        inner = f'<span class="store-top">{top}</span><span class="store-name">{name}</span>'
        if url:
            out += f'<a class="store store-{platform}" href="{url}" rel="noopener">{inner}</a>'
        else:
            any_soon = True
            out += f'<span class="store store-{platform} is-soon" aria-disabled="true">{inner}</span>'
    note = f'<p class="stores-note">{c["soon"]}</p>' if any_soon else ""
    return (f'<div class="stores-wrap"><div class="stores" role="group" '
            f'aria-label="{c["storesLabel"]}">{out}</div>{note}</div>')

# ---------------------------------------------------------------- Home
def home(lang):
    here = path_of("home", lang)
    t = T[lang]
    if lang == "en":
        c = dict(
          title="VeeWill | Your will, made simple",
          desc="A real will, written for your province. Answer simple questions or chat with VeeWill AI on your phone or computer. Start free, pay once when you're ready.",
          pill="<b>New</b>Chat your way through your will",
          h1="A real will. <span class=\"accent\">No lawyer's office.</span>",
          lede="VeeWill walks you through a will written for your province, on your phone or computer. Your progress syncs everywhere. When it's ready, you print it and sign it with two witnesses.",
          start="Start my will", plans="See plans", note="Drafting is free. No account needed to start.",
          storesLabel="VeeWill on your phone", soon="The VeeWill app for iPhone and Android is coming soon.",
          iosTop="Download on the", iosName="App Store", andTop="Get it on", andName="Google Play",
          step="Executors", q="Who will carry out your Will?",
          b1="Your executor settles your estate. Who would you trust with that?", b2="My sister, Layla",
          b3="Good choice. What is her full legal name?", c1="Add a second executor", c2="What does an executor do?",
          how="Done in three steps",
          s=[("Answer or chat", "Tap through plain questions, or tell VeeWill AI in your own words and it fills in the form for you."),
             ("Review and download", "Check every choice on one summary screen, then download your print-ready will."),
             ("Sign with two witnesses", "Print it and sign in front of two adult witnesses, as your province requires. That's what makes it valid.")],
          f=[("Every province and territory", "Wording follows each province's and territory's rules, including Québec civil law."),
             ("Phone and web, synced", "Start on one, finish on the other."),
             ("English, French, Turkish, Polish and German", "Use the app in your language. Your will is prepared in English, or French in Québec."),
             ("Trusted access", "Choose who can reach your documents, and when.")],
          more="See how it works in detail",
          e1t="Just need one document?",
          e1=f"Financial Power of Attorney <strong>{price('financialPoa')}</strong>, Health Care Directive <strong>{price('healthDirective')}</strong>. Complete Protection includes both.",
          e2t="After the first year",
          e2=f"Renew your VeeWill Membership for <strong>{price('membership')}</strong> to keep making changes. Your documents stay yours to download either way.",
          e3t="Live outside Canada?",
          e3=f"An Expat Will covers your property in Canada, alongside the will where you live. From <strong>{price('expatCanada')}</strong>.",
          compare="Compare plans in detail",
        )
    else:
        c = dict(
          title="VeeWill | Votre testament, en toute simplicité",
          desc="Un vrai testament, rédigé pour votre province. Répondez à des questions simples ou discutez avec VeeWill AI, sur téléphone ou ordinateur. Commencez gratuitement, payez une seule fois quand vous êtes prêt.",
          pill="<b>Nouveau</b>Rédigez votre testament en discutant",
          h1="Un vrai testament. <span class=\"accent\">Sans rendez-vous chez l'avocat.</span>",
          lede="VeeWill vous guide vers un testament rédigé pour votre province, sur votre téléphone ou votre ordinateur. Votre progression se synchronise partout. Une fois prêt, vous l'imprimez et le signez devant deux témoins.",
          start="Commencer mon testament", plans="Voir les forfaits", note="La rédaction est gratuite. Aucun compte requis pour commencer.",
          storesLabel="VeeWill sur votre téléphone", soon="L'application VeeWill pour iPhone et Android arrive bientôt.",
          iosTop="Télécharger dans", iosName="l'App Store", andTop="Disponible sur", andName="Google Play",
          step="Liquidateurs", q="Qui exécutera votre testament ?",
          b1="Votre liquidateur règle votre succession. À qui feriez-vous confiance ?", b2="Ma sœur, Layla",
          b3="Bon choix. Quel est son nom légal complet ?", c1="Ajouter un 2<sup>e</sup> liquidateur", c2="Que fait un liquidateur ?",
          how="Trois étapes, et c'est fait",
          s=[("Répondez ou discutez", "Touchez des réponses simples, ou expliquez-vous à VeeWill AI dans vos mots : il remplit le formulaire pour vous."),
             ("Révisez et téléchargez", "Vérifiez tous vos choix sur un seul écran de résumé, puis téléchargez votre testament prêt à imprimer."),
             ("Signez devant deux témoins", "Imprimez-le et signez-le devant deux témoins majeurs, comme l'exige votre province. C'est ce qui le rend valide.")],
          f=[("Chaque province et territoire", "La rédaction suit les règles de chaque province et territoire, y compris le droit civil du Québec."),
             ("Téléphone et Web, synchronisés", "Commencez sur l'un, terminez sur l'autre."),
             ("Français, anglais, turc, polonais et allemand", "Utilisez l'application dans votre langue. Votre testament est rédigé en anglais, ou en français au Québec."),
             ("Accès de confiance", "Choisissez qui peut consulter vos documents, et quand.")],
          more="Voir le fonctionnement en détail",
          e1t="Besoin d'un seul document ?",
          e1=f"Procuration financière <strong>{price('financialPoa')}</strong>, directive de soins de santé <strong>{price('healthDirective')}</strong>. La Protection complète inclut les deux.",
          e2t="Après la première année",
          e2=f"Renouvelez votre adhésion VeeWill pour <strong>{price('membership')}</strong> afin de continuer à faire des modifications. Vos documents restent à vous, à télécharger quand vous voulez.",
          e3t="Vous habitez à l'étranger ?",
          e3=f"Un testament d'expatrié couvre vos biens au Canada, en plus de celui de votre pays. À partir de <strong>{price('expatCanada')}</strong>.",
          compare="Comparer les forfaits en détail",
        )
    steps = "".join(f'''
        <li><span class="num" aria-hidden="true">{i+1}</span><h3>{a}</h3><p>{b}</p></li>''' for i, (a, b) in enumerate(c["s"]))
    facts = "".join(f"<div><h3>{a}</h3><p>{b}</p></div>" for a, b in c["f"])
    body = f'''
  <section class="hero">
    <div class="wrap">
      <div class="hero-copy">
        <p class="pill">{c["pill"]}</p>
        <h1>{c["h1"]}</h1>
        <p class="lede">{c["lede"]}</p>
        <div class="hero-ctas">
          <a class="btn btn-gold" href="{APP_START}">{c["start"]}</a>
          <a class="btn btn-ghost" href="#pricing">{c["plans"]}</a>
        </div>
        <p class="hero-note">{c["note"]}</p>
        {store_buttons(c)}
      </div>
      <div class="stage" aria-hidden="true">
        <div class="phone"><div class="screen">
          <img class="screen-logo" src="{{ROOT}}assets/veewill-mark.png" alt="" width="38" height="24">
          <div class="screen-step">{c["step"]}</div>
          <div class="screen-bar"><span></span></div>
          <div class="screen-title">{c["q"]}</div>
          <div class="play">
            <div class="screen-who">VeeWill AI</div>
            <div class="bubble ai">{c["b1"]}</div>
            <div class="bubble me">{c["b2"]}</div>
            <div class="screen-who">VeeWill AI</div>
            <div class="bubble ai">{c["b3"]}</div>
            <div class="chips"><span>{c["c1"]}</span><span>{c["c2"]}</span></div>
          </div>
        </div></div>
      </div>
    </div>
  </section>

  <section class="how" id="how" aria-labelledby="how-title">
    <div class="wrap">
      <h2 id="how-title">{c["how"]}</h2>
      <ol class="steps">{steps}
      </ol>
      <div class="facts">{facts}</div>
      <p class="more"><a href="{link(here,'how',lang)}">{c["more"]}</a></p>
    </div>
  </section>

  <section class="pricing" id="pricing" aria-labelledby="pricing-title">
    <div class="wrap">
      <div class="pricing-head">
        <div><h2 id="pricing-title">{t["head"]}</h2><p>{t["headSub"]}</p></div>
        {toggle(lang)}
      </div>
      {plan_cards(lang)}
      <div class="extras">
        <div><h3>{c["e1t"]}</h3><p>{c["e1"]}</p></div>
        <div><h3>{c["e2t"]}</h3><p>{c["e2"]}</p></div>
        <div><h3>{c["e3t"]}</h3><p>{c["e3"]}</p></div>
      </div>
      <p class="more"><a href="{link(here,'pricing',lang)}">{c["compare"]}</a></p>
      <p class="fineprint">{t["refund"]}</p>
    </div>
  </section>'''
    return c["title"], c["desc"], body, ""

# ---------------------------------------------------------------- How it works
def how(lang):
    here = path_of("how", lang)
    if lang == "en":
        c = dict(
          title="How VeeWill works | VeeWill",
          desc="Choose your province, answer simple questions or chat with VeeWill AI, then print and sign your will with two witnesses.",
          h1="How it works",
          lede="Four simple steps to protect your legacy and share it with confidence.",
          steps=[("Choose your province", "Tell us where you live so we can align your Will with your province's legal requirements."),
                 ("Answer simple questions", "We guide you through straightforward questions about your wishes, executors, and beneficiaries."),
                 ("Create your Will", "We generate a clear Will based on your responses, ready for review."),
                 ("Save, download, or share a copy", "Review your will, download a PDF, share a read-only copy, or store it securely in your Vault for later access.")],
          ways="Two ways to answer",
          w1t="Answer the questions", w1="Each step asks plain questions, with a short explanation of why they matter. Tap an answer and move on.",
          w2t="Chat with VeeWill AI", w2="Describe your situation in your own words, in any language. VeeWill AI fills in the form, and you check the answers before you save the step.",
          aiNote="This assistant helps you fill out your will faster. It doesn't provide legal advice.",
          signT="Signing is what makes it valid",
          signP="In most Canadian provinces, a will becomes legally enforceable once it is printed, signed by you, and witnessed according to your province's requirements. A will that is only saved in the app, or signed electronically, is not valid.",
          checkT="Legal readiness checklist",
          check=["Review your will for accuracy", "Print the final version", "Sign the document",
                 "Have it witnessed as required in your province", "Store it somewhere safe and accessible"],
          witT="Choosing your witnesses",
          wit="Sign in front of two adult witnesses who are present at the same time, and who then sign too. A witness should not be a beneficiary, or the spouse or partner of one, or that gift may be void.",
          qcT="Québec residents",
          qc="Québec recognizes notarial, holograph and witnessed Wills. VeeWill prepares one signed in front of two witnesses. A notarial Will, made with a notary, is also an option.",
          proT="Want professional help with signing?",
          pro="Using a law firm to sign your will is optional and not required in most cases. If you'd like it, you can request Law Firm Signing Assistance in the app: we connect you with a law firm in your province to review your ready-to-sign will and supervise the signing. Pricing varies by province.",
          afterT="After you sign",
          a=[("Keep it safe", "Photograph or upload your signed will to your private Vault. The Vault comes with Complete Protection, or as an add-on to the Will plan."),
             ("Choose who sees it, and when", "In Release Settings, choose who VeeWill opens your documents to after you die, and what each person receives. If someone reports a death, we wait the waiting period you chose, and a person on our team checks the proof before anything is released."),
             ("Update it as life changes", "Edit your answers and download a new will, then print, sign and witness it again. The newest signed will replaces earlier ones. Every plan includes a year of updates.")],
          start="Start my will", plans="See plans",
        )
    else:
        c = dict(
          title="Comment fonctionne VeeWill | VeeWill",
          desc="Choisissez votre province, répondez à des questions simples ou discutez avec VeeWill AI, puis imprimez et signez votre testament devant deux témoins.",
          h1="Comment ça fonctionne",
          lede="Quatre étapes simples pour protéger votre héritage et le transmettre en toute confiance.",
          steps=[("Choisissez votre province", "Dites-nous où vous habitez afin que nous puissions adapter votre testament aux exigences légales de votre province."),
                 ("Répondez à des questions simples", "Nous vous guidons à travers des questions claires sur vos volontés, vos liquidateurs et vos bénéficiaires."),
                 ("Créez votre testament", "Nous générons un testament clair à partir de vos réponses, prêt à être révisé."),
                 ("Enregistrez, téléchargez ou partagez une copie", "Révisez votre testament, téléchargez un PDF, partagez une copie en lecture seule ou conservez-le en sécurité dans votre coffre.")],
          ways="Deux façons de répondre",
          w1t="Répondez aux questions", w1="Chaque étape pose des questions simples, avec une courte explication de leur importance. Touchez une réponse et continuez.",
          w2t="Discutez avec VeeWill AI", w2="Décrivez votre situation dans vos mots, dans la langue de votre choix. VeeWill AI remplit le formulaire, et vous vérifiez les réponses avant d'enregistrer l'étape.",
          aiNote="Cet assistant vous aide à remplir votre testament plus rapidement. Il ne fournit pas de conseils juridiques.",
          signT="C'est la signature qui le rend valide",
          signP="Dans la plupart des provinces canadiennes, un testament prend effet légalement une fois imprimé, signé par vous et signé par des témoins selon les exigences de votre province. Un testament seulement enregistré dans l'application, ou signé électroniquement, n'est pas valide.",
          checkT="Liste de vérification",
          check=["Relisez votre testament", "Imprimez la version finale", "Signez le document",
                 "Faites-le signer par des témoins selon les exigences de votre province", "Rangez-le dans un endroit sûr et accessible"],
          witT="Choisir vos témoins",
          wit="Signez devant deux témoins majeurs présents en même temps, qui signent ensuite à leur tour. Un témoin ne devrait pas être bénéficiaire, ni le conjoint d'un bénéficiaire, sinon le legs pourrait être nul.",
          qcT="Résidents du Québec",
          qc="Le Québec reconnaît le testament notarié, le testament olographe et le testament devant témoins. VeeWill prépare un testament signé devant deux témoins. Un testament notarié, fait devant notaire, est aussi possible.",
          proT="Vous aimeriez de l'aide pour la signature ?",
          pro="Faire appel à un cabinet d'avocats pour la signature est facultatif et n'est pas nécessaire dans la plupart des cas. Si vous le souhaitez, demandez l'aide à la signature dans l'application : nous vous mettons en relation avec un cabinet de votre province qui révise votre testament prêt à signer et encadre la signature. Les tarifs varient selon la province.",
          afterT="Après la signature",
          a=[("Gardez-le en sécurité", "Photographiez ou téléversez votre testament signé dans votre coffre-fort privé. Le coffre-fort est inclus dans la Protection complète, ou offert en option avec le forfait Testament."),
             ("Choisissez qui le voit, et quand", "Dans les paramètres de transmission, choisissez à qui VeeWill ouvrira vos documents après votre décès, et ce que chaque personne reçoit. Si quelqu'un signale un décès, nous attendons le délai que vous avez choisi, et une personne de notre équipe vérifie la preuve avant toute transmission."),
             ("Mettez-le à jour quand la vie change", "Modifiez vos réponses et téléchargez un nouveau testament, puis imprimez-le, signez-le et faites-le signer par vos témoins à nouveau. Le testament signé le plus récent remplace les précédents. Chaque forfait inclut un an de mises à jour.")],
          start="Commencer mon testament", plans="Voir les forfaits",
        )
    steps = "".join(f'<li><span class="num" aria-hidden="true">{i+1}</span><h3>{a}</h3><p>{b}</p></li>' for i, (a, b) in enumerate(c["steps"]))
    check = "".join(f"<li>{x}</li>" for x in c["check"])
    after = "".join(f"<div><h3>{a}</h3><p>{b}</p></div>" for a, b in c["a"])
    body = f'''
  <section class="page-hero">
    <div class="wrap">
      <h1>{c["h1"]}</h1>
      <p class="lede">{c["lede"]}</p>
      <div class="hero-ctas"><a class="btn btn-gold" href="{APP_START}">{c["start"]}</a><a class="btn btn-ghost" href="{link(here,'pricing',lang)}">{c["plans"]}</a></div>
    </div>
  </section>

  <section class="how">
    <div class="wrap">
      <ol class="steps steps-4">{steps}</ol>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <h2>{c["ways"]}</h2>
      <div class="duo">
        <div class="tile"><h3>{c["w1t"]}</h3><p>{c["w1"]}</p></div>
        <div class="tile"><h3>{c["w2t"]}</h3><p>{c["w2"]}</p><p class="tile-note">{c["aiNote"]}</p></div>
      </div>
    </div>
  </section>

  <section class="paper">
    <div class="wrap split">
      <div class="prose">
        <h2>{c["signT"]}</h2>
        <p>{c["signP"]}</p>
        <h3>{c["witT"]}</h3>
        <p>{c["wit"]}</p>
        <h3>{c["qcT"]}</h3>
        <p>{c["qc"]}</p>
        <h3>{c["proT"]}</h3>
        <p>{c["pro"]}</p>
      </div>
      <aside class="checklist" aria-labelledby="checklist-title">
        <h3 id="checklist-title">{c["checkT"]}</h3>
        <ol>{check}</ol>
      </aside>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <h2>{c["afterT"]}</h2>
      <div class="extras">{after}</div>
    </div>
  </section>'''
    return c["title"], c["desc"], body, ""

# ---------------------------------------------------------------- Pricing
def pricing(lang):
    here = path_of("pricing", lang)
    t = T[lang]
    yes = "✓"
    if lang == "en":
        c = dict(
          title="Pricing | VeeWill",
          desc="Two plans, one payment each: Will $69.99 and Complete Protection $129.99, with prices for couples. Prices in Canadian dollars.",
          h1="Choose your plan",
          reassure=["Written for your province's laws, in plain language.", "One payment. Nothing renews by itself.", "Your documents are always yours to download."],
          compareT="Compare the two plans", feature="What's included", inc="Included", notInc="Not included",
          updatesRow="1 year of updates", updatesCp="1 year of updates and Vault storage",
          oneT="Just need one document?", oneSub="Each document is also sold on its own. Complete Protection includes both.",
          poaShort="Someone you trust looks after your money if you can't.",
          hcdShort="Your care wishes, and who speaks for you.",
          docItems=["Guided, step-by-step questions", "Print-ready PDF", "Guidance for your province", "Includes 1 year of updates"],
          coupleDoc="Two separate documents, one for each of you.",
          poaName="Financial Power of Attorney", hcdName="Health Care Directive",
          expT="Live outside Canada?", expSub="An Expat Will covers only your property here, and keeps the Will you made where you live in force.",
          ecName="Canada Expat Will", ecShort="A Will for your property in Canada, alongside the one where you live.",
          eqName="Québec Expat Will", eqShort="A Will for your property in Québec, alongside the one where you live.",
          ecItem="Covers your property in Canada only", eqItem="Covers your property in Québec only, in English or French",
          keeps="Keeps your Will from home in force",
          coupleExp="Two separate Expat Wills, one for each of you.",
          addonNote=f"Need both? Bought with a plan, an Expat Will is <strong>{price('expatAddon')}</strong>.",
          laterT="Add more later", 
          later=f"Already on the Will plan? Add the Vault for <strong>{price('vaultAddon')}</strong> or the executor file for <strong>{price('executorFileAddon')}</strong> from your account, anytime.",
          memT="After the first year",
          mem=f"Every plan includes a year of VeeWill Membership, which is what lets you make changes. After that, renew for <strong>{price('membership')}</strong> for one more year. It doesn't renew by itself, and your documents stay yours to download either way.",
          faqT="Questions about plans",
          faq=[("What's the difference between the plans?", "The Will plan gives you your Will, notes for loved ones, your funeral wishes, Release Settings (who receives what after you die) and a year of updates. Complete Protection adds a Financial Power of Attorney, a Health Care Directive, the Vault, an executor file with a checklist for your executor, and up to 5 versions of your Will."),
               ("Can I update my Will after creating it?", "Yes. Edit your answers and download a new Will, then print, sign and witness it again. The newest signed Will replaces earlier ones. Every plan includes a year of VeeWill Membership, which is what lets you make changes; after that you can renew it for a year at a time."),
               ("What happens when my membership ends?", "Nothing is lost. You can still download every document you made, and your Vault and notes are still released to your executor and loved ones. Editing and adding new files pause until you renew. We remind you 30 days and 7 days before it ends, and renewal never happens by itself.")],
          moreFaq="More questions in the FAQ", start="Start my will",
        )
    else:
        c = dict(
          title="Forfaits | VeeWill",
          desc="Deux forfaits, un seul paiement chacun : Testament à $69.99 et Protection complète à $129.99, avec des prix pour les couples. Prix en dollars canadiens.",
          h1="Choisissez votre forfait",
          reassure=["Rédigé selon les lois de votre province, en mots simples.", "Un seul paiement. Rien ne se renouvelle tout seul.", "Vos documents restent toujours à vous, à télécharger quand vous voulez."],
          compareT="Comparer les deux forfaits", feature="Ce qui est inclus", inc="Inclus", notInc="Non inclus",
          updatesRow="1 an de mises à jour", updatesCp="1 an de mises à jour et de stockage dans le coffre-fort",
          oneT="Besoin d'un seul document ?", oneSub="Chaque document est aussi vendu seul. La Protection complète inclut les deux.",
          poaShort="Une personne de confiance gère votre argent si vous ne le pouvez plus.",
          hcdShort="Vos volontés de soins, et qui parle pour vous.",
          docItems=["Questions guidées, étape par étape", "PDF prêt à imprimer", "Conseils propres à votre province", "Comprend 1 an de mises à jour"],
          coupleDoc="Deux documents distincts, un pour chacun de vous.",
          poaName="Procuration financière", hcdName="Directive de soins de santé",
          expT="Vous habitez à l'étranger ?", expSub="Un testament d'expatrié porte uniquement sur vos biens ici, et garde en vigueur le testament fait là où vous habitez.",
          ecName="Testament d'expatrié — Canada", ecShort="Un testament pour vos biens au Canada, en plus de celui de votre pays.",
          eqName="Testament d'expatrié — Québec", eqShort="Un testament pour vos biens au Québec, en plus de celui de votre pays.",
          ecItem="Porte uniquement sur vos biens au Canada", eqItem="Porte uniquement sur vos biens au Québec, en français ou en anglais",
          keeps="Garde en vigueur votre testament fait là où vous habitez",
          coupleExp="Deux testaments d'expatrié distincts, un pour chacun de vous.",
          addonNote=f"Besoin des deux ? Acheté avec un forfait, un testament d'expatrié coûte <strong>{price('expatAddon')}</strong>.",
          laterT="Ajoutez-en plus tard",
          later=f"Vous avez le forfait Testament ? Ajoutez le coffre-fort pour <strong>{price('vaultAddon')}</strong> ou le dossier du liquidateur pour <strong>{price('executorFileAddon')}</strong> depuis votre compte, quand vous voulez.",
          memT="Après la première année",
          mem=f"Chaque forfait inclut un an d'adhésion VeeWill, qui vous permet de faire des modifications. Ensuite, renouvelez pour <strong>{price('membership')}</strong> pour une année de plus. Rien ne se renouvelle tout seul, et vos documents restent à vous, à télécharger quand vous voulez.",
          faqT="Questions sur les forfaits",
          faq=[("Quelle est la différence entre les forfaits ?", "Le forfait Testament vous donne votre testament, des notes pour vos proches, vos volontés funéraires, les paramètres de transmission (qui reçoit quoi après votre décès) et un an de mises à jour. La Protection complète ajoute une procuration financière, une directive de soins de santé, le coffre-fort, un dossier pour votre liquidateur avec une liste de tâches, et jusqu'à 5 versions de votre testament."),
               ("Puis-je mettre à jour mon testament après l'avoir créé ?", "Oui. Modifiez vos réponses et téléchargez un nouveau testament, puis imprimez-le, signez-le et faites-le signer par vos témoins à nouveau. Le testament signé le plus récent remplace les précédents. Chaque forfait inclut un an d'adhésion VeeWill, qui vous permet de faire des modifications; ensuite, vous pouvez la renouveler un an à la fois."),
               ("Que se passe-t-il quand mon adhésion se termine ?", "Rien n'est perdu. Vous pouvez toujours télécharger chaque document que vous avez fait, et votre coffre-fort et vos notes sont toujours remis à votre liquidateur et à vos proches. Les modifications et l'ajout de fichiers sont suspendus jusqu'au renouvellement. Nous vous le rappelons 30 jours et 7 jours avant la fin, et le renouvellement ne se fait jamais tout seul.")],
          moreFaq="Plus de questions dans la FAQ", start="Commencer mon testament",
        )
    reassure = "".join(f"<li>{x}</li>" for x in c["reassure"])
    def mark(v):
        return f'<span class="yes" aria-label="{c["inc"]}">{yes}</span>' if v else f'<span class="no" aria-label="{c["notInc"]}">–</span>'
    rows = "".join(f"<tr><th scope=\"row\">{n}</th><td>{mark(a)}</td><td>{mark(b)}</td></tr>" for n, a, b in compare_rows(lang))
    rows += f'<tr><th scope="row">{c["updatesRow"]}</th><td><span class="yes" aria-label="{c["inc"]}">{yes}</span></td><td><span class="yes" aria-label="{c["inc"]}">{yes}</span></td></tr>'
    def small(name, short, pid, items, note):
        lis = "".join(f"<li>{i}</li>" for i in items)
        return f'''<article class="mini">
          <h3>{name}</h3><p class="short">{short}</p>
          <p class="mini-price">{price(pid)}</p>
          <p class="period" data-for="couple">{note}</p>
          <ul>{lis}</ul>
          <a class="btn btn-ghost" data-plan-link href="{APP}subscription?plan={pid}">{name}</a>
        </article>'''
    docs = small(c["poaName"], c["poaShort"], "financialPoa", c["docItems"], c["coupleDoc"]) + small(c["hcdName"], c["hcdShort"], "healthDirective", c["docItems"], c["coupleDoc"])
    expat = (small(c["ecName"], c["ecShort"], "expatCanada", [c["ecItem"], c["keeps"], c["docItems"][0], c["docItems"][3]], c["coupleExp"]) +
             small(c["eqName"], c["eqShort"], "expatQuebec", [c["eqItem"], c["keeps"], c["docItems"][0], c["docItems"][3]], c["coupleExp"]))
    faq = "".join(f'<details class="qa"><summary>{q}</summary><p>{a}</p></details>' for q, a in c["faq"])
    body = f'''
  <section class="page-hero">
    <div class="wrap">
      <h1>{c["h1"]}</h1>
      <p class="lede">{t["headSub"]}</p>
      <ul class="ticks">{reassure}</ul>
    </div>
  </section>

  <section class="pricing">
    <div class="wrap">
      <div class="pricing-head pricing-head-solo">{toggle(lang)}</div>
      {plan_cards(lang)}
    </div>
  </section>

  <section class="paper" aria-labelledby="compare-title">
    <div class="wrap">
      <h2 id="compare-title">{c["compareT"]}</h2>
      <div class="table-scroll">
        <table class="compare">
          <thead><tr><th scope="col">{c["feature"]}</th><th scope="col">{t["willName"]}<br><span class="th-price">{price("will")}</span></th><th scope="col">{t["cpName"]}<br><span class="th-price">{price("completeProtection")}</span></th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <h2>{c["oneT"]}</h2>
      <p class="section-lede">{c["oneSub"]}</p>
      <div class="duo">{docs}</div>
    </div>
  </section>

  <section class="band band-tight">
    <div class="wrap">
      <h2>{c["expT"]}</h2>
      <p class="section-lede">{c["expSub"]}</p>
      <div class="duo">{expat}</div>
      <p class="fineprint">{c["addonNote"]}</p>
    </div>
  </section>

  <section class="band band-tight">
    <div class="wrap">
      <div class="extras extras-2">
        <div><h3>{c["memT"]}</h3><p>{c["mem"]}</p></div>
        <div><h3>{c["laterT"]}</h3><p>{c["later"]}</p></div>
      </div>
      <p class="fineprint">{t["refund"]}</p>
    </div>
  </section>

  <section class="paper">
    <div class="wrap narrow">
      <h2>{c["faqT"]}</h2>
      <div class="qas">{faq}</div>
      <p class="more"><a href="{link(here,'faq',lang)}">{c["moreFaq"]}</a></p>
    </div>
  </section>'''
    return c["title"], c["desc"], body, ""
