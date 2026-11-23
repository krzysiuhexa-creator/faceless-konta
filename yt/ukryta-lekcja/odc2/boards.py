"""Plansze odcinka 2 („dlaczego zawsze wracasz do starych nawyków”) – metafora: ścieżka wydeptana w trawniku.
Wszystkie czasy przypięte do słów lektora."""
import json, random, re, math
from engine import *

TL = json.load(open("/home/claude/faceless/yt/odc2/timeline.json"))
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
        s = it["s"]
        t0 = float(re.search(r'data-t0="__T([\d.]+)__"', s).group(1)) if 'data-t0="__T' in s else it["t"]
        du = float(re.search(r'data-du="([\d.]+)"', s).group(1)) if 'data-du="' in s else 0
        m = max(m, t0 + du)
    return m

def slow(item, od):
    """wolniejsze znikanie (np. zarastająca ścieżka)"""
    item["s"] = item["s"].replace('data-od="0.4"', f'data-od="{od}"'); return item

random.seed(22)
GR = "rgba(237,235,228,.20)"   # wydeptana ścieżka
GY = "rgba(245,197,66,.30)"    # nowa ścieżka

# ─────────── nowe rysunki kredą (tylko pod ten odcinek) ───────────
def mug(cx, cy):
    return [f"M{cx-60} {cy-70} L{cx-52} {cy+60} Q{cx-50} {cy+75} {cx-30} {cy+75} L{cx+30} {cy+75} Q{cx+50} {cy+75} {cx+52} {cy+60} L{cx+60} {cy-70} Z",
            f"M{cx+58} {cy-35} C{cx+110} {cy-40} {cx+110} {cy+35} {cx+54} {cy+30} M{cx-25} {cy-95} C{cx-35} {cy-110} {cx-15} {cy-120} {cx-25} {cy-135} M{cx+10} {cy-95} C{cx} {cy-110} {cx+20} {cy-120} {cx+10} {cy-135}"]
def poster(x, y, w, h):
    return [f"M{x} {y} L{x+w} {y+6} L{x+w-4} {y+h} L{x+4} {y+h-4} Z", f"M{x+w/2-8:.0f} {y-14} L{x+w/2+8:.0f} {y+12}"]
def book(cx, cy, w=170, h=120):
    return [f"M{cx} {cy-h/2+10:.0f} C{cx-40} {cy-h/2-10:.0f} {cx-w/2:.0f} {cy-h/2:.0f} {cx-w/2:.0f} {cy-h/2:.0f} L{cx-w/2:.0f} {cy+h/2:.0f} C{cx-w/2:.0f} {cy+h/2:.0f} {cx-40} {cy+h/2-12:.0f} {cx} {cy+h/2+6:.0f} C{cx+40} {cy+h/2-12:.0f} {cx+w/2:.0f} {cy+h/2:.0f} {cx+w/2:.0f} {cy+h/2:.0f} L{cx+w/2:.0f} {cy-h/2:.0f} C{cx+w/2:.0f} {cy-h/2:.0f} {cx+40} {cy-h/2-10:.0f} {cx} {cy-h/2+10:.0f} L{cx} {cy+h/2+6:.0f}"]
def scroll(x, y, w, h):
    return [f"M{x} {y} L{x+w} {y} M{x} {y+h} L{x+w} {y+h}",
            f"M{x} {y} C{x-40} {y} {x-40} {y+h} {x} {y+h} M{x+w} {y} C{x+w+40} {y} {x+w+40} {y+h} {x+w} {y+h} M{x+w} {y} C{x+w-30} {y+20} {x+w-30} {y+h-20} {x+w} {y+h}"]
def flask(cx, cy):
    return [f"M{cx-22} {cy-70} L{cx-22} {cy-15} L{cx-70} {cy+60} Q{cx-75} {cy+72} {cx-60} {cy+72} L{cx+60} {cy+72} Q{cx+75} {cy+72} {cx+70} {cy+60} L{cx+22} {cy-15} L{cx+22} {cy-70} M{cx-34} {cy-70} L{cx+34} {cy-70}",
            f"M{cx-50} {cy+35} C{cx-20} {cy+25} {cx+20} {cy+45} {cx+50} {cy+35} M{cx-8} {cy+10} a6 6 0 1 1 0.1 0 M{cx+14} {cy-5} a4 4 0 1 1 0.1 0"]
def bed(x, y, w=420):
    return [f"M{x} {y-120} L{x} {y+40} M{x} {y} L{x+w} {y} L{x+w} {y+40} M{x} {y-40} L{x+w} {y-40}",
            f"M{x+20} {y-44} C{x+20} {y-90} {x+110} {y-90} {x+110} {y-44} M{x+130} {y-46} C{x+200} {y-80} {x+330} {y-80} {x+w-10} {y-46}"]
def phone(cx, cy, s=1.0):
    w, h = 54 * s, 96 * s
    return [f"M{cx-w/2:.0f} {cy-h/2:.0f} L{cx+w/2:.0f} {cy-h/2:.0f} L{cx+w/2:.0f} {cy+h/2:.0f} L{cx-w/2:.0f} {cy+h/2:.0f} Z M{cx-8*s:.0f} {cy+h/2-12*s:.0f} L{cx+8*s:.0f} {cy+h/2-12*s:.0f}"]
def watch(cx, cy, r=70):
    return [ell(cx, cy, r, r) + f" M{cx-36} {cy-r+6} L{cx-30} {cy-r-60} L{cx+30} {cy-r-60} L{cx+36} {cy-r+6} M{cx-36} {cy+r-6} L{cx-30} {cy+r+60} L{cx+30} {cy+r+60} L{cx+36} {cy+r-6}",
            f"M{cx} {cy} L{cx} {cy-44} M{cx} {cy} L{cx+30} {cy+12}"]
def wedge(cx, cy, r, frac):
    a2 = -90 + 360 * frac
    x2, y2 = cx + r * math.cos(math.radians(a2)), cy + r * math.sin(math.radians(a2))
    return f"M{cx} {cy} L{cx} {cy-r} A{r} {r} 0 {1 if frac > .5 else 0} 1 {x2:.1f} {y2:.1f} Z"
def grass(x0, y0, x1, y1, n, avoid=None):
    d = []
    for _ in range(n):
        x = random.uniform(x0, x1); y = random.uniform(y0, y1)
        if avoid and avoid(x, y): continue
        h = random.uniform(14, 30); dx = random.uniform(-6, 6)
        d.append(f"M{x:.0f} {y:.0f} l{dx:.0f} {-h:.0f} M{x+8:.0f} {y:.0f} l{dx+5:.0f} {-h*0.8:.0f}")
    return " ".join(d)
def steps_on(pts, t0, gap, out=None, color=CH):
    """ślady stóp wzdłuż łamanej"""
    res = []
    for i, (x, y) in enumerate(pts):
        side = 14 if i % 2 else -14
        res.append(D(ell(x, y + side, 9, 6), t0 + i * gap, 0.08, color, 6, x=x, out=out, snd="tick" if i % 2 == 0 else None))
    return res
def lerp_pts(p0, p1, n):
    return [(p0[0] + (p1[0] - p0[0]) * i / (n - 1), p0[1] + (p1[1] - p0[1]) * i / (n - 1)) for i in range(n)]
def bucket(cx, cy):
    return [f"M{cx-70} {cy-60} L{cx-50} {cy+80} L{cx+50} {cy+80} L{cx+70} {cy-60} Z M{cx-30} {cy-60} L{cx-20} {cy+80} M{cx+10} {cy-60} L{cx+8} {cy+80} M{cx+45} {cy-60} L{cx+34} {cy+80}",
            f"M{cx-72} {cy-60} C{cx-80} {cy-95} {cx-40} {cy-105} {cx-30} {cy-82} C{cx-25} {cy-115} {cx+15} {cy-115} {cx+12} {cy-85} C{cx+30} {cy-110} {cx+80} {cy-95} {cx+72} {cy-60}"]
def screen(x, y, w, h):
    return [f"M{x} {y} L{x+w} {y} L{x+w} {y+h} L{x} {y+h} Z", f"M{x+30} {y+h+30} L{x+w-30} {y+h+30} M{x+60} {y+h+60} L{x+w-60} {y+h+60}"]
def room(x, y, w, h):
    return [f"M{x} {y} L{x+w} {y} L{x+w} {y+h} L{x} {y+h} Z", f"M{x+w-130} {y+40} L{x+w-40} {y+40} L{x+w-40} {y+120} L{x+w-130} {y+120} Z M{x+w-85} {y+40} L{x+w-85} {y+120}"]
def carton(cx, cy):
    return [f"M{cx-80} {cy-50} L{cx+80} {cy-50} L{cx+80} {cy+60} L{cx-80} {cy+60} Z M{cx-80} {cy-50} L{cx-105} {cy-80} M{cx+80} {cy-50} L{cx+105} {cy-80} M{cx-30} {cy-50} L{cx-30} {cy-5} L{cx+30} {cy-5} L{cx+30} {cy-50}"]
def pencil(cx, cy):
    return [f"M{cx-80} {cy+40} L{cx+50} {cy-60} L{cx+72} {cy-32} L{cx-58} {cy+68} Z M{cx-80} {cy+40} L{cx-92} {cy+82} L{cx-58} {cy+68}"]
def toothbrush(cx, cy):
    return [f"M{cx-120} {cy+10} L{cx+60} {cy-10} M{cx-120} {cy+30} L{cx+60} {cy+10}", f"M{cx+60} {cy-20} L{cx+140} {cy-28} M{cx+70} {cy-20} l0 -26 M{cx+90} {cy-22} l0 -26 M{cx+110} {cy-24} l0 -26 M{cx+130} {cy-26} l0 -26"]
def spark(cx, cy, k=1.0):
    if k != 1.0:
        return re.sub(r"(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)", lambda m: m.group(0), _spark(cx, cy, k))
    return _spark(cx, cy, 1.0)
def _spark(cx, cy, k):
    q = lambda v: round(v * k)
    return f"M{cx-q(60)} {cy-q(70)} L{cx-q(10)} {cy-q(10)} L{cx-q(40)} {cy} L{cx+q(30)} {cy+q(80)} M{cx+q(40)} {cy-q(60)} l{q(26)} {-q(26)} M{cx+q(50)} {cy-q(20)} l{q(36)} {-q(6)} M{cx-q(80)} {cy+q(20)} l{-q(34)} {q(8)}"
def appgrid(x, y, moved=None):
    d = ""
    for r in range(3):
        for c in range(3):
            if (r, c) == moved: continue
            xx, yy = x + c * 58, y + r * 58
            d += f"M{xx} {yy} L{xx+40} {yy} L{xx+40} {yy+40} L{xx} {yy+40} Z "
    return d
def blocks(x, y):
    return f"M{x} {y} L{x+180} {y} L{x+180} {y+86} L{x} {y+86} Z M{x+60} {y} L{x+60} {y-22} L{x+120} {y-22} L{x+120} {y}"

# ─────────── plansze ───────────
def b01():
    tq = A(1, "Arystoteles")
    items = [T("„jesteśmy tym,", 150, 110, A(1, "Jesteśmy") - 0.05, 0.6, size=118, cv=True),
             T("co wielokrotnie robimy.”", 150, 245, A(1, "co wielokrotnie") - 0.05, 0.8, size=118, cv=True),
             T("doskonałość nie jest czynem, lecz nawykiem.", 155, 420, A(1, "Doskonałość") - 0.05, size=54, cls="dim"),
             T("– Arystoteles", 700, 540, tq - 0.05, 0.5, size=96, cls="y", cv=True),
             D("M700 660 C860 650 1000 668 1180 652", tq + 0.5, 0.3, YL, 9, x=950)]
    return dict(items=items, poses=[[0, "hang"], [1.0, "think"], [tq, "heart"]], cam=[[0.2, 1.06, 760, 380, 4.5]],
                fadeIn=0.4, resid_static=False)

def b02():
    tn = A(2, "Arystoteles nigdy"); tp = A(2, "powiedział")
    items = [*icon(mug(300, 360), A(2, "kubkach") - 0.2, 0.3, x=300),
             *icon(poster(520, 240, 260, 250), A(2, "plakatach") - 0.2, 0.3, x=650),
             T("„jesteśmy tym,", 545, 290, A(2, "plakatach") + 0.3, size=34), T("co robimy…”", 545, 340, A(2, "plakatach") + 0.6, size=34),
             *icon(book(1000, 360), A(2, "poradniku") - 0.25, 0.35, x=1000),
             *[T("– Arystoteles", x, 520, t, size=36, cls="dim", cx=True) for x, t in
               [(300, A(2, "kubkach") + 0.7), (650, A(2, "plakatach") + 0.9), (1000, A(2, "poradniku") + 0.3)]],
             T("jest tylko jeden problem:", 150, 640, A(2, "Jest tylko") - 0.05, size=62),
             *[D(f"M{x-110} 548 L{x+110} 538", tn + 0.1 + i * 0.18, 0.18, RED, 8, x=x) for i, x in enumerate([300, 650, 1000])],
             T("nigdy tego nie powiedział.", 150, 750, tn + 0.2, 0.6, size=96, cls="y", cv=True),
             POP("?!", 1250, 700, tp + 0.2, size=120, cls="r")]
    return dict(items=items, poses=[[S(2), "hips"], [A(2, "kubkach"), "pointL"], [A(2, "Jest tylko"), "think"], [tp, "shrug"]],
                shakes=[[tp + 0.25, 6]])

def b03():
    ts = A(3, "Streszczał"); ti = A(3, "A internet"); tc = A(3, "zrobił z tego")
    items = [POP("1926", 150, 80, A(3, "1926") - 0.05, size=170, cls="y"),
             T("Will Durant, pisarz z USA", 560, 120, A(3, "Will Durant") - 0.05, size=62),
             T("„The Story of Philosophy” (historia filozofii)", 565, 215, A(3, "w książce") - 0.05, size=40, cls="dim"),
             *icon(book(330, 430, 220, 150), A(3, "w książce") + 0.2, 0.35, x=330),
             T("streszczenie", 180, 560, ts - 0.05, size=56, cls="dim"),
             D(arrow_r(520, 590, 650), ts + 0.6, 0.25, CH, 8, x=580),
             T("internet", 690, 560, ti - 0.05, size=56),
             D(arrow_r(930, 590, 1060), ti + 0.4, 0.25, CH, 8, x=1000),
             T("„cytat”", 1090, 535, tc - 0.05, 0.5, size=96, cls="y", cv=True),
             D(ell(1235, 590, 155, 72), tc + 0.6, 0.45, YL, 7, x=1170)]
    return dict(items=items, poses=[[S(3), "hips"], [A(3, "Will Durant"), "pointL"], [ts, "think"], [tc, "shrug"]],
                cam=[[ti - 0.2, 1.12, 900, 580, 0.5]])

def b04():
    tn = A(4, "z nawyku"); t5 = A(5, "Ponad dwa"); tr = A(5, "miał rację")
    items = [T("najciekawsze:", 150, 80, A(4, "Ale najciekawsze") - 0.05, size=96, cv=True),
             *icon(scroll(230, 220, 520, 230), A(4, "Arystoteles naprawdę") - 0.2, 0.35, x=480),
             T("cnota rodzi się z", 260, 250, A(4, "że cnota") - 0.05, size=52),
             POP("NAWYKU", 280, 320, tn - 0.05, size=118, cls="y"),
             T("Etyka nikomachejska, ks. II", 250, 470, A(4, "Arystoteles naprawdę") + 0.6, size=36, cls="dim"),
             T("odważny?", 880, 250, A(4, "Że stajemy się") - 0.05, size=72, cv=True),
             T("→ rób odważne rzeczy", 880, 340, A(4, "robiąc odważne") - 0.05, size=50, cls="y"),
             D("M200 680 L1250 680", t5 - 0.2, 0.5, x=720),
             D("M240 655 L240 705", t5 + 0.1, 0.15, CH, 8, x=240), T("Arystoteles", 240, 715, t5 + 0.15, size=40, cx=True),
             T("+ ponad 2000 lat", 560, 610, A(5, "dwa tysiące") - 0.05, size=48, cls="dim"),
             D(arrow_r(500, 680, 1250), A(5, "naukowcy zaczęli") - 0.2, 0.5, YL, 9, x=900),
             *icon(flask(1170, 560), A(5, "naukowcy zaczęli") + 0.1, 0.3, x=1170),
             T("dziś: laboratorium", 1100, 715, A(5, "sprawdzać") - 0.05, size=40, cx=True),
             POP("miał rację.", 150, 790, tr - 0.05, size=96, cls="y"),
             T("bardziej, niż myślisz", 650, 820, A(5, "bardziej") - 0.05, size=48, cls="dim")]
    return dict(items=items, poses=[[S(4), "hips"], [A(4, "Arystoteles naprawdę"), "pointL"], [t5, "think"], [A(5, "naukowcy"), "pointLlow"], [tr + 0.1, "wow"]],
                jumps=[tr + 0.1])

def b05():
    t0 = S(6)
    items = [T("dziś:", 150, 110, t0 - 0.05, size=60, cls="dim"),
             T("dlaczego zawsze wracasz", 150, 200, A(6, "dlaczego zawsze") - 0.05, 0.7, size=124, cv=True),
             T("do starych nawyków?", 150, 340, A(6, "do starych") - 0.05, 0.6, size=124, cls="y", cv=True),
             D("M300 830 L760 830 C900 830 900 640 760 640 L520 640 M570 610 L520 640 L570 670", A(6, "Nawet wtedy") - 0.1, 1.0, YL, 10, x=600),
             *steps_on(lerp_pts((320, 830), (740, 830), 7), A(6, "Nawet wtedy") + 0.2, 0.09),
             *steps_on(lerp_pts((740, 640), (560, 640), 4), A(6, "naprawdę") + 0.1, 0.1),
             T("nawet kiedy naprawdę postanowisz inaczej.", 155, 515, A(6, "Nawet wtedy") - 0.05, size=52, cls="dim")]
    return dict(items=items, poses=[[t0, "hips"], [A(6, "dlaczego"), "wave"], [A(6, "Nawet wtedy"), "shrug"]],
                cam=[[t0, 1.05, 700, 400, 2.5]])

def b06():
    o7 = S(8) - 0.1; tb = A(7, "Wieczorem"); tt = A(7, "telefon już")
    items = [T("„koniec z telefonem w łóżku.”", 150, 90, A(7, "Postanawiasz") - 0.05, size=68, out=o7),
             *icon(bed(200, 560), tb - 0.1, 0.4, x=400, out=o7),
             T("22:47", 760, 330, tb + 0.2, size=76, cls="dim", out=o7),
             *icon(phone(560, 430, 1.3), tt - 0.05, 0.3, YL, x=560, out=o7),
             POP("!", 620, 300, tt + 0.4, size=110, cls="y", out=o7),
             BUB("…kiedy?", 860, 470, A(7, "Nawet nie wiesz") - 0.05, out=o7),
             T("słaba wola", 150, 150, A(8, "słabą wolę") - 0.05, 0.5, size=140, cv=True),
             D("M140 250 L700 230", A(8, "To znaczy, że ten") - 0.1, 0.25, RED, 10, x=420),
             T("decyzja?", 150, 360, A(8, "nie był decyzją") - 0.05, size=90, cls="dim", cv=True),
             D("M140 420 L470 410", A(8, "Był nawykiem") - 0.3, 0.2, RED, 8, x=300),
             POP("NAWYK.", 150, 520, A(8, "Był nawykiem") - 0.05, size=200, cls="y")]
    return dict(items=items, poses=[[S(7), "hips"], [A(7, "Postanawiasz"), "idea"], [tb, "hang"], [tt + 0.2, "facepalm"], [S(8), "hips"],
                                    [A(8, "słabą wolę"), "shrug"], [A(8, "Był nawykiem"), "pointL"]],
                shakes=[[A(8, "Był nawykiem") + 0.05, 7]])

def b07():
    o9 = S(10) - 0.1; tb = A(9, "piszczały"); t43 = A(10, "czterdziestu")
    items = [T("Wendy Wood i zespół", 150, 80, A(9, "Psycholożka") - 0.05, size=88, cv=True, out=o9),
             T("Wood, Quinn, Kashy, 2002", 155, 190, A(9, "z zespołem") - 0.05, size=40, cls="dim", out=o9),
             *icon(watch(330, 480), A(9, "zegarki") - 0.3, 0.3, x=330, out=o9),
             *[POP("bip!", 440 + i * 30, 290 + i * 40, tb + i * 0.45, size=62, cls="y", thud=0.4, out=o9) for i in range(3)],
             T("co godzinę", 230, 690, A(9, "co godzinę") - 0.05, size=48, cls="dim", out=o9),
             BOX(650, 330, 640, 330, A(9, "Na sygnał") - 0.1, 0.5, out=o9),
             T("co teraz robię?", 690, 370, A(9, "co się właśnie robi") - 0.05, size=54, out=o9),
             T("o czym myślę?", 690, 470, A(9, "o czym się myśli") - 0.05, size=54, out=o9),
             D("M690 590 L1240 590", A(9, "o czym się myśli") + 0.6, 0.3, CH, 5, x=960, out=o9),
             T("wynik?", 150, 90, A(10, "Wynik") - 0.05, size=90, cv=True),
             CNT(150, 220, 43, t43 - 0.05, 0.9, size=220, pre="~"),
             D(ell(1080, 470, 180, 180), A(10, "codziennych") - 0.4, 0.5, CH, 8, x=1080),
             D(wedge(1080, 470, 180, 0.43), A(10, "to były nawyki") - 0.2, 0.5, YL, 10, x=1080),
             T("nawyk", 1270, 290, A(10, "to były nawyki") + 0.3, size=52, cls="y"),
             T("codziennych zachowań to nawyki", 150, 520, A(10, "codziennych") - 0.05, size=48),
             T("robione automatycznie,", 150, 620, A(10, "automatycznie") - 0.05, size=48, cls="dim"),
             T("myśli gdzie indziej", 150, 700, A(10, "myśląc") - 0.05, size=48, cls="dim")]
    return dict(items=items, poses=[[S(9), "hips"], [A(9, "zegarki"), "pointL"], [tb + 0.2, "wow"], [A(9, "Na sygnał"), "pointLlow"], [S(10), "hips"],
                                    [t43 + 0.4, "wow"], [A(10, "Ludzie robili"), "think"]],
                shakes=[[t43 + 0.95, 6]])

def b08():
    o11 = S(12) - 0.1; tw = A(12, "Im więcej")
    ARR = "M520 420 C600 410 680 430 780 420"
    items = [T("pół dnia na autopilocie", 150, 80, A(11, "Prawie połowa") - 0.05, size=100, cv=True, out=o11),
             BOX(200, 300, 380, 180, A(11, "I ten autopilot") - 0.1, 0.5, out=o11,
                 inner='<div class="cv" style="position:absolute;inset:0;text-align:center;font-size:110px;line-height:170px">AUTO</div>'),
             BUB("postanowienie!", 720, 270, A(11, "nie słucha") - 0.4, out=A(11, "nie słucha") + 0.8),
             D("M720 330 C680 340 640 360 600 390", A(11, "postanowień") - 0.1, 0.25, RED, 7, x=650, out=o11),
             T("słucha otoczenia.", 700, 450, A(11, "Słucha otoczenia") - 0.05, 0.6, size=80, cls="y", cv=True, out=o11),
             T("nawyk =", 150, 80, A(12, "Nawyk to") - 0.05, size=96, cv=True),
             T("miejsce", 170, 260, A(12, "miejsce") - 0.05, size=62),
             T("pora", 170, 350, A(12, "pora") - 0.05, size=62),
             T("sytuacja", 170, 440, A(12, "sytuacja") - 0.05, size=62),
             D("M450 270 C490 280 480 380 500 420 C480 460 490 560 450 570", A(12, "sytuacja") + 0.3, 0.35, CH, 6, x=470),
             D(ARR, A(12, "i ruch") - 0.1, 0.35, CH, 4, x=650),
             D("M760 395 L790 420 L760 445", A(12, "i ruch") + 0.2, 0.15, CH, 6, x=780),
             POP("RUCH", 830, 360, A(12, "ruch, który") - 0.05, size=110, cls="y"),
             T("łóżko · wieczór · telefon", 170, 640, A(12, "Łóżko") - 0.05, 1.2, size=60, cls="y"),
             T("× powtórzenia", 540, 470, tw - 0.05, size=40, cls="dim"),
             *[D(ARR, tw + 0.3 + i * 0.45, 0.3, YL if i == 3 else CH, w, x=650) for i, w in enumerate([8, 13, 19, 26])],
             T("otoczenie samo odpala ruch", 170, 760, A(12, "otoczenie samo") - 0.05, size=58)]
    return dict(items=items, poses=[[S(11), "hips"], [A(11, "I ten autopilot"), "pointL"], [A(11, "Słucha"), "idea"], [S(12), "hips"],
                                    [A(12, "miejsce"), "pointLlow"], [tw, "think"], [A(12, "otoczenie samo"), "wow"]],
                cam=[[tw + 0.2, 1.15, 660, 420, 0.5], [A(12, "otoczenie samo") - 0.2, 1.0, 960, 540, 0.5]])

def b09():
    tg = A(13, "trawnik"); t1 = A(13, "Pierwszy raz"); tc = A(13, "codziennie"); tm = A(13, "Po miesiącu"); tn = A(13, "I nogi")
    PATH = "M180 520 C420 560 600 700 860 740 C1060 770 1250 810 1420 845"
    pts = [(240, 540), (380, 575), (520, 640), (660, 690), (800, 725), (940, 750), (1080, 775), (1220, 800)]
    items = [T("wyobraź sobie trawnik.", 150, 80, A(13, "Wyobraź") - 0.05, size=100, cv=True),
             D(grass(150, 420, 1350, 880, 230), tg - 0.1, 1.4, CH, 5, x=700),
             *steps_on(pts, t1 + 0.1, 0.12, out=A(13, "trawa zaraz") + 0.4),
             T("trawa się podnosi", 900, 230, A(13, "trawa zaraz") - 0.05, size=46, cls="dim", out=tc - 0.1),
             CNT(900, 200, 30, tc - 0.05, 1.6, size=90, pre="dzień ", suf=""),
             D(PATH, tm - 0.3, 1.0, GR, 70, x=800, snd="rub"),
             D(PATH, tm + 0.2, 1.0, CH, 3, x=800),
             T("po miesiącu: ścieżka.", 150, 220, tm - 0.05, size=66, cls="y"),
             *steps_on(pts, tn + 0.1, 0.08, color=YL)]
    return dict(items=items, poses=[[S(13), "hips"], [tg, "pointLlow"], [tc, "think"], [tm + 0.3, "wow"], [tn, "hips"]],
                moves=[[tn + 0.1, tn + 1.4, MX, 1150], [tn + 1.5, E(13) + 0.2, 1150, MX]], cam=[[tm - 0.2, 1.08, 800, 640, 0.8]])

def b10():
    t1 = A(14, "Część dostała świeży"); t2 = A(14, "Część tygodniowy")
    items = [T("eksperyment w kinie", 150, 80, A(14, "w kinie") - 0.6, size=104, cv=True),
             T("Uniwersytet Południowej Kalifornii · Neal i in., 2011", 155, 205, A(14, "Naukowcy") + 0.4, size=38, cls="dim"),
             *icon(screen(780, 300, 500, 200), A(14, "w kinie") - 0.2, 0.35, x=1000),
             T("kino", 1030, 350, A(14, "w kinie") + 0.5, size=72, cv=True, cx=True),
             T("popcorn dla widzów", 190, 330, A(14, "Widzom") - 0.05, size=54),
             *icon(bucket(330, 560), A(14, "popcorn") - 0.1, 0.3, x=330),
             T("świeży", 330, 680, t1 + 0.2, size=60, cls="y", cx=True),
             *icon(bucket(650, 560), t2 - 0.1, 0.3, x=650),
             T("7 dni", 650, 680, t2 + 0.2, size=60, cls="r", cx=True),
             T("gumowaty, zimny", 650, 760, A(14, "gumowaty") - 0.05, size=42, cls="dim", cx=True),
             D("M600 470 l-10 -18 M640 465 l6 -20 M690 472 l14 -14", A(14, "zimny"), 0.3, RED, 6, x=650)]
    return dict(items=items, poses=[[S(14), "hips"], [A(14, "w kinie"), "pointL"], [t1, "pointLlow"], [A(14, "gumowaty"), "facepalm"]])

def b11():
    tr = A(15, "Ludzie, którzy rzadko"); ts = A(15, "starego zjedli"); tz = A(15, "Ale ci"); tt = A(15, "Zjedli tyle")
    items = [T("ile zjedli?", 150, 70, S(15) + 0.05, size=96, cv=True),
             T("świeży", 820, 95, S(15) + 0.4, size=44), T("stary", 1010, 95, S(15) + 0.6, size=44, cls="y"),
             D("M180 820 L1260 820", tr - 0.2, 0.4, x=700),
             BAR(230, 820, 150, 380, tr + 0.1, 0.5), BAR(400, 820, 150, 150, ts - 0.05, 0.5, yellow=True),
             T("rzadko jedzą w kinie", 390, 840, tr + 0.3, size=40, cx=True),
             T("dużo mniej", 400, 600, A(15, "dużo mniej") - 0.05, size=46, cls="y"),
             T("normalne.", 230, 330, A(15, "Normalne") - 0.05, size=56, cls="dim"),
             BAR(760, 820, 150, 380, tz + 0.1, 0.5), BAR(930, 820, 150, 375, tt - 0.05, 0.5, yellow=True),
             T("zawsze jedzą w kinie", 920, 840, tz + 0.3, size=40, cx=True),
             POP("tyle samo!", 760, 270, tt + 0.3, size=100, cls="y"),
             T("rysunek poglądowy", 1060, 900, tr + 0.5, size=30, cls="dim")]
    return dict(items=items, poses=[[S(15), "hips"], [tr, "pointLlow"], [A(15, "Normalne"), "shrug"], [tz, "pointL"], [tt + 0.3, "wow"]],
                jumps=[tt + 0.35], cam=[[tz - 0.1, 1.1, 860, 560, 0.5]])

def b12():
    tsl = A(16, "w zwykłej sali"); tk = A(16, "Siedział w kinie")
    items = [T("i tu haczyk.", 150, 70, A(16, "I tu haczyk") - 0.05, size=110, cv=True),
             *icon(screen(180, 250, 420, 180), S(16) + 0.6, 0.3, x=390),
             T("KINO", 390, 300, S(16) + 1.2, size=70, cx=True, cv=True),
             *icon(room(760, 230, 500, 270), tsl - 0.2, 0.3, x=1010),
             T("zwykła sala", 920, 330, tsl + 0.3, size=50, cx=True),
             T("nawyk znika", 1010, 540, A(16, "nawyk znikał") - 0.05, size=56, cls="y", cx=True),
             *icon(bucket(1010, 700), A(16, "Stary popcorn") - 0.2, 0.3, x=1010),
             T("stary zostaje w kubełku", 1010, 800, A(16, "zostawał") - 0.05, size=40, cls="dim", cx=True),
             T("nie w popcornie.", 180, 560, A(16, "Bo nawyk") - 0.05, size=64, cls="dim"),
             T("w KINIE.", 180, 650, tk - 0.05, 0.4, size=130, cls="y", cv=True),
             D(ell(390, 340, 260, 150), tk + 0.4, 0.5, YL, 8, x=390)]
    return dict(items=items, poses=[[S(16), "hips"], [A(16, "I tu haczyk"), "idea"], [tsl, "pointL"], [A(16, "nawyk znikał"), "wow"], [tk, "pointLlow"]],
                shakes=[[tk + 0.4, 6]])

def b13():
    t3 = A(17, "trzy sposoby")
    labels = ["nowe miejsce", "doklej", "zepsuj autopilota"]
    items = [T("pracuj z otoczeniem,", 150, 80, A(17, "z otoczeniem") - 0.05, 0.6, size=104, cv=True),
             T("a nie walcz ze sobą.", 155, 220, A(17, "a nie z sobą") - 0.05, size=64, cls="dim"),
             D("M150 300 L560 290", A(17, "walczyć") + 0.1, 0.2, YL, 6, x=350)]
    for i, lab in enumerate(labels):
        x = 150 + i * 400; t = t3 - 0.3 + i * 0.25
        items += [BOX(x, 420, 340, 300, t - 0.1, 0.4, yellow=(i == 0)), POP(["I.", "II.", "III."][i], x + 30, 430, t + 0.1, size=100),
                  T(lab, x + 170, 662, t + 0.3, size=36, cx=True, cls="y" if i == 0 else "")]
    items += [D(carton(380, 560)[0], t3 + 0.2, 0.3, CH, 6, x=380),
              D(blocks(695, 560), t3 + 0.4, 0.3, CH, 6, x=760),
              D(spark(1200, 550, 0.8), t3 + 0.6, 0.3, YL, 7, x=1160)]
    return dict(items=items, poses=[[S(17), "hips"], [A(17, "z otoczeniem"), "idea"], [t3, "pointL"]])

def b14():
    o18 = A(19, "osiemset") - 0.35
    ic = [(300, A(18, "Przeprowadzka"), carton, "przeprowadzka"), (580, A(18, "nowa praca"), suitcase, "nowa praca"),
          (860, A(18, "nowa szkoła"), pencil, "nowa szkoła"), (1140, A(18, "wyjazd"), plane, "wyjazd")]
    items = [POP("I.", 150, 80, A(18, "Sposób pierwszy") - 0.05, size=120),
             T("zmieniaj nawyki, gdy zmienia się otoczenie", 290, 105, A(18, "zmieniaj") - 0.05, size=52, cls="y")]
    for x, t, fn, lab in ic:
        items += [*icon(fn(x, 420), t - 0.25, 0.25, x=x, out=o18), T(lab, x, 520, t + 0.05, size=40, cx=True, out=o18)]
    items += [POP("800 osób", 150, 250, A(19, "osiemset") - 0.05, size=150, cls="y"),
              T("Verplanken i Roy, Uniwersytet w Bath, 2016", 160, 430, A(19, "osiemset") + 0.6, size=38, cls="dim"),
              T("ta sama zachęta do eko-nawyków", 150, 500, A(19, "Ta sama") - 0.05, size=52),
              T("działała lepiej po przeprowadzce", 150, 580, A(19, "niedawno") - 0.05, size=52, cls="y")]
    to = A(19, "Okno trwało")
    for i in range(12):
        x = 150 + i * 92
        items.append(CELL(x, 720, to - 0.3 + i * 0.03))
        if i < 3: items.append(D(check(x + 12, 754, 1.0), to + 0.3 + i * 0.15, 0.12, YL, 7, x=x, snd="tick"))
    items += [T("~3 miesiące", 150, 800, to + 0.6, size=50, cls="y"), T("(okno zmiany)", 450, 808, to + 0.9, size=40, cls="dim")]
    return dict(items=items, poses=[[S(18), "hips"], [A(18, "Przeprowadzka"), "pointL"], [S(19), "hips"], [A(19, "osiemset"), "wow"],
                                    [A(19, "Ta sama"), "think"], [to, "pointLlow"]])

def b15():
    tz = A(20, "Zadanie"); tp = A(20, "połóż telefon")
    items = [T("nowe miejsce = trawnik bez ścieżek", 150, 80, S(20) - 0.05, 0.9, size=64),
             D(grass(170, 230, 1300, 400, 110), S(20) + 0.6, 1.0, CH, 5, x=700),
             T("zadanie na dziś:", 150, 440, tz - 0.05, size=84, cls="y", cv=True),
             T("coś się zmienia? → wstaw tam 1 nawyk", 150, 545, A(20, "jeśli coś") - 0.05, size=50),
             T("nic się nie zmienia? → zmień coś małego", 150, 625, A(20, "A jeśli nic") - 0.05, size=50),
             *icon(room(170, 720, 480, 150), tp - 0.6, 0.25, x=400),
             *icon(room(700, 720, 480, 150), tp - 0.3, 0.25, x=940),
             T("sypialnia", 200, 790, tp - 0.2, size=40, cls="dim"), T("inny pokój", 730, 790, tp, size=40, cls="dim"),
             D("M560 850 C610 815 660 815 720 850", tp + 0.4, 0.3, YL, 7, x=600),
             *icon(phone(985, 800, 0.9), tp + 0.7, 0.25, YL, x=900)]
    return dict(items=items, poses=[[S(20), "hips"], [tz, "idea"], [A(20, "A jeśli nic"), "think"], [tp, "pointLlow"]])

def b16():
    to = A(21, "od zera"); td = A(21, "Doklej")
    items = [POP("II.", 150, 80, A(21, "Sposób drugi") - 0.05, size=120),
             T("doklej nowy nawyk do starego", 300, 105, td - 0.05, size=60, cls="y"),
             T("od zera", 980, 250, to - 0.1, size=60, cls="dim"), D("M970 300 L1200 290", to + 0.3, 0.2, RED, 8, x=1080),
             BOX(180, 230, 300, 120, td + 0.3, 0.4, inner='<div style="text-align:center;font-size:48px;line-height:105px">stary</div>'),
             BOX(500, 230, 300, 120, A(21, "już działa") - 0.2, 0.4, yellow=True, inner='<div class="y" style="text-align:center;font-size:48px;line-height:105px">+ nowy</div>'),
             T("badanie: nitkowanie zębów", 150, 430, A(22, "W jednym") - 0.05, size=56),
             *icon(toothbrush(1080, 470), A(22, "nitkować") - 0.2, 0.3, x=1080),
             T("nitka → mycie", 170, 540, A(22, "Połowa przed") - 0.05, size=54, cls="dim"),
             T("mycie → nitka", 170, 640, A(22, "połowa po") - 0.05, size=54, cls="y"),
             D(check(560, 680, 1.4), A(22, "silniejszy") - 0.1, 0.3, YL, 9, x=560),
             T("silniejszy nawyk", 640, 650, A(22, "silniejszy") + 0.1, size=44, cls="y"),
             POP("8 miesięcy", 170, 740, A(22, "po ośmiu") - 0.05, size=96, cls="y"),
             T("…i dalej częściej", 640, 770, A(22, "robili to") - 0.05, size=44),
             T("Judah, Gardner, Aunger, 2013", 640, 830, A(22, "po ośmiu") + 0.5, size=34, cls="dim")]
    return dict(items=items, poses=[[S(21), "hips"], [to, "shrug"], [td, "idea"], [S(22), "hips"], [A(22, "Połowa"), "pointLlow"], [A(22, "po ośmiu"), "wow"]])

def b17():
    tn = A(23, "Nitka"); tz = A(23, "Zadanie"); tk = A(23, "po tym, jak zrobię")
    OLD = "M150 780 C350 760 520 700 760 690"; NEW = "M760 690 C930 682 1080 640 1300 610"
    items = [D(grass(150, 560, 1320, 880, 130, avoid=lambda x, y: abs(y - (780 - (x - 150) * 0.15)) < 45 or (x < 640 and y > 812) or (980 < x < 1200 and 530 < y < 630)), S(23) - 0.05, 0.8, CH, 4, x=700),
             D(OLD, S(23) + 0.3, 0.8, GR, 60, x=450, snd="rub"),
             T("mycie zębów", 260, 830, S(23) + 0.6, size=44, cls="dim"),
             D(NEW, tn + 0.2, 0.9, GY, 60, x=1030, snd="rub"),
             T("+ nitka", 1000, 560, tn + 0.5, size=56, cls="y"),
             *steps_on(lerp_pts((200, 775), (1250, 615), 12), tn + 0.4, 0.12, color=YL),
             T("zadanie: dokończ zdanie", 150, 80, tz - 0.05, size=60, cls="dim"),
             T("„po tym, jak…”", 150, 160, A(23, "dokończ") + 0.4, 0.6, size=110, cls="y", cv=True),
             T("po tym, jak zrobię kawę,", 150, 330, tk - 0.05, size=58),
             T("przeczytam jedną stronę.", 150, 410, A(23, "przeczytam") - 0.05, size=58, cls="y")]
    return dict(items=items, poses=[[S(23), "hips"], [S(23) + 0.3, "pointLlow"], [tz, "idea"], [tk, "pointL"]])

def b18():
    ta = A(24, "rozbroić"); tr = A(25, "drugą ręką"); tn = A(25, "I nagle")
    items = [POP("III.", 150, 80, A(24, "Sposób trzeci") - 0.05, size=120),
             T("zrób to inaczej niż zwykle", 340, 105, A(24, "zrób go") - 0.05, size=62, cls="y"),
             BOX(180, 250, 320, 150, ta - 0.4, 0.4, inner='<div class="cv" style="text-align:center;font-size:92px;line-height:140px">AUTO</div>'),
             D(spark(560, 320), ta + 0.1, 0.3, YL, 8, x=560),
             T("pamiętasz kino?", 690, 260, A(25, "Pamiętasz") - 0.05, size=58, cls="dim"),
             *icon(bucket(1250, 420), A(25, "Pamiętasz") + 0.3, 0.3, x=1160),
             T("jedz drugą ręką", 150, 470, tr - 0.5, 0.6, size=96, cv=True),
             T("praworęczni → lewą", 160, 580, A(25, "Praworęczni") - 0.05, size=50, cls="dim"),
             BUB("ej, ten popcorn jest stary!", 620, 640, tn + 0.1),
             T("zjedli dużo mniej", 160, 770, A(25, "Zjedli go") - 0.05, size=56, cls="y"),
             T("nawet ci z najmocniejszym nawykiem", 650, 780, A(25, "Nawet ci") - 0.05, size=40, cls="dim")]
    return dict(items=items, poses=[[S(24), "hips"], [ta, "idea"], [S(25), "hips"], [tr, "give"], [tn, "wow"], [A(25, "Zjedli go"), "pointLlow"]],
                shakes=[[ta + 0.3, 6]], jumps=[tn + 0.15])

def b19():
    tz = A(26, "Zadanie"); tt = A(26, "Telefon do"); ta = A(26, "aplikacja")
    items = [T("inna ręka.", 150, 70, A(26, "Inna ręka") - 0.05, 0.4, size=92, cv=True),
             T("inne miejsce.", 150, 170, A(26, "inne miejsce") - 0.05, 0.4, size=92, cv=True),
             T("inna kolejność.", 150, 270, A(26, "inna kolejność") - 0.05, 0.4, size=92, cls="y", cv=True),
             BUB("autopilot: ???", 780, 120, A(26, "Autopilot") - 0.05),
             T("a ty odzyskujesz wybór", 780, 250, A(26, "a ty") - 0.05, size=50, cls="y"),
             T("zadanie: zmień 1 szczegół", 150, 420, tz - 0.05, 0.6, size=84, cls="y", cv=True),
             *icon(phone(260, 660, 1.4), tt - 0.1, 0.25, x=260),
             T("prawa", 260, 760, tt + 0.2, size=40, cls="dim", cx=True),
             D(arrow_r(340, 660, 500), tt + 0.4, 0.25, YL, 8, x=420),
             *icon(phone(580, 660, 1.4), tt + 0.6, 0.25, YL, x=580),
             T("lewa", 580, 760, tt + 0.8, size=40, cls="y", cx=True),
             D(appgrid(800, 600, moved=(0, 0)), ta - 0.2, 0.7, CH, 5, x=860),
             D("M800 600 L840 600 L840 640 L800 640 Z", ta + 0.6, 0.2, YL, 6, x=820, out=ta + 1.2),
             D(arrow_r(850, 620, 990), ta + 0.8, 0.25, YL, 6, x=930),
             D("M1010 690 L1050 690 L1050 730 L1010 730 Z", ta + 1.1, 0.2, YL, 6, x=1030),
             T("aplikacja gdzie indziej", 800, 790, ta + 0.4, size=40, cls="dim")]
    return dict(items=items, poses=[[S(26), "hips"], [A(26, "Inna ręka"), "pointL"], [A(26, "Autopilot"), "shrug"], [tz, "idea"], [tt, "pointLlow"]])

def b20():
    t27, tp = S(27), A(27, "Pewnego dnia"); t28 = S(28); tw = A(28, "Trawa wysoka"); tdz = A(28, "Dzień po dniu")
    t29 = S(29); tst = A(29, "Stara powoli"); tg = A(29, "w gorsze dni")
    OLD = "M150 640 C450 660 800 760 1150 820 C1280 842 1380 852 1460 856"
    NEW = "M1000 790 C900 700 760 560 560 470 C420 410 280 380 150 370"
    clump = "".join(f"M{x} {y} l-8 -46 M{x+10} {y} l2 -54 M{x+20} {y} l12 -44 " for x, y in [(900, 700), (830, 630), (760, 560), (680, 520), (600, 480)])
    items = [FADE("vig", t27 - 0.2, 0.8),
             T("krótka historia", 150, 70, t27 + 0.05, size=84, cv=True, out=tp - 0.2),
             D(grass(150, 330, 1350, 880, 260), t27 + 0.2, 1.4, CH, 4, x=700),
             D(OLD, t27 + 0.5, 1.1, GR, 64, x=700, snd="rub"),
             D(OLD, t27 + 0.9, 1.0, CH, 3, x=700),
             T("inaczej?", 150, 70, tp + 0.4, 0.4, size=96, cls="y", cv=True, out=t28 - 0.1),
             D("M1000 790 C960 750 920 720 880 690", tp + 0.6, 0.4, YL, 7, x=950),
             D(clump, tw - 0.1, 0.6, YL, 6, x=760),
             T("trawa wysoka", 150, 70, tw - 0.05, size=70, out=tdz - 0.1),
             CNT(150, 60, 30, tdz - 0.05, 1.4, size=96, pre="dzień ", suf="", out=t29 - 0.1),
             slow(D(OLD, t29 + 0.2, 0.01, GR, 64, x=700, snd=None, out=tst - 0.1), 2.5),
             D(OLD, tst + 0.2, 1.2, "rgba(237,235,228,.08)", 64, x=700, snd=None),
             D(NEW, t29 + 0.1, 1.2, GY, 64, x=600, snd="rub"),
             T("dwie ścieżki.", 150, 70, t29 + 0.05, size=84, cv=True),
             T("stara zarasta…", 150, 175, tst - 0.05, size=56, cls="dim"),
             T("ale nie znika do końca.", 520, 175, A(29, "Ale nie znika") - 0.05, size=56),
             D(ell(1150, 815, 140, 50), tg - 0.1, 0.5, RED, 6, x=1150)]
    return dict(items=items, poses=[[t27, "hips"], [tp, "think"], [tp + 0.6, "pointLlow"], [t28 + 0.1, "hips"], [tw + 0.5, "facepalm"], [tdz - 0.2, "hips"],
                                    [t29 + 0.4, "wow"], [tst, "hips"], [tg, "pointLlow"]],
                moves=[[t27 + 0.6, t27 + 2.6, MX, 1150], [t27 + 2.7, tp - 0.2, 1150, MX], [t28 + 0.2, tw - 0.2, MX, 1250], [tw + 0.9, tdz - 0.3, 1250, 1040],
                       [tdz, E(28) + 0.2, 1040, MX]],
                jumps=[t29 + 0.5])

def b21():
    tw = A(30, "Wystarczy")
    items = [T("ukryta lekcja:", 150, 80, A(30, "Ukryta lekcja") - 0.05, size=80, cls="y", cv=True),
             T("nie wracasz, bo jesteś słaby.", 150, 190, A(30, "nie wracasz") - 0.05, 0.9, size=90, cv=True),
             T("wracasz, bo tamta ścieżka", 150, 320, A(30, "Wracasz, bo") - 0.05, 0.8, size=90, cv=True),
             T("wciąż tam jest.", 150, 430, A(30, "wciąż tam") - 0.05, 0.5, size=90, cv=True),
             T("nie musisz jej zasypywać.", 150, 580, A(30, "Nie musisz") - 0.05, size=62, cls="dim"),
             T("codziennie wydepcz nową.", 150, 680, tw - 0.05, 0.9, size=112, cls="y", cv=True),
             *steps_on(lerp_pts((200, 860), (1100, 830), 9), tw + 1.0, 0.12, color=YL)]
    return dict(items=items, poses=[[S(30), "hips"], [A(30, "Wracasz, bo"), "think"], [tw, "heart"]], cam=[[S(30), 1.05, 760, 460, 4.0]])

def b22():
    tn = A(31, "nie napisał"); tnx = A(31, "A w następnym")
    items = [BOX(150, 80, 1150, 170, S(31) - 0.1, 0.5, inner='<div class="cv" style="position:absolute;left:36px;top:30px;font-size:84px">„jesteśmy tym, co wielokrotnie robimy.”</div>'),
             T("– Arystoteles", 450, 280, S(31) + 0.1, size=54, cls="dim"),
             D("M440 320 L760 312", tn - 0.05, 0.25, RED, 8, x=600),
             T("– Will Durant (o Arystotelesie)", 450, 355, tn + 0.4, size=52, cls="y"),
             T("ale miał rację:", 150, 470, A(31, "Ale miał") - 0.05, size=56, cls="dim"),
             T("stajesz się tym, co powtarzasz.", 150, 540, A(31, "stajesz się") - 0.05, 0.9, size=84, cv=True),
             T("w następnym odcinku:", 150, 690, tnx - 0.05, size=48, cls="dim"),
             T("dlaczego innym dajesz świetne rady,", 150, 755, A(31, "dlaczego innym") - 0.05, size=54, cls="y"),
             T("a sobie żadnych?", 150, 830, A(31, "a sobie") - 0.05, size=54, cls="y"),
             POP("?", 640, 800, A(31, "żadnych") + 0.4, size=100, cls="r")]
    return dict(items=items, poses=[[S(31), "hips"], [tn, "shrug"], [A(31, "stajesz się"), "heart"], [tnx, "pointLlow"], [A(31, "a sobie"), "think"]])

BUILD = [("b01", 1, b01), ("b02", 2, b02), ("b03", 3, b03), ("b04", 5, b04), ("b05", 6, b05), ("b06", 8, b06), ("b07", 10, b07),
         ("b08", 12, b08), ("b09", 13, b09), ("b10", 14, b10), ("b11", 15, b11), ("b12", 16, b12), ("b13", 17, b13), ("b14", 19, b14),
         ("b15", 20, b15), ("b16", 22, b16), ("b17", 23, b17), ("b18", 25, b18), ("b19", 26, b19), ("b20", 29, b20), ("b21", 30, b21),
         ("b22", 31, b22)]

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
                [T("ukryta lekcja", 150, 140, start + 0.3, size=130, cls="y", cv=True), T("do zobaczenia w następnym odcinku.", 155, 300, start + 1.0, size=56, cls="dim"),
                 *steps_on(lerp_pts((200, 520), (1000, 480), 8), start + 1.8, 0.15, color=YL)],
                poses=[[start, "hips"], [start + 0.6, "wave"], [start + 4.5, "hips"]], fadeOut=1.2)
    boards.append(out)
    return boards

if __name__ == "__main__":
    for b in build():
        print(f"{b.name:6s} {b.start:7.2f} → {b.end:7.2f} ({b.end - b.start:5.2f}s) erase {b.erase}")
