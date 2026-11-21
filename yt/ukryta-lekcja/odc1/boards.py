"""Plansze odcinka 1 – wszystkie czasy przypięte do słów lektora."""
import json, random
from engine import *

TL = json.load(open("/home/claude/faceless/yt/odc1/timeline.json"))
F = {f["id"]: f for f in TL["frags"]}
S = lambda i: F[i]["t0"]
E = lambda i: F[i]["t1"]

def A(fid, phrase, n=1):
    txt = F[fid]["text"]; c = -1
    for _ in range(n):
        c = txt.index(phrase, c + 1)
    rows = F[fid]["map"]
    for cs, ce, ts, te in rows:
        if cs <= c < ce:
            return round(ts + (c - cs) / max(1, ce - cs) * (te - ts), 3)
    return rows[-1][3]

def te(items):
    m = 0
    for it in items:
        if not it: continue
        s = it["s"]; import re
        t0 = float(re.search(r'data-t0="__T([\d.]+)__"', s).group(1)) if 'data-t0="__T' in s else it["t"]
        du = float(re.search(r'data-du="([\d.]+)"', s).group(1)) if 'data-du="' in s else 0
        m = max(m, t0 + du)
    return m

DAYS = ["pn", "wt", "śr", "cz", "pt", "sb", "nd"]
DX = [260 + i * 150 for i in range(7)]
random.seed(4)
specs = []  # (name, last_fid, kwargs-builder)

def b01():
    t_dl = A(2, "Więc dlaczego"); t_ul = E(2) - 0.15; t_st = A(2, "z wielkiego planu")
    items = [T("dieta od poniedziałku.", 150, 180, A(1, "Dieta") - 0.05),
             T("siłownia od pierwszego.", 150, 300, A(1, "Siłownia") - 0.05),
             T("nowe życie od stycznia.", 150, 420, A(1, "Nowe życie") - 0.05),
             D("M140 240 L890 230", t_st, 0.2, RED, 7, x=500), D("M140 360 L940 350", t_st + 0.2, 0.2, RED, 7, x=520),
             D("M140 480 L955 470", t_st + 0.4, 0.2, RED, 7, x=540),
             T("dlaczego nigdy od dziś?", 150, 600, t_dl - 0.05, 0.85, size=138, cls="y", cv=True),
             D("M150 770 C420 752 820 782 1240 760", t_ul, 0.3, YL, 10, x=700)]
    return dict(items=items, poses=[[0, "hang"], [1.2, "pointL"], [t_st + 0.3, "facepalm"], [t_dl + 0.2, "shrug"]],
                moves=[[0.0, 1.1, 2100, MX]], cam=[[t_dl - 0.1, 1.12, 700, 640, 0.45]], shakes=[[t_ul + 0.05, 5]], fadeIn=0.4, resid_static=False)

def b02():
    items = [T("w tym odcinku:", 150, 110, S(3) + 0.1, size=64, cls="dim"),
             *icon(brain(330, 400), A(3, "w twojej głowie") - 0.5, 0.35, x=330),
             T("co dzieje się w głowie", 330, 500, A(3, "w twojej głowie"), size=40, cx=True),
             *icon(barchart(760, 400), A(3, "naukowcy") - 0.6, 0.3, x=760),
             T("co sprawdzili naukowcy", 760, 500, A(3, "naukowcy") - 0.1, size=40, cx=True),
             *icon(steps(1190, 400), A(3, "jak wykorzystać") - 0.3, 0.3, YL, x=1190),
             T("jak to wykorzystać", 1190, 500, A(3, "jak wykorzystać"), size=40, cls="y", cx=True)]
    return dict(items=items, poses=[[S(3), "hips"], [A(3, "w twojej głowie") - 0.3, "pointL"], [A(3, "naukowcy") - 0.3, "pointLlow"], [A(3, "jak wykorzystać"), "idea"]])

def b03():
    tk = A(5, "kreski"); walk = [A(5, "Tak twój mózg") - 0.2, A(5, "Tak twój mózg") + 0.6]
    d0 = tk + 0.3; back = [d0 + 0.5, d0 + 1.2]
    items = [T("to nie lenistwo.", 150, 110, A(4, "To nie jest lenistwo") - 0.05, 0.55, size=130, cv=True),
             T("ani słaba wola.", 150, 250, A(4, "I to nie jest") - 0.05, 0.5, size=130, cv=True),
             T("to nie wada charakteru.", 155, 395, A(5, "to nie wada") - 0.05, size=52, cls="dim"),
             T("twój mózg potrzebuje", 150, 470, A(5, "On po prostu") - 0.1, 0.6, size=72),
             POP("kreski.", 150, 560, tk - 0.05, size=190, cls="y"),
             D("M900 470 L894 660", d0, 0.45, YL, 13, id="kr3", x=900)]
    return dict(items=items, poses=[[S(4), "hips"], [A(4, "To nie jest"), "think"], [walk[0], "hips"], [tk + 0.02, "wow"], [tk + 0.2, "ik", "kr3"], [back[0], "hips"]],
                moves=[[walk[0], walk[1], MX, 980], [back[0], back[1], 980, MX]], cam=[[tk - 0.1, 1.1, 600, 600, 0.25]], shakes=[[tk, 9]])

def b04():
    tw = A(8, "Każdy z nich"); walk = [tw - 0.4, tw + 0.5]; d0 = walk[1] + 0.12; back = [d0 + 0.7, d0 + 1.5]
    ticks = [(560, "pn", A(7, "Poniedziałek")), (780, "1. dzień", A(7, "pierwszy dzień")), (1000, "1 stycznia", A(7, "nowy rok")), (1220, "urodziny", A(7, "urodziny"))]
    items = [D("M150 600 C500 596 900 604 1300 598", A(6, "oś czasu") - 0.2, 0.65, x=700),
             D("M1262 572 L1302 598 L1262 624", A(6, "oś czasu") + 0.45, 0.15, x=1280),
             T("dieta", 230, 625, A(6, "Dieta") - 0.05, size=54, cls="dim"), D("M218 662 L372 654", A(6, "która nie wyszła"), 0.2, RED, 7, x=300),
             T("treningi", 230, 695, A(6, "Treningi") - 0.05, size=54, cls="dim"), D("M218 732 L430 724", A(6, "które się nie odbyły"), 0.2, RED, 7, x=320),
             T("plany", 230, 765, A(6, "Plany") - 0.05, size=54, cls="dim"), D("M218 802 L372 795", A(6, "które się rozjechały"), 0.2, RED, 7, x=300),
             *[D(f"M{x} 575 L{x} 625", t - 0.05, 0.2, CH, 8, x=x) for x, _, t in ticks],
             *[T(lab, x + (34 if lab == "pn" else 0), 640, t, size=40, cx=True) for x, lab, t in ticks],
             T("punkty orientacyjne w czasie", 150, 90, A(7, "Badacze") - 0.05, size=66, cls="y"),
             D("M560 505 L556 680", d0, 0.5, YL, 13, id="kr4", x=560),
             T("stary ja", 190, 370, A(8, "starą wersję") - 0.05, 0.45, size=100, cv=True),
             T("nowy ja", 880, 370, A(8, "od nowej") - 0.05, 0.45, size=100, cls="y", cv=True),
             D(star(1205, 425), A(8, "od nowej") + 0.4, 0.4, YL, 8, x=1205),
             D(ell(320, 712, 175, 112), A(8, "Wszystkie dawne") + 0.2, 0.6, YL, 7, x=320)]
    return dict(items=items, poses=[[S(6), "hips"], [A(6, "oś czasu"), "pointLlow"], [A(7, "Poniedziałek"), "pointL"], [walk[0], "hips"],
                                    [walk[1] - 0.05, "ik", "kr4"], [back[0], "hips"], [back[1] + 0.05, "pointL"]],
                moves=[[walk[0], walk[1], MX, 620], [back[0], back[1], 620, MX]], cam=[[walk[1] - 0.1, 1.12, 590, 590, 0.4], [back[0], 1.0, 960, 540, 0.5]])

def b05():
    t10 = S(10); to = E(9) + 0.05
    items = [T("nowa wersja ciebie:", 150, 100, A(9, "Nowa wersja") - 0.05, size=110, cv=True, out=to),
             T("jeszcze nic nie zawaliła.", 155, 235, A(9, "jeszcze niczego") - 0.05, size=58, cls="dim", out=to),
             BOX(300, 370, 560, 330, A(9, "Ma czystą kartę") - 0.1, 0.5, out=to),
             T("czysta karta", 580, 480, A(9, "czystą kartę") + 0.2, size=100, cls="y", cv=True, cx=True, out=to),
             BUB("tym razem będzie inaczej!", 860, 250, A(9, "że tym razem") - 0.05, out=to),
             D("M1320 332 L1470 398", A(9, "że tym razem") + 0.5, 0.2, CH, 6, out=to, x=1400),
             D("M150 560 L1300 560", t10 + 0.25, 0.4, x=700),
             D("M700 532 L700 588", t10 + 0.5, 0.2, YL, 9, x=700),
             T("dziś", 700, 600, t10 + 0.55, size=50, cls="y", cx=True),
             D("M160 520 Q160 470 400 470 L680 470 Q725 470 725 430 Q725 470 770 470 L1050 470 Q1290 470 1290 520", A(10, "jak wygląda całe") - 0.1, 1.0, CH, 7, x=725),
             T("całe życie", 725, 320, A(10, "całe twoje życie") - 0.05, size=100, cv=True, cx=True),
             POP("energia", 150, 700, A(10, "dodaje energii") - 0.05, size=110, cls="y"),
             D(arrow_up(560, 830, 120), A(10, "dodaje energii") + 0.2, 0.35, YL, 11, x=560)]
    return dict(items=items, poses=[[S(9), "hips"], [A(9, "Ma czystą kartę"), "pointL"], [A(9, "I właśnie"), "heart"], [t10, "hips"], [A(10, "dodaje energii"), "wow"]],
                cam=[[t10 + 0.05, 2.4, 700, 560, 0.3], [A(10, "jak wygląda całe") - 0.2, 1.0, 960, 540, 1.4]],
                jumps=[A(10, "dodaje energii") + 0.1])

def b06():
    t82 = A(12, "Aż o")
    items = [T("sprawdzili to.", 150, 90, A(11, "Sprawdzili") - 0.05, 0.55, size=136, cv=True),
             T("Uniwersytet Pensylwanii (Wharton), 2014", 155, 240, A(11, "Uniwersytetu") - 0.05, size=40, cls="dim"),
             *icon(magnifier(1180, 200), A(11, "wyszukiwarki Google") - 0.3, 0.3, x=1180),
             BOX(150, 330, 620, 90, A(12, "wpisują słowo") - 0.2, 0.45, out=A(12, "O czternaście") - 0.4,
                 inner='<div style="position:absolute;left:28px;top:2px;font-size:54px">dieta<span style="opacity:.8">|</span></div>'),
             D("M260 860 L1180 860", A(12, "na początku tygodnia") - 0.4, 0.35, x=720),
             BAR(380, 860, 200, 70, A(12, "na początku tygodnia") - 0.1, 0.4),
             T("początek tygodnia", 480, 878, A(12, "na początku tygodnia") + 0.1, size=40, cx=True),
             CNT(400, 660, 14, A(12, "O czternaście") - 0.05, 0.6),
             BAR(760, 860, 200, 400, A(12, "A na początku roku") - 0.05, 0.6, yellow=True),
             T("początek roku", 860, 878, A(12, "A na początku roku") + 0.2, size=40, cls="y", cx=True),
             CNT(778, 330, 82, t82 - 0.05, 0.9),
             T("wzrost wyszukiwań „diet” w Google (USA)", 262, 960, t82 + 0.7, size=42, cls="dim")]
    return dict(items=items, poses=[[S(11), "hips"], [S(11) + 0.1, "think"], [A(12, "Okazało"), "hips"], [A(12, "na początku tygodnia"), "pointLlow"], [t82 + 0.8, "wow"]],
                cam=[[A(12, "A na początku roku") - 0.2, 1.12, 860, 640, 0.5]], shakes=[[t82 + 0.85, 8]], jumps=[t82 + 0.8])

def b07():
    t14 = S(14); tt = A(13, "Na początku tygodnia")
    items = [T("potem: siłownia.", 150, 90, A(13, "Potem sprawdzili") - 0.05, size=120, cv=True),
             T("prawie 12 000 osób", 155, 225, A(13, "Prawie dwanaście") - 0.05, size=46, cls="dim"),
             D("M260 860 L1360 860", tt - 0.5, 0.35, out=t14, x=800),
             BAR(330, 860, 190, 300, tt - 0.3, 0.4, out=t14), T("zwykły dzień", 425, 878, tt - 0.2, size=40, cx=True, out=t14),
             BAR(650, 860, 190, 400, tt + 0.2, 0.5, yellow=True, out=t14), T("początek tygodnia", 745, 878, tt + 0.3, size=40, cls="y", cx=True, out=t14),
             CNT(660, 330, 33, A(13, "o jedną trzecią") - 0.05, 0.6, out=t14),
             BAR(970, 860, 190, 441, A(13, "Na początku semestru") - 0.05, 0.5, yellow=True, out=t14),
             T("początek semestru", 1065, 878, A(13, "Na początku semestru") + 0.1, size=40, cls="y", cx=True, out=t14),
             CNT(980, 290, 47, A(13, "jeszcze bardziej") - 0.1, 0.6, out=t14),
             *icon(tree(350, 520), A(14, "po świętach") - 0.3, 0.3, x=350), T("święta", 350, 600, A(14, "po świętach"), size=44, cx=True),
             D(arrow_up(450, 560, 90), A(14, "po świętach") + 0.2, 0.25, YL, 9, x=450),
             *icon(suitcase(760, 520), A(14, "po przerwach") - 0.3, 0.3, x=760), T("przerwy", 760, 600, A(14, "po przerwach"), size=44, cx=True),
             D(arrow_up(860, 560, 90), A(14, "po przerwach") + 0.2, 0.25, YL, 9, x=860),
             *icon(cake(1170, 520), A(14, "urodzinach") - 0.4, 0.25, x=1170), T("urodziny", 1170, 600, A(14, "urodzinach"), size=44, cx=True),
             D(arrow_up(1270, 560, 90), A(14, "urodzinach") + 0.2, 0.25, YL, 9, x=1270)]
    tj = A(13, "jeszcze bardziej") + 0.5
    return dict(items=items, poses=[[S(13), "hips"], [tt - 0.3, "pointLlow"], [tj - 0.05, "wow"], [t14, "hips"], [A(14, "po świętach"), "pointL"]],
                jumps=[tj], shakes=[[tj + 0.45, 6]])

def b08():
    walk = [S(16) - 0.1, S(16) + 0.9]; back = [E(16) + 0.05, E(16) + 0.9]; tb = A(16, "dobra, zacznę")
    curve = smooth([(x + 18, y) for x, y in zip(DX, [300, 395, 475, 532, 570, 592, 604])])
    items = [T("ale jest haczyk.", 150, 70, A(15, "Ale jest haczyk") - 0.05, 0.6, size=136, cv=True),
             D("M220 700 L1220 700", A(15, "Ten zastrzyk") - 0.3, 0.35, x=720),
             *[T(d, x, 714, A(15, "Ten zastrzyk") - 0.1 + i * 0.05, 0.15, size=40) for i, (d, x) in enumerate(zip(DAYS, DX))],
             T("motywacja", 225, 225, A(15, "motywacji") - 0.1, size=40, cls="dim"),
             D(curve, A(15, "z czasem słabnie") - 0.3, 1.2, CH, 8, x=700),
             T("im dalej od kreski, tym mniej chęci.", 150, 830, A(15, "Im dalej") - 0.05, size=56, out=S(16)),
             D(ell(580, 744, 52, 40), A(16, "a w środę") - 0.05, 0.4, YL, 7, x=580),
             BUB("zacznę od następnego poniedziałku…", 780, 230, tb - 0.05, out=back[0]),
             D("M870 314 L765 372", tb + 0.6, 0.2, CH, 6, out=back[0], x=800)]
    return dict(items=items, poses=[[S(15), "hips"], [walk[1] - 0.05, "pointDown"], [A(16, "już się nie chce"), "facepalm"], [tb + 0.4, "shrug"], [back[0], "hips"]],
                moves=[[walk[0], walk[1], MX, 700], [back[0], back[1], 700, MX]],
                cam=[[A(15, "z czasem słabnie") - 0.35, 1.12, 420, 420, 0.35], [A(15, "z czasem słabnie") + 0.05, 1.12, 900, 560, 0.9], [A(15, "Im dalej") - 0.1, 1.0, 960, 540, 0.45]],
                shakes=[[A(16, "już się nie chce"), 4]])

def b09():
    cx, cy, r = 720, 560, 250
    words = [("kreska", cx, cy - r - 40, "Kreska,"), ("start", cx + r + 20, cy - 30, "start,"), ("środa", cx, cy + r - 10, "środa,"), ("odpuszczenie", cx - r - 30, cy - 30, "odpuszczenie")]
    arcs = [(-62, -22), (22, 62), (118, 158), (202, 242)]
    t2 = A(17, "Kreska", 2)
    items = [T("i tak w kółko.", 150, 70, A(17, "I tak w kółko") - 0.05, size=110, cv=True)]
    for (w, x, y, ph), (a1, a2) in zip(words, arcs):
        tw = A(17, ph)
        items += [T(w, x, y, tw - 0.05, size=60, cls="y" if w == "środa" else "", cx=True), D(arc(cx, cy, r, a1, a2), tw + 0.25, 0.3, CH, 7, x=x)]
    sec = [A(17, "Kreska", 2), A(17, "start", 2), A(17, "środa", 2), E(17) - 0.15]
    for (a1, a2), ts in zip(arcs, sec):
        items.append(D(arc(cx, cy, r, a1, a2), ts + 0.1, 0.3, YL, 10, x=720))
    k1 = A(17, "Kreska,")
    return dict(items=items, poses=[[S(17), "hips"]], moves=[[k1, k1 + 0.6, MX, 1330], [k1 + 0.6, k1 + 1.2, 1330, MX], [t2, t2 + 0.6, MX, 1330], [t2 + 0.6, t2 + 1.2, 1330, MX]])

def b10():
    t3 = A(18, "trzy sposoby")
    items = [T("dobra wiadomość:", 150, 100, A(18, "Dobra wiadomość") - 0.05, size=110, cv=True),
             T("możesz obrócić to na swoją korzyść", 155, 240, A(18, "możesz obrócić") - 0.05, size=54, cls="dim"),
             POP("I.", 170, 360, t3 - 0.05, size=100), WIPE(300, 407, 620, t3 + 0.15),
             POP("II.", 170, 520, t3 + 0.35, size=100), WIPE(300, 567, 540, t3 + 0.55),
             POP("III.", 170, 680, t3 + 0.7, size=100), WIPE(300, 727, 580, t3 + 0.9)]
    return dict(items=items, poses=[[S(18), "hips"], [A(18, "Dobra wiadomość"), "idea"], [t3 - 0.1, "pointL"]])

def b11():
    tw = A(19, "Kreska nie musi"); walk = [tw + 0.3, tw + 1.1]; d0 = A(19, "narysować") - 0.1; back = [d0 + 0.7, d0 + 1.5]
    items = [POP("I.", 150, 90, A(19, "Pierwszy") - 0.05, size=120),
             T("zrób sobie poniedziałek dziś", 290, 108, A(19, "Zrób sobie") - 0.05, size=72, cls="y"),
             *icon(calendar(250, 360, 240, 200), tw - 0.1, 0.3, x=370),
             T("pn", 370, 430, tw + 0.4, size=80, cv=True, cx=True),
             D(cross(268, 372, 6.4), A(19, "w kalendarzu"), 0.35, RED, 10, x=370),
             D("M900 470 L894 660", d0, 0.5, YL, 13, id="kr11", x=900),
             T("dziś", 897, 680, d0 + 0.5, size=54, cls="y", cx=True)]
    return dict(items=items, poses=[[S(19), "hips"], [walk[1] - 0.05, "ik", "kr11"], [back[0], "hips"]],
                moves=[[walk[0], walk[1], MX, 980], [back[0], back[1], 980, MX]], cam=[[d0 - 0.2, 1.1, 900, 560, 0.35]])

def b12():
    c1, c2, c3 = A(20, "dwudziesty marca"), A(20, "Innym jako"), A(20, "Ta druga grupa")
    card = lambda big, small, cls: (f'<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center">'
                                    f'<div class="cv" style="font-size:96px">{big}</div><div class="{cls}" style="font-size:52px;margin-top:6px">{small}</div></div>')
    items = [T("eksperyment", 150, 80, A(20, "zrobili eksperyment") - 0.2, size=110, cv=True),
             BOX(200, 300, 460, 300, c1 - 0.1, 0.5, inner=card("20 marca", "zwykły czwartek", "dim")),
             BOX(780, 300, 500, 300, c2 - 0.05, 0.5, yellow=True, inner=card("20 marca", "1. dzień wiosny", "y")),
             *icon(sprout(1220, 370), c2 + 0.6, 0.3, x=1220),
             T("mniej chętnych", 430, 640, c3 + 0.2, size=46, cls="dim", cx=True),
             T("więcej chętnych, by zacząć", 1030, 640, c3 - 0.05, size=46, cls="y", cx=True),
             D(check(1000, 760, 1.6), c3 + 0.9, 0.3, YL, 10, x=1030)]
    return dict(items=items, poses=[[S(20), "hips"], [c1, "pointLlow"], [c2, "pointL"], [c3, "idea"]], cam=[[c3 - 0.2, 1.1, 1030, 560, 0.5]])

def b13():
    t1 = A(21, "dzień pierwszy")
    items = [T("liczy się znaczenie, nie data.", 150, 90, A(21, "liczy się nie data") - 0.05, size=100, cv=True),
             T("dziś też może być takim dniem", 155, 215, A(21, "Dzień, w którym") - 0.05, size=54, cls="dim"),
             BOX(420, 330, 640, 420, A(21, "Weź kartkę") - 0.1, 0.5, style="background:rgba(237,235,228,.05)"),
             T("data: ___ . ___ . ______", 470, 380, A(21, "napisz dzisiejszą") - 0.05, size=48, cls="dim"),
             T("dzień 1", 560, 500, t1 - 0.05, 0.6, size=170, cls="y", cv=True),
             D("M560 690 C700 680 820 700 930 684", t1 + 0.6, 0.3, YL, 10, x=740)]
    return dict(items=items, poses=[[S(21), "hips"], [A(21, "Weź kartkę"), "pointLlow"], [t1 + 0.6, "wow"]], jumps=[t1 + 0.6],
                cam=[[t1 - 0.2, 1.15, 740, 560, 0.5]])

def b14():
    items = [POP("II.", 150, 90, A(22, "Drugi") - 0.05, size=120),
             T("krok tak mały, że głupio go nie zrobić", 300, 112, A(22, "Zrób pierwszy krok") - 0.05, size=56, cls="y"),
             T("godzina na siłowni", 150, 360, A(22, "Nie godzina") - 0.05, size=60, cls="dim"),
             D("M140 402 L625 394", A(22, "tylko założenie") - 0.1, 0.2, RED, 7, x=380), D(arrow_r(660, 400, 780), A(22, "tylko założenie"), 0.25, CH, 8, x=720),
             T("załóż buty", 820, 360, A(22, "założenie butów") - 0.05, size=60, cls="y"),
             T("cała nowa dieta", 150, 520, A(22, "Nie cała") - 0.05, size=60, cls="dim"),
             D("M140 562 L545 554", A(22, "tylko jeden") - 0.1, 0.2, RED, 7, x=340), D(arrow_r(660, 560, 780), A(22, "tylko jeden"), 0.25, CH, 8, x=720),
             T("1 porządny posiłek", 820, 520, A(22, "jeden porządny") - 0.05, size=60, cls="y")]
    return dict(items=items, poses=[[S(22), "hips"], [A(22, "Nie godzina"), "think"], [A(22, "tylko założenie"), "idea"], [A(22, "Nie cała"), "pointL"]])

def b15():
    tf1, tf2 = A(23, "jeśli wracam"), A(23, "to od razu")
    items = [T("plan w jednym zdaniu:", 150, 90, A(23, "zaplanuj go") - 0.1, size=100, cv=True),
             T("jeśli", 150, 300, A(23, "jeśli wydarzy") - 0.05, size=110, cv=True), D("M380 400 L1240 400", A(23, "jeśli wydarzy") + 0.25, 0.35, CH, 7, x=800),
             T("X", 780, 310, A(23, "się X") - 0.05, size=76, cls="dim", out=tf1 - 0.15),
             T("to", 150, 520, A(23, "to robię") - 0.05, size=110, cv=True), D("M300 620 L1240 620", A(23, "to robię") + 0.2, 0.35, CH, 7, x=800),
             T("Y", 760, 530, A(23, "robię Y") - 0.05, size=76, cls="dim", out=tf2 - 0.15),
             T("wracam z pracy", 420, 310, tf1 - 0.05, size=76, cls="y"),
             T("od razu zakładam buty", 330, 530, tf2 - 0.05, size=76, cls="y")]
    return dict(items=items, poses=[[S(23), "hips"], [A(23, "jeśli wydarzy"), "think"], [A(23, "Na przykład"), "idea"], [tf2, "pointL"]])

def b16():
    tu = A(24, "wyraźnie zwiększają")
    items = [T("intencje implementacyjne", 150, 90, A(24, "intencjami implementacyjnymi") - 0.05, size=104, cv=True),
             T("= plany „jeśli–to”", 155, 220, A(24, "intencjami implementacyjnymi") + 0.9, size=54, cls="dim"),
             POP("94 badania", 150, 340, A(24, "dziewięćdziesięciu czterech") - 0.05, size=170, cls="y"),
             T("Gollwitzer i Sheeran, 2006", 160, 545, A(24, "badań pokazał") - 0.05, size=44, cls="dim"),
             T("szansa, że naprawdę to zrobisz", 150, 700, tu + 0.2, size=60),
             D(arrow_up(1180, 820, 260), tu - 0.05, 0.5, YL, 12, x=1180)]
    return dict(items=items, poses=[[S(24), "hips"], [A(24, "dziewięćdziesięciu"), "pointL"], [tu + 0.3, "wow"]], jumps=[tu + 0.3], shakes=[[tu + 0.75, 5]])

def b17():
    tp = A(25, "nie musisz już"); walk = [tp - 0.1, tp + 1.5]; back = [E(25) + 0.02, E(25) + 0.8]
    items = [T("dlaczego to działa?", 150, 80, A(25, "Dlaczego to działa") - 0.05, size=110, cv=True),
             D("M220 760 L1250 760", S(25) + 0.6, 0.3, x=720),
             T("motywacja", 250, 270, A(25, "motywacja spada") - 0.1, size=40, cls="dim"),
             D(smooth([(240, 330), (500, 470), (760, 600), (1000, 670), (1230, 700)]), A(25, "motywacja spada") - 0.1, 0.9, CH, 7, x=700),
             D("M240 400 L1240 400", tp - 0.1, 0.8, YL, 9, x=740),
             T("plan", 1100, 320, tp + 0.4, size=58, cls="y"),
             T("decyzja zapadła wcześniej.", 150, 830, A(25, "Decyzja zapadła") - 0.05, size=62)]
    return dict(items=items, poses=[[S(25), "hips"], [S(25) + 0.1, "think"], [walk[0] - 0.05, "hips"]],
                moves=[[walk[0], walk[1], MX, 1350], [back[0], back[1], 1350, MX]])

def b18():
    tf = A(26, "Bo ona przyjdzie")
    items = [POP("III.", 150, 90, A(26, "Trzeci") - 0.05, size=120),
             T("zaplanuj wpadkę", 370, 100, A(26, "Zaplanuj wpadkę") - 0.05, size=96, cls="y", cv=True),
             T("bo ona przyjdzie.", 155, 260, tf - 0.05, size=62),
             T("nie: czy opuścisz dzień", 155, 420, A(26, "czy opuścisz") - 0.2, size=62, cls="dim"),
             D("M145 462 L765 454", A(26, "tylko co zrobisz") - 0.1, 0.2, RED, 7, x=450),
             T("tylko: co zrobisz potem", 155, 540, A(26, "tylko co zrobisz") - 0.05, size=72, cls="y")]
    return dict(items=items, poses=[[S(26), "hips"], [tf + 0.1, "trip"], [A(26, "Pytanie"), "hips"], [A(26, "tylko co zrobisz"), "idea"]],
                sfx=[("thud", tf + 0.35, 0.6, 1450)], shakes=[[tf + 0.35, 4]])

def b19():
    t66 = A(27, "sześćdziesiąt sześć dni")
    items = [T("UCL, 2010 · 96 osób · 12 tygodni", 155, 100, A(27, "Naukowcy") - 0.05, size=50, cls="dim"),
             T("ile trwa budowanie nawyku?", 150, 190, A(27, "budowały nowy nawyk") - 0.1, size=64),
             T("średnio", 160, 320, A(27, "Średnio") - 0.05, size=54, cls="dim"),
             POP("66 dni", 150, 380, t66 - 0.05, size=200, cls="y"),
             D("M200 760 L1250 760", A(27, "U niektórych") - 0.3, 0.4, x=720),
             D("M413 728 L413 792", A(27, "U niektórych") - 0.1, 0.2, YL, 9, x=413), T("66", 413, 800, A(27, "U niektórych"), size=50, cls="y", cx=True),
             D("M200 735 L200 785", A(27, "osiemnaście") - 0.1, 0.2, CH, 8, x=200), T("18", 200, 800, A(27, "osiemnaście") - 0.05, size=50, cx=True),
             D("M1250 735 L1250 785", A(27, "ponad dwieście") - 0.1, 0.2, CH, 8, x=1250), T("254", 1250, 800, A(27, "ponad dwieście") - 0.05, size=50, cx=True)]
    return dict(items=items, poses=[[S(27), "hips"], [S(27) + 0.2, "think"], [t66, "wow"], [t66 + 1.2, "hips"], [A(27, "U niektórych"), "pointLlow"]],
                jumps=[t66 + 0.05], shakes=[[t66 + 0.05, 7]])

def b20():
    t1 = A(28, "jeden opuszczony"); t2 = A(28, "Problem zaczynał")
    items = [T("jeden opuszczony dzień:", 150, 90, t1 - 0.05, size=90, cv=True)]
    for row, (y, tb, marks) in enumerate([(260, t1 + 0.1, ["c"] * 6 + ["x"] + ["c"] * 5), (560, t2 - 0.3, ["c"] * 5 + ["x"] * 5 + [None] * 2)]):
        for i, mk in enumerate(marks):
            x = 150 + i * 92
            items.append(CELL(x, y, tb + i * 0.04))
            if mk:
                tm = tb + 0.5 + i * 0.07
                p = check(x + 12, y + 34, 1.0) if mk == "c" else cross(x + 16, y + 16, 1.0)
                items.append(D(p, tm, 0.12, YL if mk == "c" else RED, 7, x=x, snd="tick"))
    items += [T("ok", 150 + 6 * 92 + 31, 340, t1 + 1.1, size=46, cls="y", cx=True),
              T("praktycznie bez szkody", 150, 410, A(28, "praktycznie nie zaszkodził") - 0.05, size=56, cls="y"),
              T("przerwy raz za razem = problem", 150, 680, A(28, "gdy przerwy") - 0.05, size=56, cls="r")]
    return dict(items=items, poses=[[S(28), "hips"], [t1, "pointLlow"], [A(28, "gdy przerwy"), "facepalm"]])

def b21():
    tf = A(29, "Możesz wypaść raz"); tu = A(29, "Nigdy dwa razy"); tw = A(29, "Wracasz jutro")
    items = [T("zasada:", 150, 90, A(29, "zasada jest prosta") - 0.05, size=100, cv=True),
             T("możesz wypaść raz.", 155, 230, tf - 0.05, size=72),
             POP("nigdy dwa razy z rzędu.", 150, 340, tu - 0.05, size=120, cls="y"),
             T("nie czekasz na poniedziałek. wracasz jutro.", 155, 520, A(29, "Nie czekasz") - 0.05, size=60)]
    return dict(items=items, poses=[[S(29), "hips"], [tf + 0.15, "down"], [tu - 0.1, "hips"], [tu + 0.3, "wow"], [tw - 0.15, "hips"]],
                moves=[[tw - 0.1, tw + 0.6, MX, 1380], [tw + 0.6, tw + 1.3, 1380, MX]],
                sfx=[("thud", tf + 0.4, 0.7, 1300)], shakes=[[tu, 7]])

def b22():
    t31 = S(31); walk = [t31, t31 + 0.9]; d1 = A(31, "linię startu") - 0.25; er = A(32, "ścierał ją"); d2 = A(32, "rysował nową") - 0.1
    tpr = A(33, "Po roku"); back = [tpr, tpr + 0.8]
    items = [FADE("vig", S(30) - 0.2, 0.8),
             T("krótka historia", 760, 420, A(30, "krótka historia") - 0.05, size=110, cv=True, cx=True, out=t31 - 0.2),
             D("M700 480 L696 670", d1, 0.5, YL, 12, id="s1", x=700, out=er), T("start", 640, 420, d1 + 0.5, size=46, cls="y", cx=True, out=er),
             FADE("streak ch", er, 0.4, style="left:665px;top:470px;height:220px", snd="rub", x=700),
             D("M735 480 L731 670", d2, 0.45, YL, 12, id="s2", x=735, out=tpr + 0.05),
             FADE("streak ch", tpr + 0.05, 0.3, style="left:700px;top:470px;height:220px", snd="rub", x=735)]
    for i, x in enumerate([230, 380, 520, 860, 1000, 1140, 1280, 600, 300, 950]):
        h = random.randint(240, 420); tt = tpr + 0.25 + i * 0.16
        items.append(FADE("streak ch", tt, 0.25, style=f"left:{x}px;top:{random.randint(300, 470)}px;height:{h}px", snd="rub", x=x))
    items += [POP("52 starty", 150, 130, A(33, "Pięćdziesiąt dwa") - 0.05, size=120, cls="y"),
              POP("0 met", 680, 130, A(33, "ani jednej mety") - 0.05, size=120, cls="r")]
    return dict(items=items, poses=[[S(30), "hips"], [walk[1] - 0.05, "ik", "s1"], [d1 + 0.6, "hips"], [er - 0.3, "facepalm"], [d2 - 0.3, "ik", "s2"],
                                    [d2 + 0.55, "hips"], [A(33, "ani jednej mety"), "shrug"]],
                moves=[[walk[0], walk[1], MX, 790], [back[0], back[1], 790, MX]])

def b23():
    items = [T("ukryta lekcja:", 150, 150, A(34, "Ukryta lekcja") - 0.05, size=80, cls="y", cv=True),
             T("nie potrzebujesz nowej kreski.", 150, 290, A(34, "nie potrzebujesz") - 0.05, size=96, cv=True),
             T("potrzebujesz przestać", 150, 440, A(34, "Potrzebujesz przestać") - 0.05, size=96, cls="y", cv=True),
             T("ścierać starą.", 150, 560, A(34, "ścierać starą") - 0.05, size=96, cls="y", cv=True)]
    return dict(items=items, poses=[[S(34), "hips"], [A(34, "Potrzebujesz przestać"), "heart"]], cam=[[S(34), 1.06, 760, 480, 4.0]])

def b24():
    tw = A(35, "wyślij go")
    items = [T("wyślij to komuś,", 150, 160, tw - 0.05, size=110, cv=True),
             T("kto od lat zaczyna od poniedziałku.", 155, 300, A(35, "kto od lat") - 0.05, size=64),
             *icon(plane(700, 600), tw + 0.3, 0.35, x=700),
             BOX(1290, 505, 165, 92, tw + 0.35, 0.3, out=E(35) - 0.6, inner='<div style="font-size:34px;text-align:center;line-height:80px">dla ciebie</div>')]
    return dict(items=items, poses=[[S(35), "hips"], [tw, "give"]])

def b25():
    ta = A(36, "Arystotelesowi"); tn = A(36, "nigdy go nie napisał")
    items = [T("w następnym odcinku:", 150, 100, A(36, "w następnym odcinku") - 0.05, size=64, cls="dim"),
             BOX(150, 220, 1150, 240, A(36, "najsłynniejszy cytat") - 0.1, 0.6, inner='<div class="cv" style="position:absolute;left:30px;top:-6px;font-size:130px">„</div>'),
             WIPE(270, 285, 860, A(36, "najsłynniejszy cytat") + 0.5), WIPE(270, 365, 640, A(36, "najsłynniejszy cytat") + 0.8),
             T("— Arystoteles?", 700, 490, ta - 0.05, size=90, cv=True),
             D("M690 548 L1240 538", tn - 0.05, 0.3, RED, 10, x=960),
             POP("?!", 1250, 470, tn + 0.3, size=110, cls="r")]
    return dict(items=items, poses=[[S(36), "hips"], [A(36, "najsłynniejszy"), "think"], [tn, "shrug"]], shakes=[[tn + 0.3, 6]])

BUILD = [("b01", 2, b01), ("b02", 3, b02), ("b03", 5, b03), ("b04", 8, b04), ("b05", 10, b05), ("b06", 12, b06), ("b07", 14, b07),
         ("b08", 16, b08), ("b09", 17, b09), ("b10", 18, b10), ("b11", 19, b11), ("b12", 20, b12), ("b13", 21, b13), ("b14", 22, b14),
         ("b15", 23, b15), ("b16", 24, b16), ("b17", 25, b17), ("b18", 26, b18), ("b19", 27, b19), ("b20", 28, b20), ("b21", 29, b21),
         ("b22", 33, b22), ("b23", 34, b23), ("b24", 35, b24), ("b25", 36, b25)]

def build():
    boards, start = [], 0.0
    for name, last, fn in BUILD:
        kw = fn()
        items = [i for i in kw.pop("items") if i]
        moves_end = max([m[1] for m in kw.get("moves", [])] + [0])
        es = max(E(last) + 0.06, te(items) + 0.05, moves_end + 0.05)
        erase = [round(es, 3), round(es + 0.68, 3)]
        end = round(es + 0.72, 3)
        boards.append(Board(name, round(start, 3), end, items, erase=erase, **kw))
        start = end
    out = Board("outro", start, start + 8.0,
                [T("ukryta lekcja", 150, 140, start + 0.3, size=130, cls="y", cv=True), T("dzięki, że jesteś.", 155, 300, start + 1.0, size=60, cls="dim")],
                poses=[[start, "hips"], [start + 0.6, "wave"], [start + 4.5, "hips"]], fadeOut=1.2)
    boards.append(out)
    return boards

if __name__ == "__main__":
    for b in build():
        print(f"{b.name:6s} {b.start:7.2f} → {b.end:7.2f} ({b.end - b.start:5.2f}s) erase {b.erase}")
