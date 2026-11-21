import sys, asyncio, math
sys.path.insert(0, "/home/claude/faceless-konta/tools")
from templates import links, page
FONTS = links(["poppins/900-italic.css", "poppins/800.css", "poppins/600.css"]) if True else ""
Y, P = "#FFD21F", "#FF4FA0"
CSS = f"""
body{{margin:0}} .f{{width:1920px;height:1080px;position:relative;overflow:hidden;background:#111317;font-family:Poppins;color:#fff}}
.f:before{{content:"";position:absolute;inset:0;background:radial-gradient(1200px 700px at 60% 55%,rgba(255,255,255,.06),transparent 70%)}}
.grain{{position:absolute;inset:0;opacity:.10;mix-blend-mode:overlay;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}}
.bar{{position:absolute;left:0;right:0;top:0;height:250px;background:#0a0b0d}}
.h{{position:absolute;left:90px;top:38px;font-weight:900;font-style:italic;font-size:118px;line-height:1;text-transform:uppercase;letter-spacing:-2px}}
.sub{{position:absolute;left:96px;top:178px;font-weight:600;font-size:40px;color:#e9e9e9}}
.src{{position:absolute;left:60px;bottom:40px;font-weight:600;font-size:26px;color:#9aa0a8;letter-spacing:1px}}
.badge{{position:absolute;right:70px;bottom:40px;width:96px;height:96px;border-radius:50%;background:{Y};color:#111;font-weight:900;font-style:italic;font-size:52px;display:flex;align-items:center;justify-content:center;transform:rotate(-8deg);box-shadow:0 6px 0 #000}}
.chyba{{position:absolute;padding:8px 26px;border-radius:30px;background:{P};color:#fff;font-weight:900;font-style:italic;font-size:44px;transform:rotate(-6deg);box-shadow:0 6px 0 #000}}
.card{{position:absolute;background:#1c1f25;border-radius:34px;border:6px solid #fff;box-shadow:0 10px 0 #000;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.emo{{font-family:'Noto Color Emoji';font-size:170px;line-height:1}}
.lab{{font-weight:800;font-size:44px;margin-top:14px;text-transform:uppercase}}
.stamp{{position:absolute;border:10px solid #ff3b3b;color:#ff3b3b;font-weight:900;font-style:italic;font-size:92px;padding:6px 34px;border-radius:16px;transform:rotate(-12deg);opacity:.92;letter-spacing:2px}}
.logo{{position:absolute;right:190px;bottom:52px;font-weight:900;font-style:italic;font-size:34px;color:#fff;opacity:.85}}
"""
def bear(x, y, s=1.0, helmet=True):
    hel = (f'<path d="M-118 -40 C-110 -150 110 -150 118 -40 Z" fill="#55652f" stroke="#fff" stroke-width="10" paint-order="stroke"/>'
           f'<rect x="-140" y="-52" width="280" height="26" rx="13" fill="#46552a" stroke="#fff" stroke-width="8" paint-order="stroke"/>') if helmet else ""
    return f"""<svg style="position:absolute;left:{x}px;top:{y}px;overflow:visible" width="1" height="1"><g transform="scale({s})">
<g stroke="#fff" stroke-width="12" paint-order="stroke">
<circle cx="-92" cy="-70" r="44" fill="#7b4a22"/><circle cx="92" cy="-70" r="44" fill="#7b4a22"/>
<circle cx="-92" cy="-70" r="22" fill="#c08a5a" stroke="none"/><circle cx="92" cy="-70" r="22" fill="#c08a5a" stroke="none"/>
<ellipse cx="0" cy="10" rx="138" ry="124" fill="#8b5a2b"/></g>
<ellipse cx="0" cy="62" rx="66" ry="50" fill="#d2a679"/><ellipse cx="0" cy="38" rx="26" ry="18" fill="#1a1110"/>
<path d="M-16 74 Q0 88 16 74" stroke="#1a1110" stroke-width="7" fill="none" stroke-linecap="round"/>
<circle cx="-50" cy="-8" r="16" fill="#111"/><circle cx="50" cy="-8" r="16" fill="#111"/><circle cx="-44" cy="-14" r="5" fill="#fff"/><circle cx="56" cy="-14" r="5" fill="#fff"/>
{hel}</g></svg>"""
F1 = f"""<div class="f"><div class="bar"></div><div class="h" style="color:{Y}">W POLSKIEJ ARMII SŁUŻYŁ…</div>
<div class="sub">kapral, o którym nie uczą w szkole</div>
<div class="card" style="left:190px;top:350px;width:440px;height:440px;transform:rotate(-4deg)"><div class="emo">🍺</div><div class="lab">pił piwo</div></div>
<div class="card" style="left:740px;top:330px;width:440px;height:440px;transform:rotate(3deg)"><div class="emo">🚬</div><div class="lab">jadł papierosy</div></div>
<div class="card" style="left:1290px;top:360px;width:440px;height:440px;transform:rotate(-2deg)"><div class="emo">🤼</div><div class="lab">mocował się</div></div>
<div class="src">ŹRÓDŁO: BRITANNICA, BRITISH LIBRARY</div><div class="logo">nie wiem, ale bangla</div><div class="badge">?!</div><div class="grain"></div></div>"""
F2 = f"""<div class="f"><div class="bar"></div><div class="h" style="color:{Y}">SZEREGOWY WOJTEK</div>
<div class="sub">tak go wpisano, żeby mógł płynąć na front (według większości relacji)</div>
<div class="card" style="left:360px;top:330px;width:1200px;height:600px;align-items:flex-start;justify-content:flex-start;padding:0;border-color:{Y}">
 <div style="position:absolute;left:60px;top:50px;width:380px;height:470px;border-radius:22px;background:#2a2f37"></div>
 <div style="position:absolute;left:500px;top:70px;font-weight:800;font-size:38px;color:#9aa0a8">KSIĄŻECZKA ŻOŁNIERZA</div>
 <div style="position:absolute;left:500px;top:140px;font-weight:900;font-style:italic;font-size:86px">WOJTEK</div>
 <div style="position:absolute;left:500px;top:260px;font-weight:600;font-size:38px;line-height:1.6">stopień: <b>szeregowy</b><br>jednostka: 22. Kompania Zaopatrywania Artylerii<br>gatunek: <b style="color:{Y}">niedźwiedź</b></div></div>
{bear(610, 620, 1.05)}
<div class="stamp" style="left:1290px;top:470px">WCIELONY</div>
<div class="src">ŹRÓDŁO: BBC WILDLIFE, BRITANNICA</div><div class="logo">nie wiem, ale bangla</div><div class="badge">?!</div><div class="grain"></div></div>"""
# mapa – uproszczone położenia (dł./szer. geogr. → px)
pts = [("Szkocja", -3.2, 55.9), ("Monte Cassino", 13.8, 41.5), ("Egipt", 31.2, 30.0), ("Palestyna", 35.2, 31.8), ("Syria", 36.3, 33.5), ("Irak", 44.4, 33.3), ("Iran", 51.4, 35.7)]
def xy(lo, la): return 160 + (lo + 8) * 26.5, 1030 - (la - 25) * 21
route = [xy(lo, la) for _, lo, la in reversed(pts)]
d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in route)
dots = "".join(f'<circle cx="{xy(lo,la)[0]:.0f}" cy="{xy(lo,la)[1]:.0f}" r="16" fill="{P if n=="Monte Cassino" else Y}" stroke="#111" stroke-width="6"/>' for n, lo, la in pts)
OFF = {"Syria": (-60, -70), "Palestyna": (-275, -40), "Egipt": (-20, 26), "Irak": (-20, -66), "Iran": (24, -58), "Szkocja": (30, -24), "Monte Cassino": (24, -58)}
labs = "".join(f'<div style="position:absolute;left:{xy(lo,la)[0]+OFF[n][0]:.0f}px;top:{xy(lo,la)[1]+OFF[n][1]:.0f}px;font-weight:800;font-size:36px;text-shadow:0 4px 0 #000">{n}</div>' for n, lo, la in pts)
F3 = f"""<div class="f"><div class="bar"></div><div class="h" style="color:{P}">TRASA WOJTKA</div><div class="sub">1942–1947: z Iranu aż do Szkocji</div>
<svg style="position:absolute;left:0;top:0" width="1920" height="1080"><defs><pattern id="g" width="60" height="60" patternUnits="userSpaceOnUse"><path d="M60 0 L0 0 0 60" fill="none" stroke="rgba(255,255,255,.05)" stroke-width="2"/></pattern></defs>
<rect y="250" width="1920" height="830" fill="url(#g)"/><path d="{d}" fill="none" stroke="#fff" stroke-width="8" stroke-dasharray="22 16" stroke-linecap="round"/>{dots}</svg>{labs}
{bear(int(xy(13.8,41.5)[0])-40, int(xy(13.8,41.5)[1])+170, 0.55)}
<div class="chyba" style="left:1270px;top:320px">bez paszportu (chyba)</div>
<div class="src">MAPA UPROSZCZONA</div><div class="logo">nie wiem, ale bangla</div><div class="badge">?!</div><div class="grain"></div></div>"""
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": 1920, "height": 1080})
        for i, body in enumerate([F1, F2, F3], 1):
            f = f"/home/claude/bangla-yt/styl/_k{i}.html"; open(f, "w", encoding="utf-8").write(page(FONTS, CSS, body, 1920, 1080))
            await pg.goto(f"file://{f}", wait_until="networkidle"); await pg.evaluate("document.fonts.ready.then(()=>0)"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=f"/home/claude/bangla-yt/styl/kadr{i}.jpg", type="jpeg", quality=88)
        await b.close()
asyncio.run(main())
