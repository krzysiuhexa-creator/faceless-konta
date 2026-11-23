"""Tnie lektor na 31 fragmentów, skraca pauzy, liczy czasy zdań → lektor_cut.wav + timeline.json"""
import re, json, subprocess, numpy as np, wave

SRC = "/home/claude/faceless/yt/odc2/glos/lektor.mp3"
TXT = "/home/claude/faceless/yt/odc2/glos/lektor.txt"
OUT = "/home/claude/faceless/yt/odc2"
SR = 44100
# pierwszy fragment każdej planszy (numeracja od 1)
NF = 31
BOARD_FIRST = [1, 2, 3, 4, 6, 7, 9, 11, 13, 14, 15, 16, 17, 18, 20, 21, 23, 24, 26, 27, 30, 31]
GAP_IN, GAP_BOARD, LEAD, TAIL = 0.45, 1.0, 0.5, 2.0

raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", SRC, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
x = np.frombuffer(raw, dtype=np.float32).copy()
dur = len(x) / SR

def silences(d=0.25, noise="-38dB"):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", SRC, "-af", f"silencedetect=noise={noise}:d={d}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(v) for v in re.findall(r"silence_start: ([\d.]+)", out)]
    en = [float(v) for v in re.findall(r"silence_end: ([\d.]+)", out)]
    if len(en) < len(st): en.append(dur)
    return list(zip(st, en))

sil = silences()
longp = [tuple(p) for p in json.load(open("/home/claude/wideo/yt/ukryta-lekcja/odc2/granice.json"))["pauzy"]]
assert len(longp) == NF - 1
# granice mowy
lead_end = sil[0][1] if sil and sil[0][0] < 0.05 else 0.0
tail_start = sil[-1][0] if sil and sil[-1][1] > dur - 0.05 else dur
bounds = [lead_end] + [v for s, e in longp for v in (s, e)] + [tail_start]
frags = [(bounds[2 * i], bounds[2 * i + 1]) for i in range(NF)]

texts = [t.strip() for t in open(TXT, encoding="utf-8").read().split("[long pause]")]
assert len(texts) == NF, len(texts)

def split_sent(t):
    parts = re.split(r"(?<=[.?!…:])\s+", t)
    out, pos = [], 0
    for p in parts:
        i = t.index(p, pos); out.append((i, i + len(p))); pos = i + len(p)
    return out

timeline, chunks_audio, cur = [], [], LEAD
chunks_audio.append(np.zeros(int(LEAD * SR), dtype=np.float32))
for i, (fs, fe) in enumerate(frags):
    fid = i + 1
    if i > 0:
        g = GAP_BOARD if fid in BOARD_FIRST else GAP_IN
        chunks_audio.append(np.zeros(int(g * SR), dtype=np.float32)); cur += g
    pad = 0.04
    a0, a1 = max(0, fs - pad), min(dur, fe + pad)
    seg = x[int(a0 * SR):int(a1 * SR)].copy()
    n = len(seg); f = int(0.01 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    chunks_audio.append(seg)
    off = cur - a0
    # krótkie pauzy wewnątrz fragmentu → kawałki mowy
    inner = [(s, e) for s, e in sil if s > fs + 0.05 and e < fe - 0.05]
    speech, p = [], fs
    for s, e in inner:
        speech.append((p, s)); p = e
    speech.append((p, fe))
    sents = split_sent(texts[i])
    mapping = []
    if len(sents) == len(speech):
        for (cs, ce), (ts, te) in zip(sents, speech):
            mapping.append([cs, ce, ts + off, te + off])
        mode = "zdania"
    else:  # proporcjonalnie do czasu mowy
        tot = sum(e - s for s, e in speech); L = len(texts[i]); acc = 0
        for s, e in speech:
            c0 = int(acc / tot * L); acc += e - s; c1 = int(acc / tot * L)
            mapping.append([c0, c1, s + off, e + off])
        mode = f"proporcja ({len(sents)} zdań / {len(speech)} kawałków)"
    timeline.append(dict(id=fid, text=texts[i], t0=round(fs + off, 3), t1=round(fe + off, 3), map=mapping, mode=mode,
                         board_first=fid in BOARD_FIRST))
    cur += a1 - a0
chunks_audio.append(np.zeros(int(TAIL * SR), dtype=np.float32)); cur += TAIL
y = np.concatenate(chunks_audio)
with wave.open(f"{OUT}/lektor_cut.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y, -1, 1) * 32767).astype("<i2").tobytes())
json.dump(dict(total=round(len(y) / SR, 3), frags=timeline), open(f"{OUT}/timeline.json", "w"), ensure_ascii=False, indent=1)
print("total", round(len(y) / SR, 2))
for f in timeline:
    print(f'F{f["id"]:02d} {f["t0"]:7.2f}-{f["t1"]:7.2f} ({f["t1"]-f["t0"]:5.2f}s) {f["mode"]:30s} {f["text"][:50]}')
