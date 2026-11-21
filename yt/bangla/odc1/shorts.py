"""3 Shortsy 1080x1920 z odcinka o Wojtku: kadrowanie gotowego filmu + tytuł + napisy + plansza końcowa."""
import asyncio, re, subprocess, wave, numpy as np, sys
from engine import FR, CSS, DEFS, FONTS, page, bear_head, Y, P, G
OUT = "/home/claude/bangla-yt/odc1/shorts"
SRC_V = "/home/claude/bangla-yt/odc1/paczka/Dziwne-historie-1-Wojtek.mp4"
SRC_A = "/home/claude/bangla-yt/odc1/dzwiek_final.wav"
SR = 44100
HOOK = (15.95, 20.09)   # „Ten kapral był niedźwiedziem. Nazywał się Wojtek.”
SHORTS = {
    "s1": dict(segs=[(0.0, 20.09), (123.10, 129.89)], t1="TEN KAPRAL", t2="JADŁ PAPIEROSY"),
    "s2": dict(segs=[HOOK, (142.47, 175.99)], t1="JAK PRZEMYCIĆ", t2="MISIA NA WOJNĘ?"),
    "s3": dict(segs=[HOOK, (280.35, 323.56)], t1="POLSKI KAPRAL", t2="W SZKOCKIM ZOO"),
}
TAIL = 1.8
CX, CY, CW, CH = 180, 262, 1560, 713      # kadr z filmu 16:9
HY = 470                                  # pasek z nagłówkiem planszy
HH = 154; HP = 22
VY = HY + HH + HP                         # treść planszy
VH = round(CH * 1080 / CW / 2) * 2

def _vf():
    y0 = HH + HP - 6
    return (f"split[a][b];[a]crop=1400:200:60:30,scale=1080:{HH}:flags=lanczos,pad=1080:{HH + HP}:0:0:color=0x0a0b0d,"
            f"drawbox=x=0:y={y0}:w=360:h=6:color=0xFFD21F:t=fill,drawbox=x=360:y={y0}:w=360:h=6:color=0xFF4FA0:t=fill,drawbox=x=720:y={y0}:w=360:h=6:color=white:t=fill[h];"
            f"[b]crop={CW}:{CH}:{CX}:{CY},scale=1080:{VH}:flags=lanczos[c];[h][c]vstack")
GRID = "background-image:linear-gradient(rgba(255,255,255,.035) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.035) 2px,transparent 2px);background-size:60px 60px"
def bg_html(t1, t2):
    return f"""<div style="position:relative;width:1080px;height:1920px;overflow:hidden;font-family:Poppins;color:#fff;background:radial-gradient(900px 900px at 50% 40%,#22262d,#111317 70%)">
<div style="position:absolute;inset:0;{GRID}"></div>
<div style="position:absolute;left:70px;top:112px;display:flex;align-items:center;gap:18px">
 <div style="width:74px;height:74px;border-radius:50%;background:{Y};color:#111;font-weight:900;font-style:italic;font-size:40px;display:flex;align-items:center;justify-content:center;box-shadow:0 5px 0 #000;transform:rotate(-8deg)">?!</div>
 <div style="font-weight:900;font-style:italic;font-size:38px">nie wiem, ale bangla</div>
 <div style="margin-left:6px;background:{P};font-weight:900;font-style:italic;font-size:26px;padding:4px 16px;border-radius:30px;transform:rotate(-6deg)">dziwne historie</div></div>
<div id="t" style="position:absolute;left:66px;top:205px;width:960px;font-weight:900;font-style:italic;line-height:1.02;letter-spacing:-2px;text-shadow:0 10px 0 #000;text-transform:uppercase">
 <div class="l" style="font-size:116px;white-space:nowrap">{t1}</div><div class="l" style="font-size:116px;white-space:nowrap;color:{Y}">{t2}</div></div>
<div style="position:absolute;left:0;right:0;top:{HY - 10}px;height:6px;background:linear-gradient(90deg,{Y} 0 33%,{P} 33% 66%,#fff 66%)"></div>
<div style="position:absolute;left:0;right:0;top:{VY + VH + 4}px;height:6px;background:linear-gradient(90deg,#fff 0 33%,{P} 33% 66%,{Y} 66%)"></div>
</div><script>document.querySelectorAll('#t .l').forEach(e=>{{let s=116;while(e.scrollWidth>950&&s>60){{s-=2;e.style.fontSize=s+'px'}}}})</script>"""

END = f"""<div style="position:relative;width:1080px;height:1920px;font-family:Poppins;color:#fff">
<div style="position:absolute;left:0;top:{HY}px;width:1080px;height:{VY + VH - HY}px;background:rgba(17,19,23,.88)"></div>
<div style="position:absolute;left:50%;top:{VY + 40}px;transform:translateX(-50%)">{bear_head(True, size=210)}</div>
<div style="position:absolute;left:0;right:0;top:{VY + 275}px;text-align:center;font-weight:900;font-style:italic;font-size:70px;line-height:1.05;text-shadow:0 8px 0 #000">CAŁA HISTORIA<br><span style="color:{Y}">NA KANALE</span></div></div>"""

async def pngs():
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for k, s in SHORTS.items():
            f = f"{OUT}/_{k}_bg.html"; open(f, "w", encoding="utf-8").write(page(FONTS, CSS, DEFS + bg_html(s["t1"], s["t2"]), 1080, 1920))
            await pg.goto(f"file://{f}", wait_until="networkidle"); await pg.evaluate("document.fonts.ready.then(()=>0)"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=f"{OUT}/_{k}_bg.png")
        f = f"{OUT}/_end.html"; open(f, "w", encoding="utf-8").write(page(FONTS, CSS.replace("body{margin:0;background:#111317}", "body{margin:0;background:transparent}"), DEFS + END, 1080, 1920))
        await pg.goto(f"file://{f}", wait_until="networkidle"); await pg.evaluate("document.fonts.ready.then(()=>0)"); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f"{OUT}/_end.png", omit_background=True)
        await b.close()

# ── napisy ──
def tchar(fid, c):
    for cs, ce, ts, te in FR[fid]["map"]:
        if cs <= c <= ce: return ts + (c - cs) / max(1, ce - cs) * (te - ts)
    return FR[fid]["t1"]

def chunks():
    out = []
    for fid in sorted(FR):
        txt = FR[fid]["text"]; words = [(m.start(), m.group()) for m in re.finditer(r"\S+", txt)]
        cur, cs = [], None
        for i, (c, w) in enumerate(words):
            if not cur: cs = c
            cur.append(w)
            end_punct = re.search(r"[.,?!:;…]$", w)
            weak = w.lower() in ("i", "a", "w", "z", "o", "u", "że", "do", "na", "po", "ze", "od", "jak", "się", "nie")
            if (len(cur) >= 3 or end_punct or len(" ".join(cur)) >= 16 or i == len(words) - 1) and not (weak and not end_punct and i < len(words) - 1 and len(cur) < 4):
                ce = c + len(w); out.append([tchar(fid, cs), tchar(fid, ce), " ".join(cur), fid]); cur = []
    for i in range(len(out) - 1):
        if out[i + 1][3] == out[i][3]: out[i][1] = out[i + 1][0]
        out[i][1] = max(out[i][1], out[i][0] + 0.25)
    return out

def ass_time(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def make_ass(segs, path):
    lines = []; off = 0.0
    for a, b in segs:
        for t0, t1, txt, fid in chunks():
            if t0 >= a - 0.05 and t0 < b - 0.1:
                s0, s1 = t0 - a + off, min(t1, b) - a + off
                lines.append(f"Dialogue: 0,{ass_time(s0)},{ass_time(s1)},Cap,,0,0,0,,{{\\an5\\pos(540,1270)\\fscx86\\fscy86\\t(0,90,\\fscx100\\fscy100)}}{txt.upper()}")
        off += b - a
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Poppins,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,-1,0,0,100,100,0,0,1,8,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    open(path, "w", encoding="utf-8").write(head + "\n".join(lines) + "\n")

# ── dźwięk ──
def read_wav(p):
    with wave.open(p) as w:
        ch = w.getnchannels(); a = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32767
    return a.reshape(-1, ch)

def write_wav(p, x):
    with wave.open(p, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())

def audio(segs, path, mus):
    full = read_wav(SRC_A); parts = []
    for i, (a, b) in enumerate(segs):
        x = full[int(a * SR):int(b * SR)].copy(); f = int(0.03 * SR)
        x[:f] *= np.linspace(0, 1, f)[:, None]; x[-f:] *= np.linspace(1, 0, f)[:, None]; parts.append(x)
    b = segs[-1][1]; n = int(TAIL * SR)
    tail = mus[int(b * SR):int(b * SR) + n].copy(); tail *= np.linspace(1, 0, n)[:, None] ** 1.5
    parts.append(tail)
    write_wav(path, np.concatenate(parts))

def build():
    global VF
    VF = _vf()
    asyncio.run(pngs())
    sys.argv = ["x"]
    import mix as M
    from boards import build as bb, A
    bs = bb(); N = int(bs[-1].end * SR) + 1
    mus = M.music(N, A(24, "robi się smutna") - 0.2, FR[32]["t0"] - 0.3, bs[-1].end) * 0.30
    for k, s in SHORTS.items():
        segs = s["segs"]; dur = sum(b - a for a, b in segs)
        make_ass(segs, f"{OUT}/{k}.ass"); audio(segs, f"{OUT}/{k}_audio.wav", mus)
        parts = []
        for i, (a, b) in enumerate(segs):
            p = f"{OUT}/_{k}_seg{i}.mp4"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{a:.3f}", "-i", SRC_V, "-t", f"{b - a:.3f}", "-an",
                            "-vf", VF, "-r", "30", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", p], check=True)
            parts.append(p)
        lst = f"{OUT}/_{k}_list.txt"; open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{OUT}/_{k}_main.mp4"], check=True)
        fc = [f"[0:v]tpad=stop_mode=clone:stop_duration={TAIL}[cv]",
              f"[1:v][cv]overlay=0:{HY}:shortest=1[base]",
              f"[2:v]format=rgba,fade=in:st={dur}:d=0.25:alpha=1[end]",
              f"[base][end]overlay=0:0:enable='gte(t,{dur})'[ov]",
              f"[ov]ass={OUT}/{k}.ass,format=yuv420p[vout]"]
        tmp, dst = f"{OUT}/short-{k}.tmp.mp4", f"{OUT}/short-{k}.mp4"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", f"{OUT}/_{k}_main.mp4", "-loop", "1", "-framerate", "30", "-t", str(dur + TAIL), "-i", f"{OUT}/_{k}_bg.png",
               "-loop", "1", "-framerate", "30", "-t", str(dur + TAIL), "-i", f"{OUT}/_end.png", "-i", f"{OUT}/{k}_audio.wav",
               "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "3:a", "-r", "30", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
               "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", f"{dur + TAIL:.3f}", tmp]
        r = subprocess.run(cmd)
        if r.returncode == 0:
            import os; os.replace(tmp, dst); print("ok", k, round(dur + TAIL, 2))
        else: print("FAIL", k)

if __name__ == "__main__":
    build()
