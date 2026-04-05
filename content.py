"""
Single source of truth voor alle inhoud van de Koersbepaling.
Wordt gebruikt door zowel de facilitation app (via /api/content) als de PDF handout.
"""

TITLE = "Koersbepaling Maatschap"
SUBTITLE = "Huisartsenpraktijk Binnenstad Utrecht"
DATE = "Zaterdag 5 april 2026"
TIME_RANGE = "13:00 – 17:00"

SCHEDULE = [
    {"time": "13:00–13:15", "label": "Welkom & binnenkomst", "minutes": 15},
    {"time": "13:15–13:45", "label": "Check-in (huiswerk)", "minutes": 30},
    {"time": "13:45–14:15", "label": "Domein 4 — Organisatie", "minutes": 30},
    {"time": "14:15–14:40", "label": "Pauze", "minutes": 25},
    {"time": "14:40–15:10", "label": "Domein 5 — Medewerkers", "minutes": 30},
    {"time": "15:10–15:40", "label": "Domein 6 — Kansen/bedreigingen", "minutes": 30},
    {"time": "15:40–16:25", "label": "Synthese & actiepunten", "minutes": 45},
    {"time": "16:25–16:40", "label": "Feedbackafspraken", "minutes": 15},
    {"time": "16:40–16:55", "label": "Afsluiting", "minutes": 15},
]

GROUND_RULES = [
    {
        "title": "Doen, niet alleen praten",
        "description": "Elk domein sluit af met een tastbare uitkomst. Discussie stopt zodra we kunnen besluiten.",
    },
    {
        "title": "Twee sporen per domein",
        "description": "Kort (15 min) of uitgebreid (30 min). Bij tijdnood: altijd kort. Liever 6 domeinen kort dan 3 half.",
    },
    {
        "title": "Begin bij onszelf",
        "description": "De sessie opent met een persoonlijke check-in. Pas als iedereen gehoord is, bouwen we de koers op.",
    },
]

# ── CHECK-IN ──

CHECKIN = {
    "title": "Persoonlijke Check-in",
    "subtitle": "Max. 3 minuten per persoon. De rest luistert — geen discussie, wel kort doorvragen.",
    "time": "13:15–13:45",
    "minutes": 30,
    "questions": [
        "Hoe zit jij er nu in — wat geeft je energie?",
        "Wat is voor jou een energie-drain?",
        "Wat heb jij van de maatschap nodig?",
        "Hoe ziet jouw ideale werkdag eruit?",
        "Wat zou je de maatschap willen vragen dat je nu nog niet vraagt?",
    ],
}

# ── ORGANISATIE ──

ORGANISATIE = {
    "title": "Organisatie & processen",
    "subtitle": "Van triage tot ICT, kwaliteit tot veiligheid. En: de financiële koers.",
    "time": "13:45–14:15",
    "minutes": 30,
    "stellingen": [
        {"id": "o-l1", "text": "Wij zijn een reactieve praktijk — we blussen brandjes in plaats van ze te voorkomen."},
        {"id": "o-l2", "text": "Onze pragmatische aanpak werkt prima — we hoeven geen groot plan om goede zorg te leveren."},
        {"id": "o-l3", "text": "We bezuinigen op plekken waar we eigenlijk zouden moeten investeren."},
        {"id": "o-l4", "text": "Met slimmere IT-keuzes zouden we merkbaar meer tijd overhouden voor de patiënt."},
        {"id": "o-l5", "text": "Er zit meer werkplezier in deze praktijk dan we er nu uithalen."},
        {"id": "o-l6", "text": "Als we nu de juiste organisatorische keuzes maken, kunnen we over twee jaar een wezenlijk betere praktijk zijn."},
        {"id": "o-l7", "text": "We zijn duurzaam, maar het mag geen geld kosten."},
        {"id": "o-l8", "text": "Onze dagstructuur klopt."},
    ],
    "principles": [
        {"key": "principle-org-org-l", "label": "Organisatieprincipe", "icon": "⚙️", "placeholder": "Wij organiseren onze praktijk zo dat..."},
        {"key": "principle-org-fin-l", "label": "Financieel principe", "icon": "💰", "placeholder": "Financieel sturen wij op..."},
    ],
}

# ── MEDEWERKERS ──

MEDEWERKERS = {
    "title": "Medewerkers",
    "subtitle": "Wat voor werkgever willen we zijn? Visie en cultuur, niet individuele personen.",
    "time": "14:40–15:10",
    "minutes": 30,
    "questions": [
        "Wat voor werkgever willen we zijn — en is dat ook hoe onze medewerkers ons ervaren?",
        "Geven wij medewerkers voldoende ruimte en vertrouwen om eigenaarschap te nemen — en durven zij dat ook te pakken?",
        "Hoe houden we ons team scherp en geïnspireerd — door nascholing, teambuilding, extra beloning, of iets anders?",
        "Streven wij naar een team waar verschillende mensen zich thuis voelen, of zoeken we juist gelijkgestemden?",
        "Hoe herkennen we op tijd dat iemand niet op de juiste plek zit — en wat doen we dan?",
    ],
    "principles": [
        {"key": "principle-mw-wg", "label": "Wij geven", "icon": "👥", "placeholder": "Wij bieden onze medewerkers..."},
        {"key": "principle-mw-on", "label": "Wij verwachten", "icon": "🎯", "placeholder": "Van onze medewerkers verwachten wij..."},
    ],
}

# ── KANSEN & BEDREIGINGEN ──

KANSEN = {
    "title": "Kansen & bedreigingen",
    "subtitle": "Welke externe én interne ontwikkelingen raken ons — in de samenleving, de zorg én binnen onze eigen maatschap?",
    "time": "15:10–15:40",
    "minutes": 30,
    "intern_hint": "Denk aan: samenwerking maten, taakverdeling, werkdruk, cultuur, opvolging, ICT-volwassenheid, financiële ruimte.",
    "extern_hint": "Denk aan: AI, leefstijlgeneeskunde, samenwerking welzijn, wijkfinanciering, taakdelegatie VS/POH, onze rol in de stad — maar ook: huisartsentekort, ANW-beleid, vergrijzing, bureaucratie, kosten.",
    "principles": [
        {"key": "principle-kb-int", "label": "Intern principe", "icon": "🏠", "placeholder": "Binnen onze maatschap pakken wij kansen door..."},
        {"key": "principle-kb-ext", "label": "Extern principe", "icon": "🌍", "placeholder": "Op externe ontwikkelingen reageren wij door..."},
    ],
}

# ── FEEDBACK ──

FEEDBACK = {
    "title": "Feedbackafspraken",
    "subtitle": "Veilig feedback geven is een voorwaarde voor alles wat jullie afspreken.",
    "time": "16:25–16:40",
    "minutes": 15,
    "questions": [
        "Op een vast moment of zodra iets speelt?",
        "Hoe vaak? Voorstel: jaarlijks bilateraal.",
        "Wie initieert?",
        "Wat als feedback niet landt?",
    ],
    "sbi_example": "Tijdens het overleg viel je me tweemaal in de rede. Ik voelde me niet gehoord. Hoe zag jij dat?",
}

# ── AFSLUITING ──

AFSLUITING = {
    "title": "Afsluiting / Check-out",
    "subtitle": "Wat neem jij mee — en wat ga jij de komende week anders doen?",
    "time": "16:40–16:55",
    "minutes": 15,
    "reminders": [
        "Direct vastleggen. Afspraken die niet opgeschreven worden, bestaan niet.",
        "Nu in de agenda: evaluatiemoment + vervolgafspraken.",
    ],
}

# ── RESERVE DOMEINEN ──

IDENTITEIT = {
    "title": "Identiteit",
    "subtitle": "Wie zijn wij, wat maakt ons onderscheidend, hoe verhouden we ons tot de stad?",
    "missie": "Laagdrempelige diagnostische, therapeutische en preventieve zorg — op maat, op afstand waar het kan, persoonlijk als het nodig is.",
    "visie": "Integrale, persoonsgerichte en continue zorg. Ruimte voor innovatie. Werkplezier als voorwaarde.",
    "stappen": [
        'Ieder schrijft twee stickies: "Wij zijn een praktijk die..." en "Onze rol in Utrecht is..."',
        "Clusteren: sleep de stickies samen",
        "Missiezin formuleren: schrijf samen 1–2 zinnen",
    ],
}

PATIENTEN = {
    "title": "Patiënten",
    "subtitle": "Hoe kijken we naar en gaan we om met onze patiënten?",
    "questions": [
        "Bejegening: empowerend, ontzorgend, of situationeel?",
        "Toegankelijk voor lagere gezondheidsvaardigheden?",
        "Hoe om met ver-weg-patiënten en wisselaars?",
        "Verwachtingen qua bereikbaarheid?",
    ],
    "stellingen": [
        {"id": "pat-s1b", "text": "Wij zijn primair empowerend — we sturen op eigen regie."},
        {"id": "pat-s2b", "text": "Onze praktijk is voldoende toegankelijk voor kwetsbare en laaggeletterde patiënten."},
        {"id": "pat-s3b", "text": "We zeggen consequent nee als zorg niet bij ons hoort — eenduidig."},
        {"id": "pat-s4b", "text": "Patiënten weten wat ze van ons kunnen verwachten qua bereikbaarheid."},
    ],
}

ZORGINHOUD = {
    "title": "Zorginhoud — wat doen we wel, wat niet?",
    "subtitle": "Er komt steeds meer zorg onze kant op. Hoe prioriteren we?",
    "stellingen": [
        {"id": "z-l1", "text": "Wij zeggen te vaak ja tegen zorg die eigenlijk niet bij ons hoort."},
        {"id": "z-l2", "text": "Substitutie vanuit het ziekenhuis accepteren we te makkelijk."},
        {"id": "z-l3", "text": "We moeten ruimte maken voor zorg die de POH/assistent leuk vindt en goed kan."},
        {"id": "z-l4", "text": "We hebben geen helder criterium om te bepalen of we iets wel of niet oppakken."},
    ],
    "toetsingscriteria": [
        "Missie — past het bij wie wij willen zijn?",
        "Competenties — kunnen wij dit, of kunnen we het realistisch leren?",
        "Financiering — is het betaald, of worden we er armer van?",
        "Capaciteit — past het erbij zonder dat de rest lijdt?",
        "Werkplezier — vindt iemand het leuk en wil die het trekken?",
    ],
}


def to_dict():
    """Return all content as a JSON-serializable dict for the /api/content endpoint."""
    import copy

    return copy.deepcopy(
        {
            "title": TITLE,
            "subtitle": SUBTITLE,
            "date": DATE,
            "timeRange": TIME_RANGE,
            "schedule": SCHEDULE,
            "groundRules": GROUND_RULES,
            "checkin": CHECKIN,
            "organisatie": ORGANISATIE,
            "medewerkers": MEDEWERKERS,
            "kansen": KANSEN,
            "feedback": FEEDBACK,
            "afsluiting": AFSLUITING,
            "identiteit": IDENTITEIT,
            "patienten": PATIENTEN,
            "zorginhoud": ZORGINHOUD,
        }
    )
