from fpdf import FPDF

ARIAL_UNI = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
ARIAL_ITALIC = "/System/Library/Fonts/Supplemental/Arial Narrow Italic.ttf"

PRIMARY = (27, 77, 79)
ACCENT = (193, 105, 79)
GREEN = (45, 125, 70)
YELLOW = (184, 141, 45)
RED = (184, 61, 61)
TEXT = (30, 30, 30)
TEXT_SEC = (110, 115, 120)
BG = (245, 243, 238)
WHITE = (255, 255, 255)
LIGHT_LINE = (215, 212, 205)

PW = 174


class H(FPDF):
    def setup_fonts(self):
        self.add_font("U", "", ARIAL_UNI)
        self.add_font("U", "B", ARIAL_BOLD)
        self.add_font("U", "I", ARIAL_ITALIC)

    def f(self, style="", size=10):
        super().set_font("U", style, size)

    def header(self):
        if self.page_no() <= 1:
            return
        self.f("", 7)
        self.set_text_color(*TEXT_SEC)
        self.set_y(8)
        self.cell(PW / 2, 5, "Koersbepaling Maatschap -- 5 april 2026", align="L")
        self.cell(PW / 2, 5, f"pagina {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*LIGHT_LINE)
        self.line(self.l_margin, 14, self.w - self.r_margin, 14)

    def footer(self):
        self.set_y(-10)
        self.f("", 6.5)
        self.set_text_color(*TEXT_SEC)
        self.cell(0, 5, "Vertrouwelijk -- Huisartsenpraktijk Binnenstad Utrecht", align="C")

    def dh(self, title, time=""):
        self.f("B", 15)
        self.set_text_color(*PRIMARY)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        if time:
            self.f("", 9)
            self.set_text_color(*TEXT_SEC)
            self.cell(0, 5, time, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*PRIMARY)
        self.set_line_width(0.6)
        self.line(self.l_margin, self.get_y() + 2, self.w - self.r_margin, self.get_y() + 2)
        self.set_line_width(0.2)
        self.ln(6)

    def sub(self, text):
        self.f("I", 9)
        self.set_text_color(*TEXT_SEC)
        self.multi_cell(0, 5, text)
        self.ln(4)

    def st(self, label):
        self.f("B", 11)
        self.set_text_color(*PRIMARY)
        self.cell(0, 7, label, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def si(self, text):
        self.f("I", 8.5)
        self.set_text_color(*TEXT_SEC)
        self.multi_cell(0, 4.5, text)
        self.ln(3)

    def stelling(self, nr, text):
        y = self.get_y()
        if y + 11 > self.h - 18:
            self.add_page()
            y = self.get_y()
        self.set_fill_color(*BG)
        self.rect(self.l_margin, y, PW, 10, style="F")
        self.set_xy(self.l_margin + 3, y + 1.5)
        self.f("B", 9)
        self.set_text_color(*PRIMARY)
        self.cell(8, 6, str(nr))
        self.f("", 9)
        self.set_text_color(*TEXT)
        self.cell(PW - 50, 6, text)
        x = self.w - self.r_margin - 38
        self.set_draw_color(*LIGHT_LINE)
        for label in ["+", "~", chr(8211)]:
            self.rect(x, y + 1.5, 11, 7, style="D")
            self.set_xy(x, y + 1.5)
            self.f("B", 9)
            self.set_text_color(*TEXT_SEC)
            self.cell(11, 7, label, align="C")
            x += 13
        self.set_y(y + 12)

    def q(self, nr, text):
        if self.get_y() + 12 > self.h - 18:
            self.add_page()
        self.f("B", 9.5)
        self.set_text_color(*PRIMARY)
        self.cell(8, 5.5, f"{nr}.")
        self.f("", 9.5)
        self.set_text_color(*TEXT)
        self.multi_cell(PW - 8, 5.5, text)
        self.ln(2)

    def nl(self, n=4, label=""):
        if label:
            self.f("I", 8)
            self.set_text_color(*TEXT_SEC)
            self.cell(0, 5, label, new_x="LMARGIN", new_y="NEXT")
            self.ln(2)
        self.set_draw_color(*LIGHT_LINE)
        for _ in range(n):
            y = self.get_y()
            if y + 8 > self.h - 18:
                self.add_page()
                y = self.get_y()
            self.line(self.l_margin, y, self.w - self.r_margin, y)
            self.ln(8)

    def pp(self, l1, ph1, c1, l2, ph2, c2):
        colors = {
            "teal": (PRIMARY, (232, 240, 240)),
            "yellow": (YELLOW, (255, 248, 225)),
            "orange": (ACCENT, (252, 238, 232)),
            "green": (GREEN, (232, 245, 236)),
        }
        y = self.get_y()
        if y + 38 > self.h - 18:
            self.add_page()
            y = self.get_y()
        w = (PW - 8) / 2
        h = 34
        for i, (label, ph, cls) in enumerate([(l1, ph1, c1), (l2, ph2, c2)]):
            x = self.l_margin + i * (w + 8)
            fg, bg = colors[cls]
            self.set_fill_color(*bg)
            self.set_draw_color(*fg)
            self.set_dash_pattern(2, 1.5)
            self.rect(x, y, w, h, style="DF")
            self.set_dash_pattern()
            self.set_xy(x + 4, y + 3)
            self.f("B", 7.5)
            self.set_text_color(*fg)
            self.cell(w - 8, 4, label.upper())
            self.set_xy(x + 4, y + 10)
            self.f("I", 9)
            self.set_text_color(*TEXT_SEC)
            self.multi_cell(w - 8, 5, ph)
        self.set_y(y + h + 5)

    def pbox(self, label, placeholder):
        y = self.get_y()
        if y + 34 > self.h - 18:
            self.add_page()
            y = self.get_y()
        self.set_fill_color(232, 240, 240)
        self.set_draw_color(*PRIMARY)
        self.set_dash_pattern(2, 1.5)
        self.rect(self.l_margin, y, PW, 30, style="DF")
        self.set_dash_pattern()
        self.set_xy(self.l_margin + 4, y + 3)
        self.f("B", 7.5)
        self.set_text_color(*PRIMARY)
        self.cell(PW - 8, 4, label.upper())
        self.set_xy(self.l_margin + 4, y + 10)
        self.f("I", 9)
        self.set_text_color(*TEXT_SEC)
        self.multi_cell(PW - 8, 5, placeholder)
        self.set_y(y + 34)

    def kb(self, title, hint):
        if self.get_y() + 50 > self.h - 18:
            self.add_page()
        self.f("B", 10)
        self.set_text_color(*PRIMARY)
        self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)
        self.set_fill_color(255, 248, 225)
        hy = self.get_y()
        self.rect(self.l_margin, hy, PW, 10, style="F")
        self.set_xy(self.l_margin + 3, hy + 1)
        self.f("I", 8)
        self.set_text_color(*TEXT_SEC)
        self.multi_cell(PW - 6, 4, hint)
        self.set_y(hy + 12)
        w = (PW - 8) / 2
        y2 = self.get_y()
        for i, (label, color) in enumerate([("KANSEN", GREEN), ("BEDREIGINGEN", RED)]):
            x = self.l_margin + i * (w + 8)
            self.set_xy(x, y2)
            self.f("B", 8)
            self.set_text_color(*color)
            self.cell(w, 5, label)
            self.set_draw_color(*LIGHT_LINE)
            self.rect(x, y2 + 6, w, 24, style="D")
        self.set_y(y2 + 34)

    def smart(self, rows=8):
        cols = [("#", 10), ("Actiepunt", 64), ("Eigenaar", 36), ("Deadline", 32), ("Hoe meten?", 32)]
        self.f("B", 8)
        self.set_fill_color(*PRIMARY)
        self.set_text_color(*WHITE)
        for label, w in cols:
            self.cell(w, 7, f"  {label}", fill=True)
        self.cell(0, 7, "", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*TEXT)
        self.f("", 8.5)
        for i in range(1, rows + 1):
            bg = BG if i % 2 == 1 else WHITE
            self.set_fill_color(*bg)
            for j, (_, w) in enumerate(cols):
                val = f"  {i}" if j == 0 else ""
                self.cell(w, 8, val, fill=True)
            self.cell(0, 8, "", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*LIGHT_LINE)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def sp(self, needed=40):
        if self.get_y() + needed > self.h - 18:
            self.add_page()

    def bullet(self, text):
        if self.get_y() + 7 > self.h - 18:
            self.add_page()
        self.f("", 9.5)
        self.set_text_color(*TEXT)
        self.cell(6, 5.5, chr(8226))
        self.multi_cell(PW - 6, 5.5, text)
        self.ln(1)


def build():
    p = H(orientation="P", unit="mm", format="A4")
    p.setup_fonts()
    p.set_auto_page_break(auto=True, margin=16)
    p.set_margins(18, 18, 18)

    # ── COVER ──
    p.add_page()
    p.ln(50)
    p.f("B", 32)
    p.set_text_color(*PRIMARY)
    p.cell(0, 16, "Koersbepaling", align="C", new_x="LMARGIN", new_y="NEXT")
    p.cell(0, 16, "Maatschap", align="C", new_x="LMARGIN", new_y="NEXT")
    p.ln(10)
    p.f("", 13)
    p.set_text_color(*TEXT_SEC)
    p.cell(0, 8, "Huisartsenpraktijk Binnenstad", align="C", new_x="LMARGIN", new_y="NEXT")
    p.cell(0, 8, "Utrecht", align="C", new_x="LMARGIN", new_y="NEXT")
    p.ln(6)
    p.set_draw_color(*PRIMARY)
    p.set_line_width(0.8)
    mid = p.w / 2
    p.line(mid - 30, p.get_y(), mid + 30, p.get_y())
    p.set_line_width(0.2)
    p.ln(10)
    p.f("", 11)
    p.cell(0, 7, "Zaterdag 5 april 2026  |  13:00 - 17:00", align="C", new_x="LMARGIN", new_y="NEXT")
    p.ln(20)
    p.f("I", 11)
    p.cell(0, 7, "Persoonlijke handout", align="C", new_x="LMARGIN", new_y="NEXT")
    p.ln(6)
    p.f("", 11)
    p.set_text_color(*TEXT)
    p.cell(0, 7, "Naam: ________________________________", align="C", new_x="LMARGIN", new_y="NEXT")

    # ── DAGPROGRAMMA ──
    p.add_page()
    p.dh("Dagprogramma")
    sched = [
        ("13:00 - 13:15", "Welkom & binnenkomst", "15 min"),
        ("13:15 - 13:45", "Check-in", "30 min"),
        ("13:45 - 14:15", "Organisatie & processen", "30 min"),
        ("14:15 - 14:40", "Pauze", "25 min"),
        ("14:40 - 15:10", "Medewerkers", "30 min"),
        ("15:10 - 15:40", "Kansen & bedreigingen", "30 min"),
        ("15:40 - 16:25", "Synthese & actiepunten", "45 min"),
        ("16:25 - 16:40", "Feedbackafspraken", "15 min"),
        ("16:40 - 16:55", "Afsluiting", "15 min"),
    ]
    p.f("B", 8)
    p.set_fill_color(*PRIMARY)
    p.set_text_color(*WHITE)
    p.cell(38, 7, "  Tijd", fill=True)
    p.cell(100, 7, "  Onderdeel", fill=True)
    p.cell(PW - 138, 7, "  Duur", fill=True, new_x="LMARGIN", new_y="NEXT")
    for i, (t, o, d) in enumerate(sched):
        bg = BG if i % 2 == 0 else WHITE
        p.set_fill_color(*bg)
        p.set_text_color(*TEXT)
        p.f("I" if "Pauze" in o else "", 9.5)
        p.cell(38, 8, f"  {t}", fill=True)
        p.cell(100, 8, f"  {o}", fill=True)
        p.cell(PW - 138, 8, f"  {d}", fill=True, new_x="LMARGIN", new_y="NEXT")
    p.f("I", 8)
    p.set_text_color(*TEXT_SEC)
    p.ln(3)
    p.cell(0, 5, "Reserve (indien tijd): Identiteit / Patienten / Zorginhoud", new_x="LMARGIN", new_y="NEXT")

    p.ln(10)
    p.st("Drie afspraken")
    p.ln(2)
    for i, (t, d) in enumerate([
        ("Doen, niet alleen praten", "Elk domein sluit af met een tastbare uitkomst."),
        ("Een format per domein", "Stellingen, reflectie, stickies, principes."),
        ("Begin bij onszelf", "Eerst check-in, dan pas de koers."),
    ], 1):
        p.f("B", 9.5)
        p.set_text_color(*TEXT)
        p.cell(0, 6, f"{i}. {t}", new_x="LMARGIN", new_y="NEXT")
        p.f("", 8.5)
        p.set_text_color(*TEXT_SEC)
        p.cell(0, 5, f"    {d}", new_x="LMARGIN", new_y="NEXT")
        p.ln(2)

    # ── CHECK-IN ──
    p.add_page()
    p.dh("Check-in", "13:15 - 13:45  |  30 minuten")
    p.sub("Max. 3 minuten per persoon. De rest luistert -- geen discussie, wel kort doorvragen.")
    for i, q in enumerate([
        "Hoe zit jij er nu in -- wat geeft je energie?",
        "Wat is voor jou een energie-drain?",
        "Wat heb jij van de maatschap nodig?",
        "Hoe ziet jouw ideale werkdag eruit?",
        "Wat zou je de maatschap willen vragen dat je nu nog niet vraagt?",
    ], 1):
        p.q(i, q)
    p.ln(4)
    p.nl(5, "Terugkerende thema's die je opvallen:")

    # ── ORGANISATIE ──
    p.add_page()
    p.dh("Organisatie & processen", "13:45 - 14:15  |  30 minuten")
    p.sub("Van triage tot ICT, kwaliteit tot veiligheid. En: de financiele koers.")
    p.st("Stap 1 -- Stem op de stellingen")
    p.si("Wees eerlijk, niet beleefd. Stem met  +  (eens)   ~  (neutraal)   -  (oneens)")
    for i, s in enumerate([
        "Wij zijn een reactieve praktijk -- we blussen brandjes in plaats van ze te voorkomen.",
        "Onze pragmatische aanpak werkt prima -- we hoeven geen groot plan om goede zorg te leveren.",
        "We bezuinigen op plekken waar we eigenlijk zouden moeten investeren.",
        "Met slimmere IT-keuzes zouden we merkbaar meer tijd overhouden voor de patient.",
        "Er zit meer werkplezier in deze praktijk dan we er nu uithalen.",
        "Als we nu de juiste organisatorische keuzes maken, kunnen we over twee jaar een betere praktijk zijn.",
        "We zijn duurzaam, maar het mag geen geld kosten.",
        "Onze dagstructuur klopt.",
    ], 1):
        p.stelling(i, s)
    p.ln(4)
    p.nl(3, "Waar zit de spanning?")
    p.sp(45)
    p.st("Principes")
    p.ln(2)
    p.pp("Organisatieprincipe", "Wij organiseren onze praktijk zo dat...", "teal",
         "Financieel principe", "Financieel sturen wij op...", "yellow")

    # ── MEDEWERKERS ──
    p.add_page()
    p.dh("Medewerkers", "14:40 - 15:10  |  30 minuten")
    p.sub("Wat voor werkgever willen we zijn? Visie en cultuur, niet individuele personen.")
    p.st("Stap 1 -- Individueel nadenken (5 min)")
    p.si("Lees de vragen in stilte. Plak per vraag een sticky met jouw kernantwoord.")
    for i, q in enumerate([
        "Wat voor werkgever willen we zijn -- en is dat ook hoe onze medewerkers ons ervaren?",
        "Geven wij medewerkers voldoende ruimte en vertrouwen om eigenaarschap te nemen -- en durven zij dat ook te pakken?",
        "Hoe houden we ons team scherp en geinspireerd -- door nascholing, teambuilding, extra beloning, of iets anders?",
        "Streven wij naar een team waar verschillende mensen zich thuis voelen, of zoeken we juist gelijkgestemden?",
        "Hoe herkennen we op tijd dat iemand niet op de juiste plek zit -- en wat doen we dan?",
    ], 1):
        p.q(i, q)
    p.ln(2)
    p.st("Stap 2 -- Scan & selecteer (3 min)")
    p.si("Lees alle stickies. Kies de 2 vragen waar de meeste spanning zit.")
    p.st("Stap 3 -- Diepte op 2 vragen (15 min)")
    p.si("Bespreek alleen de 2 vragen waar het schuurt.")
    p.nl(3, "Mijn kernpunten:")
    p.sp(45)
    p.st("Stap 4 -- Principes (7 min)")
    p.ln(2)
    p.pp("Wij geven", "Wij bieden onze medewerkers...", "orange",
         "Wij verwachten", "Van onze medewerkers verwachten wij...", "green")

    # ── KANSEN & BEDREIGINGEN ──
    p.add_page()
    p.dh("Kansen & bedreigingen", "15:10 - 15:40  |  30 minuten")
    p.sub("Welke externe en interne ontwikkelingen raken ons -- in de samenleving, de zorg en binnen onze eigen maatschap?")
    p.kb("Intern -- binnen de maatschap & praktijk",
         "Denk aan: samenwerking maten, taakverdeling, werkdruk, cultuur, opvolging, ICT, financiele ruimte.")
    p.kb("Extern -- zorg, samenleving & ontwikkelingen",
         "Denk aan: AI, leefstijlgeneeskunde, wijkfinanciering, taakdelegatie, onze rol in de stad -- maar ook: huisartsentekort, vergrijzing, kosten.")
    p.sp(45)
    p.st("Principes")
    p.ln(2)
    p.pp("Intern principe", "Binnen onze maatschap pakken wij kansen door...", "teal",
         "Extern principe", "Op externe ontwikkelingen reageren wij door...", "orange")

    # ── SYNTHESE ──
    p.add_page()
    p.dh("Synthese & actiepunten", "15:40 - 16:25  |  45 minuten")
    p.sub("Principes samenvoegen, taakverdeling, SMART-actiepunten.")
    p.st("Alle principes (6-8 stuks)")
    p.ln(2)
    p.nl(8)
    p.sp(75)
    p.st("SMART-actiepunten")
    p.ln(2)
    p.smart(8)
    p.sp(30)
    p.st("Verbetercyclus")
    p.ln(3)
    p.f("", 10)
    p.set_text_color(*TEXT)
    p.cell(40, 8, "Evaluatiedatum:")
    p.set_draw_color(*LIGHT_LINE)
    p.cell(70, 8, "", border="B", new_x="LMARGIN", new_y="NEXT")
    p.ln(2)
    p.cell(40, 8, "Bewaker:")
    p.cell(70, 8, "", border="B", new_x="LMARGIN", new_y="NEXT")

    # ── FEEDBACK ──
    p.add_page()
    p.dh("Feedbackafspraken", "16:25 - 16:40  |  15 minuten")
    p.sub("Veilig feedback geven is een voorwaarde voor alles wat jullie afspreken.")
    p.st("Bespreek")
    p.ln(1)
    for q in [
        "Op een vast moment of zodra iets speelt?",
        "Hoe vaak? Voorstel: jaarlijks bilateraal.",
        "Wie initieert?",
        "Wat als feedback niet landt?",
    ]:
        p.bullet(q)
    p.ln(4)
    p.st("SBI-model")
    p.ln(2)
    p.f("B", 9.5)
    p.set_text_color(*TEXT)
    p.cell(0, 6, "Situatie -- Gedrag -- Impact", new_x="LMARGIN", new_y="NEXT")
    p.ln(2)
    p.set_fill_color(*BG)
    y = p.get_y()
    p.rect(p.l_margin, y, PW, 14, style="F")
    p.set_xy(p.l_margin + 4, y + 2)
    p.f("I", 9)
    p.set_text_color(*TEXT_SEC)
    p.multi_cell(PW - 8, 5, '"Tijdens het overleg viel je me tweemaal in de rede. Ik voelde me niet gehoord. Hoe zag jij dat?"')
    p.set_y(y + 16)
    p.f("", 9)
    p.set_text_color(*TEXT)
    p.cell(0, 5, "Eindig altijd met een vraag.", new_x="LMARGIN", new_y="NEXT")
    p.ln(6)
    p.pbox("Feedbackafspraken", "Minimaal 2 concrete afspraken...")

    # ── AFSLUITING ──
    p.add_page()
    p.dh("Afsluiting / Check-out", "16:40 - 16:55  |  15 minuten")
    p.sub("Wat neem jij mee -- en wat ga jij de komende week anders doen?")
    p.nl(4, "Wat neem ik mee:")
    p.ln(4)
    p.f("B", 9.5)
    p.set_text_color(*PRIMARY)
    p.cell(0, 6, "Reminders", new_x="LMARGIN", new_y="NEXT")
    p.ln(2)
    p.bullet("Direct vastleggen. Afspraken die niet opgeschreven worden, bestaan niet.")
    p.bullet("Nu in de agenda: evaluatiemoment + vervolgafspraken.")

    # ── RESERVE: IDENTITEIT ──
    p.add_page()
    p.dh("Reserve -- Identiteit")
    p.sub("Wie zijn wij, wat maakt ons onderscheidend, hoe verhouden we ons tot de stad?")
    p.set_fill_color(*BG)
    y = p.get_y()
    p.rect(p.l_margin, y, PW, 22, style="F")
    p.set_xy(p.l_margin + 4, y + 2)
    p.f("B", 8.5)
    p.set_text_color(*PRIMARY)
    p.cell(PW - 8, 5, "Huidige missie:", new_x="LMARGIN", new_y="NEXT")
    p.set_x(p.l_margin + 4)
    p.f("", 8.5)
    p.set_text_color(*TEXT)
    p.multi_cell(PW - 8, 4.5, "Laagdrempelige diagnostische, therapeutische en preventieve zorg -- op maat, op afstand waar het kan, persoonlijk als het nodig is.")
    p.set_y(y + 24)

    p.st("Werkvorm")
    p.ln(1)
    p.q(1, 'Ieder schrijft twee stickies: "Wij zijn een praktijk die..." en "Onze rol in Utrecht is..."')
    p.q(2, "Clusteren: sleep de stickies samen")
    p.q(3, "Missiezin formuleren: schrijf samen 1-2 zinnen")
    p.ln(2)
    p.pbox("Kernwaarden + missiezin", "3-5 kernwaarden + een missiezin als kompas...")

    # ── RESERVE: PATIENTEN ──
    p.add_page()
    p.dh("Reserve -- Patienten")
    p.sub("Hoe kijken we naar en gaan we om met onze patienten?")
    p.st("Reflectievragen")
    p.ln(1)
    for i, q in enumerate([
        "Bejegening: empowerend, ontzorgend, of situationeel?",
        "Toegankelijk voor lagere gezondheidsvaardigheden?",
        "Hoe om met ver-weg-patienten en wisselaars?",
        "Verwachtingen qua bereikbaarheid?",
    ], 1):
        p.q(i, q)
    p.ln(2)
    p.st("Stellingen")
    p.ln(1)
    for i, s in enumerate([
        "Wij zijn primair empowerend -- we sturen op eigen regie.",
        "Onze praktijk is voldoende toegankelijk voor kwetsbare en laaggeletterde patienten.",
        "We zeggen consequent nee als zorg niet bij ons hoort -- eenduidig.",
        "Patienten weten wat ze van ons kunnen verwachten qua bereikbaarheid.",
    ], 1):
        p.stelling(i, s)
    p.ln(4)
    p.pbox("Patientprincipe(s)", "1-2 principes over hoe wij omgaan met patienten...")

    # ── RESERVE: ZORGINHOUD ──
    p.add_page()
    p.dh("Reserve -- Zorginhoud")
    p.sub("Er komt steeds meer zorg onze kant op. Hoe prioriteren we?")
    p.st("Stellingen")
    p.ln(1)
    for i, s in enumerate([
        "Wij zeggen te vaak ja tegen zorg die eigenlijk niet bij ons hoort.",
        "Substitutie vanuit het ziekenhuis accepteren we te makkelijk.",
        "We moeten ruimte maken voor zorg die de POH/assistent leuk vindt en goed kan.",
        "We hebben geen helder criterium om te bepalen of we iets wel of niet oppakken.",
    ], 1):
        p.stelling(i, s)
    p.ln(4)
    p.st("Toetsingscriteria voor nieuwe zorg")
    p.ln(2)
    for i, c in enumerate([
        "Missie -- past het bij wie wij willen zijn?",
        "Competenties -- kunnen wij dit, of kunnen we het realistisch leren?",
        "Financiering -- is het betaald, of worden we er armer van?",
        "Capaciteit -- past het erbij zonder dat de rest lijdt?",
        "Werkplezier -- vindt iemand het leuk en wil die het trekken?",
    ], 1):
        p.q(i, c)
    p.ln(2)
    p.pbox("Top prioriteiten + nee-punt", "Top 2-3 zorgprioriteiten + minimaal een bewust nee-punt...")

    # ── NOTITIES ──
    p.add_page()
    p.dh("Notities")
    p.nl(28)

    # ── OUTPUT ──
    out = "handout.pdf"
    p.output(out)
    print(f"PDF gegenereerd: {out}")


if __name__ == "__main__":
    build()
