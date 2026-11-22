"""Granice fragmentów lektora dopasowane do długości tekstu (nie tylko do najdłuższych pauz).

ElevenLabs v4 nie zawsze robi z każdego [long pause] długą pauzę (np. w drugiej połowie nagrania
pauzy po tagach bywają tak krótkie jak zwykłe przerwy między zdaniami). Ten skrypt wybiera
(fragmenty−1) pauz tak, żeby czas każdego fragmentu pasował do liczby znaków w jego tekście,
z premią za dłuższe pauzy.

Użycie:  python3 -I granice.py nagranie.mp3 lektor.txt [wynik.json] [nazwa pliku z yt-inbox]
Wynik:   {"pauzy": [[start, koniec], ...], "ocena": "ok"|"zle", ...}; align.py bierze "pauzy" zamiast najdłuższych pauz.
"""
import re, sys, json, math, subprocess, statistics

LAM = 20.0          # premia za długość pauzy
MIN_R, MAX_R = 0.6, 1.7   # dopuszczalny stosunek czasu fragmentu do oczekiwanego
MAX_MED = 0.15      # dopuszczalna mediana |ln(stosunek)|

def pauzy(f, d=0.2):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", f, "-af", f"silencedetect=noise=-38dB:d={d}", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    return [(float(e) - float(du), float(e), float(du)) for e, du in re.findall(r"silence_end: ([0-9.]+) \| silence_duration: ([0-9.]+)", o)]

def czas(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)

def dopasuj(mp3, txt):
    fr = [t.strip() for t in open(txt, encoding="utf-8").read().split("[long pause]")]
    ch = [len(re.sub(r"\s+", " ", t)) for t in fr]; N = len(fr); K = N - 1
    T = czas(mp3); P = pauzy(mp3)
    t0 = P[0][1] if P and P[0][0] < 0.05 else 0.0
    t1 = P[-1][0] if P and P[-1][1] > T - 0.05 else T
    P = [p for p in P if p[0] > t0 + 0.3 and p[1] < t1 - 0.3]
    M = len(P)
    if M < K:
        return {"ocena": "zle", "powod": f"za mało pauz w nagraniu ({M}, potrzeba {K})", "fragmenty": N}
    rate = sum(ch) / ((t1 - t0) - sum(sorted((p[2] for p in P), reverse=True)[:K]))
    c = lambda a, b, n: ((b - a) - n / rate) ** 2 / (n / rate)
    INF = float("inf")
    best = [[INF] * M for _ in range(K)]; arg = [[-1] * M for _ in range(K)]
    for j in range(M):
        best[0][j] = c(t0, P[j][0], ch[0]) - LAM * P[j][2]
    for k in range(1, K):
        for j in range(k, M):
            b, a = INF, -1
            for i in range(k - 1, j):
                v = best[k - 1][i] + c(P[i][1], P[j][0], ch[k])
                if v < b: b, a = v, i
            best[k][j] = b - LAM * P[j][2]; arg[k][j] = a
    _, j = min((best[K - 1][j] + c(P[j][1], t1, ch[K]), j) for j in range(M) if best[K - 1][j] < INF)
    sel = [j]
    for k in range(K - 1, 0, -1):
        j = arg[k][j]; sel.append(j)
    sel = sel[::-1]
    starts = [t0] + [P[j][1] for j in sel]; ends = [P[j][0] for j in sel] + [t1]
    ratios = [(ends[i] - starts[i]) / (ch[i] / rate) for i in range(N)]
    med = statistics.median(abs(math.log(r)) for r in ratios)
    ok = all(MIN_R <= r <= MAX_R for r in ratios) and med <= MAX_MED
    return {"ocena": "ok" if ok else "zle", "fragmenty": N, "tempo_zn_s": round(rate, 1),
            "mediana_odchylenia": round(med, 3), "stosunki": [round(r, 2) for r in ratios],
            "najkrotsza_wybrana_pauza": round(min(P[j][2] for j in sel), 2),
            "pauzy": [[P[j][0], P[j][1]] for j in sel]}

if __name__ == "__main__":
    w = dopasuj(sys.argv[1], sys.argv[2]); w["nagranie"] = sys.argv[4] if len(sys.argv) > 4 else sys.argv[1].rsplit("/", 1)[-1]
    if len(sys.argv) > 3:
        json.dump(w, open(sys.argv[3], "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in w.items() if k != "pauzy"}, ensure_ascii=False))
