"""Miks: lektor + efekty (ściszane pod głosem) + tło sali z zegarem → dzwiek_final.wav"""
import math, wave, numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from boards import build

SR = 44100
OUT = "/home/claude/faceless/yt/odc1"
boards = build()
total = boards[-1].end
N = int(total * SR) + 1
rng = np.random.default_rng(11)

def read_wav(p):
    with wave.open(p) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32767
    return a
voice = np.zeros(N, dtype=np.float32); v = read_wav(f"{OUT}/lektor_cut.wav"); voice[:min(N, len(v))] = v[:N]

def filt(x, lo=None, hi=None, order=2):
    if lo and hi: sos = butter(order, [lo, hi], btype="band", fs=SR, output="sos")
    elif lo: sos = butter(order, lo, btype="high", fs=SR, output="sos")
    else: sos = butter(order, hi, btype="low", fs=SR, output="sos")
    return sosfilt(sos, x)

sfx = np.zeros((N, 2))
def add(sig, t, x=960, g=1.0):
    i = int(t * SR); p = 0.15 + 0.7 * min(max(x / 1920, 0), 1); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    sfx[i:i + n, 0] += sig[:n] * g * math.cos(p * math.pi / 2); sfx[i:i + n, 1] += sig[:n] * g * math.sin(p * math.pi / 2)
def env(n, a, r):
    e = np.ones(n); na, nr = max(1, int(a * SR)), max(1, int(r * SR)); e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return e
def stroke(d, fc, amp):
    n = int(d * SR); w = rng.standard_normal(n); grit = (rng.random(n) < 0.06) * rng.standard_normal(n) * 3
    s = filt(w, fc * 0.55, min(fc * 1.9, 15000)) + 0.6 * filt(grit, 1200, 7000); tt = np.arange(n) / SR
    return s * (1 + 0.45 * np.sin(2 * np.pi * rng.uniform(25, 55) * tt)) * env(n, 0.004, 0.018) * amp
def tap(amp=1.0):
    n = int(0.03 * SR); return filt(rng.standard_normal(n), 700, 3500) * np.exp(-np.arange(n) / (0.006 * SR)) * amp

for b in boards:
    for e in b.events():
        kind, t = e[0], max(0.0, e[1])
        if kind == "write":
            du, x, size = e[2], e[3], e[4]; big = size >= 100; g = 0.20 if size < 50 else (0.30 if big else 0.25); tt, cnt = t, 0
            while tt < t + du:
                d = rng.uniform(0.05, 0.11) if big else rng.uniform(0.035, 0.085)
                add(stroke(d, rng.uniform(1900, 3000) if big else rng.uniform(2300, 4200), rng.uniform(0.6, 1.0)), tt, x, g)
                if cnt % 4 == 0: add(tap(0.8), tt, x, g * 0.9)
                tt += d + rng.uniform(0.008, 0.04); cnt += 1
        elif kind == "draw":
            du, x = e[2], e[3]; n = int(du * SR); tt = np.arange(n) / SR
            s = filt(rng.standard_normal(n), 1400, 5200) * (1 + 0.35 * np.sin(2 * np.pi * 7 * tt)) * env(n, 0.02, 0.05)
            s += 0.5 * filt((rng.random(n) < 0.05) * rng.standard_normal(n) * 3, 1000, 6000)
            add(s, t, x, 0.22); add(tap(0.9), t, x, 0.2)
        elif kind == "rub":
            du, x = e[2], e[3]; n = int(du * SR); add(filt(rng.standard_normal(n), 180, 1400) * env(n, 0.05, 0.12), t, x, 0.18)
        elif kind == "erase":
            du = e[2]; n = int(du * SR); u = np.arange(n) / n; amp = 0.25 + 0.75 * np.abs(np.cos(2 * np.pi * 5.5 * u))
            s = filt(rng.standard_normal(n), 220, 2600) * amp * env(n, 0.06, 0.1) + 0.4 * filt(rng.standard_normal(n), 60, 400) * amp
            i = int(t * SR); m = min(n, N - i); pan = (0.15 + 0.7 * u[:m]) * np.pi / 2
            sfx[i:i + m, 0] += s[:m] * 0.30 * np.cos(pan); sfx[i:i + m, 1] += s[:m] * 0.30 * np.sin(pan)
        elif kind == "step":
            x = e[2]; n = int(0.09 * SR); k = np.arange(n) / SR
            add(filt(rng.standard_normal(n), None, 520) * np.exp(-k / 0.018) * 2.2 + 0.5 * np.sin(2 * np.pi * 95 * k) * np.exp(-k / 0.03), t, x, 0.16)
        elif kind == "thud":
            a, x = e[2], e[3]; n = int(0.45 * SR); k = np.arange(n) / SR; f = 72 * np.exp(-k * 2.2) + 40
            s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-k / 0.11) + 0.5 * filt(rng.standard_normal(n), None, 900) * np.exp(-k / 0.015)
            add(s, t, x, 0.55 * a); add(tap(1.0), t, x, 0.25 * a)
        elif kind == "whoosh":
            du, x = max(0.25, e[2]), e[3]; n = int(du * SR); u = np.arange(n) / n
            add(filt(rng.standard_normal(n), 350, 2400) * np.sin(np.pi * u) ** 2, t, x, 0.09)
        elif kind in ("ticks", "tick"):
            du, x = (e[2], e[3]); tt = t
            while tt < t + max(du, 0.01):
                n = int(0.012 * SR); add(filt(rng.standard_normal(n), 2500, 7000) * np.exp(-np.arange(n) / (0.002 * SR)), tt, x, 0.22); tt += 1 / 16

# pogłos pokoju na efektach
n_ir = int(0.35 * SR); ir = rng.standard_normal(n_ir) * np.exp(-np.arange(n_ir) / (0.07 * SR)); ir /= np.abs(ir).sum() / 6
sfx = sfx + 0.18 * np.stack([fftconvolve(sfx[:, c], ir)[:N] for c in range(2)], axis=1)
sfx *= 0.32 / (np.max(np.abs(sfx)) + 1e-9)

# tło: szum sali + zegar
brown = np.cumsum(rng.standard_normal(N)); brown = filt(filt(brown, 25, None), None, 380); brown /= np.sqrt(np.mean(brown ** 2)) + 1e-9
air = filt(rng.standard_normal(N), 2000, 9000); air /= np.sqrt(np.mean(air ** 2)) + 1e-9
amb = np.stack([0.010 * brown + 0.002 * air, np.roll(0.010 * brown + 0.002 * air, 900)], axis=1)
clock = np.zeros((N, 2))
for s_ in range(int(total)):
    n = int(0.02 * SR); fc = 3200 if s_ % 2 == 0 else 2500
    tk = filt(rng.standard_normal(n), fc * 0.7, fc * 1.4) * np.exp(-np.arange(n) / (0.003 * SR)); i = int((s_ + 0.5) * SR)
    if i + n < N: clock[i:i + n, 0] += tk * 0.030; clock[i:i + n, 1] += tk * 0.042
amb += clock

# ściszanie pod głosem (sidechain)
win = int(0.03 * SR); e2 = np.sqrt(np.convolve(voice ** 2, np.ones(win) / win, mode="same"))
envv = np.zeros_like(e2); a_up, a_dn = 1 - math.exp(-1 / (0.02 * SR)), 1 - math.exp(-1 / (0.35 * SR)); cur = 0.0
for i in range(0, N, 64):  # zgrubnie, potem interpolacja
    tgt = min(1.0, e2[i] / 0.08); cur += (tgt - cur) * (1 - (1 - (a_up if tgt > cur else a_dn)) ** 64); envv[i:i + 64] = cur
duck_sfx = (1 - 0.45 * envv)[:, None]; duck_amb = (1 - 0.35 * envv)[:, None]
mix = np.stack([voice, voice], axis=1) * 0.92 + sfx * duck_sfx + amb * duck_amb
fi = int(0.4 * SR); mix[:fi] *= np.linspace(0, 1, fi)[:, None]
fo = int(1.2 * SR); mix[N - fo:] *= np.linspace(1, 0, fo)[:, None]
mix /= max(1.0, np.max(np.abs(mix)) / 0.95)
with wave.open(f"{OUT}/dzwiek_mix.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(mix, -1, 1) * 32767).astype("<i2").tobytes())
print("mix ok", round(total, 2))
