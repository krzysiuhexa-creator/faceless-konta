"""3 Shortsy (1080x1920) z odcinka 1. python3 shorts.py stills | render s1 s2 s3 | final"""
import sys, os, re, json, asyncio, subprocess, wave
import numpy as np
import engine as EN
# ── pionowa wersja silnika ──
W, H = 1080, 1920
EN.W, EN.H, EN.MX, EN.GROUND = W, H, 540, 1560
EN.CSS = (EN.CSS.replace(".b{width:1920px;height:1080px", f".b{{width:{W}px;height:{H}px")
          .replace("#cam{position:absolute;left:0;top:0;width:1920px;height:1080px", f"#cam{{position:absolute;left:0;top:0;width:{W}px;height:{H}px")
          .replace("svg.lay{position:absolute;left:0;top:0;width:1920px;height:1080px", f"svg.lay{{position:absolute;left:0;top:0;width:{W}px;height:{H}px")
          .replace(".brand{position:absolute;right:70px;bottom:46px", ".brand{position:absolute;left:70px;top:70px")
          .replace("radial-gradient(1200px 700px at 50% 45%", "radial-gradient(900px 1300px at 50% 42%"))
EN.JS = (EN.JS.replace("let s=1,cx=960,cy=540;", f"let s=1,cx={W//2},cy={H//2};")
         .replace("let tx=960-cx*s, ty=540-cy*s; tx=Math.min(0,Math.max(1920-1920*s,tx)); ty=Math.min(0,Math.max(1080-1080*s,ty));",
                  f"let tx={W//2}-cx*s, ty={H//2}-cy*s; tx=Math.min(0,Math.max({W}-{W}*s,tx)); ty=Math.min(0,Math.max({H}-{H}*s,ty));")
         .replace("X=-260+qe*(1920+520), Y=560+300*Math.sin(q*Math.PI*2*5.5)", f"X=-260+qe*({W}+520), Y={H//2}+650*Math.sin(q*Math.PI*2*5.5)"))
EN.DEFS = EN.DEFS.replace('x="-200" y="-200" width="2320" height="1480"', 'x="-300" y="-300" width="1700" height="2600"')
EN.RESID = "".join(f'<i style="left:{x}px;top:{y}px;width:{w}px"></i>' for x, y, w in [(60, 260, 900), (40, 520, 980), (80, 800, 880), (50, 1060, 950)])
from engine import *
from boards import A, S, E
import mixlib

OUT = "/home/claude/faceless/yt/odc1/shorts"; os.makedirs(OUT, exist_ok=True)
SR = 44100
CLIPS = {"s1": [[1, 2], [4, 5]], "s2": [[11, 12, 13]], "s3": [[27, 28, 29]]}
LEAD, GAP, TAIL = 0.3, 0.5, 0.0

class TM:
    """Mapa czasu: oryginał odcinka → czas w Shorcie."""
    def __init__(self, runs):
        self.runs, n = [], LEAD
        for r in runs:
            o0, o1 = S(r[0]) - 0.12, E(r[-1]) + 0.12
            self.runs.append((r, o0, o1, n)); n += (o1 - o0) + GAP
        self.voice_end = n - GAP
    def f(self, fid):
        for r, o0, o1, n0 in self.runs:
            if fid in r: return lambda t: round(n0 + (t - o0), 3)
    def A(self, fid, ph, n=1): return self.f(fid)(A(fid, ph, n))
    def S(self, fid): return self.f(fid)(S(fid))
    def E(self, fid): return self.f(fid)(E(fid))

def strike(x, y, w):
    return f"M{x-10} {y+6} L{x+w} {y-4}"

def s1(tm):
    a, s, e = tm.A, tm.S, tm.E
    tst = a(2, "z wielkiego planu"); tdl = a(2, "Więc dlaczego")
    A1 = dict(items=[T("dieta od poniedziałku.", 90, 250, a(1, "Dieta") - 0.05, size=78),
                     T("siłownia od pierwszego.", 90, 370, a(1, "Siłownia") - 0.05, size=78),
                     T("nowe życie od stycznia.", 90, 490, a(1, "Nowe życie") - 0.05, size=78),
                     D(strike(90, 306, 712), tst, 0.2, RED, 7, x=400), D(strike(90, 426, 760), tst + 0.2, 0.2, RED, 7, x=420),
                     D(strike(90, 546, 775), tst + 0.4, 0.2, RED, 7, x=430),
                     T("dlaczego nigdy", 90, 700, tdl - 0.05, 0.5, size=150, cls="y", cv=True),
                     T("od dziś?", 90, 860, a(2, "od dziś") - 0.15, 0.4, size=150, cls="y", cv=True),
                     D("M90 1030 C300 1015 520 1040 700 1022", e(2) - 0.1, 0.3, YL, 10, x=400)],
              poses=[[0, "hang"], [1.1, "pointL"], [tst + 0.3, "facepalm"], [tdl + 0.2, "shrug"]],
              moves=[[0.0, 1.0, 1300, 540]], cam=[[tdl - 0.1, 1.1, 540, 800, 0.45]], shakes=[[e(2) + 0.0, 5]], fadeIn=0.3, resid_static=False, last=2)
    tk = a(5, "kreski"); walk = [a(5, "Tak twój mózg") - 0.2, a(5, "Tak twój mózg") + 0.4]; d0 = tk + 0.3; back = [d0 + 0.55, d0 + 1.0]
    B1 = dict(items=[T("to nie lenistwo.", 90, 200, a(4, "To nie jest lenistwo") - 0.05, 0.55, size=124, cv=True),
                     T("ani słaba wola.", 90, 340, a(4, "I to nie jest") - 0.05, 0.5, size=124, cv=True),
                     T("to nie wada charakteru.", 95, 490, a(5, "to nie wada") - 0.05, size=54, cls="dim"),
                     T("twój mózg potrzebuje", 90, 600, a(5, "On po prostu") - 0.1, 0.6, size=76),
                     POP("kreski.", 90, 700, tk - 0.05, size=210, cls="y"),
                     D("M380 1160 L376 1340", d0, 0.45, YL, 13, id="krs", x=380)],
              poses=[[s(4), "hips"], [a(4, "To nie jest"), "think"], [walk[0], "hips"], [tk + 0.02, "wow"], [tk + 0.2, "ik", "krs"], [back[0], "hips"]],
              moves=[[walk[0], walk[1], 540, 460], [back[0], back[1], 460, 540]], cam=[[tk - 0.1, 1.08, 540, 700, 0.25]], shakes=[[tk, 9]], last=5)
    return [A1, B1]

def s2(tm):
    a, s, e = tm.A, tm.S, tm.E
    t82 = a(12, "Aż o")
    A2 = dict(items=[T("sprawdzili to.", 90, 170, a(11, "Sprawdzili") - 0.05, 0.55, size=130, cv=True),
                     T("Uniwersytet Pensylwanii, 2014", 95, 320, a(11, "Uniwersytetu") - 0.05, size=44, cls="dim"),
                     T("wyszukiwania „diet” w Google (USA)", 95, 372, a(11, "wyszukiwarki Google") - 0.05, size=44, cls="dim"),
                     *icon(magnifier(900, 230), a(11, "wyszukiwarki Google") - 0.3, 0.3, x=900),
                     BOX(90, 460, 620, 90, a(12, "wpisują słowo") - 0.2, 0.45, out=a(12, "O czternaście") - 0.4,
                         inner='<div style="position:absolute;left:28px;top:2px;font-size:54px">dieta<span style="opacity:.8">|</span></div>'),
                     D("M90 920 L960 920", a(12, "na początku tygodnia") - 0.4, 0.35, x=540),
                     BAR(150, 920, 260, 80, a(12, "na początku tygodnia") - 0.1, 0.4),
                     T("początek tygodnia", 280, 936, a(12, "na początku tygodnia") + 0.1, size=38, cx=True),
                     CNT(170, 710, 14, a(12, "O czternaście") - 0.05, 0.6),
                     BAR(560, 920, 300, 360, a(12, "A na początku roku") - 0.05, 0.6, yellow=True),
                     T("początek roku", 710, 936, a(12, "A na początku roku") + 0.2, size=38, cls="y", cx=True),
                     CNT(590, 430, 82, t82 - 0.05, 0.9, size=120)],
              poses=[[s(11), "hips"], [s(11) + 0.1, "think"], [a(12, "Okazało"), "hips"], [a(12, "na początku tygodnia"), "pointL"], [t82 + 0.8, "wow"]],
              cam=[[a(12, "A na początku roku") - 0.2, 1.08, 600, 700, 0.5]], shakes=[[t82 + 0.85, 8]], jumps=[t82 + 0.8], fadeIn=0.3, resid_static=False, last=12)
    tt = a(13, "Na początku tygodnia"); tj = a(13, "jeszcze bardziej") + 0.5
    B2 = dict(items=[T("potem: siłownia.", 90, 170, a(13, "Potem sprawdzili") - 0.05, size=120, cv=True),
                     T("prawie 12 000 osób", 95, 310, a(13, "Prawie dwanaście") - 0.05, size=48, cls="dim"),
                     D("M90 920 L960 920", tt - 0.5, 0.35, x=540),
                     BAR(120, 920, 220, 240, tt - 0.3, 0.4), T("zwykły dzień", 230, 936, tt - 0.2, size=36, cx=True),
                     BAR(410, 920, 220, 320, tt + 0.2, 0.5, yellow=True), T("początek tygodnia", 520, 936, tt + 0.3, size=36, cls="y", cx=True),
                     CNT(420, 470, 33, a(13, "o jedną trzecią") - 0.05, 0.6),
                     BAR(690, 920, 220, 353, a(13, "Na początku semestru") - 0.05, 0.5, yellow=True),
                     T("początek semestru", 800, 936, a(13, "Na początku semestru") + 0.1, size=36, cls="y", cx=True),
                     CNT(700, 437, 47, a(13, "jeszcze bardziej") - 0.1, 0.6)],
              poses=[[s(13), "hips"], [tt - 0.3, "pointL"], [tj - 0.05, "wow"]], jumps=[tj], shakes=[[tj + 0.45, 6]], last=13)
    return [A2, B2]

def s3(tm):
    a, s, e = tm.A, tm.S, tm.E
    t66 = a(27, "sześćdziesiąt sześć dni"); x66 = 100 + (66 - 18) / (254 - 18) * 880
    A3 = dict(items=[T("ile trwa budowanie nawyku?", 90, 170, a(27, "Naukowcy") - 0.05, 0.7, size=70),
                     T("UCL, 2010 · 96 osób · 12 tygodni", 95, 290, a(27, "przez dwanaście") - 0.05, size=44, cls="dim"),
                     T("średnio", 100, 430, a(27, "Średnio") - 0.05, size=54, cls="dim"),
                     POP("66 dni", 90, 490, t66 - 0.05, size=230, cls="y"),
                     D("M100 900 L980 900", a(27, "U niektórych") - 0.3, 0.4, x=540),
                     D(f"M{x66:.0f} 868 L{x66:.0f} 932", a(27, "U niektórych") - 0.1, 0.2, YL, 9, x=300), T("66", x66, 945, a(27, "U niektórych"), size=50, cls="y", cx=True),
                     D("M100 875 L100 925", a(27, "osiemnaście") - 0.1, 0.2, CH, 8, x=100), T("18", 100, 945, a(27, "osiemnaście") - 0.05, size=50, cx=True),
                     D("M980 875 L980 925", a(27, "ponad dwieście") - 0.1, 0.2, CH, 8, x=980), T("254", 980, 945, a(27, "ponad dwieście") - 0.05, size=50, cx=True)],
              poses=[[s(27), "hips"], [s(27) + 0.2, "think"], [t66, "wow"], [t66 + 1.2, "hips"], [a(27, "U niektórych"), "pointL"]],
              jumps=[t66 + 0.05], shakes=[[t66 + 0.05, 7]], fadeIn=0.3, resid_static=False, last=27)
    t1 = a(28, "jeden opuszczony"); t2 = a(28, "Problem zaczynał")
    it = [T("jeden opuszczony dzień:", 90, 170, t1 - 0.05, size=90, cv=True)]
    for (y, tb, marks) in [(330, t1 + 0.1, ["c"] * 5 + ["x"] + ["c"] * 4), (620, t2 - 0.3, ["c"] * 4 + ["x"] * 5 + [None])]:
        for i, mk in enumerate(marks):
            x = 90 + i * 92
            it.append(CELL(x, y, tb + i * 0.04))
            if mk:
                p = check(x + 12, y + 34, 1.0) if mk == "c" else cross(x + 16, y + 16, 1.0)
                it.append(D(p, tb + 0.5 + i * 0.07, 0.12, YL if mk == "c" else RED, 7, x=x, snd="tick"))
    it += [T("ok", 90 + 5 * 92 + 31, 410, t1 + 1.1, size=46, cls="y", cx=True),
           T("praktycznie bez szkody", 90, 480, a(28, "praktycznie nie zaszkodził") - 0.05, size=56, cls="y"),
           T("przerwy raz za razem = problem", 90, 760, a(28, "gdy przerwy") - 0.05, size=52, cls="r")]
    B3 = dict(items=it, poses=[[s(28), "hips"], [t1, "pointL"], [a(28, "gdy przerwy"), "facepalm"]], last=28)
    tf, tu, tw = a(29, "Możesz wypaść raz"), a(29, "Nigdy dwa razy"), a(29, "Wracasz jutro")
    C3 = dict(items=[T("zasada:", 90, 170, a(29, "zasada jest prosta") - 0.05, size=100, cv=True),
                     T("możesz wypaść raz.", 95, 320, tf - 0.05, size=72),
                     POP("nigdy dwa razy", 90, 440, tu - 0.05, size=140, cls="y"),
                     T("z rzędu.", 90, 600, tu + 0.35, 0.4, size=140, cls="y", cv=True),
                     T("nie czekasz na poniedziałek.", 95, 800, a(29, "Nie czekasz") - 0.05, size=58),
                     T("wracasz jutro.", 95, 880, tw - 0.05, size=58, cls="y")],
              poses=[[s(29), "hips"], [tf + 0.15, "down"], [tu - 0.1, "hips"], [tu + 0.3, "wow"], [tw - 0.15, "hips"]],
              moves=[[tw - 0.1, tw + 0.6, 540, 760], [tw + 0.6, tw + 1.3, 760, 540]], sfx=[("thud", tf + 0.4, 0.7, 500)], shakes=[[tu, 7]], last=29)
    return [A3, B3, C3]

def build_short(key):
    tm = TM(CLIPS[key]); specs = {"s1": s1, "s2": s2, "s3": s3}[key](tm)
    boards, start = [], 0.0
    for i, kw in enumerate(specs):
        last = kw.pop("last"); items = [x for x in kw.pop("items") if x]
        from boards import te
        moves_end = max([m[1] for m in kw.get("moves", [])] + [0])
        es = max(tm.E(last) + 0.06, te(items) + 0.05, moves_end + 0.05)
        boards.append(Board(f"{key}_{i}", round(start, 3), round(es + 0.72, 3), items, erase=[round(es, 3), round(es + 0.68, 3)], **kw))
        start = round(es + 0.72, 3)
    end = Board(f"{key}_end", start, start + 2.6,
                [T("cały odcinek na kanale:", 90, 300, start + 0.15, size=60, cls="dim"),
                 T("dlaczego zawsze", 90, 420, start + 0.5, 0.5, size=110, cls="y", cv=True),
                 T("zaczynasz od poniedziałku", 90, 545, start + 0.9, 0.6, size=84, cls="y", cv=True)],
                poses=[[start, "hips"], [start + 0.3, "wave"]], fadeOut=0.4)
    end.erase = None
    boards.append(end)
    return tm, boards

def voice_for(tm, total):
    src = mixlib.read_wav("/home/claude/faceless/yt/odc1/lektor_cut.wav")
    out = np.zeros(int(total * SR) + 1, dtype=np.float32)
    for r, o0, o1, n0 in tm.runs:
        seg = src[int(o0 * SR):int(o1 * SR)].copy(); f = int(0.02 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        i = int(n0 * SR); out[i:i + len(seg)] = seg[:len(out) - i]
    return out

if __name__ == "__main__":
    mode = sys.argv[1]
    keys = sys.argv[2:] or ["s1", "s2", "s3"]
    if mode == "stills":
        for k in keys:
            tm, bs = build_short(k)
            spec = {b.name: [round((b.erase[0] - 0.15) if b.erase else b.end - 0.6, 2)] for b in bs}
            ps = asyncio.run(stills(bs, spec, OUT))
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *sum([["-i", p] for p in ps], []), "-filter_complex",
                            "".join(f"[{i}]scale=360:640[v{i}];" for i in range(len(ps))) + "".join(f"[v{i}]" for i in range(len(ps))) + f"hstack={len(ps)}",
                            f"{OUT}/arkusz_{k}.jpg"], check=True)
            print(k, [(b.name, b.start, b.end) for b in bs])
    elif mode == "render":
        for k in keys:
            tm, bs = build_short(k)
            for b in bs: asyncio.run(render_board(b, OUT))
    elif mode == "final":
        for k in keys:
            tm, bs = build_short(k); total = bs[-1].end
            mixlib.make_mix(bs, voice_for(tm, total), f"{OUT}/{k}_mix.wav")
            open(f"{OUT}/{k}_list.txt", "w").write("".join(f"file 'scena_{b.name}.mp4'\n" for b in bs))
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{OUT}/{k}_list.txt", "-c", "copy", f"{OUT}/_{k}_v.mp4"], check=True)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{OUT}/_{k}_v.mp4", "-i", f"{OUT}/{k}_mix.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                            "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart",
                            f"{OUT}/short-{k}.mp4"], check=True)
            print("final", k, round(total, 2))
