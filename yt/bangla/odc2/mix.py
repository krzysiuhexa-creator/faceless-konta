"""Miks Bangla: lektor + efekty (z animacji) + podkład (groove → smutne akordy → groove) → dzwiek_mix.wav"""
import math, wave, numpy as np
from numba import njit
from scipy.signal import butter, sosfilt, fftconvolve
from boards import build, A, E, FR, TL

SR = 44100
OUT = "/home/claude/bangla-yt/odc2"
rng = np.random.default_rng(7)


def read_wav(p):
    with wave.open(p) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32767

def filt(x, lo=None, hi=None, order=2):
    if lo and hi: sos = butter(order, [lo, hi], btype="band", fs=SR, output="sos")
    elif lo: sos = butter(order, lo, btype="high", fs=SR, output="sos")
    else: sos = butter(order, hi, btype="low", fs=SR, output="sos")
    return sosfilt(sos, x)

def env(n, a, r):
    e = np.ones(n); na, nr = max(1, int(a * SR)), max(1, int(r * SR)); e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return e

def tone(f, d, decay=None, harm=(1,), phase_jit=False):
    n = int(d * SR); t = np.arange(n) / SR
    if callable(f): ph = 2 * np.pi * np.cumsum(f(t)) / SR
    else: ph = 2 * np.pi * f * t
    s = sum(a * np.sin((k + 1) * ph) for k, a in enumerate(harm))
    if decay: s = s * np.exp(-t / decay)
    return s

@njit(cache=True)
def ks(n, period, damp, seed_noise):
    buf = seed_noise.copy(); out = np.zeros(n); L = len(buf); i = 0
    for k in range(n):
        v = buf[i]; nxt = buf[(i + 1) % L]
        out[k] = v; buf[i] = damp * 0.5 * (v + nxt); i = (i + 1) % L
    return out

def pluck(f, d, bright=0.6, damp=0.996):
    L = max(2, int(SR / f)); seed = filt(rng.standard_normal(L + 64), None, 2000 + 6000 * bright)[:L]
    s = ks(int(d * SR), L, damp, seed.astype(np.float64)); return s / (np.max(np.abs(s)) + 1e-9) * env(len(s), 0.002, 0.05)


# ─────────── efekty ───────────
def sfx_bank(kind, extra):
    r = rng.uniform
    if kind == "pop":
        f0 = r(650, 950); s = tone(lambda t: f0 * np.exp(-t * 18) + 260, 0.09, decay=0.03)
        c = filt(rng.standard_normal(int(0.008 * SR)), 2500, 9000) * 0.25; s[:len(c)] += c
        return s * 0.6
    if kind in ("swish", "swish_s", "whip", "swipe"):
        d = {"swish": 0.26, "swish_s": 0.17, "whip": 0.32, "swipe": extra[0] if extra else 0.3}[kind]; d = min(max(d, 0.15), 0.6)
        n = int(d * SR); u = np.arange(n) / n
        lo, hi = (500, 7000) if kind == "whip" else (900, 6000)
        s = filt(rng.standard_normal(n), lo, hi) * np.sin(np.pi * u ** (0.7 if kind == "whip" else 1.0)) ** 2
        return s * {"swish": 0.28, "swish_s": 0.18, "whip": 0.42, "swipe": 0.16}[kind]
    if kind == "stamp":
        body = tone(lambda t: 110 * np.exp(-t * 9) + 48, 0.32, decay=0.09)
        slap = filt(rng.standard_normal(int(0.05 * SR)), 300, 3500) * np.exp(-np.arange(int(0.05 * SR)) / (0.009 * SR))
        s = body * 0.9; s[:len(slap)] += slap * 0.8; return s
    if kind == "boom":
        a = extra[0] if extra else 0.7
        s = tone(lambda t: 70 * np.exp(-t * 4) + 38, 0.55, decay=0.16) + 0.3 * filt(rng.standard_normal(int(0.55 * SR)), None, 400) * np.exp(-np.arange(int(0.55 * SR)) / (0.05 * SR))
        return s * 0.75 * a
    if kind == "hit":
        n = int(0.16 * SR); k = np.arange(n) / SR
        return (filt(rng.standard_normal(n), 1200, 7000) * np.exp(-k / 0.03) * 0.25 + tone(lambda t: 190 * np.exp(-t * 6) + 90, 0.16, decay=0.05) * 0.35)
    if kind == "snap":
        n = int(0.06 * SR); return filt(rng.standard_normal(n), 1500, 9000) * np.exp(-np.arange(n) / (0.008 * SR)) * 0.5
    if kind == "marker":
        d = min(max(extra[0] if extra else 0.5, 0.2), 2.0); n = int(d * SR); t = np.arange(n) / SR
        am = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * r(6, 10) * t))
        return filt(rng.standard_normal(n), 2200, 6500) * am * env(n, 0.02, 0.06) * 0.10
    if kind == "rise":
        d = min(max(extra[0] if extra else 1.0, 0.4), 2.0)
        return tone(lambda t: 260 + 700 * (t / d) ** 2, d, harm=(1, 0.3)) * env(int(d * SR), 0.3 * d, 0.08) * 0.13
    if kind == "ticks":
        d = extra[0] if extra else 1.0; n = int(d * SR) + 1; s = np.zeros(n); tt = 0.0
        while tt < d:
            m = int(0.012 * SR); i = int(tt * SR)
            if i + m < n: s[i:i + m] += filt(rng.standard_normal(m), 2500, 8000) * np.exp(-np.arange(m) / (0.002 * SR))
            tt += 1 / 18
        return s * 0.3
    if kind == "ding":
        return sum(a * tone(f, 0.9, decay=dc) for f, a, dc in [(1318.5, 0.5, 0.35), (2637, 0.25, 0.18), (3951, 0.12, 0.1), (1975.5, 0.18, 0.25)]) * 0.45
    if kind == "buzz":
        n = int(0.38 * SR); t = np.arange(n) / SR
        s = np.sign(np.sin(2 * np.pi * 138 * t)) + np.sign(np.sin(2 * np.pi * 146 * t))
        return filt(s, None, 1800) * env(n, 0.005, 0.06) * 0.12
    if kind == "alarm":
        d = 1.3; return tone(lambda t: 820 + 230 * np.sin(2 * np.pi * 1.6 * t), d, harm=(1, 0.35)) * env(int(d * SR), 0.05, 0.3) * 0.10
    if kind == "sad":
        s = np.zeros(int(2.4 * SR))
        for i, f in enumerate([659.25, 587.33, 523.25]):
            p = pluck(f, 1.6, bright=0.3, damp=0.9985) * 0.5; j = int(i * 0.42 * SR); s[j:j + len(p)] += p[:len(s) - j]
        return s * 0.5
    return None


def build_sfx(boards, N):
    sfx = np.zeros((N, 2))
    def add(sig, t, x, g=1.0):
        i = int(t * SR); p = 0.18 + 0.64 * min(max(x / 1920, 0), 1); n = min(len(sig), N - i)
        if n <= 0 or i < 0: return
        sfx[i:i + n, 0] += sig[:n] * g * math.cos(p * math.pi / 2); sfx[i:i + n, 1] += sig[:n] * g * math.sin(p * math.pi / 2)
    used = {}
    for b in boards:
        for e in b.events():
            kind, t, x = e[0], max(0.0, e[1]), e[2] if len(e) > 2 else 960
            key = (kind, round(t, 1))
            if kind in ("pop", "swish") and used.get(key): continue  # bez stłoczonych duplikatów
            used[key] = 1
            s = sfx_bank(kind, list(e[3:]))
            if s is None: print("?? efekt", kind); continue
            add(s, t, x)
    n_ir = int(0.3 * SR); ir = rng.standard_normal(n_ir) * np.exp(-np.arange(n_ir) / (0.05 * SR)); ir /= np.abs(ir).sum() / 5
    sfx = sfx + 0.12 * np.stack([fftconvolve(sfx[:, c], ir)[:N] for c in range(2)], axis=1)
    return sfx


# ─────────── podkład ───────────
BPM = 100; BEAT = 60 / BPM; BAR = 4 * BEAT
def midi(m): return 440 * 2 ** ((m - 69) / 12)
GROOVE = [(48, [60, 64, 67, 72]), (43, [59, 62, 67, 71]), (45, [57, 60, 64, 69]), (41, [57, 60, 65, 69])]  # C G Am F
SADP = [(45, [57, 60, 64]), (41, [57, 60, 65]), (48, [55, 60, 64]), (43, [55, 59, 62])]          # Am F C G


def music(N, sad_from, sad_to, end):
    out = np.zeros((N, 2)); T = N / SR
    def put(sig, t, pan=0.5, g=1.0):
        i = int(t * SR); n = min(len(sig), N - i)
        if n <= 0: return
        out[i:i + n, 0] += sig[:n] * g * math.cos(pan * math.pi / 2); out[i:i + n, 1] += sig[:n] * g * math.sin(pan * math.pi / 2)
    kick = tone(lambda t: 120 * np.exp(-t * 30) + 50, 0.3, decay=0.09)
    clap = filt(rng.standard_normal(int(0.18 * SR)), 900, 6000) * np.exp(-np.arange(int(0.18 * SR)) / (0.035 * SR))
    hat = filt(rng.standard_normal(int(0.05 * SR)), 6000, 14000) * np.exp(-np.arange(int(0.05 * SR)) / (0.01 * SR))
    plk_cache = {}
    def P(m, d=0.5, br=0.55):
        k = (m, d, br)
        if k not in plk_cache: plk_cache[k] = pluck(midi(m), d, bright=br)
        return plk_cache[k]
    bar = 0; t = 0.0
    while t < T:
        sad = sad_from <= t < sad_to
        if sad:
            root, ch = SADP[bar % 4]
            # pad: miękkie akordy
            d = BAR + 0.6; n = int(d * SR); e = env(n, 0.8, 1.0)
            pad = sum(np.sin(2 * np.pi * midi(m) * np.arange(n) / SR + 0.3 * np.sin(2 * np.pi * 0.25 * np.arange(n) / SR)) for m in ch) / len(ch)
            put(filt(pad, None, 1400) * e * 0.16, t, 0.35); put(filt(pad, None, 1400) * e * 0.16, t + 0.01, 0.65)
            put(tone(midi(root - 12), BAR, decay=1.5) * 0.18, t, 0.5)
            for k, m in enumerate([ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 12]):
                put(P(m, 1.2, 0.3) * 0.16, t + k * BEAT, 0.3 + 0.4 * (k % 2))
        else:
            root, ch = GROOVE[bar % 4]
            intro = t < 0.5
            for k in range(4):
                tb = t + k * BEAT
                if k in (0, 2) and not intro: put(kick * 0.55, tb, 0.5)
                if k in (1, 3): put(clap * 0.16, tb, 0.55)
                for h in (0, 1):
                    put(hat * (0.07 if h == 0 else 0.045), tb + h * BEAT / 2 + (0.03 if h else 0), 0.7)
            for tb, m in [(0, root), (1.5, root), (2, root + 7), (3.5, root + 12)]:
                d = 0.42; n = int(d * SR); tt = np.arange(n) / SR
                bs = (np.sin(2 * np.pi * midi(m - 12) * tt) + 0.3 * np.sin(4 * np.pi * midi(m - 12) * tt)) * np.exp(-tt / 0.25) * env(n, 0.005, 0.04)
                put(bs * 0.30, t + tb * BEAT, 0.5)
            arp = [ch[0], ch[2], ch[1], ch[3], ch[2], ch[1], ch[3], ch[2]]
            for k, m in enumerate(arp):
                put(P(m + 12, 0.5) * 0.11, t + k * BEAT / 2 + (0.02 if k % 2 else 0), 0.25 + 0.5 * (k % 2))
        t += BAR; bar += 1
    # przejścia: wyciszenie przed smutną częścią, powrót, koniec
    g = np.ones(N)
    def ramp(a, b, v0, v1):
        i0, i1 = int(a * SR), int(b * SR); g[i0:i1] = np.linspace(v0, v1, i1 - i0)
    i_end = int(end * SR)
    ramp(end - 2.5, end, 1, 0); g[i_end:] = 0
    out *= g[:, None]
    return out


def duck_env(voice):
    N = len(voice); win = int(0.03 * SR); e2 = np.sqrt(np.convolve(voice ** 2, np.ones(win) / win, mode="same"))
    envv = np.zeros(N); up, dn = 1 - math.exp(-64 / (0.03 * SR)), 1 - math.exp(-64 / (0.45 * SR)); cur = 0.0
    for i in range(0, N, 64):
        tgt = min(1.0, e2[i] / 0.06); cur += (tgt - cur) * (up if tgt > cur else dn); envv[i:i + 64] = cur
    return envv


def make_mix(boards, voice_src, out_path):
    total = boards[-1].end; N = int(total * SR) + 1
    voice = np.zeros(N, dtype=np.float32); voice[:min(N, len(voice_src))] = voice_src[:N]
    voice = filt(voice, 70, None).astype(np.float32)
    sfx = build_sfx(boards, N)
    sad_from = FR[21]["t0"] - 0.3   # cisza: Lustig czeka na gazety
    sad_to = FR[23]["t0"] - 0.3
    mus = music(N, sad_from, sad_to, total)
    # muzyka cichnie płynnie na granicach smutnej części (crossfade 1.2 s)
    g = np.ones(N)
    for a in (sad_from, sad_to):
        i0, i1 = int((a - 0.6) * SR), int((a + 0.6) * SR); g[i0:i1] = np.minimum(g[i0:i1], np.abs(np.linspace(-1, 1, i1 - i0)) * 0.7 + 0.3)
    mus *= g[:, None]
    ev = duck_env(voice)
    mix = (np.stack([voice, voice], axis=1) * 1.0 + sfx * 0.45 * (1 - 0.35 * ev)[:, None] + mus * 0.27 * (1 - 0.5 * ev)[:, None])
    fi = int(0.05 * SR); mix[:fi] *= np.linspace(0, 1, fi)[:, None]
    mix /= max(1.0, np.max(np.abs(mix)) / 0.95)
    with wave.open(out_path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(mix, -1, 1) * 32767).astype("<i2").tobytes())
    print("mix ok", round(total, 2), "smutne:", round(sad_from, 1), "-", round(sad_to, 1))


if __name__ == "__main__":
    make_mix(build(), read_wav(f"{OUT}/lektor_cut.wav"), f"{OUT}/dzwiek_mix.wav")
