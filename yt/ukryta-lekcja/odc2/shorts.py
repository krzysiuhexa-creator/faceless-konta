"""3 Shortsy 1080x1920 z odcinka 2: kadr z gotowego filmu + tytuł kredą + napisy + plansza końcowa.
python3 shorts.py  (po zrobieniu paczka/film.mp4)"""
import asyncio, re, subprocess, os
from engine import FONTS, CSS, DEFS, page
from boards import F, S, E

D = "/home/claude/faceless/yt/odc2"
OUT = f"{D}/shorts"; os.makedirs(OUT, exist_ok=True)
SRC = f"{D}/paczka/film.mp4"
SHORTS = {
    "s1": dict(segs=[(0.0, E(3) + 0.35)], fids=[1, 2, 3], t1="ten cytat zna każdy.", t2="tylko autor się nie zgadza"),
    "s2": dict(segs=[(S(14) - 0.3, E(16) + 0.35)], fids=[14, 15, 16], t1="stary popcorn", t2="i twoje nawyki"),
    "s3": dict(segs=[(S(11) - 0.3, E(13) + 0.35)], fids=[11, 12, 13], t1="pół dnia", t2="na autopilocie"),
}
TAIL = 2.2
VY = 600; VW = 1000; VH = round(VW * 1080 / 1920 / 2) * 2

def bg_html(t1, t2):
    return f"""<div class="b" style="width:1080px;height:1920px">{DEFS}
<div class="board" style="background:radial-gradient(900px 1300px at 50% 42%,#262b2c,#15191a 75%)"></div>
<div class="tx ch cv y" style="visibility:visible;left:70px;top:70px;font-size:56px;opacity:.85">ukryta lekcja</div>
<div class="tx ch cv" style="visibility:visible;left:66px;top:190px;font-size:112px;transform:rotate(-1.5deg)">{t1}</div>
<div class="tx ch cv y" style="visibility:visible;left:66px;top:330px;font-size:112px;transform:rotate(-1.5deg)">{t2}</div>
<div class="ch" style="position:absolute;left:32px;top:{VY - 8}px;width:{VW + 6}px;height:{VH + 6}px;border:5px solid rgba(237,235,228,.5);border-radius:14px"></div>
<div class="dust"></div></div>
<script>document.querySelectorAll('.tx').forEach(e=>{{let s=parseFloat(e.style.fontSize);while(e.scrollWidth>950&&s>40){{s-=2;e.style.fontSize=s+'px'}}}})</script>"""

END = f"""<div style="position:relative;width:1080px;height:1920px">
<div style="position:absolute;left:0;top:{VY - 40}px;width:1080px;height:{VH + 80}px;background:rgba(21,25,26,.94)"></div>
<div class="tx ch" style="visibility:visible;left:0;width:1080px;text-align:center;top:{VY + 110}px;font-size:56px;opacity:.85;color:#EDEBE4;font-family:Kalam">cały odcinek na kanale:</div>
<div class="tx ch cv y" style="visibility:visible;left:0;width:1080px;text-align:center;top:{VY + 210}px;font-size:96px;white-space:normal;line-height:1.05">dlaczego zawsze wracasz<br>do starych nawyków</div></div>"""

async def pngs():
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for k, s in SHORTS.items():
            f = f"{OUT}/_{k}_bg.html"; open(f, "w", encoding="utf-8").write(page(FONTS, CSS, bg_html(s["t1"], s["t2"]), 1080, 1920))
            await pg.goto(f"file://{f}", wait_until="networkidle"); await pg.evaluate("document.fonts.ready.then(()=>0)"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=f"{OUT}/_{k}_bg.png")
        f = f"{OUT}/_end.html"
        open(f, "w", encoding="utf-8").write(page(FONTS, CSS.replace("body{margin:0;background:#15191a}", "body{margin:0;background:transparent}"), DEFS + END, 1080, 1920))
        await pg.goto(f"file://{f}", wait_until="networkidle"); await pg.evaluate("document.fonts.ready.then(()=>0)"); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f"{OUT}/_end.png", omit_background=True)
        await b.close()

def tchar(fid, c):
    for cs, ce, ts, te in F[fid]["map"]:
        if cs <= c <= ce: return ts + (c - cs) / max(1, ce - cs) * (te - ts)
    return F[fid]["t1"]

def chunks(fids):
    out = []
    for fid in fids:
        txt = F[fid]["text"]; words = [(m.start(), m.group()) for m in re.finditer(r"\S+", txt)]
        cur, cs = [], None
        for i, (c, w) in enumerate(words):
            if not cur: cs = c
            cur.append(w)
            end_p = re.search(r"[.,?!:;…”]$", w)
            if len(cur) >= 4 or end_p or len(" ".join(cur)) >= 20 or i == len(words) - 1:
                out.append([tchar(fid, cs), tchar(fid, c + len(w)), " ".join(cur), fid]); cur = []
    for i in range(len(out) - 1):
        if out[i + 1][3] == out[i][3]: out[i][1] = out[i + 1][0]
        out[i][1] = max(out[i][1], out[i][0] + 0.3)
    return out

def at(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def make_ass(segs, fids, path):
    lines, off = [], 0.0
    for a, b in segs:
        for t0, t1, txt, fid in chunks(fids):
            if a - 0.05 <= t0 < b - 0.1:
                lines.append(f"Dialogue: 0,{at(t0 - a + off)},{at(min(t1, b) - a + off)},Cap,,0,0,0,,{{\\an5\\pos(540,1420)\\fscx90\\fscy90\\t(0,90,\\fscx100\\fscy100)}}{txt}")
        off += b - a
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Kalam,80,&H00E4EBED,&H00FFFFFF,&H001A1915,&H00000000,-1,0,0,0,100,100,0,0,1,7,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    open(path, "w", encoding="utf-8").write(head + "\n".join(lines) + "\n")

def build():
    asyncio.run(pngs())
    for k, s in SHORTS.items():
        segs = s["segs"]; dur = sum(b - a for a, b in segs)
        make_ass(segs, s["fids"], f"{OUT}/{k}.ass")
        a, b = segs[0]
        fc = [f"[0:v]scale={VW}:{VH}:flags=lanczos,tpad=stop_mode=clone:stop_duration={TAIL}[cv]",
              f"[1:v][cv]overlay=35:{VY - 5}:shortest=1[base]",
              f"[2:v]format=rgba,fade=in:st={dur:.3f}:d=0.3:alpha=1[end]",
              f"[base][end]overlay=0:0:enable='gte(t,{dur:.3f})'[ov]",
              f"[ov]ass={OUT}/{k}.ass:fontsdir={OUT}/fonts,format=yuv420p[vout]",
              f"[0:a]apad=pad_dur={TAIL},afade=t=out:st={dur - 0.2:.3f}:d={TAIL:.2f},loudnorm=I=-14:TP=-1.5:LRA=11[aout]"]
        tmp, dst = f"{OUT}/short-{k}.tmp.mp4", f"{OUT}/short-{k}.mp4"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", SRC,
               "-loop", "1", "-framerate", "30", "-t", f"{dur + TAIL:.3f}", "-i", f"{OUT}/_{k}_bg.png",
               "-loop", "1", "-framerate", "30", "-t", f"{dur + TAIL:.3f}", "-i", f"{OUT}/_end.png",
               "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]", "-r", "30", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
               "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-t", f"{dur + TAIL:.3f}", tmp]
        r = subprocess.run(cmd)
        if r.returncode == 0:
            os.replace(tmp, dst); print("ok", k, round(dur + TAIL, 2))
        else: print("FAIL", k)

if __name__ == "__main__":
    build()
