"""34 plansze „Dziwne historie #1: Wojtek” (Nie wiem, ale bangla)."""
from engine import *

SAD = "#cfd6df"
CH = {1: "<b>01</b>kapral?!", 2: "<b>02</b>skąd się wziął", 3: "<b>03</b>życie w wojsku", 4: "<b>04</b>szeregowy wojtek",
      5: "<b>05</b>monte cassino", 6: "<b>06</b>po wojnie", 7: "<b>07</b>dziś"}
SEC = {**{i: 1 for i in range(1, 5)}, **{i: 2 for i in range(5, 13)}, **{i: 3 for i in range(13, 16)}, **{i: 4 for i in range(16, 20)},
       **{i: 5 for i in range(20, 24)}, **{i: 6 for i in range(24, 32)}, **{i: 7 for i in range(32, 35)}}
OUTRO = 6.5


def B(fid, head, sub="", **kw):
    kw.setdefault("chip", CH[SEC[fid]])
    return Board(fid, head, sub, **kw)


def check(size=90, color=GREEN):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="{color}" stroke="#fff" stroke-width="7"/>'
            '<path d="M28 52 L44 67 L73 35" stroke="#111" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def cross(size=90, color=RED):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="{color}" stroke="#fff" stroke-width="7"/>'
            '<path d="M32 32 L68 68 M68 32 L32 68" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round"/></svg>')


def lab(txt, size=44, color="#fff", extra=""):
    return f'<div class="lab" style="font-size:{size}px;color:{color};{extra}">{txt}</div>'


def T(txt, size=44, color="#fff", cls="txt", extra=""):
    return f'<div class="{cls}" style="font-size:{size}px;color:{color};{extra}">{txt}</div>'


def cnt_span(b, frm, to, t, du, fmt="#", x=960):
    b.sfx("ticks", t, x, du)
    return f'<span data-count="1" data-from="{frm}" data-to="{to}" data-t="__T{t}__" data-d="{du}" data-fmt="{fmt}">{fmt.replace("#", str(frm))}</span>'


def dot(x, y, color=Y, r=16):
    return f'<svg width="{2 * r + 12}" height="{2 * r + 12}"><circle cx="{r + 6}" cy="{r + 6}" r="{r}" fill="{color}" stroke="#111" stroke-width="6"/></svg>'


def maplab(txt, size=36):
    return f'<div style="font-weight:800;font-size:{size}px;text-shadow:0 4px 0 #000;white-space:nowrap">{txt}</div>'


def photo_slot(q=True):
    return (f'<div style="width:330px;height:420px;border:6px dashed {G};border-radius:22px;display:flex;align-items:center;justify-content:center;'
            f'font-weight:900;font-size:170px;color:{G};font-style:italic">{"?" if q else ""}</div>')


def build():
    bs = []

    # ── 01 HOOK ──
    b = B(1, "W polskiej armii służył…", "kapral, o którym nie uczą w szkole", src="źródło: Britannica, British Library")
    for x, y, rot, e, l, ph in [(410, 610, -4, "🍺", "pił piwo", "pił piwo"), (960, 590, 3, "🚬", "jadł papierosy", "jadł papierosy"),
                                (1510, 620, -2, "🤼", "mocował się", "mocował się")]:
        b.el(card(emo(e, 170) + lab(l), 440, 440), x, y, A(1, ph), rot=rot, idle="float")
    b.punch.append([A(1, "mocował"), 0.02])
    tp = A(1, "pił piwo") - 0.15
    b.el(emo("🪖", 250), 960, 540, 0.25, a="drop", idle="bob", out=tp, oa="pop", od=0.22)
    b.el('<div class="ypill" style="font-size:80px;padding:16px 56px">KAPRAL</div>', 960, 790, A(1, "kapral"), a="stamp", rot=-4, out=tp, oa="pop", od=0.22, z=8)
    b.shake(A(1, "kapral") + 0.2, 7)
    bs.append(b)

    # ── 02 ──
    b = B(2, "Awans?!", "bez munduru i bez czytania rozkazów")
    b.el(card("", 1160, 560, border=Y), 960, 630, b.start + 0.12, a="pop", snd=False)
    b.el(photo_slot(), 610, 630, b.start + 0.3, idle="pulse", z=6)
    b.el(T("KARTA ŻOŁNIERZA", 34, G), 850, 405, b.start + 0.35, a="fade", c=False, z=6)
    b.el(T("IMIĘ: <span style='color:#9aa0a8'>???</span>", 48), 850, 470, b.start + 0.45, a="sl", c=False, z=6)
    b.el(T(f"MUNDUR: <span style='color:{RED}'>BRAK</span>", 48), 850, 560, A(2, "Nie miał munduru"), a="sl", c=False, z=6)
    b.el(T(f"ROZKAZY: <span style='color:{RED}'>NIE CZYTA</span>", 48), 850, 650, A(2, "nie umiał czytać"), a="sl", c=False, z=6)
    t = A(2, "dostał awans")
    b.el('<div class="stamp">AWANS</div>', 1300, 830, t, a="stamp", rot=-12, z=8)
    b.shake(t + 0.2, 12); b.flash.append(t + 0.2); b.punch.append([t + 0.2, 0.025])
    bs.append(b)

    # ── 03 ──
    b = B(3, "To nie żart", "ten kapral naprawdę istniał")
    tb = A(3, "niedźwiedziem")
    b.el(card("", 1160, 560, border=Y), 960, 630, b.start, a="none", snd=False)
    b.el(photo_slot(), 610, 630, b.start, a="none", out=tb, od=0.18, oa="pop", z=6, snd=False)
    b.el(bear_head(True, size=300), 610, 630, tb, a="drop", z=7, idle="bob")
    b.shake(tb + 0.25, 11); b.flash.append(tb + 0.25); b.punch.append([tb + 0.25, 0.03])
    b.el(T("KARTA ŻOŁNIERZA", 34, G), 850, 405, b.start, a="none", c=False, z=6, snd=False)
    b.el(T("GATUNEK: <span style='color:#9aa0a8'>???</span>", 48), 850, 470, b.start, a="none", c=False, z=6, out=tb, od=0.15, snd=False)
    b.el(T(f"GATUNEK: <span style='color:{Y}'>NIEDŹWIEDŹ</span>", 48), 850, 470, tb + 0.1, a="sl", c=False, z=6)
    tw = A(3, "Wojtek")
    b.el(T("IMIĘ: <span style='color:#9aa0a8'>???</span>", 48), 850, 560, b.start, a="none", c=False, z=6, out=tw, od=0.15, snd=False)
    b.el(T(f"IMIĘ: <span style='color:{Y}'>WOJTEK</span>", 48), 850, 560, tw + 0.05, a="sl", c=False, z=6)
    b.el('<div class="ypill" style="background:#2BE38B">TO PRAWDA</div>', 1370, 380, A(3, "Ale to prawda"), rot=6, z=9)
    b.el(f'<div class="big" style="font-size:130px;color:{Y}">WOJTEK!</div>', 1190, 790, tw + 0.15, a="stamp", rot=-6, z=9)
    b.shake(tw + 0.35, 9)
    bs.append(b)

    # ── 04 ──
    b = B(4, "Przez pół świata", "z polską armią… aż do szkockiego zoo")
    order = ["Iran", "Irak", "Syria", "Palestyna", "Egipt", "Monte Cassino", "Szkocja"]
    pts = [WORLD(*PLACES[n]) for n in order]
    t0, t1 = A(4, "przeszedł"), E(4, "świata")
    for i, (n, (x, y)) in enumerate(zip(order, pts)):
        b.el(dot(0, 0, P if n == "Monte Cassino" else Y), round(x), round(y), b.start + 0.25 + 0.08 * i, z=6, snd=i % 2 == 0)
    d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts)
    b.draw(d, t0, t1 - t0, dash="22 16", w=8)
    for n, dx, dy in [("Iran", 70, 0), ("Egipt", 0, 50), ("Monte Cassino", 30, -45), ("Szkocja", 95, -40)]:
        x, y = WORLD(*PLACES[n]); b.el(maplab(n), round(x + dx), round(y + dy), b.start + 0.6, a="fade", z=6, snd=False)
    x, y = WORLD(*PLACES["Iran"])
    b.el(bear_head(True, size=150), round(x), round(y - 130), b.start + 0.5, idle="bob", z=7)
    tz = A(4, "szkockim zoo")
    b.el(f'<div class="big" style="font-size:150px;color:{P}">?</div>', 230, 480, tz, rot=10, idle="wig", z=8)
    b.el('<div class="ypill">SZKOCKIE ZOO?!</div>', 720, 430, tz + 0.2, rot=-5, z=8)
    b.punch.append([tz, 0.02])
    bs.append(b)

    # ── 05 SKĄD SIĘ WZIĄŁ ──
    b = B(5, "Wiosna 1942", "armia Andersa wychodzi z ZSRR", src="źródło: Britannica")
    b.count(430, 420, 1939, 1942, b.start + 0.25, 1.0, size=210)
    b.el('<div class="pill">ARMIA ANDERSA</div>', 430, 630, A(5, "armia generała"), a="sl")
    b.el('<div class="pill">+ TYSIĄCE CYWILÓW</div>', 430, 740, A(5, "tysiące polskich"), a="sl")
    b.el(T("wcześniej zesłanych do łagrów", 36, G, extra="font-weight:600"), 430, 840, A(5, "zesłanych"), a="fade")
    b.el(card(f'<div class="big" style="font-size:84px;color:{RED}">ZSRR</div>', 420, 140), 1430, 390, A(5, "Z ZSRR"))
    ta = A(5, "wychodzi"); tir = A(5, "do Iranu")
    b.draw("M1430 470 C1560 540 1300 620 1430 680", ta, max(0.6, tir - ta - 0.2), w=10, dash="26 18")
    b.el('<svg width="60" height="50"><path d="M5 5 L30 45 L55 5 Z" fill="#fff"/></svg>', 1430, 698, tir - 0.15, z=6, snd=False)
    b.el(card(f'<div class="big" style="font-size:84px;color:{Y};margin-bottom:46px">IRAN</div>', 420, 200), 1430, 830, tir)
    b.el(T("(wtedy: Persja)", 36, G, extra="font-weight:600"), 1430, 875, A(5, "wtedy Persji"), a="fade", z=7)
    bs.append(b)

    # ── 06 ──
    b = B(6, "Kwiecień 1942, Iran", "spotkanie gdzieś w drodze")
    b.draw("M140 950 L1780 950", b.start + 0.2, 1.0, color=G, w=8, dash="40 30", snd="swipe")
    b.el(emo("👦", 240), 620, 690, A(6, "irańskiego chłopca"), a="drop", idle="bob")
    b.el(bear_head(False, cub=True, size=250), 1180, 680, A(6, "małego niedźwiadka"), idle="bob")
    b.el(T("matkę zastrzelili myśliwi", 34, G, extra="font-weight:600"), 1180, 870, A(6, "którego matkę"), a="fade")
    b.el(f'<div class="chyba" style="background:{Y};color:#111">SIEROTA</div>', 1420, 520, A(6, "zastrzelili"), rot=8)
    bs.append(b)

    # ── 07 ──
    b = B(7, "Wymiana", "niedźwiadek za trochę jedzenia")
    tw = A(7, "wymieniają")
    b.el(card(emo("🥫", 170) + lab("jedzenie"), 400, 400), 520, 560, tw, a="sl", rot=-3, idle="float")
    b.el(card(bear_head(False, cub=True, size=210) + lab("niedźwiadek"), 400, 400), 1400, 560, tw + 0.2, a="sr", rot=3, idle="float")
    tn = A(7, "Niedźwiadek")
    b.draw("M770 500 L1140 500 M1110 470 L1145 500 L1110 530", tn, 0.45, w=10)
    b.draw("M1150 625 L780 625 M810 595 L775 625 L810 655", tn + 0.35, 0.45, w=10, color=Y)
    tl = A(7, "Lepszego interesu")
    b.el('<div class="ypill" style="font-size:50px">NAJLEPSZY INTERES TEJ ARMII</div>', 960, 865, tl, a="stamp", rot=-3, z=9)
    b.shake(tl + 0.2, 7); b.sfx("ding", tl + 0.25, 960)
    b.el('<div class="chyba">(chyba)</div>', 1530, 790, E(7, "nie zrobiła") - 0.25, rot=-8, z=10)
    bs.append(b)

    # ── 08 ──
    b = B(8, "Butelka ze smoczkiem", "miś był za słaby, żeby sam przełykać")
    b.el(bear_head(False, cub=True, size=240), 470, 620, A(8, "Miś jest"), idle="sway")
    b.el(T("za słaby, żeby przełykać", 36, G, extra="font-weight:600"), 470, 820, A(8, "nie umie"), a="fade")
    tb, tm = A(8, "butelkę ze smoczkiem"), A(8, "W środku")
    bottle = f"""<svg width="300" height="520" viewBox="-150 -260 300 520" style="overflow:visible"><g filter="url(#stk)">
<path d="M-34 -180 C-34 -262 34 -262 34 -180 Z" fill="#e8a66a"/><rect x="-58" y="-190" width="116" height="30" rx="8" fill="#cfd6df"/>
<rect x="-42" y="-162" width="84" height="70" fill="#3a4450"/><rect x="-112" y="-100" width="224" height="340" rx="44" fill="#3a4450"/></g>
<rect x="-98" y="-30" width="196" height="256" rx="34" fill="#f4ecd8" data-a="growy" data-t="__T{tm}__" data-d="1.4" data-og="center bottom"/>
<rect x="-112" y="-100" width="224" height="340" rx="44" fill="rgba(255,255,255,.08)" stroke="#fff" stroke-width="6"/>
<path d="M-80 -70 V180" stroke="rgba(255,255,255,.35)" stroke-width="14" stroke-linecap="round"/></svg>"""
    b.el(bottle, 1100, 650, tb, idle="float")
    b.sfx("rise", tm, 1100, 1.4)
    tq = A(8, "Z czego?")
    b.el(f'<div class="big" style="font-size:170px;color:{P}">?</div>', 1330, 430, tq, rot=12, out=A(8, "Ze starej") + 0.4, oa="pop", z=8)
    b.el('<div style="background:#fff;color:#111;font-weight:900;font-style:italic;font-size:54px;padding:10px 26px;border-radius:12px;box-shadow:0 6px 0 #000">W***A</div>',
         1100, 700, A(8, "po wódce"), a="stamp", rot=-5, z=8)
    b.shake(A(8, "po wódce") + 0.2, 5)
    b.el('<div class="ypill" style="font-size:38px">mleko skondensowane</div>', 1570, 830, A(8, "mleko skondensowane"), a="sr", rot=-3, z=9)
    bs.append(b)

    # ── 09 ──
    b = B(9, "Dzieciństwo po polsku", "mleko z butelki po wódce i wujkowie w mundurach")
    b.el('<div style="width:780px;height:660px;background:#f3f0e8;border-radius:10px;box-shadow:0 14px 0 #000"></div>', 960, 620, b.start + 0.12, z=3, snd=False)
    b.el('<div style="width:700px;height:480px;background:#2a2f37;border-radius:6px"></div>', 960, 570, b.start + 0.18, a="fade", z=3, snd=False)
    b.el('<div style="width:170px;height:46px;background:rgba(255,79,160,.75)"></div>', 640, 300, b.start + 0.3, rot=-28, z=4, snd=False)
    b.el('<div style="width:170px;height:46px;background:rgba(255,79,160,.75)"></div>', 1280, 300, b.start + 0.3, rot=28, z=4, snd=False)
    b.el(T("rodzinne zdjęcie, 1942", 40, "#222", extra="font-style:italic;font-weight:800"), 960, 885, b.start + 0.4, a="fade", z=4)
    b.el(bear_head(False, cub=True, size=210), 960, 640, b.start + 0.35, z=5, idle="bob")
    b.el(emo("🍼", 130), 760, 680, A(9, "mleko z butelki"), z=6, rot=-12, idle="wig")
    for i, (x, y) in enumerate([(770, 440), (960, 410), (1150, 440)]):
        b.el(emo("🪖", 120), x, y, A(9, "wujkowie") + 0.12 * i, z=6, idle="bob")
    b.el('<div class="chyba">(chyba)</div>', 1370, 380, E(9) - 0.5, rot=8, z=9)
    bs.append(b)

    # ── 10 ──
    b = B(10, "Irena i miś", "opieka w obozie dla uchodźców")
    b.el(card(emo("👧", 170) + lab("Irena") + T("nastolatka z obozu", 34, G, extra="font-weight:600;margin-top:8px"), 560, 470), 520, 590, A(10, "Irena"), rot=-2)
    ruler = "M1640 330 V930 " + " ".join(f"M1640 {y} H{1610 if (y - 330) % 120 else 1590}" for y in range(330, 931, 60))
    b.draw(ruler, b.start + 0.3, 1.0, w=6, color=G)
    tg = A(10, "miś rośnie")
    b.el(bear_head(False, cub=True, size=320), 1300, 770, A(10, "nim"), s=0.42, og="50% 100%", sk=[(tg, 0.7), (tg + 0.55, 1.0)], z=6)
    b.el('<div class="stamp" style="font-size:54px;border-width:8px">OBÓZ TO NIE MIEJSCE</div>', 640, 905, A(10, "obóz to nie"), a="stamp", rot=-5, z=8)
    b.shake(A(10, "obóz to nie") + 0.2, 6)
    bs.append(b)

    # ── 11 ──
    b = B(11, "Sierpień 1942", "Wojtek trafia do żołnierzy", src="źródło: ANSA, Wikipedia")
    b.el(card(T("22. KOMPANIA", 64, Y, cls="big") + T("ZAOPATRYWANIA ARTYLERII", 50, "#fff", extra="font-weight:800;margin-top:10px"), 1220, 230),
         960, 470, A(11, "kompanii zaopatrywania"))
    b.el(emo("🚚", 230), 720, 770, A(11, "trafia do żołnierzy"), a="sl", idle="drive")
    b.el(bear_head(False, cub=True, size=180), 1000, 780, A(11, "trafia do żołnierzy") + 0.3, idle="bob")
    b.el(emo("❤️", 150), 1440, 740, A(11, "Od teraz"), idle="pulse")
    b.el('<div class="pill">RODZINA</div>', 1440, 900, A(11, "jego rodzina"))
    bs.append(b)

    # ── 12 ──
    b = B(12, "Radosny wojownik", "skąd się wzięło imię Wojtek")
    b.el(card(T("WOJCIECH", 96, "#fff", cls="big"), 720, 160), 960, 400, A(12, "od Wojciecha"))
    tt = A(12, "tłumaczy")
    b.draw("M900 485 Q700 500 600 545", tt - 0.2, 0.4, w=7, color=G)
    b.draw("M1020 485 Q1220 500 1320 545", tt, 0.4, w=7, color=G)
    b.el(card(T("„WÓJ”", 70, "#fff", cls="big") + T("→ wojownik", 40, G, extra="font-weight:700;margin-top:8px"), 520, 210), 560, 650, tt, rot=-2)
    b.el(f'<div class="big" style="font-size:110px;color:{P}">+</div>', 960, 650, tt + 0.25, z=6)
    b.el(card(T("„CIESZYĆ”", 70, "#fff", cls="big") + T("→ radosny", 40, G, extra="font-weight:700;margin-top:8px"), 520, 210), 1360, 650, tt + 0.45, rot=2)
    tr = A(12, "„radosny")
    b.el('<div class="ypill" style="font-size:70px;padding:18px 50px">RADOSNY WOJOWNIK</div>', 960, 870, tr, a="stamp", rot=-2, z=8)
    b.shake(tr + 0.2, 8); b.flash.append(tr + 0.2)
    b.el(emo("💯", 130), 1580, 860, A(12, "Lepiej się"), rot=10, idle="wig", z=9)
    bs.append(b)

    # ── 13 ŻYCIE W WOJSKU ──
    b = B(13, "Przez Bliski Wschód", "Irak, Syria, Palestyna, Egipt", src="źródło: British Library")
    M = proj((27, 55, 27, 38.5, 120, 1150, 330, 960))
    order = ["Iran", "Irak", "Syria", "Palestyna", "Egipt"]
    P2 = {n: M(*PLACES[n]) for n in order}
    times = {"Iran": b.start + 0.3, "Irak": A(13, "Irak"), "Syria": A(13, "Syrię"), "Palestyna": A(13, "Palestynę"), "Egipt": A(13, "Egipt")}
    LOFF = {"Iran": (40, -55), "Irak": (0, 50), "Syria": (10, -50), "Palestyna": (100, 10), "Egipt": (0, 50)}
    for n in order:
        x, y = P2[n]; b.el(dot(0, 0), round(x), round(y), times[n], z=6)
        b.el(maplab(n), round(x + LOFF[n][0]), round(y + LOFF[n][1]), times[n] + 0.05, a="fade", z=6, snd=False)
    for a_, c_ in zip(order, order[1:]):
        (x1, y1), (x2, y2) = P2[a_], P2[c_]
        b.draw(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", times[c_] - 0.35, 0.4, w=8, dash="20 14")
    for i, (e, l, ph) in enumerate([("😴", "śpi", "Śpi"), ("🍲", "je", "je z"), ("🤼", "mocuje się", "mocuje")]):
        b.el(f'<div class="pill" style="display:flex;align-items:center;gap:14px;font-size:34px"><span class="emo flat" style="font-size:44px">{e}</span>{l} z żołnierzami</div>',
             1520, 370 + 96 * i, A(13, ph), a="sr")
    tw = A(13, "Zwykle wygrywa")
    sc = cnt_span(b, 0, 47, tw, 0.7, x=1500)
    b.el(card(T("ZAPASY: WYNIK", 30, G, extra="font-weight:800;letter-spacing:2px") +
              f'<div class="big" style="font-size:64px;margin-top:10px"><span style="color:{Y}">WOJTEK</span> {sc} : 0</div>' +
              T("vs. żołnierze", 30, G, extra="font-weight:600;margin-top:6px"), 700, 250), 1500, 810, A(13, "mocuje") + 0.6)
    b.el('<div class="chyba">(chyba)</div>', 1720, 690, tw + 0.55, rot=8, z=9)
    bs.append(b)

    # ── 14 ──
    b = B(14, "Piwo? Tak.", "według wspomnień żołnierzy", src="źródło: wspomnienia żołnierzy (BBC Wildlife)")
    tp = A(14, "lubił piwo")
    b.el(card(emo("🍺", 180) + '<div style="height:110px"></div>', 460, 460), 560, 600, tp, rot=-3)
    b.el(lab("PIWO", 56), 560, 740, tp + 0.1, z=6, snd=False)
    b.el(check(110), 760, 410, tp + 0.4, z=7, snd="ding")
    tc = A(14, "A papierosy?")
    b.el(card(emo("🚬", 180) + '<div style="height:110px"></div>', 460, 460), 1360, 600, tc, rot=3)
    b.el(lab("PALIŁ", 56), 1360, 740, tc + 0.1, z=6, snd=False)
    tn = A(14, "nie palił")
    b.el(f'<div style="width:300px;height:16px;background:{RED};border-radius:8px"></div>', 1360, 751, tn, a="wipe", d=0.3, rot=-2, z=7)
    b.sfx("buzz", tn + 0.1, 1360)
    tz = A(14, "On je zjadał")
    b.el(f'<div class="big" style="font-size:110px;color:{Y}">ZJADAŁ!</div>', 1360, 875, tz, a="stamp", rot=-5, z=9)
    b.shake(tz + 0.2, 11); b.flash.append(tz + 0.2); b.punch.append([tz + 0.2, 0.025])
    bs.append(b)

    # ── 15 ──
    b = B(15, "Podobno…", "nocna wizyta w magazynie z amunicją", src="źródło: relacje żołnierzy")
    b.dim.append([b.start, b.start + 0.6, 0, 0.38])
    b.el(emo("🌙", 110, flat=True), 300, 390, b.start + 0.3, a="fade", idle="float", snd=False)
    shed = "M1040 940 V520 L1350 380 L1660 520 V940 M1240 940 V650 H1460 V940"
    b.draw(shed, b.start + 0.25, 1.1, w=9, color="#cfd6df")
    b.el('<div style="width:212px;height:282px;background:#000"></div>', 1350, 797, b.start + 0.9, a="fade", z=3, snd=False)
    b.el(f'<div class="chyba" style="background:{RED};font-size:38px">AMUNICJA</div>', 1350, 560, A(15, "magazynu"), z=6)
    b.el(emo("🥷", 210), 640, 760, A(15, "złodzieja"), a="sl", idle="sway")
    te = A(15, "znalazł niedźwiedzia")
    eyes = '<svg width="200" height="60" style="overflow:visible"><g filter="url(#glow)"><ellipse cx="45" cy="30" rx="26" ry="18" fill="#FFD21F"/><ellipse cx="155" cy="30" rx="26" ry="18" fill="#FFD21F"/></g><circle cx="45" cy="30" r="8" fill="#111"/><circle cx="155" cy="30" r="8" fill="#111"/></svg>'
    b.el(eyes, 1350, 760, te, z=6, idle="blinkop")
    b.shake(te + 0.15, 10)
    b.el(f'<div class="big" style="font-size:100px;color:{P}">ups</div>', 640, 560, te + 0.35, rot=-10, idle="wig", z=8)
    th = A(15, "Hałas")
    b.dim.append([th, th + 0.25, 0.38, 0.05])
    b.flash.append(th); b.el(emo("🚨", 150), 1775, 380, th, idle="wig", z=8)
    b.el(f'<div class="big" style="font-size:120px;color:{Y}">!!!</div>', 1790, 610, th + 0.3, rot=8, z=8)
    b.sfx("alarm", th, 1700)
    bs.append(b)

    # ── 16 SZEREGOWY WOJTEK ──
    b = B(16, "Czas na front", "kompania płynie z Egiptu do Włoch")
    b.draw("M100 860 Q200 820 300 860 T500 860 T700 860 T900 860 T1100 860 T1300 860 T1500 860 T1700 860 T1900 860", b.start + 0.2, 1.0, color="#4aa3ff", w=10, snd="swipe")
    b.el(emo("🚢", 260), 640, 720, A(16, "płynąć"), a="sl", idle="bob")
    b.el('<div class="pill">Z EGIPTU DO WŁOCH</div>', 640, 450, A(16, "z Egiptu"))
    tp = A(16, "Problem")
    b.el(f'<div class="big" style="font-size:110px;color:{RED}">PROBLEM:</div>', 1360, 400, tp, a="stamp", rot=-4, z=8)
    b.shake(tp + 0.2, 6)
    tz = A(16, "nie wolno")
    b.el(bear_head(True, size=270), 1360, 700, tz - 0.3, z=6)
    b.el('<svg width="380" height="380" viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="none" stroke="#ff3b3b" stroke-width="9"/><path d="M19 19 L81 81" stroke="#ff3b3b" stroke-width="9" stroke-linecap="round"/></svg>',
         1360, 700, tz + 0.1, a="stamp", z=8, snd="buzz")
    bs.append(b)

    # ── 17 ──
    b = B(17, "Dwa wyjścia", "co robią żołnierze?")
    for x, letter, e, l, ph, border, idle, col in [(560, "A", "😢", "zostawić Wojtka", "Zostawić", "#fff", "", G),
                                                   (1360, "B", "😏", "coś bardzo polskiego", "coś bardzo polskiego", Y, "wig", Y)]:
        t = A(17, ph)
        b.el(card(emo(e, 190) + lab(l, 46), 640, 500, border=border), x, 620, t, idle=idle)
        b.el(f'<div style="width:110px;height:110px;border-radius:50%;background:{col};color:#111;font-weight:900;font-style:italic;font-size:64px;display:flex;align-items:center;justify-content:center;box-shadow:0 6px 0 #000">{letter}</div>',
             x - 290, 380, t + 0.15, z=7)
    bs.append(b)

    # ── 18 ──
    b = B(18, "Szeregowy Wojtek", "według większości relacji", src="źródło: BBC Wildlife, Britannica")
    b.el('<div class="ypill">WYBÓR: B</div>', 520, 360, A(18, "opcję numer dwa"), rot=-6, z=9)
    b.el(card("", 1200, 560, border=Y), 960, 650, b.start + 0.12, snd=False)
    b.el(bear_head(True, size=300), 610, 650, b.start + 0.3, z=6, idle="bob")
    b.el(T("KSIĄŻECZKA ŻOŁNIERZA", 34, G), 880, 410, b.start + 0.3, a="fade", c=False, z=6)
    b.el(f'<div class="big" style="font-size:86px">WOJTEK</div>', 880, 455, A(18, "Wojtek zostaje"), a="sl", c=False, z=6)
    for i, (l, ph) in enumerate([("NUMER", "z numerem"), ("KSIĄŻECZKA", "z książeczką"), ("STOPIEŃ: SZEREGOWY", "ze stopniem")]):
        b.el(f'<div class="txt" style="display:flex;align-items:center;gap:16px">{check(54)}{l}</div>', 880, 580 + 72 * i, A(18, ph), a="sl", c=False, z=6)
    tn = A(18, "Niedźwiedź na wojnie?"); ts = A(18, "Szeregowy Wojtek")
    b.el(f'<div class="chyba" style="font-size:40px">niedźwiedź na wojnie?</div>', 1330, 860, tn, rot=-4, out=ts, oa="pop", od=0.2, z=9)
    b.el(f'<div style="width:470px;height:12px;background:#111;border-radius:6px"></div>', 1330, 869, A(18, "Nie."), a="wipe", d=0.3, rot=-4, z=10, out=ts, oa="pop", od=0.2)
    b.sfx("buzz", A(18, "Nie.") + 0.05, 1330)
    b.el('<div class="stamp" style="font-size:76px">WCIELONY</div>', 1290, 865, ts + 0.1, a="stamp", rot=-10, z=10)
    b.shake(ts + 0.3, 11); b.flash.append(ts + 0.3)
    bs.append(b)

    # ── 19 ──
    b = B(19, "Dla uczciwości", "źródła mówią tu różne rzeczy")
    b.el(card(T("WCIELONY", 76, "#fff", cls="big") + T("większość relacji", 36, G, extra="font-weight:600;margin-top:10px"), 620, 300), 540, 560, b.start + 0.3, rot=-2)
    b.el(f'<div style="width:130px;height:130px;border-radius:50%;background:{P};font-weight:900;font-style:italic;font-size:58px;display:flex;align-items:center;justify-content:center;box-shadow:0 6px 0 #000">VS</div>',
         960, 560, A(19, "część źródeł"), z=7)
    b.el(card(T("MASKOTKA", 76, "#fff", cls="big") + T("część źródeł", 36, G, extra="font-weight:600;margin-top:10px"), 620, 300), 1380, 560, A(19, "maskotką"), rot=2)
    tw = A(19, "na statek wszedł")
    b.el(f'<div class="stamp" style="border-color:{GREEN};color:{GREEN};font-size:80px">NA POKŁADZIE</div>', 860, 870, tw, a="stamp", rot=-4, z=9)
    b.shake(tw + 0.2, 9)
    b.el(emo("🚢", 150), 1390, 830, tw + 0.25, idle="bob", z=8)
    bs.append(b)

    # ── 20 MONTE CASSINO ──
    b = B(20, "Monte Cassino", "maj 1944")
    hill = "M120 960 C420 960 560 520 900 470 C1240 520 1380 960 1800 960"
    b.draw(hill, b.start + 0.2, 1.3, w=9)
    b.draw("M820 470 V385 H980 V470 M865 385 V330 H905 V385 M770 470 H1030", b.start + 1.2, 0.8, w=8, color=Y)
    tb = A(20, "Bitwa o Monte Cassino")
    for i, (x, y) in enumerate([(640, 580), (1290, 700), (1450, 820)]):
        b.el(emo("💥", 100), x, y, tb + 0.3 + 0.35 * i, idle="pulse", z=6, snd=False)
        b.shake(tb + 0.35 + 0.35 * i, 4)
    b.el('<div class="pill" style="font-size:36px">jedna z najcięższych bitew</div>', 1500, 400, A(20, "jedna z najcięższych"), a="sr")
    b.el(emo("🚚", 130), 430, 890, A(20, "dowozi amunicję"), a="sl", idle="drive", z=6)
    b.el('<div class="ypill" style="font-size:32px">AMUNICJA NA FRONT</div>', 330, 560, A(20, "dowozi amunicję") + 0.25, rot=-3, z=7)
    bs.append(b)

    # ── 21 ──
    b = B(21, "Tu zaczyna się legenda", "według relacji żołnierzy", src="źródło: relacje żołnierzy")
    tp = A(21, "Wojtek patrzył"); tw0 = A(21, "Wstał na tylne")
    b.el('<div class="ypill" style="font-size:52px">MONTE CASSINO, 1944</div>', 960, 600, b.start + 0.3, a="stamp", rot=-3, out=tp - 0.1, oa="pop", od=0.2, z=8)
    b.el(emo("📜", 150), 960, 440, b.start + 0.45, idle="wig", out=tp - 0.1, oa="pop", od=0.2)
    b.el(bear_head(True, size=260), 960, 640, tp, idle="bob", out=tw0 - 0.05, oa="fade", od=0.12, z=6)
    b.el(emo("👀", 90, flat=True), 1130, 520, tp + 0.3, idle="wig", out=tw0 - 0.05, oa="fade", od=0.12, z=7)
    tk = A(21, "koledzy noszą")
    for i, x in enumerate([250, 380, 510]):
        b.el(emo("📦", 110), x, 890, tk + 0.15 * i, a="sl", idle="bob", snd=i == 0)
    tw = A(21, "Wstał na tylne")
    b.el(bear_body(True, "crate", 520), 960, 640, tw, a="drop", idle="bob", z=6)
    b.shake(tw + 0.4, 8); b.punch.append([tw + 0.4, 0.025])
    tn = A(21, "zaczął nosić")
    crate = '<div style="width:230px;height:92px;background:#b8843f;border:7px solid #7a5524;border-radius:8px;box-shadow:0 6px 0 #000;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:30px;color:#2a1a0a">AMUNICJA</div>'
    for i in range(5):
        b.el(crate, 1500, 895 - 98 * i, tn + 0.3 * i, a="drop", rot=(-2, 2, -1, 3, -2)[i], z=6)
    tu = A(21, "nie upuścił")
    b.el('<div class="ypill" style="font-size:44px">UPUSZCZONE: 0</div>', 1500, 400, tu, a="stamp", rot=-3, z=8)
    b.shake(tu + 0.2, 5)
    b.el(f'<div class="chyba" style="background:#3a4450;font-size:34px">podobno</div>', 1240, 330, A(21, "Podobno"), rot=-8, z=9)
    bs.append(b)

    # ── 22 ──
    b = B(22, "Wersja numer 2", "według innej relacji", src="źródło: Farmers Journal")
    b.draw("M960 300 V980", b.start + 0.15, 0.4, w=6, color=G, snd="swipe")
    b.el('<div class="pill" style="font-size:34px">WERSJA 1</div>', 480, 340, b.start + 0.2)
    b.el(bear_body(True, "crate", 380), 480, 650, b.start + 0.35, a="fade", idle="bob", snd=False)
    b.el('<div class="ypill" style="font-size:38px">WERSJA 2</div>', 1440, 340, A(22, "druga wersja"))
    tt = A(22, "wlazł na drzewo")
    tree = """<svg width="460" height="560" viewBox="-230 -330 460 560" style="overflow:visible"><g filter="url(#stk)"><rect x="-34" y="-40" width="68" height="260" rx="10" fill="#6e4220"/>
<circle cx="-110" cy="-100" r="120" fill="#2f6b3a"/><circle cx="110" cy="-100" r="120" fill="#2f6b3a"/><circle cx="0" cy="-190" r="140" fill="#3a8048"/></g></svg>"""
    b.el(tree, 1420, 640, tt, a="su", z=4)
    b.el(bear_head(True, size=170), 1460, 470, tt + 0.35, idle="wig", z=6)
    to = A(22, "w czasie ostrzału")
    for i, (x, y) in enumerate([(1700, 420), (1200, 450)]):
        b.el(emo("💥", 100), x, y, to + 0.3 * i, idle="pulse", z=7, snd=False); b.shake(to + 0.05 + 0.3 * i, 5)
    tb = A(22, "Obie wersje")
    b.el('<div class="ypill" style="font-size:40px">OBIE JAK NORMALNY CZŁOWIEK</div>', 960, 905, tb, a="stamp", rot=-2, z=9)
    b.el('<div class="chyba">(chyba)</div>', 1560, 880, A(22, "normalny człowiek"), rot=-8, z=10)
    bs.append(b)

    # ── 23 ──
    b = B(23, "Awans na kaprala", "i nowy znak kompanii")
    b.el(card("", 620, 440, border=Y), 560, 600, b.start + 0.12, snd=False)
    b.el(bear_head(True, size=220), 420, 600, b.start + 0.3, z=6)
    b.el(f'<div class="big" style="font-size:64px">WOJTEK</div>', 690, 520, b.start + 0.35, a="sl", z=6)
    tk = A(23, "awans na kaprala")
    b.el('<div class="stamp" style="font-size:80px">KAPRAL</div>', 650, 700, tk, a="stamp", rot=-10, z=8)
    b.shake(tk + 0.2, 11); b.flash.append(tk + 0.2)
    te = A(23, "na emblemacie")
    b.el(f'<div style="width:480px;height:480px;border-radius:50%;background:#1c1f25;border:12px solid {Y};box-shadow:0 10px 0 #000"></div>', 1380, 610, A(23, "zmienia swój znak"), z=5)
    b.el(bear_body(False, "shell", 360), 1380, 640, te, a="pop", z=6, idle="breathe")
    b.el(T("nowy znak kompanii (nasz rysunek)", 32, G, extra="font-weight:600"), 1380, 900, te + 0.3, a="fade")
    bs.append(b)

    # ── 24 PO WOJNIE ──
    b = B(24, "Wojna się kończy", "i tu ta historia robi się smutna")
    b.draw("M120 1000 C420 1000 560 680 900 600 C1240 680 1380 1000 1800 1000", b.start + 0.15, 0.7, w=9)
    b.draw("M820 600 V515 H980 V600 M865 515 V460 H905 V515 M770 600 H1030", b.start + 0.5, 0.5, w=8, color=Y)
    tz = A(24, "zdobywają")
    b.el(emo("🇵🇱", 150), 960, 395, tz, a="drop", idle="sway", z=6)
    b.el(f'<div class="stamp" style="border-color:{GREEN};color:{GREEN};font-size:70px">ZDOBYTE</div>', 1450, 470, tz + 0.4, a="stamp", rot=-8, z=8)
    b.shake(tz + 0.6, 7)
    b.el('<div class="ypill" style="font-size:60px">1945</div>', 460, 470, A(24, "Wojna się kończy"), rot=-4)
    ts = A(24, "robi się smutna")
    b.gray.append([ts - 0.2, ts + 1.4, 0, 0.6]); b.dim.append([ts - 0.2, ts + 1.4, 0, 0.18])
    b.sfx("sad", ts - 0.2, 960)
    bs.append(b)

    sad_kw = dict(color=SAD)
    def sad(b):
        b.gray.append([b.start, b.start + 0.01, 0.6, 0.6]); b.dim.append([b.start, b.start + 0.01, 0.12, 0.12]); return b

    # ── 25 ──
    b = sad(B(25, "Nie ma powrotu", "Polska trafia pod wpływy Moskwy", **sad_kw))
    E2 = proj((-8, 32, 36, 60, 160, 1760, 300, 980))
    pl, it, sc_ = E2(*PLACES["Polska"]), E2(*PLACES["Włochy"]), E2(*PLACES["Szkocja"])
    for (x, y), n, off in [(pl, "Polska", (90, -40)), (it, "Włochy", (0, 50)), (sc_, "Szkocja", (20, -48))]:
        b.el(dot(0, 0, Y), round(x), round(y), b.start + 0.25, z=6)
        b.el(maplab(n), round(x + off[0]), round(y + off[1]), b.start + 0.35, a="fade", z=6, snd=False)
    b.el(f'<div style="width:240px;height:240px;border-radius:50%;background:rgba(255,59,59,.22);border:6px solid {RED}"></div>', round(pl[0]), round(pl[1]),
         A(25, "pod wpływy Moskwy"), idle="pulse", z=5)
    tw = A(25, "Wielu żołnierzy")
    b.draw(f"M{it[0]:.0f} {it[1]:.0f} Q1250 740 {pl[0] - 20:.0f} {pl[1] + 40:.0f}", tw, 0.9, w=9, dash="22 16")
    tn = A(25, "nie może bezpiecznie")
    b.el(cross(130), 1215, 690, tn + 0.2, a="stamp", z=8, snd="buzz")
    b.el('<div class="pill">ZOSTAJĄ NA ZACHODZIE</div>', 450, 880, A(25, "Zostają na Zachodzie"), a="sl")
    tsz = A(25, "trafia do Szkocji")
    b.draw(f"M{it[0]:.0f} {it[1]:.0f} Q560 830 {sc_[0] + 15:.0f} {sc_[1] + 35:.0f}", tsz - 0.3, 0.9, w=9, dash="22 16", color=Y)
    bs.append(b)

    # ── 26 ──
    b = sad(B(26, "Winfield, 1946", "obóz w hrabstwie Berwickshire, Szkocja", **sad_kw))
    tw = A(26, "obozie Winfield")
    b.el('<div style="width:34px;height:330px;background:#6e4220;border-radius:6px;box-shadow:0 6px 0 #000"></div>', 520, 790, tw, a="su", z=4, snd=False)
    b.el('<div style="background:#b8843f;border:8px solid #7a5524;border-radius:14px;padding:18px 36px;font-weight:900;font-style:italic;font-size:58px;color:#2a1a0a;box-shadow:0 8px 0 #000;white-space:nowrap">WINFIELD CAMP</div>',
         520, 600, tw + 0.1, rot=-4, z=5)
    ts = A(26, "Wyobraź sobie")
    b.el(emo("🏠", 210), 1330, 720, ts)
    b.el(emo("👴", 160), 1560, 790, ts + 0.25, idle="bob")
    b.el('<div class="pill" style="font-size:36px">SĄSIAD: POLSKI KAPRAL</div>', 1380, 420, A(26, "mieszka polski kapral"), a="sd")
    tn = A(26, "I jest niedźwiedziem")
    b.el(bear_head(True, size=230), 980, 760, tn, a="drop", idle="bob", z=6)
    b.shake(tn + 0.3, 8)
    b.el(f'<div class="big" style="font-size:110px;color:{P}">?!</div>', 1650, 590, tn + 0.45, rot=10, idle="wig", z=8)
    bs.append(b)

    # ── 27 ──
    b = sad(B(27, "Koniec wojska", "żołnierze rozjeżdżają się po świecie", **sad_kw))
    tr = A(27, "rozjeżdżają")
    for i, (x, y, oa) in enumerate([(820, 520, "left"), (960, 480, "up"), (1100, 520, "right"), (840, 680, "left"), (960, 720, "down"), (1080, 680, "right")]):
        b.el(emo("🪖", 110), x, y, b.start + 0.2 + 0.06 * i, out=tr + 0.08 * i, od=0.5, oa=oa, idle="bob", snd=i == 0)
    tk = A(27, "A niedźwiedzia")
    b.draw("M700 920 V560 H1220 V920 Z M1100 920 V760 H1170 V920 M760 640 H880 V730 H760 Z", tk, 0.7, w=8, color="#cfd6df")
    b.el(emo("🌍", 200), 960, 620, tr + 0.35, out=tk - 0.05, oa="pop", od=0.2, idle="spin")
    b.el(T("KAWALERKA", 40, G, extra="font-weight:800;letter-spacing:3px"), 470, 600, tk + 0.3, a="fade")
    tz = A(27, "nie zabierzesz")
    b.el(bear_head(True, size=520), 960, 730, tz, a="pop", z=6, idle="jit")
    b.shake(tz + 0.25, 9)
    b.el('<div class="chyba">(chyba)</div>', 1460, 520, E(27) - 0.35, rot=8, z=9)
    bs.append(b)

    # ── 28 ──
    b = sad(B(28, "Edinburgh Zoo", "15 listopada 1947", src="źródło: ANSA", **sad_kw))
    b.el(f'<div class="big" style="font-size:150px">15.11.1947</div>', 960, 440, A(28, "Piętnastego"), a="wipe", d=1.0)
    tz = A(28, "trafia do zoo")
    b.el(bear_head(False, mood="sad", size=260), 960, 830, tz + 0.2, a="fade", z=3, snd=False)
    b.draw("M600 980 V720 Q960 540 1320 720 V980", tz - 0.3, 0.8, w=12, color="#cfd6df")
    b.draw(" ".join(f"M{x} {700 if 640 < x < 1280 else 760} V980" for x in range(680, 1260, 80)), tz + 0.4, 0.7, w=9, color="#cfd6df", snd="swipe")
    b.el(f'<div class="big" style="font-size:70px;color:{Y}">ZOO</div>', 960, 655, tz + 0.1, z=6)
    bs.append(b)

    # ── 29 ──
    b = sad(B(29, "Po polsku", "podobno reagował na nasz język", src="źródło: relacje odwiedzających", **sad_kw))
    b.el(emo("💔", 120), 430, 800, A(29, "łamie serce"), idle="pulse")
    to = A(29, "od razu się ożywiał")
    b.el(bear_head(False, mood="sleepy", size=300), 1200, 690, b.start + 0.3, a="fade", rot=9, out=to, od=0.12, oa="fade", snd=False)
    bubble = (f'<div style="position:relative;background:#fff;color:#111;border-radius:40px;padding:26px 54px;font-weight:900;font-style:italic;font-size:86px;box-shadow:0 10px 0 #000;white-space:nowrap">Wojtek!'
              '<div style="position:absolute;right:70px;bottom:-40px;width:0;height:0;border-left:30px solid transparent;border-right:30px solid transparent;border-top:44px solid #fff"></div></div>')
    b.el(bubble, 700, 520, A(29, "zawołał"), rot=-4, idle="wig")
    b.el(bear_head(False, size=330), 1200, 670, to, a="pop", idle="wig", z=6)
    b.punch.append([to, 0.025])
    for i, (x, y) in enumerate([(1420, 450), (980, 470), (1450, 880)]):
        b.el(emo("✨", 90, flat=True), x, y, to + 0.15 + 0.12 * i, idle="pulse", snd=False)
    b.sfx("ding", to + 0.1, 1200)
    bs.append(b)

    # ── 30 ──
    b = sad(B(30, "Odwiedziny", "dawni koledzy z wojska", **sad_kw))
    td = A(30, "Dawni koledzy")
    b.el(emo("👴", 180), 380, 720, td, idle="bob")
    b.el(emo("👴", 170), 600, 740, td + 0.2, idle="bob")
    for x, e, ph in [(860, "🍬", "słodycze"), (1040, "🍺", "piwo"), (1220, "🚬", "papierosy")]:
        b.el(emo(e, 120), x, 450, A(30, ph), idle="float")
    b.el(bear_head(False, size=290), 1500, 720, b.start + 0.3, idle="bob", z=6)
    tm = A(30, "mocowali się")
    b.el(emo("🤼", 160), 1040, 760, tm, idle="jit", z=7)
    b.shake(tm + 0.2, 4)
    bs.append(b)

    # ── 31 ──
    b = sad(B(31, "1942–1963", "szesnaście lat w zoo", push=0.02, **sad_kw))
    b.el(bear_head(False, size=330), 960, 540, b.start + 0.2, a="fade", d=1.0, idle="breathe", snd=False)
    b.el(T("16 LAT W ZOO", 50, "#fff", extra="font-weight:800"), 960, 790, A(31, "przeżył w zoo"), a="fade", d=0.6)
    b.el(T("zmarł w 1963", 44, G, extra="font-weight:700"), 960, 865, A(31, "Zmarł"), a="fade", d=0.6)
    b.el(T("miał 21 lat", 44, G, extra="font-weight:700"), 960, 935, A(31, "Miał dwadzieścia"), a="fade", d=0.6)
    bs.append(b)

    # ── 32 DZIŚ ──
    b = B(32, "Dziś pamiętają", "pomniki i ulica jego imienia", src="źródło: Wikipedia")
    b.gray.append([b.start, b.start + 1.3, 0.6, 0]); b.dim.append([b.start, b.start + 1.3, 0.12, 0])
    b.sfx("rise", b.start, 960, 1.3)
    for n in ["Polska", "Szkocja", "Włochy"]:
        x, y = E2(*PLACES[n]); b.el(dot(0, 0, "#3a4450", 12), round(x), round(y), b.start + 0.2, a="fade", z=4, snd=False)
    for n, ph, lx, ly in [("Kraków", "w Krakowie", 110, 30), ("Edynburg", "w Edynburgu", 50, 85), ("Duns", "Duns", 170, 40), ("Poznań", "w Poznaniu", -130, -20)]:
        x, y = E2(*PLACES[n]); t = A(32, ph)
        if n == "Duns": x, y = x + 20, y + 5
        b.el(emo("📍", 90), round(x), round(y - 45), t, a="drop", z=6)
        b.el(maplab(n, 38), round(x + lx), round(y + ly), t + 0.15, a="fade", z=6, snd=False)
    tu = A(32, "ulica Kaprala")
    b.el('<div style="background:#123f93;border:8px solid #fff;border-radius:12px;padding:18px 44px;font-weight:800;font-size:58px;color:#fff;box-shadow:0 10px 0 #000;white-space:nowrap">ul. Kaprala Wojtka</div>',
         1380, 850, tu, rot=-3, z=8)
    b.shake(tu + 0.2, 5)
    bs.append(b)

    # ── 33 ──
    b = B(33, "Kapral Wojtek", "piwo, papierosy i pociski pod Monte Cassino")
    tn = A(33, "Nie wiem.")
    for x, e, l, ph in [(560, "🍺", "piwo", "pił piwo"), (960, "🚬", "papierosy", "jadł papierosy"), (1360, "📦", "pociski", "nosił pociski")]:
        b.el(card(emo(e, 130) + lab(l, 40), 300, 300), x, 560, A(33, ph), out=tn - 0.2, oa="pop", od=0.25, idle="float")
    tq = A(33, "Dziwna historia?")
    b.el(f'<div class="big" style="font-size:180px;color:{P}">?</div>', 960, 830, tq, out=tn, oa="pop", od=0.2, idle="wig", z=8)
    tb = A(33, "Ale bangla")
    b.el(f'<div class="big" style="font-size:150px">NIE WIEM,</div>', 960, 525, tn + 0.05, a="stamp", z=9)
    b.shake(tn + 0.25, 6)
    b.el(f'<div class="big" style="font-size:150px;color:{Y}">ALE BANGLA</div>', 960, 680, tb, a="stamp", z=9)
    b.shake(tb + 0.2, 12); b.flash.append(tb + 0.2); b.punch.append([tb + 0.2, 0.03])
    b.el('<div class="chyba" style="font-size:52px">(chyba)</div>', 1480, 800, tb + 0.45, rot=-8, z=10)
    b.el(bear_head(True, size=200), 320, 870, tb + 0.3, idle="wig", z=9)
    bs.append(b)

    # ── 34 ──
    b = B(34, "Następny odcinek", "facet, który sprzedał Wieżę Eiffla")
    tw = A(34, "wyślij mu")
    tn = A(34, "A w następnym")
    b.el('<div class="ypill" style="font-size:52px">WYŚLIJ TO KOMUŚ</div>', 560, 560, tw, rot=-3, out=tn, oa="up", od=0.3)
    b.el(emo("📤", 140), 560, 760, tw + 0.2, out=tn, oa="up", od=0.3, idle="bob")
    te = A(34, "Wieżę Eiffla")
    tower = ("M380 980 Q470 800 505 580 L516 330 L528 330 L539 580 Q574 800 664 980 "
             "M430 980 Q522 870 614 980 M462 800 H582 M495 600 H549 M516 330 V290")
    b.draw(tower, te - 0.4, 1.4, w=9, color="#fff")
    b.draw("M540 600 Q640 600 700 640", te + 0.9, 0.3, w=5, color=G, snd=False)
    b.el(f'<div style="background:{Y};color:#111;font-weight:900;font-style:italic;font-size:40px;padding:12px 30px;border-radius:12px 40px 40px 12px;box-shadow:0 6px 0 #000;white-space:nowrap">NA SPRZEDAŻ</div>',
         830, 680, te + 1.1, rot=10, idle="sway", z=7)
    b.el(f'<div class="big" style="font-size:120px;color:{P}">?!</div>', 820, 430, A(34, "I to nie jest"), rot=8, idle="wig", z=8)
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
