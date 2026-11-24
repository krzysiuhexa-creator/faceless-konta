import sys, asyncio, subprocess, glob, os
from boards import build
from engine import stills
bs = build()
which = sys.argv[1:] or [b.name for b in bs]
spec = {}
for b in bs:
    if b.name not in which: continue
    d = b.end - b.start
    # tuż przed końcem + środek + najgęstszy moment (ostatnie wejście elementu)
    spec[b.name] = sorted({round(b.end - 0.4, 2), round(b.start + d * 0.45, 2)})
os.makedirs("qa", exist_ok=True)
for f in glob.glob("qa/kadr_*.jpg") + glob.glob("qa/sheet_*.jpg"): os.remove(f)
res = asyncio.run(stills(bs, spec, "qa"))
res.sort()
for i in range(0, len(res), 4):
    grp = res[i:i + 4]
    args = []
    for g in grp: args += ["-i", g]
    n = len(grp)
    while n < 4: args += ["-f", "lavfi", "-i", "color=c=black:s=1920x1080"]; n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + args + ["-filter_complex",
        "[0]scale=960:540[a];[1]scale=960:540[b];[2]scale=960:540[c];[3]scale=960:540[d];[a][b]hstack[t];[c][d]hstack[u];[t][u]vstack",
        "-frames:v", "1", "-q:v", "3", f"qa/sheet_{i // 4:02d}.jpg"])
print(len(res), "kadrów")
