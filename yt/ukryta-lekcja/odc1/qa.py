import sys, asyncio, json, subprocess, glob, os
from boards import build
from engine import stills
bs = build()
which = sys.argv[1] if len(sys.argv) > 1 else "full"
spec = {}
for b in bs:
    if which == "full":
        t = (b.erase[0] - 0.15) if b.erase else b.end - 2.0
        spec[b.name] = [round(t, 2)]
    elif which == "mid":
        t = (b.start + (b.erase[0] if b.erase else b.end)) / 2
        spec[b.name] = [round(t, 2)]
    else:
        d = json.loads(which); spec.update(d)
for f in glob.glob("qa/kadr_*"): os.remove(f)
paths = asyncio.run(stills(bs, spec, "/home/claude/faceless/yt/odc1/qa"))
paths.sort()
for i in range(0, len(paths), 9):
    grp = paths[i:i + 9]
    while len(grp) < 9: grp.append(grp[-1])
    inp = sum([["-i", p] for p in grp], [])
    fc = "".join(f"[{k}]scale=640:360,drawtext=text='{os.path.basename(grp[k])[5:-4]}':x=8:y=8:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.6[v{k}];" for k in range(9))
    fc += "[v0][v1][v2]hstack=3[a];[v3][v4][v5]hstack=3[b];[v6][v7][v8]hstack=3[c];[a][b][c]vstack=3"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inp, "-filter_complex", fc, f"qa/sheet_{which[:4]}_{i//9}.jpg"], check=True)
print("ok", len(paths))
