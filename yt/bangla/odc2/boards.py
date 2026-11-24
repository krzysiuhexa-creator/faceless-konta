"""35 plansz „Dziwne historie #2: facet, który sprzedał Wieżę Eiffla” (Nie wiem, ale bangla).
Wszystkie rysunki własne (SVG/HTML). Lustig i Capone to rysunkowe ikonki z podpisem, bez podobieństwa do zdjęć."""
from engine import *

CH = {1: "<b>01</b>wieża na złom", 2: "<b>02</b>hrabia", 3: "<b>03</b>plan", 4: "<b>04</b>haczyk",
      5: "<b>05</b>drugi raz", 6: "<b>06</b>ameryka", 7: "<b>07</b>koniec"}
SEC = {**{i: 1 for i in range(1, 5)}, **{i: 2 for i in range(5, 8)}, **{i: 3 for i in range(8, 15)}, **{i: 4 for i in range(15, 21)},
       **{i: 5 for i in range(21, 26)}, **{i: 6 for i in range(26, 34)}, **{i: 7 for i in range(34, 36)}}
OUTRO = 6.5
MONEY = "#3fbf6a"
PAPER = "#f3ecd9"


def B(fid, head, sub="", **kw):
    kw.setdefault("chip", CH[SEC[fid]])
    return Board(fid, head, sub, **kw)


def T(txt, size=44, color="#fff", cls="txt", extra=""):
    return f'<div class="{cls}" style="font-size:{size}px;color:{color};{extra}">{txt}</div>'


def lab(txt, size=44, color="#fff", extra=""):
    return f'<div class="lab" style="font-size:{size}px;color:{color};{extra}">{txt}</div>'


def cnt(b, frm, to, t, du, fmt="#", x=960):
    b.sfx("ticks", t, x, du)
    return f'<span data-count="1" data-from="{frm}" data-to="{to}" data-t="__T{t}__" data-d="{du}" data-fmt="{fmt}">{fmt.replace("#", str(frm))}</span>'


def tag(txt, bg=Y, fg="#111", size=40):
    return (f'<div style="background:{bg};color:{fg};font-weight:900;font-style:italic;font-size:{size}px;padding:12px 30px;'
            f'border-radius:12px 40px 40px 12px;box-shadow:0 6px 0 #000;white-space:nowrap">{txt}</div>')


def check(size=90, color=GREEN):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="{color}" stroke="#fff" stroke-width="7"/>'
            '<path d="M28 52 L44 67 L73 35" stroke="#111" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def cross(size=90, color=RED):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="{color}" stroke="#fff" stroke-width="7"/>'
            '<path d="M32 32 L68 68 M68 32 L32 68" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round"/></svg>')


# ─────────── rysunki ───────────
def eiffel(h=560, col="#cfd6df", fill="#2a2f37"):
    """wieża: sylwetka z kratownicą, rysowana od zera"""
    return f"""<svg width="{h * 0.62:.0f}" height="{h}" viewBox="-190 -310 380 620" style="overflow:visible;display:block"><g filter="url(#stk)">
<path d="M-170 300 Q-95 120 -52 -40 L-20 -270 L20 -270 L52 -40 Q95 120 170 300 L110 300 Q60 190 0 170 Q-60 190 -110 300 Z" fill="{fill}"/>
<rect x="-88" y="40" width="176" height="26" rx="4" fill="{col}"/><rect x="-58" y="-60" width="116" height="20" rx="4" fill="{col}"/>
<rect x="-24" y="-290" width="48" height="26" rx="6" fill="{col}"/><rect x="-5" y="-318" width="10" height="34" fill="{col}"/></g>
<path d="M-132 260 L-70 66 M132 260 L70 66 M-95 230 L70 66 M95 230 L-70 66 M-48 40 L-24 -60 M48 40 L24 -60 M-40 0 L24 -60 M40 0 L-24 -60
 M-18 -80 L12 -150 M18 -80 L-12 -150 M-12 -150 L10 -220 M12 -150 L-10 -220" stroke="{col}" stroke-width="5" opacity=".55" fill="none"/></svg>"""


def conman(size=300, mono=True, smile=True, bag=False):
    """rysunkowy elegant w meloniku (ikonka, nie portret)"""
    eye = ('<circle cx="-30" cy="-8" r="11" fill="#111"/><circle cx="30" cy="-8" r="11" fill="#111"/>'
           '<circle cx="-26" cy="-12" r="4" fill="#fff"/><circle cx="34" cy="-12" r="4" fill="#fff"/>')
    mon = '<circle cx="30" cy="-8" r="24" fill="none" stroke="#FFD21F" stroke-width="6"/><path d="M52 2 Q64 40 50 80" stroke="#FFD21F" stroke-width="3" fill="none"/>' if mono else ""
    mouth = '<path d="M-22 48 Q0 64 22 48" stroke="#1a1110" stroke-width="6" fill="none" stroke-linecap="round"/>' if smile else '<path d="M-18 54 H18" stroke="#1a1110" stroke-width="6" stroke-linecap="round"/>'
    sb = ('<g transform="translate(150,150)"><rect x="-60" y="-40" width="120" height="90" rx="12" fill="#7a4a22"/><rect x="-24" y="-58" width="48" height="22" rx="8" fill="none" stroke="#7a4a22" stroke-width="10"/>'
          '<rect x="-60" y="-6" width="120" height="10" fill="#5a3416"/></g>') if bag else ""
    return f"""<svg width="{size}" height="{size * 1.3:.0f}" viewBox="-180 -200 360 470" style="overflow:visible;display:block"><g filter="url(#stk)">
<path d="M-150 270 Q-150 120 -60 100 L60 100 Q150 120 150 270 Z" fill="#2b2f3a"/><path d="M-40 100 L0 190 L40 100 Z" fill="#f4f4f4"/>
<path d="M-16 112 L0 132 L16 112 L0 150 Z" fill="#FF4FA0"/>
<ellipse cx="0" cy="10" rx="96" ry="104" fill="#f1c9a5"/>
<path d="M-60 30 Q-30 18 0 30 Q30 18 60 30 Q40 44 0 38 Q-40 44 -60 30 Z" fill="#3a2414"/>
<ellipse cx="0" cy="-78" rx="150" ry="22" fill="#15161a"/><path d="M-86 -80 Q-90 -190 0 -192 Q90 -190 86 -80 Z" fill="#15161a"/>
<rect x="-86" y="-104" width="172" height="20" fill="#3a3d46"/>{sb}</g>{eye}{mon}{mouth}</svg>"""


def person(size=150, col="#3a4450", hi=False):
    c = Y if hi else col
    return f"""<svg width="{size}" height="{size * 1.25:.0f}" viewBox="-60 -70 120 150" style="overflow:visible;display:block"><g filter="url(#stk)">
<circle cx="0" cy="-32" r="30" fill="{c}"/><path d="M-52 78 Q-52 6 0 6 Q52 6 52 78 Z" fill="{c}"/></g></svg>"""


def envelope(w=200, col=PAPER, seal=RED):
    return f"""<svg width="{w}" height="{w * 0.66:.0f}" viewBox="0 0 200 132" style="overflow:visible;display:block"><g filter="url(#stk)">
<rect x="0" y="0" width="200" height="132" rx="10" fill="{col}"/></g><path d="M4 6 L100 78 L196 6" stroke="#b9ad8f" stroke-width="6" fill="none"/>
<circle cx="100" cy="78" r="18" fill="{seal}"/></svg>"""


def suitcase(w=330, open_=False):
    notes = "".join(f'<rect x="{-110 + 46 * i}" y="-72" width="40" height="70" rx="5" fill="{MONEY}" stroke="#1e6e3a" stroke-width="4" transform="rotate({(-8, 5, -3, 7, -6)[i]} {-90 + 46 * i} -40)"/>' for i in range(5)) if open_ else ""
    return f"""<svg width="{w}" height="{w * 0.8:.0f}" viewBox="-170 -140 340 270" style="overflow:visible;display:block"><g filter="url(#stk)">
<rect x="-50" y="-112" width="100" height="40" rx="14" fill="none" stroke="#5a3416" stroke-width="16"/>
<rect x="-160" y="-80" width="320" height="200" rx="26" fill="#8a5428"/></g>{notes}
<rect x="-160" y="-6" width="320" height="14" fill="#5a3416"/><rect x="-100" y="-80" width="22" height="200" fill="#5a3416"/><rect x="78" y="-80" width="22" height="200" fill="#5a3416"/>
<rect x="-18" y="-12" width="36" height="26" rx="5" fill="#FFD21F"/></svg>"""


def bill(w=300, txt="100", col=MONEY):
    return (f'<div style="width:{w}px;height:{w * 0.45:.0f}px;background:{col};border:6px solid #fff;border-radius:12px;box-shadow:0 8px 0 #000;'
            f'display:flex;align-items:center;justify-content:space-between;padding:0 22px;box-sizing:border-box;font-weight:900;font-style:italic;color:#0f3d20">'
            f'<span style="font-size:{w * 0.14:.0f}px;white-space:nowrap">{txt}</span><span style="flex:none;width:{w * 0.22:.0f}px;height:{w * 0.22:.0f}px;border-radius:50%;border:5px solid #0f3d20"></span>'
            f'<span style="font-size:{w * 0.14:.0f}px;white-space:nowrap">{txt}</span></div>')


def paper(inner, w, h, rot=0, col=PAPER, pad=34):
    return (f'<div style="width:{w}px;height:{h}px;background:{col};color:#1b1b1b;border-radius:8px;box-shadow:0 12px 0 #000;padding:{pad}px;'
            f'box-sizing:border-box;font-family:Poppins;transform:rotate({rot}deg)">{inner}</div>')


def train(w=420, col=P):
    return f"""<svg width="{w}" height="{w * 0.5:.0f}" viewBox="0 0 420 210" style="overflow:visible;display:block"><g filter="url(#stk)">
<rect x="20" y="40" width="250" height="120" rx="20" fill="{col}"/><rect x="250" y="80" width="150" height="80" rx="16" fill="{col}"/>
<rect x="300" y="30" width="40" height="60" rx="6" fill="#3a4450"/></g>
<rect x="50" y="62" width="60" height="44" rx="8" fill="#cfe7ff"/><rect x="130" y="62" width="60" height="44" rx="8" fill="#cfe7ff"/><rect x="205" y="62" width="44" height="44" rx="8" fill="#cfe7ff"/>
<circle cx="80" cy="172" r="26" fill="#111" stroke="#fff" stroke-width="6"/><circle cx="200" cy="172" r="26" fill="#111" stroke="#fff" stroke-width="6"/>
<circle cx="330" cy="172" r="26" fill="#111" stroke="#fff" stroke-width="6"/></svg>"""


def ship(w=380):
    return f"""<svg width="{w}" height="{w * 0.62:.0f}" viewBox="0 0 380 236" style="overflow:visible;display:block"><g filter="url(#stk)">
<path d="M10 140 L370 140 L320 220 L60 220 Z" fill="#e8e8e8"/><rect x="90" y="80" width="200" height="62" rx="8" fill="#ff3b3b"/>
<rect x="140" y="20" width="44" height="64" fill="#3a4450"/><rect x="210" y="34" width="44" height="50" fill="#3a4450"/></g>
<circle cx="130" cy="110" r="12" fill="#cfe7ff"/><circle cx="190" cy="110" r="12" fill="#cfe7ff"/><circle cx="250" cy="110" r="12" fill="#cfe7ff"/></svg>"""


def box(w=360):
    """skrzynka „do drukowania pieniędzy” (rysunek)"""
    return f"""<svg width="{w}" height="{w * 0.82:.0f}" viewBox="-200 -170 400 330" style="overflow:visible;display:block"><g filter="url(#stk)">
<rect x="-170" y="-120" width="300" height="240" rx="14" fill="#a8743a"/><circle cx="160" cy="-10" r="18" fill="#6e4220"/></g>
<path d="M-170 -40 H130 M-170 40 H130" stroke="#7a5524" stroke-width="7"/><rect x="-110" y="-150" width="180" height="14" rx="7" fill="#111"/>
<path d="M160 -10 L180 -90" stroke="#cfd6df" stroke-width="12" stroke-linecap="round"/><circle cx="182" cy="-96" r="14" fill="#FFD21F"/>
<rect x="-60" y="-18" width="80" height="36" rx="6" fill="#111"/><circle cx="-20" cy="0" r="8" fill="#ff3b3b"/></svg>"""


def safe(w=330, open_=False):
    door = ('<path d="M-130 -130 L-230 -100 L-230 150 L-130 130 Z" fill="#5c6470"/>' if open_ else
            '<rect x="-130" y="-130" width="260" height="260" rx="14" fill="#5c6470"/><circle cx="0" cy="0" r="58" fill="#3a4450" stroke="#cfd6df" stroke-width="8"/>'
            '<path d="M0 -40 V40 M-40 0 H40" stroke="#cfd6df" stroke-width="8"/>')
    inside = "".join(f'<rect x="-100" y="{-90 + 46 * i}" width="200" height="38" rx="6" fill="{MONEY}" stroke="#1e6e3a" stroke-width="4"/>' for i in range(4)) if open_ else ""
    return f"""<svg width="{w}" height="{w}" viewBox="-240 -170 420 360" style="overflow:visible;display:block"><g filter="url(#stk)">
<rect x="-150" y="-150" width="300" height="300" rx="20" fill="#3a4450"/></g><rect x="-130" y="-130" width="260" height="260" rx="14" fill="#1c1f25"/>{inside}{door}</svg>"""


def hat(w=200):
    return f"""<svg width="{w}" height="{w * 0.6:.0f}" viewBox="-160 -110 320 140" style="overflow:visible;display:block"><g filter="url(#stk)">
<ellipse cx="0" cy="8" rx="150" ry="22" fill="#15161a"/><path d="M-86 6 Q-90 -104 0 -106 Q90 -104 86 6 Z" fill="#15161a"/></g>
<rect x="-86" y="-22" width="172" height="20" fill="#3a3d46"/></svg>"""


def stamp(txt, size=86, col=RED):
    return f'<div class="stamp" style="font-size:{size}px;border-color:{col};color:{col}">{txt}</div>'


def bulb(w=150):
    return f"""<svg width="{w}" height="{w * 1.3:.0f}" viewBox="-60 -70 120 156" style="overflow:visible;display:block"><g filter="url(#glow)">
<circle cx="0" cy="-12" r="50" fill="#FFD21F"/></g><rect x="-24" y="34" width="48" height="36" rx="6" fill="#cfd6df"/>
<path d="M-14 -10 L0 10 L14 -10" stroke="#a87b00" stroke-width="6" fill="none"/></svg>"""


def clock(w=170):
    return f"""<svg width="{w}" height="{w}" viewBox="-60 -60 120 120" style="overflow:visible;display:block"><g filter="url(#stk)"><circle r="52" fill="#fff"/></g>
<circle r="44" fill="none" stroke="#111" stroke-width="5"/><path d="M0 0 V-32" stroke="#111" stroke-width="7" stroke-linecap="round"/>
<path d="M0 0 L26 14" stroke="#ff3b3b" stroke-width="6" stroke-linecap="round"/><circle r="6" fill="#111"/></svg>"""


# ─────────── mapy (uproszczone) ───────────
EU = proj((-6, 24, 40, 54, 220, 1700, 300, 960))
CITY = {"Paryż": (2.35, 48.86), "Wiedeń": (16.37, 48.21), "Hostinné": (15.72, 50.54)}


def dot(color=Y, r=16):
    return f'<svg width="{2 * r + 12}" height="{2 * r + 12}"><circle cx="{r + 6}" cy="{r + 6}" r="{r}" fill="{color}" stroke="#111" stroke-width="6"/></svg>'


def maplab(txt, size=38):
    return f'<div style="font-weight:800;font-size:{size}px;text-shadow:0 4px 0 #000;white-space:nowrap">{txt}</div>'


def build():
    bs = []

    # ── 01 HOOK ──
    b = B(1, "Paryż, 1925", "ktoś sprzedał Wieżę Eiffla. Na złom.")
    b.el(eiffel(600), 960, 650, 0.2, a="su", idle="breathe")
    tw = A(1, "sprzedał")
    b.el(tag("NA SPRZEDAŻ"), 1290, 440, tw - 0.1, rot=12, idle="sway", z=7)
    tz = A(1, "Na złom")
    b.el(stamp("SPRZEDANE", 100), 960, 790, tz, a="stamp", rot=-12, z=9)
    b.shake(tz + 0.2, 13); b.flash.append(tz + 0.2); b.punch.append([tz + 0.2, 0.03])
    b.el(f'<div class="big" style="font-size:120px;color:{P}">1925</div>', 430, 450, A(1, "1925"), rot=-6, idle="float")
    b.el(emo("🔩", 120), 1520, 860, A(1, "Wieżę Eiffla"), idle="wig", z=8)
    b.el(emo("🔩", 90), 420, 860, A(1, "Wieżę Eiffla") + 0.2, rot=40, idle="wig", z=8)
    bs.append(b)

    # ── 02 ──
    b = B(2, "Mały problem", "a właściwie dwa")
    b.el(eiffel(380), 330, 660, b.start + 0.2, a="sl", idle="breathe")
    for i, (l, ph, y) in enumerate([("WŁAŚCICIEL", "nie należała", 470), ("URZĘDNIK", "nie był nawet", 720)]):
        t = A(2, ph)
        b.el(card(T(l, 72, "#fff", cls="big"), 820, 170), 1080, y, t, a="sr", rot=(-2, 2)[i])
        b.el(cross(130), 1530, y, t + 0.45, a="stamp", z=8, snd="buzz")
        b.shake(t + 0.6, 6)
    b.el(f'<div class="chyba" style="background:#3a4450;font-size:36px">za którego się podawał</div>', 1060, 870, A(2, "za którego"), rot=-3, z=9)
    bs.append(b)

    # ── 03 ──
    b = B(3, "To nie koniec", "")
    b.el(eiffel(330), 520, 650, b.start + 0.15, a="drop", rot=-6, idle="sway")
    td = A(3, "dwa razy")
    b.el(eiffel(330), 900, 650, td - 0.2, a="drop", rot=5, idle="sway")
    b.el(f'<div class="big" style="font-size:330px;color:{Y}">×2</div>', 1440, 640, td, a="stamp", rot=-8, z=9)
    b.shake(td + 0.2, 14); b.flash.append(td + 0.2); b.punch.append([td + 0.2, 0.035])
    b.el('<div class="chyba" style="font-size:64px">?!</div>', 1690, 410, td + 0.4, rot=12, idle="wig", z=10)
    bs.append(b)

    # ── 04 ──
    b = B(4, "Victor Lustig", "najgładszy oszust w historii")
    b.el(card("", 560, 680, border=Y), 640, 640, b.start + 0.12, snd=False)
    b.el(conman(330), 640, 610, A(4, "Victora"), a="drop", z=6, idle="bob")
    b.el(T("HRABIA (TAK SIĘ PRZEDSTAWIAŁ)", 26, G, extra="font-weight:800;letter-spacing:2px"), 640, 935, A(4, "Victora") + 0.3, a="fade", z=6)
    tg = A(4, "najgładszym")
    for i, (l, v) in enumerate([("ELEGANCJA", 10), ("GADANE", 10), ("SZCZEROŚĆ", 0)]):
        barh = f'<div style="width:420px;height:30px;border-radius:15px;background:#2a2f37;overflow:hidden"><div style="width:{max(14, v * 42)}px;height:30px;background:{(Y, Y, RED)[i]}"></div></div>'
        b.el(f'<div style="display:flex;flex-direction:column;gap:10px">{T(l, 40, extra="font-weight:800")}{barh}</div>', 1400, 440 + 150 * i, tg + 0.35 * i, a="sr", z=6)
    b.el(T("rysunek, nie portret", 28, G, extra="font-weight:600"), 1400, 900, b.start + 0.6, a="fade", snd=False)
    bs.append(b)

    # ── 05 KIM BYŁ ──
    b = B(5, "Rok 1890", "Austro-Węgry → dziś Czechy", src="źródło: Smithsonian, The Mob Museum")
    b.el(card("", 760, 520, border=Y), 1220, 640, b.start + 0.2, a="zoom", snd=False)
    b.el(maplab("AUSTRO-WĘGRY", 50), 1220, 450, A(5, "Austro-Węgrzech"), a="sd", z=6)
    b.el(emo("📍", 110), 1220, 610, A(5, "w miasteczku"), a="drop", z=6)
    b.el(f'<div class="pill" style="font-size:38px">dziś: <span style="color:{Y}">CZECHY</span></div>', 1220, 780, A(5, "dziś leży"), a="su", z=6)
    b.count(420, 470, 1850, 1890, b.start + 0.4, 1.2, size=180)
    tt = A(5, "Przynajmniej tak twierdził")
    b.el('<div class="chyba">(podobno)</div>', 420, 650, tt, rot=-7, z=9)
    tp = A(5, "nigdy nic")
    b.el(f'<div class="big" style="font-size:150px;color:{P}">???</div>', 420, 840, tp, a="stamp", rot=6, idle="wig", z=9)
    b.shake(tp + 0.2, 6)
    bs.append(b)

    # ── 06 ──
    b = B(6, "Dziesiątki nazwisk", "hrabia, poliglota, „milioner”")
    names = ["HRABIA LUSTIG", "R. MILLER", "G. SIMON", "C. GRUBER", "V. SCHARF", "?????"]
    t0 = A(6, "dziesiątek nazwisk")
    for i, n in enumerate(names):
        b.el(paper(f'<div style="font-weight:900;font-style:italic;font-size:40px;white-space:nowrap">{n}</div><div style="font-weight:600;font-size:22px;color:#6a6252;margin-top:6px">wizytówka</div>', 420, 140, pad=26),
             (360, 800)[i % 2], (420, 590, 760)[i // 2], t0 + 0.16 * i, a="pop", rot=(-6, 4, 3, -5, -3, 6)[i], z=4 + i, snd=i % 2 == 0)
    th = A(6, "hrabią")
    b.el(hat(260), 1380, 430, th, a="drop", rot=-6, idle="bob")
    tj = A(6, "kilku językach")
    for i, (w, x, y) in enumerate([("Bonjour!", 1220, 600), ("Guten Tag!", 1560, 640), ("Hello!", 1330, 740)]):
        b.el(f'<div class="pill" style="font-size:34px">{w}</div>', x, y, tj + 0.22 * i, rot=(-4, 5, -2)[i], z=6)
    tm = A(6, "jak milioner")
    b.el(emo("💎", 120), 1620, 880, tm, idle="pulse", z=7)
    b.el('<div class="ypill" style="font-size:42px">STYL: MILIONER</div>', 1290, 880, tm + 0.1, rot=-3, z=7)
    bs.append(b)

    # ── 07 ──
    b = B(7, "Akta policji", "nawet to nie jest pewne", src="źródło: The Mob Museum, The Hustle")
    b.el(paper("", 760, 560, rot=-3, col="#c9a25a"), 760, 640, b.start + 0.15, a="drop")
    b.el(T("AKTA", 70, "#3a2a0a", cls="big", extra="text-shadow:none"), 760, 430, b.start + 0.3, a="fade", z=6)
    tm = A(7, "Robert Miller")
    b.el(paper(f'<div style="font-weight:600;font-size:26px;color:#6a6252">PRAWDZIWE NAZWISKO:</div><div style="font-weight:900;font-style:italic;font-size:64px;margin-top:6px;white-space:nowrap">Robert Miller</div>', 640, 200, rot=2, pad=30),
         760, 640, tm, a="sl", z=6)
    tn = A(7, "Ale nawet")
    b.el(stamp("???", 120), 980, 800, tn, a="stamp", rot=-14, z=9)
    b.shake(tn + 0.2, 9)
    b.el(emo("🕵️", 190), 1480, 640, A(7, "Policja"), idle="sway")
    b.el(f'<div class="big" style="font-size:110px;color:{P}">?</div>', 1600, 430, tn + 0.3, rot=14, idle="wig", z=8)
    bs.append(b)

    # ── 08 PLAN ──
    b = B(8, "Maj 1925", "Lustig czyta gazetę w Paryżu", src="źródło: Smithsonian")
    b.el(conman(230, smile=False), 360, 690, b.start + 0.3, a="sl", idle="bob")
    tg = A(8, "czyta w Paryżu")
    news = paper(f'<div style="font-weight:900;font-size:30px;letter-spacing:3px;border-bottom:4px solid #222;padding-bottom:8px">GAZETA PARYSKA · 1925</div>'
                 f'<div style="font-weight:900;font-style:italic;font-size:62px;line-height:1.05;margin-top:16px">WIEŻA KOSZTUJE<br>FORTUNĘ!</div>'
                 f'<div style="margin-top:22px;height:14px;background:#cfc6ae;border-radius:7px"></div><div style="margin-top:14px;height:14px;width:80%;background:#cfc6ae;border-radius:7px"></div>'
                 f'<div style="margin-top:14px;height:14px;background:#cfc6ae;border-radius:7px"></div>', 760, 470, rot=2)
    b.el(news, 1060, 620, tg, a="zoom")
    tk = A(8, "kosztuje majątek")
    b.el(card(f'<div class="big" style="font-size:60px;color:{Y}">KOSZTY ↑↑↑</div>', 380, 130, border=Y), 1660, 470, tk, rot=4, z=8)
    b.el(emo("💸", 130), 1680, 720, tk + 0.4, idle="float", z=8)
    bs.append(b)

    # ── 09 ──
    b = B(9, "Wieża na 20 lat", "potem miała zniknąć… uratowało ją radio", src="źródło: toureiffel.paris")
    b.el(eiffel(500), 1180, 700, b.start + 0.2, a="su")
    t20 = A(9, "dwadzieścia lat")
    b.el(card(f'<div class="big" style="font-size:92px">1889 <span style="color:{Y}">+ 20</span></div>' + lab("pozwolenie", 34, G), 600, 220), 560, 430, t20, rot=-3)
    tr = A(9, "Uratowało ją radio")
    waves = "".join(f'<path d="M{1180 - r} {440 - r * 0.3:.0f} A{r} {r} 0 0 1 {1180 + r} {440 - r * 0.3:.0f}" stroke="{Y}" stroke-width="10" fill="none" stroke-linecap="round" data-draw="1" data-t="__T{tr + 0.2 * i}__" data-d="0.4"/>' for i, r in enumerate([45, 80, 115]))
    b.svg(waves, tr, 0.6)
    b.el('<div class="ypill" style="font-size:42px">RADIO RATUJE WIEŻĘ</div>', 560, 640, tr + 0.2, a="stamp", rot=-2, z=8)
    b.shake(tr + 0.4, 6)
    ta = A(9, "wcale nie brzmiał")
    b.el(card(lab("„pozbądźmy się jej”?", 34) + f'<div class="big" style="font-size:70px;color:{GREEN};margin-top:10px">BRZMI REALNIE</div>', 760, 230), 560, 860, ta, rot=2, z=7)
    bs.append(b)

    # ── 10 ──
    b = B(10, "Papier z pieczątką", "i listy do handlarzy złomem")
    tf = A(10, "u fałszerza")
    b.el(emo("🖋️", 140), 330, 430, tf, idle="wig")
    tp = A(10, "papier firmowy")
    b.el(paper(f'<div style="font-weight:900;font-size:26px;letter-spacing:2px">MINISTERSTWO · PARYŻ</div><div style="margin-top:18px;height:12px;background:#cfc6ae;border-radius:6px"></div>'
               f'<div style="margin-top:12px;height:12px;width:70%;background:#cfc6ae;border-radius:6px"></div><div style="margin-top:12px;height:12px;background:#cfc6ae;border-radius:6px"></div>', 460, 560, rot=-4),
         560, 680, tp, a="su")
    tz = A(10, "pieczątkami")
    b.el(f'<div style="width:150px;height:150px;border-radius:50%;border:10px solid {RED};color:{RED};font-weight:900;font-size:30px;display:flex;align-items:center;justify-content:center;text-align:center;line-height:1">RZĄD<br>FR</div>',
         680, 840, tz, a="stamp", rot=-18, z=7)
    b.shake(tz + 0.2, 6)
    t6 = A(10, "sześciu")
    for i in range(6):
        x, y = 1160 + (i % 3) * 230, 470 + (i // 3) * 200
        b.el(envelope(190), x, y, t6 + 0.13 * i, a="sl", rot=(-6, 4, -2, 5, -4, 3)[i], idle="float", z=6, snd=i % 2 == 0)
    b.el('<div class="ypill" style="font-size:40px">6 NAJWIĘKSZYCH HANDLARZY</div>', 1390, 870, A(10, "handlarzy złomem"), rot=-2, z=8)
    bs.append(b)

    # ── 11 ──
    b = B(11, "„Pan wicedyrektor”", "ministerstwo poczt i telegrafów", src="źródło: Smithsonian, The Hustle")
    tw = A(11, "wicedyrektor")
    b.el(paper(f'<div style="font-weight:600;font-size:24px;color:#6a6252;letter-spacing:2px">MINISTERSTWO POCZT I TELEGRAFÓW</div>'
               f'<div style="font-weight:900;font-style:italic;font-size:62px;margin-top:10px">V. Lustig</div><div style="font-weight:800;font-size:34px;color:#b3261e">WICEDYREKTOR</div>', 620, 260, rot=-3),
         520, 520, tw, a="drop")
    b.el('<div class="chyba" style="background:#3a4450;font-size:34px">nieprawda</div>', 700, 690, tw + 0.9, rot=6, z=8)
    th = A(11, "tajne spotkanie")
    hotel = """<svg width="620" height="500" viewBox="0 0 620 500" style="overflow:visible;display:block"><g filter="url(#stk)"><rect x="40" y="120" width="540" height="380" fill="#e9dfc8"/>
<path d="M20 130 L310 30 L600 130 Z" fill="#cfc2a2"/></g>""" + "".join(
        f'<rect x="{80 + 92 * c}" y="{170 + 100 * r}" width="56" height="70" rx="28" fill="#2a2f37"/>' for c in range(5) for r in range(3)) + \
        '<rect x="260" y="400" width="100" height="100" rx="50" fill="#6e4220"/><rect x="40" y="485" width="540" height="15" fill="#b8a77d"/></svg>'
    b.el(hotel, 1370, 650, th, a="su")
    tc = A(11, "Hôtel de Crillon")
    b.el(tag("HÔTEL DE CRILLON", P, "#fff", 44), 1370, 380, tc, rot=-4, z=8)
    b.el(T("(rysunek)", 26, G, extra="font-weight:600"), 1370, 930, tc + 0.3, a="fade", snd=False)
    b.el(emo("🤫", 120), 520, 860, th + 0.2, idle="wig")
    bs.append(b)

    # ── 12 ──
    b = B(12, "„Rząd sprzedaje wieżę”", "tak brzmiała bajka na spotkaniu")
    b.el(eiffel(500), 470, 660, b.start + 0.25, a="su", idle="breathe")
    ts = A(12, "na złom")
    b.el(tag("NA ZŁOM"), 690, 520, ts, rot=10, idle="sway", z=7)
    tt = A(12, "siedem tysięcy")
    b.el(card(f'<div class="big" style="font-size:120px;color:{Y}">{cnt(b, 0, 7000, tt, 1.1, "#+")}</div>' + lab("ton żelaza (tak mówił)", 38, G), 760, 300, border=Y), 1300, 520, tt, rot=-2)
    tb = A(12, "kto da najwięcej")
    b.el(emo("🔨", 170), 1300, 830, tb, a="drop", rot=-25, idle="wig", z=7)
    b.shake(tb + 0.35, 9); b.sfx("stamp", tb + 0.3, 1300)
    b.el('<div class="ypill" style="font-size:40px">LICYTACJA</div>', 1560, 860, tb + 0.4, rot=4, z=8)
    bs.append(b)

    # ── 13 ──
    b = B(13, "Ale sza…", "")
    b.dim.append([b.start + 0.2, b.start + 0.8, 0, 0.3])
    b.el(emo("🤫", 330), 560, 640, b.start + 0.25, idle="bob")
    ta = A(13, "będzie afera")
    for i, (x, y) in enumerate([(1180, 470), (1500, 520), (1340, 360)]):
        b.el(emo("📰", 110), x, y, ta + 0.12 * i, rot=(-12, 10, 3)[i], idle="jit", z=6, snd=i == 0)
    b.el('<div class="big" style="font-size:96px;color:#ff3b3b">AFERA!</div>', 1340, 640, ta + 0.35, rot=-5, idle="jit", z=7)
    tt = A(13, "wszystko jest tajne")
    b.el(stamp("ŚCIŚLE TAJNE", 92), 1260, 830, tt, a="stamp", rot=-8, z=9)
    b.shake(tt + 0.2, 11); b.flash.append(tt + 0.2)
    bs.append(b)

    # ── 14 ──
    b = B(14, "Wycieczka po wieży", "i cichy casting na ofiarę")
    b.el(eiffel(470), 1560, 640, b.start + 0.15, a="sr")
    tl = A(14, "limuzyną")
    b.el(emo("🚗", 190), 560, 880, tl, a="sl", idle="drive")
    b.draw("M200 960 L1820 960", tl - 0.1, 0.8, color=G, w=6, dash="30 22", snd="swipe")
    tp = A(14, "A sam patrzy")
    for i in range(6):
        b.el(person(120), 330 + 150 * i, 560, tp - 0.9 + 0.08 * i, a="pop", z=5, snd=i == 0)
    th = A(14, "połknie haczyk")
    lens = '<svg width="260" height="260" viewBox="-130 -130 260 260" style="overflow:visible"><circle r="90" fill="rgba(255,255,255,.12)" stroke="#fff" stroke-width="16"/><path d="M64 64 L120 120" stroke="#fff" stroke-width="22" stroke-linecap="round"/></svg>'
    b.el(lens, 330, 560, tp, a="pop", z=8)
    b.el(emo("🪝", 120), 1100, 400, th, a="drop", idle="sway", z=8)
    bs.append(b)

    # ── 15 HACZYK ──
    b = B(15, "Wybór: jeden", "nowy w Paryżu, chce do wielkich graczy")
    tj = A(15, "Wybiera jednego")
    for i in range(6):
        if i == 3: continue
        b.el(person(120), 360 + 240 * i, 860, b.start + 0.15 + 0.06 * i, a="su", z=5, snd=i == 0, style="filter:brightness(.55)")
    b.el(person(120), 1080, 860, b.start + 0.33, a="su", z=5, snd=False, out=tj, oa="up", od=0.3)
    b.el(person(190), 1080, 600, tj + 0.15, a="pop", z=6, idle="bob", style="filter:drop-shadow(0 0 30px #FFD21F)")
    b.el(stamp("CEL", 80), 1080, 370, tj + 0.35, a="stamp", rot=-8, z=8)
    b.shake(tj + 0.5, 8)
    for i, (l, ph, x, y) in enumerate([("NOWY W PARYŻU", "nowego w Paryżu", 500, 470), ("NIEPEWNY SIEBIE", "niepewnego", 500, 640), ("CHCE DO WIELKICH", "dołączyć", 1580, 560)]):
        b.el(f'<div class="pill" style="font-size:36px">{l}</div>', x, y, A(15, ph), a="sl" if x < 960 else "sr", rot=(-3, 2, 3)[i], z=7)
    bs.append(b)

    # ── 16 ──
    b = B(16, "Coś mu nie pasuje", "i tu wchodzi najlepszy ruch")
    b.el(person(220, hi=True), 520, 650, b.start + 0.2, a="fade", idle="bob", snd=False)
    tq = A(16, "dużo pytań")
    for i, (x, y, s) in enumerate([(380, 400, 110), (560, 360, 150), (720, 430, 100)]):
        b.el(f'<div class="big" style="font-size:{s}px;color:{P}">?</div>', x, y, tq + 0.18 * i, rot=(-12, 6, 15)[i], idle="wig", z=7)
    tn = A(16, "nie pasuje")
    b.el(f'<div class="pill" style="font-size:36px;border-color:{RED}">PODEJRZANE…</div>', 560, 900, tn, a="su", z=7)
    tg = A(16, "najbardziej genialną")
    b.el(conman(240), 1380, 730, tg - 0.6, a="sr", idle="bob")
    b.el(bulb(150), 1640, 470, tg, a="pop", z=8, idle="pulse")
    b.sfx("ding", tg + 0.1, 1380)
    b.punch.append([tg, 0.025])
    bs.append(b)

    # ── 17 ──
    b = B(17, "„Wie pan…”", "i cisza")
    b.el(conman(250), 380, 680, b.start + 0.2, a="fade", idle="bob", snd=False)
    bub = (f'<div style="position:relative;background:#fff;color:#111;border-radius:40px;padding:30px 50px;font-weight:800;font-size:46px;line-height:1.2;box-shadow:0 10px 0 #000;white-space:nowrap">'
           f'Urzędnik zarabia mało…<br><b style="color:{P}">a decyzja jest duża.</b>'
           '<div style="position:absolute;left:60px;bottom:-40px;width:0;height:0;border-left:30px solid transparent;border-right:30px solid transparent;border-top:44px solid #fff"></div></div>')
    b.el(bub, 1010, 430, A(17, "urzędnik zarabia"), a="pop", rot=-2)
    tm = A(17, "zarabia mało")
    b.el(f'<div class="card" style="width:250px;height:190px;border-color:{G}"><div class="emo flat" style="font-size:96px">👛</div>{lab("pusto", 36, G)}</div>', 910, 780, tm + 0.3, rot=-4)
    tc = A(17, "I czeka")
    b.el(clock(190), 1420, 780, tc, a="pop", z=7, idle="pulse")
    b.el('<div class="big" style="font-size:76px;color:#fff">…</div>', 1640, 780, tc + 0.2, idle="blinkop")
    b.sfx("ticks", tc + 0.1, 1420, 1.2)
    bs.append(b)

    # ── 18 ──
    b = B(18, "Łapówka?", "to musi być prawdziwy urzędnik")
    tl = A(18, "chodzi o łapówkę")
    b.el(envelope(300, col="#e7d8a8", seal=MONEY), 960, 560, tl, a="pop", rot=-6, idle="float")
    b.draw("M520 780 Q960 660 1400 780", tl + 0.3, 0.6, w=8, dash="20 14")
    b.el(emo("🫴", 150), 470, 800, tl + 0.1, a="sl")
    b.el(emo("🫴", 150), 1450, 800, tl + 0.3, a="sr")
    tz = A(18, "wszystko się zgadza")
    b.el(check(130), 1200, 420, tz, a="stamp", z=8, snd="ding")
    tk = A(18, "kto prosi o łapówkę")
    b.el(f'<div class="pill" style="font-size:40px">KTO PROSI O ŁAPÓWKĘ?</div>', 600, 380, tk, a="sl", rot=-3, z=7)
    tu = A(18, "prawdziwy urzędnik")
    b.el('<div class="ypill" style="font-size:50px">PRAWDZIWY URZĘDNIK!</div>', 960, 940, tu, a="stamp", rot=-3, z=9)
    b.shake(tu + 0.2, 7)
    b.el('<div class="chyba">(chyba)</div>', 1600, 640, tu + 0.45, rot=8, z=10)
    bs.append(b)

    # ── 19 ──
    b = B(19, "Ile?", "źródła podają różne kwoty", src="źródło: Smithsonian, The Hustle (różne kwoty)")
    tp = A(19, "Płaci za wieżę")
    for i in range(5):
        b.el(bill(260, "FR"), 420 + 20 * i, 520 - 26 * i, tp + 0.12 * i, a="drop", rot=(-8, 4, -3, 6, -2)[i], z=4 + i, snd=i == 0)
    tl = A(19, "daje łapówkę")
    b.el(envelope(220, col="#e7d8a8", seal=MONEY), 470, 820, tl, a="sl", rot=8, z=9)
    t7 = A(19, "siedemdziesiąt tysięcy")
    b.el(card(f'<div class="big" style="font-size:110px;color:{Y}">~{cnt(b, 0, 70, t7, 0.9, "# 000")}</div>' + lab("franków (różne wersje)", 32, G), 860, 270, border=Y),
         1240, 470, t7, rot=-2, z=6)
    td = A(19, "czyli dziś")
    b.draw("M1240 620 V700", td - 0.1, 0.3, w=9, color=G, snd=False)
    b.el(card(f'<div class="big" style="font-size:70px">dziś: <span style="color:{GREEN}">fortuna</span></div>' + lab("szacunki mocno się różnią", 28, G), 760, 200), 1240, 820, td, a="su", rot=2, z=6)
    bs.append(b)

    # ── 20 ──
    b = B(20, "A Lustig?", "pociąg do Wiednia")
    (px, py), (wx, wy) = (520, 640), (1400, 660)
    for n, (x, y) in [("Paryż", (px, py)), ("Wiedeń", (wx, wy))]:
        b.el(dot(Y), round(x), round(y), b.start + 0.25, z=6)
        b.el(maplab(n, 44), round(x), round(y + 56), b.start + 0.35, a="fade", z=6, snd=False)
    tw = A(20, "w pociągu")
    b.draw(f"M{px:.0f} {py:.0f} Q{(px + wx) / 2:.0f} {py - 300:.0f} {wx:.0f} {wy:.0f}", tw - 0.2, 1.3, w=9, dash="24 16")
    b.el(train(330), round((px + wx) / 2), 400, tw, a="sl", idle="drive", z=7)
    ts = A(20, "Z walizką")
    b.el(suitcase(300, open_=True), 960, 840, ts, a="drop", rot=-3, z=8, idle="bob")
    b.shake(ts + 0.35, 7); b.sfx("ding", ts + 0.4, 960)
    bs.append(b)

    # ── 21 DRUGI RAZ ──
    b = B(21, "Cisza", "codziennie gazeta… i nic")
    b.dim.append([b.start, b.start + 0.6, 0, 0.25])
    tg = A(21, "czyta gazety")
    for i in range(4):
        b.el(paper(f'<div style="font-weight:900;font-size:26px;letter-spacing:2px;border-bottom:3px solid #222;padding-bottom:6px">GAZETA · DZIEŃ {i + 1}</div>'
                   f'<div style="margin-top:18px;font-weight:800;font-size:30px;color:#9a917c">(nic o wieży)</div>', 420, 230, rot=(-6, 4, -2, 7)[i], pad=24),
             520 + 70 * i, 500 + 60 * i, tg + 0.25 * i, a="drop", z=4 + i, snd=i % 2 == 0)
    tn = A(21, "Nic.")
    b.el(card(f'<div class="big" style="font-size:150px">0</div>' + lab("artykułów", 36, G), 480, 340), 1380, 600, tn, a="pop")
    ta = A(21, "Ani słowa")
    b.el(emo("🦗", 120), 1550, 870, ta, a="sr", idle="bob")
    bs.append(b)

    # ── 22 ──
    b = B(22, "Wstyd > pieniądze", "oszukany handlarz woli milczeć")
    b.el(person(260, hi=True), 520, 680, b.start + 0.2, a="fade", snd=False)
    tm = A(22, "woli milczeć")
    bag = '<svg width="230" height="200" viewBox="-115 -100 230 200" style="overflow:visible"><g filter="url(#stk)"><path d="M-90 80 Q-110 -40 -40 -80 Q0 -96 40 -80 Q110 -40 90 80 Z" fill="#c9a25a"/></g><path d="M-60 60 Q0 76 60 60" stroke="#7a5524" stroke-width="8" fill="none"/></svg>'
    b.el(bag, 520, 520, tm, a="drop", z=7, idle="wig")
    b.shake(tm + 0.3, 5)
    tp = A(22, "przyznać się")
    b.el(card(T("„Kupiłem Wieżę Eiffla", 46, extra="font-weight:800") + T("od faceta z hotelu”", 46, Y, extra="font-weight:800"), 820, 220), 1300, 500, tp, rot=2)
    th = A(22, "od faceta z hotelu")
    b.el(cross(130), 1680, 390, th + 0.3, a="stamp", z=8, snd="buzz")
    b.el('<div class="ypill" style="font-size:42px">LEPIEJ NIC NIE MÓWIĆ</div>', 1300, 790, th + 0.6, rot=-3, z=8)
    bs.append(b)

    # ── 23 ──
    b = B(23, "Powrót do Paryża", "bo czemu nie jeszcze raz?")
    (px, py), (wx, wy) = (520, 520), (1400, 540)
    for n, (x, y) in [("Paryż", (px, py)), ("Wiedeń", (wx, wy))]:
        b.el(dot(Y), round(x), round(y), b.start + 0.2, z=6, snd=False)
        b.el(maplab(n, 44), round(x), round(y - 56), b.start + 0.25, a="fade", z=6, snd=False)
    tw = A(23, "wraca do Paryża")
    b.draw(f"M{wx:.0f} {wy:.0f} Q{(px + wx) / 2:.0f} {wy + 230:.0f} {px:.0f} {py:.0f}", tw - 0.2, 1.1, w=9, dash="24 16", color=P)
    b.el(train(300, Y), round((px + wx) / 2), 700, tw, a="sr", idle="drive", z=7)
    tn = A(23, "normalny człowiek")
    b.el(f'<div class="pill" style="font-size:36px">NORMALNY CZŁOWIEK: UCIEKA</div>', 960, 350, tn, a="sd", z=7)
    tr = A(23, "jeszcze raz")
    b.el(stamp("SPRZEDANE ×2", 84), 820, 860, tr, a="stamp", rot=-10, z=9)
    b.shake(tr + 0.2, 12); b.flash.append(tr + 0.2)
    bs.append(b)

    # ── 24 ──
    b = B(24, "Tym razem: policja", "Lustig ucieka za ocean")
    for i, (l, ph) in enumerate([("NOWI HANDLARZE", "Nowi handlarze"), ("TEN SAM HOTEL", "ten sam hotel"), ("TA SAMA BAJKA", "ta sama bajka")]):
        b.el(f'<div class="pill" style="font-size:34px">{l}</div>', 420, 380 + 100 * i, A(24, ph), a="sl", rot=(-2, 1, -1)[i], z=6)
    tp = A(24, "idzie na policję")
    b.el(emo("🚨", 170), 1080, 450, tp, idle="wig", z=7)
    b.sfx("alarm", tp, 1080); b.flash.append(tp)
    b.el(emo("👮", 150), 1300, 470, tp + 0.2, a="sr", idle="bob", z=7)
    tu = A(24, "ucieka w ostatniej")
    to = A(24, "Za ocean")
    b.el(conman(170, smile=False, bag=True), 760, 760, tu, a="sr", idle="jit", out=to + 0.2, oa="left", od=0.5, z=7)
    b.draw("M560 880 Q960 820 1360 880 T1860 880", to - 0.2, 0.8, color="#4aa3ff", w=10, snd="swipe")
    b.el(ship(300), 1300, 790, to, a="sl", idle="bob", z=6)
    b.el('<div class="ypill" style="font-size:40px">→ AMERYKA</div>', 1620, 640, A(24, "do Ameryki"), rot=-4, z=8)
    bs.append(b)

    # ── 25 ──
    b = B(25, "Dla uczciwości", "źródła się różnią", src="źródło: Smithsonian, The Hustle, Mental Floss")
    beam = '<svg width="900" height="420" viewBox="-450 -60 900 420" style="overflow:visible"><g filter="url(#stk)"><path d="M-30 340 L0 0 L30 340 Z" fill="#cfd6df"/><rect x="-400" y="-12" width="800" height="24" rx="12" fill="#cfd6df"/></g></svg>'
    b.el(beam, 960, 800, b.start + 0.2, a="fade", z=3, snd=False)
    tm = A(25, "po miesiącu")
    b.el(card(T("MIESIĄC", 66, cls="big") + lab("część źródeł", 30, G), 460, 220), 610, 600, tm, a="drop", rot=-3, z=5)
    tp = A(25, "po pół roku")
    b.el(card(T("PÓŁ ROKU", 66, cls="big") + lab("inne źródła", 30, G), 460, 220), 1310, 600, tp, a="drop", rot=3, z=5)
    td = A(25, "druga sprzedaż")
    b.el(f'<div class="pill" style="font-size:36px">DRUGA SPRZEDAŻ: <span style="color:{P}">?</span></div>', 960, 950, td, a="su", z=7)
    tz = A(25, "musiał zwiewać")
    b.el(stamp("UCIECZKA", 76, GREEN), 960, 380, tz, a="stamp", rot=-6, z=9)
    b.shake(tz + 0.2, 9)
    bs.append(b)

    # ── 26 AMERYKA ──
    b = B(26, "Część 2", "wieża to nie było najdziwniejsze")
    tz = A(26, "W zapowiedzi")
    tp = A(26, "najdziwniejsze")
    b.el(eiffel(380), 960, 650, tz, a="pop", z=9, out=tp - 0.1, oa="pop", od=0.25)
    for side, x in [(-1, 480), (1, 1440)]:
        b.el(f'<div style="width:980px;height:900px;background:repeating-linear-gradient(90deg,#9e1b2c 0 60px,#7d1322 60px 120px);box-shadow:0 0 0 8px #000"></div>', x, 650,
             b.start + 0.1, a="none", out=tp, oa="left" if side < 0 else "right", od=0.6, z=8, snd=False)
    b.el(f'<div class="big" style="font-size:180px;color:{Y}">CZĘŚĆ 2</div>', 960, 600, A(26, "No to proszę"), a="stamp", rot=-4, z=6)
    b.shake(A(26, "No to proszę") + 0.2, 10); b.flash.append(A(26, "No to proszę") + 0.2)
    b.el('<div class="chyba" style="font-size:50px">jeszcze dziwniej</div>', 1240, 800, tp + 0.5, rot=-6, z=9)
    b.sfx("swish", tp, 960)
    bs.append(b)

    # ── 27 ──
    b = B(27, "Maszyna do pieniędzy", "„drukuje studolarówki” (podobno)", src="źródło: Smithsonian")
    tb = A(27, "skrzynkę")
    b.el(box(380), 620, 660, tb, a="drop", idle="breathe")
    b.el('<div class="chyba">(podobno)</div>', 620, 400, A(27, "podobno"), rot=-8, z=9)
    td = A(27, "drukuje studolarówki")
    for i in range(3):
        b.el(bill(260, "100"), 1040 + 130 * i, 470 + 50 * i, td + 0.3 * i, a="sl", rot=(-10, 6, -4)[i], idle="float", z=6)
    tn = A(27, "Naprawdę w środku")
    b.el(card(lab("w środku:", 34, G) + T("prawdziwe banknoty", 46, Y, extra="font-weight:800"), 620, 190), 1220, 820, tn, a="su", rot=2, z=7)
    tl = A(27, "Lustig był daleko")
    b.el(emo("💨", 160), 1680, 400, tl, a="sr", idle="wig", z=8)
    b.el('<div class="ypill" style="font-size:40px">PA PA!</div>', 1660, 620, tl + 0.2, rot=8, z=8)
    bs.append(b)

    # ── 28 ──
    b = B(28, "Pożyczka od Ala Capone", "tak, tego Ala Capone", src="źródło: Smithsonian")
    tc = A(28, "Ala Capone")
    b.el(card(person(170, col="#5c6470") + T("AL CAPONE", 56, cls="big", extra="margin-top:10px") + lab("(sam napis, bez portretu)", 24, G), 460, 470, border=RED),
         470, 640, tc, rot=-3)
    tt = A(28, "Tak, tego")
    b.el(f'<div class="big" style="font-size:120px;color:{P}">!!</div>', 760, 400, tt, rot=10, idle="wig", z=8)
    t5 = A(28, "pięćdziesiąt tysięcy")
    b.el(card(f'<div class="big" style="font-size:110px;color:{GREEN}">{cnt(b, 0, 50, t5, 0.8, "# 000 $")}</div>' + lab("pożyczka", 32, G), 740, 240, border=GREEN), 1330, 480, t5, a="sr", rot=2)
    tx = A(28, "odda podwójnie")
    b.el(clock(150), 1080, 800, A(28, "za dwa miesiące"), a="pop", z=7)
    b.el(f'<div class="big" style="font-size:150px;color:{Y}">×2</div>', 1400, 790, tx, a="stamp", rot=-6, z=8)
    b.shake(tx + 0.2, 8)
    b.el('<div class="pill" style="font-size:30px">OBIETNICA</div>', 1640, 840, tx + 0.3, rot=4, z=8)
    bs.append(b)

    # ── 29 ──
    b = B(29, "Najdziwniejszy zwrot", "według relacji", src="źródło: Smithsonian")
    tn = A(29, "w ogóle nie rusza")
    to = A(29, "oddaje całe")
    b.el(safe(330), 440, 620, b.start + 0.25, a="drop", idle="breathe", out=to - 0.05, oa="fade", od=0.2)
    b.el(f'<div class="pill" style="font-size:34px">NIETKNIĘTE</div>', 440, 890, tn, a="su", z=7)
    b.el(safe(330, open_=True), 440, 620, to, a="fade", d=0.2, snd=False)
    b.el(card(f'<div class="big" style="font-size:90px;color:{GREEN}">50 000 $</div>' + lab("wraca do Capone", 30, G), 600, 210), 1140, 420, to + 0.1, a="sr", rot=-2)
    b.el('<div style="background:#fff;color:#111;border-radius:40px;padding:20px 40px;font-weight:800;font-style:italic;font-size:44px;box-shadow:0 8px 0 #000;white-space:nowrap">„Interes nie wyszedł, przepraszam.”</div>',
         1140, 610, A(29, "interes nie wyszedł"), rot=2, z=7)
    tz = A(29, "zaskoczony")
    b.el(emo("😲", 130), 1600, 410, tz, idle="wig", z=8)
    t5 = A(29, "pięć tysięcy")
    b.el(f'<div class="big" style="font-size:150px;color:{Y}">+5000 $</div>', 1100, 820, t5, a="stamp", rot=-5, z=9)
    b.shake(t5 + 0.2, 10); b.flash.append(t5 + 0.2); b.sfx("ding", t5 + 0.25, 1100)
    tc = A(29, "I o to właśnie")
    b.el(conman(150), 1660, 660, tc, a="pop", idle="wig", z=9)
    b.el('<div class="chyba" style="font-size:36px">to był plan</div>', 1660, 830, tc + 0.3, rot=-6, z=10)
    bs.append(b)

    # ── 30 ──
    b = B(30, "„Pieniądze Lustiga”", "tak Secret Service nazwało jego fałszywki", src="źródło: Smithsonian")
    tp = A(30, "podrabiać dolary")
    for i in range(4):
        b.el(bill(300, "100"), 520 + 30 * i, 470 + 70 * i, tp + 0.15 * i, a="drop", rot=(-8, 5, -3, 7)[i], z=4 + i, snd=i % 2 == 0)
    tt = A(30, "Tak dobre")
    lens = '<svg width="330" height="330" viewBox="-165 -165 330 330" style="overflow:visible"><circle r="120" fill="rgba(255,255,255,.14)" stroke="#fff" stroke-width="18"/><path d="M86 86 L150 150" stroke="#fff" stroke-width="26" stroke-linecap="round"/></svg>'
    b.el(lens, 760, 600, tt, a="sr", idle="float", z=9)
    b.el(f'<div class="ypill" style="font-size:40px;background:{GREEN}">WYGLĄDA JAK PRAWDZIWY</div>', 600, 920, tt + 0.4, rot=-3, z=10)
    ts = A(30, "Secret Service")
    b.el(card(lab("SECRET SERVICE:", 32, G) + T("„PIENIĄDZE LUSTIGA”", 56, Y, cls="big", extra="margin-top:8px"), 760, 220, border=Y), 1420, 450, ts, a="sr", rot=2, z=8)
    tl = A(30, "pieniędzmi Lustiga")
    b.el(stamp("FAŁSZYWE", 80), 1420, 720, tl + 0.3, a="stamp", rot=-10, z=9)
    b.shake(tl + 0.5, 8)
    bs.append(b)

    # ── 31 ──
    b = B(31, "Nowy Jork, 1935", "ucieczka dzień przed procesem", src="źródło: Smithsonian, The Mob Museum")
    tw = A(31, "wpada w Nowym Jorku")
    td = A(31, "Dzień przed")
    b.el(stamp("ZŁAPANY", 72), 470, 430, tw + 0.4, a="stamp", rot=-6, z=8, out=td, oa="pop", od=0.25)
    bld = ('<svg width="460" height="558" viewBox="0 0 560 680" style="overflow:visible;display:block"><g filter="url(#stk)"><rect x="20" y="20" width="520" height="660" fill="#5c6470"/></g>'
           + "".join(f'<rect x="{60 + 120 * c}" y="{60 + 130 * r}" width="80" height="90" rx="6" fill="{"#cfe7ff" if (c, r) == (2, 0) else "#2a2f37"}"/>' for c in range(4) for r in range(5)) + '</svg>')
    b.el(bld, 1100, 640, b.start + 0.2, a="su", z=3)
    tl = A(31, "linę z prześcieradeł")
    b.draw("M1150 480 C1130 560 1170 620 1150 700 C1130 760 1170 820 1150 880", tl, 0.9, w=16, color="#fff")
    tm = A(31, "udaje, że myje")
    b.el(emo("🧽", 110), 1250, 560, tm, a="pop", idle="wig", z=8)
    b.el(f'<div class="pill" style="font-size:34px">„TYLKO MYJĘ OKNA”</div>', 1600, 440, tm + 0.2, rot=4, z=8)
    tz = A(31, "Przechodnie patrzą")
    for i, x in enumerate([380, 520, 660]):
        b.el(person(110), x, 880, tz + 0.12 * i, a="su", z=6, snd=i == 0)
    b.el(f'<div class="big" style="font-size:90px;color:{G}">…</div>', 520, 700, A(31, "i nic") + 0.1, idle="blinkop", z=7)
    bs.append(b)

    # ── 32 ──
    b = B(32, "Koniec ucieczki", "Pittsburgh → wyrok → Alcatraz", src="źródło: Smithsonian, The Mob Museum")
    usa = '<svg width="1500" height="560" viewBox="0 0 1500 560" style="overflow:visible;display:block"><path d="M60 140 L330 90 L700 110 L1000 130 L1180 90 L1330 150 L1420 120 L1390 260 L1300 380 L1220 470 L1150 420 L900 440 L760 530 L640 430 L420 420 L240 360 L120 320 L70 240 Z" fill="#1c1f25" stroke="#cfd6df" stroke-width="7" stroke-linejoin="round"/></svg>'
    b.el(usa, 960, 640, b.start + 0.15, a="fade", z=2, snd=False)
    ny, pi = (1580, 520), (1400, 560)
    b.el(dot(Y), *ny, b.start + 0.3, z=6); b.el(maplab("Nowy Jork", 34), ny[0] + 30, ny[1] - 50, b.start + 0.35, a="fade", z=6, snd=False)
    tp = A(32, "w Pittsburghu")
    b.draw(f"M{ny[0]} {ny[1]} Q1500 620 {pi[0]} {pi[1]}", tp - 0.5, 0.5, w=8, dash="18 12")
    b.el(dot(P), *pi, tp, z=6); b.el(maplab("Pittsburgh", 34), pi[0] - 30, pi[1] + 52, tp + 0.05, a="fade", z=6, snd=False)
    b.el(stamp("ZŁAPANY", 60), 1150, 380, tp + 0.2, a="stamp", rot=-8, z=8)
    t20 = A(32, "dwadzieścia lat")
    b.el(card(f'<div class="big" style="font-size:110px">{cnt(b, 0, 20, t20, 0.7, "# LAT")}</div>', 440, 180, border=RED), 900, 800, t20, rot=-2, z=7)
    ta = A(32, "Alcatraz")
    al = (330, 640)
    b.el(f'<div style="width:150px;height:76px;border-radius:50%;background:#5c6470;border:6px solid #fff;box-shadow:0 6px 0 #000"></div>', *al, ta, a="pop", z=6)
    b.el('<div class="ypill" style="font-size:46px">ALCATRAZ</div>', al[0] + 60, al[1] + 110, ta + 0.1, rot=-3, z=8)
    b.shake(ta + 0.3, 8)
    bs.append(b)

    # ── 33 ──
    b = B(33, "Rok 1947", "akt zgonu i jedna rubryka", src="źródło: The Mob Museum, Wikipedia")
    b.el(f'<div class="big" style="font-size:140px;color:{G}">1947</div>', 400, 480, A(33, "Umiera"), a="fade", d=0.6)
    tn = A(33, "I tu najlepsze")
    b.el('<div class="chyba" style="background:#3a4450">i tu najlepsze</div>', 400, 680, tn, rot=-6, z=8)
    ta = A(33, "akcie zgonu")
    doc = paper(f'<div style="font-weight:900;font-size:34px;letter-spacing:3px;text-align:center;border-bottom:4px solid #222;padding-bottom:10px">AKT ZGONU</div>'
                + "".join(f'<div style="display:flex;gap:16px;margin-top:26px;align-items:flex-end;height:48px"><div style="font-weight:800;font-size:26px;width:180px;color:#6a6252">{k}</div><div style="flex:1;border-bottom:3px dotted #999;font-weight:700;font-size:30px">{v}</div></div>'
                          for k, v in [("NAZWISKO", "Lustig"), ("ROK", "1947"), ("ZAWÓD", "")]), 760, 460, rot=0)
    b.el(doc, 1190, 640, ta, a="su")
    tz = A(33, "w rubryce zawód")
    b.el(f'<div style="width:500px;height:74px;border:6px solid {P};border-radius:14px"></div>', 1300, 774, tz, a="pop", z=7)
    tw = A(33, "praktykant sprzedawcy")
    b.el(f'<div style="font-family:Poppins;font-style:italic;font-weight:800;font-size:36px;color:#1f3fa8;white-space:nowrap">praktykant sprzedawcy</div>', 1300, 770, tw, a="wipe", d=1.0, z=8, snd="marker")
    b.el('<div class="chyba">(podobno)</div>', 1600, 380, A(33, "Podobno"), rot=8, z=9)
    b.shake(tw + 1.0, 6)
    bs.append(b)

    # ── 34 KONIEC ──
    b = B(34, "Praktykant sprzedawcy", "który sprzedał Wieżę Eiffla dwa razy")
    tn = A(34, "Nie wiem.")
    b.el(eiffel(340), 470, 650, b.start + 0.25, a="pop", out=tn - 0.2, oa="pop", od=0.25, idle="sway")
    b.el(f'<div class="big" style="font-size:120px;color:{Y}">×2</div>', 720, 470, A(34, "dwa razy") + 0.1, out=tn - 0.2, oa="pop", od=0.25, rot=-8, z=7)
    b.el(card(lab("ZAWÓD:", 30, G) + T("praktykant", 56, cls="big") + T("sprzedawcy", 56, Y, cls="big"), 560, 300), 1360, 560, A(34, "Praktykant"), out=tn - 0.2, oa="pop", od=0.25, rot=2)
    tq = A(34, "Dziwna historia?")
    b.el(f'<div class="big" style="font-size:180px;color:{P}">?</div>', 960, 830, tq, out=tn, oa="pop", od=0.2, idle="wig", z=8)
    tb = A(34, "Ale bangla")
    b.el('<div class="big" style="font-size:150px">NIE WIEM,</div>', 960, 525, tn + 0.05, a="stamp", z=9)
    b.shake(tn + 0.25, 6)
    b.el(f'<div class="big" style="font-size:150px;color:{Y}">ALE BANGLA</div>', 960, 680, tb, a="stamp", z=9)
    b.shake(tb + 0.2, 12); b.flash.append(tb + 0.2); b.punch.append([tb + 0.2, 0.03])
    b.el('<div class="chyba" style="font-size:52px">(chyba)</div>', 1480, 800, tb + 0.45, rot=-8, z=10)
    b.el(hat(180), 360, 860, tb + 0.3, rot=-10, idle="wig", z=9)
    bs.append(b)

    # ── 35 ──
    b = B(35, "Następny odcinek", "armia, która wypowiedziała wojnę ptakom")
    tw = A(35, "Wyślij to")
    tn = A(35, "A w następnym")
    b.el('<div class="ypill" style="font-size:52px">WYŚLIJ TO KOMUŚ</div>', 560, 450, tw, rot=-3, out=tn, oa="up", od=0.3)
    b.el(card(T("„MNIE NIKT", 54, cls="big") + T("NIE OSZUKA”", 54, Y, cls="big"), 640, 250), 560, 700, A(35, "nikt nie oszuka"), rot=2, out=tn, oa="up", od=0.3)
    ta = min(A(35, "armia"), tn + 0.15)
    emu = """<svg width="360" height="460" viewBox="-180 -260 360 460" style="overflow:visible;display:block"><g filter="url(#stk)">
<path d="M-40 160 L-50 60 M30 160 L40 60" stroke="#6e5a3a" stroke-width="16" stroke-linecap="round"/>
<ellipse cx="0" cy="0" rx="130" ry="90" fill="#5a4a36"/><path d="M60 -40 Q90 -150 70 -200" stroke="#5a4a36" stroke-width="34" fill="none" stroke-linecap="round"/>
<circle cx="70" cy="-210" r="34" fill="#4a5a6a"/></g><circle cx="80" cy="-216" r="7" fill="#111"/><path d="M100 -206 L128 -200 L100 -194 Z" fill="#2a2a2a"/>
<path d="M-90 -20 L-150 -170" stroke="#cfd6df" stroke-width="8"/><path d="M-150 -170 L-70 -150 L-80 -110 L-148 -128 Z" fill="#fff"/></svg>"""
    b.el(emu, 1360, 620, ta, a="drop", idle="bob")
    b.el(emo("🪖", 110), 1080, 380, ta + 0.3, rot=-10, idle="wig")
    tp = A(35, "I przegrała")
    b.el(stamp("PRZEGRANA", 70), 1360, 890, tp, a="stamp", rot=-6, z=9)
    b.shake(tp + 0.2, 8)
    b.el('<div class="chyba">(serio)</div>', 1650, 400, tp + 0.4, rot=8, z=10)
    b.end = round(TL["total"] + OUTRO, 3)
    bs.append(b)

    import re as _re
    for b in bs:
        late = [float(v) for v in _re.findall(r"__T(-?[\d.]+)__", "".join(b.items)) if float(v) > b.end - 0.35]
        if late: print("UWAGA późno:", b.name, b.end, late)
    for b1, b2 in zip(bs, bs[1:]):
        assert abs(b1.end - b2.start) < 1e-6, (b1.name, b1.end, b2.start)
    return bs


if __name__ == "__main__":
    for b in build():
        print(b.name, round(b.start, 2), round(b.end, 2), round(b.end - b.start, 2), len(b.items), len(b.events()))
