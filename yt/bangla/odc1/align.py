"""Tnie lektora Wojtka na 34 fragmenty, skraca pauzy, liczy czasy zdań → lektor_cut.wav + timeline.json"""
import re, json, subprocess, numpy as np, wave
SRC = "/home/claude/bangla-yt/odc1/glos/lektor.mp3"
TXT = "/home/claude/bangla-yt/odc1/lektor-wojtek-do-elevenlabs.txt"
OUT = "/home/claude/bangla-yt/odc1"
SR = 44100
NF = 34
SECTION_FIRST = [5, 13, 16, 20, 24, 32]
GAP_IN, GAP_SEC, LEAD, TAIL = 0.42, 0.85, 0.6, 1.2
raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", SRC, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
x = np.frombuffer(raw, dtype=np.float32).copy(); dur = len(x) / SR
def silences(d=0.18, noise="-38dB"):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", SRC, "-af", f"silencedetect=noise={noise}:d={d}", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(v) for v in re.findall(r"silence_start: ([\d.]+)", out)]; en = [float(v) for v in re.findall(r"silence_end: ([\d.]+)", out)]
    if len(en) < len(st): en.append(dur)
    return list(zip(st, en))
sil = silences()
lead_end = sil[0][1] if sil and sil[0][0] < 0.05 else 0.0
tail_start = sil[-1][0] if sil and sil[-1][1] > dur - 0.05 else dur
mid = [s for s in sil if s[0] > 0.05 and s[1] < dur - 0.05]
longp = sorted(sorted(mid, key=lambda s: s[1] - s[0], reverse=True)[:NF - 1])
print("najkrótsza długa pauza", round(min(e - s for s, e in longp), 3), "| najdłuższa reszta", round(sorted([e - s for s, e in mid if (s, e) not in longp])[-1], 3))
bounds = [lead_end] + [v for s, e in longp for v in (s, e)] + [tail_start]
frags = [(bounds[2 * i], bounds[2 * i + 1]) for i in range(NF)]
texts = [t.strip() for t in open(TXT, encoding="utf-8").read().split("[long pause]")]
assert len(texts) == NF
def split_sent(t):
    parts = re.split(r"(?<=[.?!…:])\s+", t); out, pos = [], 0
    for p in parts:
        i = t.index(p, pos); out.append((i, i + len(p))); pos = i + len(p)
    return out
timeline, chunks, cur = [], [np.zeros(int(LEAD * SR), dtype=np.float32)], LEAD
for i, (fs, fe) in enumerate(frags):
    fid = i + 1
    if i > 0:
        g = GAP_SEC if fid in SECTION_FIRST else GAP_IN
        chunks.append(np.zeros(int(g * SR), dtype=np.float32)); cur += g
    pad = 0.04; a0, a1 = max(0, fs - pad), min(dur, fe + pad)
    seg = x[int(a0 * SR):int(a1 * SR)].copy(); f = int(0.01 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    chunks.append(seg); off = cur - a0
    inner = [(s, e) for s, e in sil if s > fs + 0.05 and e < fe - 0.05]
    speech, p = [], fs
    for s, e in inner: speech.append((p, s)); p = e
    speech.append((p, fe))
    sents = split_sent(texts[i]); mapping = []
    if len(sents) == len(speech):
        for (cs, ce), (ts, te) in zip(sents, speech): mapping.append([cs, ce, ts + off, te + off])
        mode = "zdania"
    else:
        # granice kawałków mowy kładziemy na znakach interpunkcji (DP: równe tempo mówienia)
        t = texts[i]; L = len(t)
        punct = set(m.end() for m in re.finditer(r"[.,?!…:;–—]+\s+", t))
        cands = sorted(set(m.end() for m in re.finditer(r"\s+", t)) | punct)
        PEN = 45.0
        k = len(speech); durs = [e - s for s, e in speech]; rate = L / sum(durs)
        best = None
        if len(cands) >= k - 1:
            import functools
            @functools.lru_cache(None)
            def dp(j, start):  # j = numer kawałka, start = indeks znaku
                if j == k - 1: return ((L - start - rate * durs[j]) ** 2, ())
                if L - start < 3 * (k - j): return None
                res = None
                for c in cands:
                    if c <= start + 2: continue
                    cost = (c - start - rate * durs[j]) ** 2 + (0 if c in punct else PEN)
                    sub = dp(j + 1, c)
                    if sub is None: continue
                    tot = cost + sub[0]
                    if res is None or tot < res[0]: res = (tot, (c,) + sub[1])
                return res
            best = dp(0, 0)
        if best:
            cuts = [0] + list(best[1]) + [L]
            for j, (s, e) in enumerate(speech): mapping.append([cuts[j], cuts[j + 1], s + off, e + off])
            mode = f"interp ({len(sents)}z/{k}k)"
        else:
            tot = sum(durs); acc = 0
            for s, e in speech:
                c0 = int(acc / tot * L); acc += e - s; c1 = int(acc / tot * L); mapping.append([c0, c1, s + off, e + off])
            mode = f"proporcja ({len(sents)}z/{k}k)"
    timeline.append(dict(id=fid, text=texts[i], t0=round(fs + off, 3), t1=round(fe + off, 3), map=mapping, mode=mode))
    cur += a1 - a0
chunks.append(np.zeros(int(TAIL * SR), dtype=np.float32)); cur += TAIL
y = np.concatenate(chunks)
with wave.open(f"{OUT}/lektor_cut.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y, -1, 1) * 32767).astype("<i2").tobytes())
json.dump(dict(total=round(len(y) / SR, 3), frags=timeline), open(f"{OUT}/timeline.json", "w"), ensure_ascii=False, indent=1)
print("total", round(len(y) / SR, 2))
for f in timeline:
    d = f["t1"] - f["t0"]; print(f'F{f["id"]:02d} {f["t0"]:7.2f}-{f["t1"]:7.2f} ({d:5.2f}s, {len(f["text"])/d:4.1f} zn/s) {f["mode"]:18s} {f["text"][:44]}')
