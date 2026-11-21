"""Napisy .srt, rozdziały i opis pod film."""
import json, re
from boards import build, A, S, F

OUT = "/home/claude/faceless/yt/odc1/paczka"
import os; os.makedirs(OUT, exist_ok=True)
bs = build()

def tc(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"

def tchar(fid, c):
    for cs, ce, ts, te in F[fid]["map"]:
        if cs <= c <= ce:
            return ts + (c - cs) / max(1, ce - cs) * (te - ts)
    return F[fid]["t1"]

subs = []
for fid in sorted(F):
    txt = F[fid]["text"]
    # dziel na zdania, długie zdania po przecinkach, maks ~60 znaków
    parts, pos = [], 0
    for m in re.finditer(r"[^.?!…:]+[.?!…:]*\s*", txt):
        seg = m.group(0)
        if len(seg.strip()) > 60:
            sub, cur = re.split(r"(?<=,)\s+", seg), ""
            for p in sub:
                if len(cur) + len(p) > 60 and cur:
                    parts.append(cur); cur = p + " "
                else:
                    cur += p + " "
            if cur.strip(): parts.append(cur)
        else:
            parts.append(seg)
    merged = []
    for p in parts:
        if merged and len(merged[-1].strip()) + len(p.strip()) <= 30: merged[-1] = merged[-1].rstrip() + " " + p
        else: merged.append(p)
    parts = merged
    c = 0
    for p in parts:
        p_clean = p.strip()
        if not p_clean: continue
        c0 = txt.index(p_clean, c); c1 = c0 + len(p_clean); c = c1
        t0, t1 = tchar(fid, c0), tchar(fid, c1)
        if t1 - t0 < 0.9: t1 = t0 + 0.9
        line = p_clean
        if len(line) > 42:
            words, l1 = line.split(), ""
            while words and len(l1) + len(words[0]) < len(line) / 2 + 4: l1 += words.pop(0) + " "
            line = l1.strip() + "\n" + " ".join(words)
        subs.append([t0, t1, line])
for i in range(len(subs) - 1):  # bez nakładania
    subs[i][1] = min(subs[i][1], subs[i + 1][0] - 0.02)
with open(f"{OUT}/napisy-pl.srt", "w", encoding="utf-8") as f:
    for i, (a, b, l) in enumerate(subs, 1):
        f.write(f"{i}\n{tc(a)} --> {tc(b)}\n{l}\n\n")

def mmss(t):
    t = int(t); return f"{t // 60}:{t % 60:02d}"
board = {b.name: b for b in bs}
chap = [(0, "Dlaczego zawsze od poniedziałku?"), (board["b03"].start, "To nie lenistwo"), (board["b04"].start, "Kreska w czasie: jak to działa"),
        (board["b06"].start, "Co sprawdzili naukowcy"), (board["b08"].start, "Haczyk: dlaczego w środę się nie chce"),
        (board["b11"].start, "Sposób 1: zrób sobie poniedziałek dziś"), (board["b14"].start, "Sposób 2: pierwszy krok na 2 minuty"),
        (board["b18"].start, "Sposób 3: zaplanuj wpadkę"), (board["b22"].start, "Ukryta lekcja")]
chapters = "\n".join(f"{mmss(t)} {n}" for t, n in chap)

opis = f"""Dieta od poniedziałku, siłownia od pierwszego, nowe życie od stycznia… a w środę już się nie chce. To nie lenistwo. Naukowcy nazywają to efektem nowego startu. W tym odcinku: jak działa, co pokazały badania i 3 sposoby, żeby wykorzystać go na swoją korzyść.

{chapters}

Źródła:
• Dai, Milkman, Riis (2014). The Fresh Start Effect: Temporal Landmarks Motivate Aspirational Behavior. Management Science. https://doi.org/10.1287/mnsc.2014.1901
• Dai, Milkman, Riis (2015). Put Your Imperfections Behind You: Temporal Landmarks Spur Goal Initiation When They Signal New Beginnings. Psychological Science 26(12). https://doi.org/10.1177/0956797615605818
• Gollwitzer, Sheeran (2006). Implementation intentions and goal achievement: A meta-analysis of effects and processes. Advances in Experimental Social Psychology 38. https://doi.org/10.1016/S0065-2601(06)38002-1
• Lally, van Jaarsveld, Potts, Wardle (2010). How are habits formed: Modelling habit formation in the real world. European Journal of Social Psychology 40. https://doi.org/10.1002/ejsp.674

Jeśli ten odcinek coś ci dał, wyślij go komuś, kto od lat zaczyna od poniedziałku.
Więcej krótkich lekcji: Instagram @ukryta.lekcja

#psychologia #nawyki #motywacja
"""
tytul = "dlaczego zawsze zaczynasz od poniedziałku"
tagi = "efekt nowego startu, fresh start effect, motywacja, nawyki, prokrastynacja, od poniedziałku, psychologia, samorozwój, jak zacząć, silna wola, intencje implementacyjne, jak zbudować nawyk, 66 dni nawyk"
open(f"{OUT}/opis.txt", "w", encoding="utf-8").write(f"TYTUŁ:\n{tytul}\n\nOPIS:\n{opis}\nTAGI:\n{tagi}\n")
print(chapters); print(len(subs), "napisów")
