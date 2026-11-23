"""Napisy .srt, rozdziały i opis pod film."""
import json, re
from boards import build, A, S, F

OUT = "/home/claude/faceless/yt/odc2/paczka"
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
    for m in re.finditer(r"[^.?!…:]+[.?!…:”]*\s*", txt):
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
        if merged and len(merged[-1].strip()) + len(p.strip()) <= 30: merged[-1] = merged[-1] + p
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
chap = [(0, "Cytat, którego Arystoteles nie powiedział"), (board["b06"].start, "Słaba wola czy nawyk?"),
        (board["b07"].start, "43% dnia na autopilocie"), (board["b09"].start, "Ścieżka w trawniku"),
        (board["b10"].start, "Eksperyment z popcornem w kinie"), (board["b14"].start, "Sposób 1: nowe miejsce"),
        (board["b16"].start, "Sposób 2: doklej nowy nawyk do starego"), (board["b18"].start, "Sposób 3: zepsuj autopilota"),
        (board["b20"].start, "Ukryta lekcja")]
chapters = "\n".join(f"{mmss(t)} {n}" for t, n in chap)

opis = f"""„Jesteśmy tym, co wielokrotnie robimy” – tego Arystoteles nie powiedział. Ale miał rację bardziej, niż myślisz. Dlaczego wracasz do starych nawyków, nawet kiedy naprawdę postanowisz inaczej? Bo nawyk nie słucha postanowień, tylko otoczenia. W tym odcinku: co pokazały badania (od zegarków, które piszczały co godzinę, po stary popcorn w kinie) i 3 sposoby, żeby pracować z otoczeniem, a nie walczyć ze sobą.

{chapters}

Źródła:
• Will Durant (1926), The Story of Philosophy – autor zdania „We are what we repeatedly do…”, streszczenia myśli Arystotelesa.
• Arystoteles, Etyka nikomachejska, księga II – cnota etyczna powstaje z przyzwyczajenia.
• Wood, Quinn, Kashy (2002). Habits in everyday life. Journal of Personality and Social Psychology 83(6).
• Neal, Wood, Quinn (2006). Habits: A repeat performance. Current Directions in Psychological Science 15(4).
• Neal, Wood, Wu, Kurlander (2011). The pull of the past: When do habits persist despite conflict with motives? Personality and Social Psychology Bulletin 37(11).
• Verplanken, Roy (2016). Empowering interventions to promote sustainable lifestyles: Testing the habit discontinuity hypothesis in a field experiment. Journal of Environmental Psychology 45.
• Judah, Gardner, Aunger (2013). Forming a flossing habit: An exploratory study of the psychological determinants of habit formation. British Journal of Health Psychology 18(2).

Wykres popcornu w odcinku to rysunek poglądowy, nie dokładne dane z badania. Głos lektora wygenerowany z pomocą AI.

Jeśli ten odcinek coś ci dał, wyślij go komuś, kto co tydzień zaczyna od nowa.

#psychologia #nawyki #samorozwój
"""
tytul = "dlaczego zawsze wracasz do starych nawyków"
tagi = "nawyki, stare nawyki, jak zmienić nawyk, psychologia nawyków, autopilot, silna wola, Wendy Wood, efekt otoczenia, habit stacking, doklejanie nawyków, samorozwój, motywacja, Arystoteles cytat, Will Durant"
open(f"{OUT}/opis.txt", "w", encoding="utf-8").write(f"TYTUŁ:\n{tytul}\n\nOPIS:\n{opis}\nTAGI:\n{tagi}\n")
print(chapters); print(len(subs), "napisów")
