import sys, asyncio, subprocess, glob, os
from boards import build
from engine import stills
bs = build()
which = sys.argv[1:] or [b.name for b in bs]
spec = {}
for b in bs:
    if b.name not in which: continue
    spec[b.name] = [round(b.end - 0.4, 2)]
extra = {"b03": [-1.2], "b14": [-1.6], "b15": [-2.6], "b18": [-2.4], "b33": [-3.0], "b27": [-3.0]}
for n, offs in extra.items():
    if n in spec:
        b = [x for x in bs if x.name == n][0]; spec[n] += [round(b.end + o, 2) for o in offs]
os.makedirs("qa", exist_ok=True)
for f in glob.glob("qa/kadr_*.jpg"): os.remove(f)
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
