"""Generate a printable PDF handout from content.py (single source of truth)."""

import os
import sys

from fpdf import FPDF

sys.path.insert(0, os.path.dirname(__file__))
import content as C  # noqa: E402

ARIAL_UNI = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
ARIAL_ITALIC = "/System/Library/Fonts/Supplemental/Arial Narrow Italic.ttf"

# Fallback fonts for Linux (VPS)
if not os.path.exists(ARIAL_UNI):
    ARIAL_UNI = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ARIAL_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    ARIAL_ITALIC = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

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


def _clean(s):
    """Strip emoji for PDF rendering (most fonts can't handle them)."""
    import re
    return re.sub(r"[\U00010000-\U0010ffff]", "", s).strip()


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
        self.cell(PW / 2, 5, f"{C.TITLE} -- {C.DATE}", align="L")
        self.cell(PW / 2, 5, f"pagina {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*LIGHT_LINE)
        self.line(self.l_margin, 14, self.w - self.r_margin, 14)

    def footer(self):
        self.set_y(-10)
        self.f("", 6.5)
        self.set_text_color(*TEXT_SEC)
        self.cell(0, 5, f"Vertrouwelijk -- {C.SUBTITLE}", align="C")

    def dh(self, title, time=""):
        self.f("B", 15)
        self.set_text_color(*PRIMARY)
        self.cell(0, 10, _clean(title), new_x="LMARGIN", new_y="NEXT")
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
        self.multi_cell(0, 5, _clean(text))
        self.ln(4)

    def st(self, label):
        self.f("B", 11)
        self.set_text_color(*PRIMARY)
        self.cell(0, 7, _clean(label), new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def si(self, text):
        self.f("I", 8.5)
        self.set_text_color(*TEXT_SEC)
        self.multi_cell(0, 4.5, _clean(text))
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
        self.cell(PW - 50, 6, _clean(text))
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
        self.multi_cell(PW - 8, 5.5, _clean(text))
        self.ln(2)

    def nl(self, n=4, label=""):
        if label:
            self.f("I", 8)
            self.set_text_color(*TEXT_SEC)
            self.cell(0, 5, _clean(label), new_x="LMARGIN", new_y="NEXT")
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
            self.cell(w - 8, 4, _clean(label).upper())
            self.set_xy(x + 4, y + 10)
            self.f("I", 9)
            self.set_text_color(*TEXT_SEC)
            self.multi_cell(w - 8, 5, _clean(ph))
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
        self.cell(PW - 8, 4, _clean(label).upper())
        self.set_xy(self.l_margin + 4, y + 10)
        self.f("I", 9)
        self.set_text_color(*TEXT_SEC)
        self.multi_cell(PW - 8, 5, _clean(placeholder))
        self.set_y(y + 34)

    def kb(self, title, hint):
        if self.get_y() + 50 > self.h - 18:
            self.add_page()
        self.f("B", 10)
        self.set_text_color(*PRIMARY)
        self.cell(0, 6, _clean(title), new_x="LMARGIN", new_y="NEXT")
        self.ln(1)
        self.set_fill_color(255, 248, 225)
        hy = self.get_y()
        self.rect(self.l_margin, hy, PW, 10, style="F")
        self.set_xy(self.l_margin + 3, hy + 1)
        self.f("I", 8)
        self.set_text_color(*TEXT_SEC)
        self.multi_cell(PW - 6, 4, _clean(hint))
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
        self.multi_cell(PW - 6, 5.5, _clean(text))
        self.ln(1)


def build(output=None):
    """Build the PDF. Returns bytes if output is None, otherwise writes to file."""
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
    p.cell(0, 8, C.SUBTITLE, align="C", new_x="LMARGIN", new_y="NEXT")
    p.ln(6)
    p.set_draw_color(*PRIMARY)
    p.set_line_width(0.8)
    mid = p.w / 2
    p.line(mid - 30, p.get_y(), mid + 30, p.get_y())
    p.set_line_width(0.2)
    p.ln(10)
    p.f("", 11)
    p.cell(0, 7, f"{C.DATE}  |  {C.TIME_RANGE}", align="C", new_x="LMARGIN", new_y="NEXT")
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
    p.f("B", 8)
    p.set_fill_color(*PRIMARY)
    p.set_text_color(*WHITE)
    p.cell(38, 7, "  Tijd", fill=True)
    p.cell(100, 7, "  Onderdeel", fill=True)
    p.cell(PW - 138, 7, "  Duur", fill=True, new_x="LMARGIN", new_y="NEXT")
    for i, s in enumerate(C.SCHEDULE):
        bg = BG if i % 2 == 0 else WHITE
        p.set_fill_color(*bg)
        p.set_text_color(*TEXT)
        is_pauze = "Pauze" in s["label"]
        p.f("I" if is_pauze else "", 9.5)
        p.cell(38, 8, f"  {s['time']}", fill=True)
        p.cell(100, 8, f"  {s['label']}", fill=True)
        p.cell(PW - 138, 8, f"  {s['minutes']} min", fill=True, new_x="LMARGIN", new_y="NEXT")
    p.f("I", 8)
    p.set_text_color(*TEXT_SEC)
    p.ln(3)
    p.cell(0, 5, "Reserve (indien tijd): Identiteit / Patienten / Zorginhoud", new_x="LMARGIN", new_y="NEXT")

    p.ln(10)
    p.st("Drie afspraken")
    p.ln(2)
    for i, rule in enumerate(C.GROUND_RULES, 1):
        p.f("B", 9.5)
        p.set_text_color(*TEXT)
        p.cell(0, 6, f"{i}. {rule['title']}", new_x="LMARGIN", new_y="NEXT")
        p.f("", 8.5)
        p.set_text_color(*TEXT_SEC)
        p.cell(0, 5, f"    {rule['description']}", new_x="LMARGIN", new_y="NEXT")
        p.ln(2)

    # ── CHECK-IN ──
    p.add_page()
    ci = C.CHECKIN
    p.dh(ci["title"], f"{ci['time']}  |  {ci['minutes']} minuten")
    p.sub(ci["subtitle"])
    for i, q in enumerate(ci["questions"], 1):
        p.q(i, q)
    p.ln(4)
    p.nl(5, "Terugkerende thema's die je opvallen:")

    # ── ORGANISATIE ──
    p.add_page()
    org = C.ORGANISATIE
    p.dh(org["title"], f"{org['time']}  |  {org['minutes']} minuten")
    p.sub(org["subtitle"])
    p.st("Stap 1 -- Stem op de stellingen")
    p.si("Wees eerlijk, niet beleefd. Stem met  +  (eens)   ~  (neutraal)   -  (oneens)")
    for i, s in enumerate(org["stellingen"], 1):
        p.stelling(i, s["text"])
    p.ln(4)
    p.nl(3, "Waar zit de spanning?")
    p.sp(45)
    p.st("Principes")
    p.ln(2)
    pr = org["principles"]
    p.pp(pr[0]["label"], pr[0]["placeholder"], "teal", pr[1]["label"], pr[1]["placeholder"], "yellow")

    # ── MEDEWERKERS ──
    p.add_page()
    mw = C.MEDEWERKERS
    p.dh(mw["title"], f"{mw['time']}  |  {mw['minutes']} minuten")
    p.sub(mw["subtitle"])
    p.st("Stap 1 -- Individueel nadenken (5 min)")
    p.si("Lees de vragen in stilte. Plak per vraag een sticky met jouw kernantwoord.")
    for i, q in enumerate(mw["questions"], 1):
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
    pr = mw["principles"]
    p.pp(pr[0]["label"], pr[0]["placeholder"], "orange", pr[1]["label"], pr[1]["placeholder"], "green")

    # ── KANSEN & BEDREIGINGEN ──
    p.add_page()
    kb = C.KANSEN
    p.dh(kb["title"], f"{kb['time']}  |  {kb['minutes']} minuten")
    p.sub(kb["subtitle"])
    p.kb("Intern -- binnen de maatschap & praktijk", kb["intern_hint"])
    p.kb("Extern -- zorg, samenleving & ontwikkelingen", kb["extern_hint"])
    p.sp(45)
    p.st("Principes")
    p.ln(2)
    pr = kb["principles"]
    p.pp(pr[0]["label"], pr[0]["placeholder"], "teal", pr[1]["label"], pr[1]["placeholder"], "orange")

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
    fb = C.FEEDBACK
    p.dh(fb["title"], f"{fb['time']}  |  {fb['minutes']} minuten")
    p.sub(fb["subtitle"])
    p.st("Bespreek")
    p.ln(1)
    for q in fb["questions"]:
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
    p.multi_cell(PW - 8, 5, f'"{fb["sbi_example"]}"')
    p.set_y(y + 16)
    p.f("", 9)
    p.set_text_color(*TEXT)
    p.cell(0, 5, "Eindig altijd met een vraag.", new_x="LMARGIN", new_y="NEXT")
    p.ln(6)
    p.pbox("Feedbackafspraken", "Minimaal 2 concrete afspraken...")

    # ── AFSLUITING ──
    p.add_page()
    af = C.AFSLUITING
    p.dh(af["title"], f"{af['time']}  |  {af['minutes']} minuten")
    p.sub(af["subtitle"])
    p.nl(4, "Wat neem ik mee:")
    p.ln(4)
    p.f("B", 9.5)
    p.set_text_color(*PRIMARY)
    p.cell(0, 6, "Reminders", new_x="LMARGIN", new_y="NEXT")
    p.ln(2)
    for r in af["reminders"]:
        p.bullet(r)

    # ── RESERVE: IDENTITEIT ──
    p.add_page()
    iden = C.IDENTITEIT
    p.dh(f"Reserve -- {iden['title']}")
    p.sub(iden["subtitle"])
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
    p.multi_cell(PW - 8, 4.5, _clean(iden["missie"]))
    p.set_y(y + 24)
    p.st("Werkvorm")
    p.ln(1)
    for i, s in enumerate(iden["stappen"], 1):
        p.q(i, s)
    p.ln(2)
    p.pbox("Kernwaarden + missiezin", "3-5 kernwaarden + een missiezin als kompas...")

    # ── RESERVE: PATIENTEN ──
    p.add_page()
    pat = C.PATIENTEN
    p.dh(f"Reserve -- {_clean(pat['title'])}")
    p.sub(pat["subtitle"])
    p.st("Reflectievragen")
    p.ln(1)
    for i, q in enumerate(pat["questions"], 1):
        p.q(i, q)
    p.ln(2)
    p.st("Stellingen")
    p.ln(1)
    for i, s in enumerate(pat["stellingen"], 1):
        p.stelling(i, s["text"])
    p.ln(4)
    p.pbox("Patientprincipe(s)", "1-2 principes over hoe wij omgaan met patienten...")

    # ── RESERVE: ZORGINHOUD ──
    p.add_page()
    zorg = C.ZORGINHOUD
    p.dh(f"Reserve -- {_clean(zorg['title'])}")
    p.sub(zorg["subtitle"])
    p.st("Stellingen")
    p.ln(1)
    for i, s in enumerate(zorg["stellingen"], 1):
        p.stelling(i, s["text"])
    p.ln(4)
    p.st("Toetsingscriteria voor nieuwe zorg")
    p.ln(2)
    for i, c in enumerate(zorg["toetsingscriteria"], 1):
        p.q(i, c)
    p.ln(2)
    p.pbox("Top prioriteiten + nee-punt", "Top 2-3 zorgprioriteiten + minimaal een bewust nee-punt...")

    # ── NOTITIES ──
    p.add_page()
    p.dh("Notities")
    p.nl(28)

    # ── OUTPUT ──
    if output is None:
        return p.output()
    p.output(output)
    return None


if __name__ == "__main__":
    out = "handout.pdf"
    build(out)
    print(f"PDF gegenereerd: {out}")
