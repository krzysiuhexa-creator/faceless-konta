import sys, math, asyncio
sys.path.insert(0, "/home/claude/faceless/yt/odc1")
from engine import FONTS, CSS, MASCOT, page, brain, barchart, steps, calendar, tree, cake, sprout, plane, star, arrow_up, smooth, ell, check, cross
W, H = 2560, 1440
SX0, SY0, SW, SH = (W - 1546) // 2, (H - 423) // 2, 1546, 423   # bezpieczny pas
R = math.pi / 180
def arm(a):
    ex, ey = math.sin(a[0]*R)*72, 175 + math.cos(a[0]*R)*72
    return f"M0 175 L{ex:.1f} {ey:.1f} L{ex+math.sin(a[1]*R)*68:.1f} {ey+math.cos(a[1]*R)*68:.1f}"
sc = 0.74; mcx = SX0 + 165; feet = SY0 + SH - 18
m = MASCOT.replace('<path id="mL"/>', f'<path d="{arm([-63,35])}"/>').replace('<path id="mR"/>', f'<path d="{arm([128,122])}"/>')
m = m.replace('<path id="lL"/>', '<path d="M0 330 L-43 471"/>').replace('<path id="lR"/>', '<path d="M0 330 L43 471"/>')
m = m.replace('<g id="mhead">', '<g id="mhead" transform="rotate(5 0 128)">').replace('<g id="eyes">', '<g id="eyes" transform="translate(6 0)">')
m = m.replace('id="mascot"', f'id="mascot" style="left:{mcx-160}px;top:{feet-511}px;transform:scale({sc});transform-origin:160px 511px"')
# rysunki kredą poza bezpiecznym pasem (widać na komputerze / TV)
doodles = []
def add(paths, color="#EDEBE4", w=8, op=0.42):
    for p in paths: doodles.append(f'<path d="{p}" stroke="{color}" stroke-width="{w}" opacity="{op}"/>')
add(brain(260, 720)); add(barchart(2300, 700)); add(steps(250, 1080), "#F5C542", op=0.5); add(calendar(2180, 980, 220, 190))
add(tree(560, 330)); add(cake(2020, 330)); add(sprout(380, 470)); add(plane(2300, 430))
add([star(1280, 250, 40, 17)], "#F5C542", op=0.55); add([star(860, 1200, 30, 13)], "#F5C542", op=0.5); add([star(1760, 1190, 34, 15)], "#F5C542", op=0.5)
add(["M700 1180 C900 1176 1100 1184 1300 1178 M1262 1152 L1302 1178 L1262 1204", "M960 1145 L957 1215"], op=0.4)
add(["M1520 1110 L1900 1110", smooth([(1530, 1000), (1620, 1045), (1720, 1080), (1820, 1098), (1900, 1104)])], op=0.38)
add([check(130, 1300, 1.4), check(210, 1300, 1.4), cross(2350, 1270, 1.2)], "#F5C542", op=0.45)
txt = lambda s, x, y, size, color, op, cls="": f'<div class="tx ch {cls}" style="visibility:visible;left:{x}px;top:{y}px;font-size:{size}px;color:{color};opacity:{op}">{s}</div>'
deco_txt = [txt("66 dni", 120, 170, 90, "#F5C542", .35, "cv"), txt("+82%", 2290, 150, 90, "#F5C542", .35, "cv"),
            txt("jeśli ___, to ___", 1420, 140, 70, "#EDEBE4", .3), txt("nigdy dwa razy z rzędu", 140, 1330, 54, "#EDEBE4", .28)]
tx0 = SX0 + 380
body = f"""<div class="b" style="width:{W}px;height:{H}px"><svg width="0" height="0" style="position:absolute">
<filter id="chb" filterUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><feTurbulence type="fractalNoise" baseFrequency="1.2" numOctaves="2" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="3"/><feComponentTransfer><feFuncA type="table" tableValues="0 .85 .95"/></feComponentTransfer></filter>
<filter id="chalk"><feTurbulence type="fractalNoise" baseFrequency="1.2" numOctaves="2" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3"/>
<feComponentTransfer><feFuncA type="table" tableValues="0 .85 .95"/></feComponentTransfer></filter></svg>
<div class="board" style="background:radial-gradient(1500px 800px at 50% 50%,#2a3031,#15191a 80%)"></div>
<div class="smudge" style="left:700px;top:420px;width:1200px;height:500px"></div><div class="smudge" style="left:200px;top:900px;width:800px;height:300px"></div>
<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0"><g filter="url(#chb)" fill="none" stroke-linecap="round" stroke-linejoin="round">{''.join(doodles)}
<path d="M{tx0} {SY0+262} C{tx0+300} {SY0+246} {tx0+700} {SY0+272} {tx0+1040} {SY0+250}" stroke="#F5C542" stroke-width="11"/></g></svg>
{''.join(deco_txt)}
{txt("ukryta lekcja", tx0, SY0 + 52, 200, "#F5C542", 1, "cv")}
{txt("krótkie lekcje o tym, jak działa twoja głowa", tx0 + 6, SY0 + 296, 60, "#EDEBE4", .95)}
{m}<div class="dust"></div></div>"""
html = page(FONTS, CSS, body, W, H)
open("/home/claude/faceless/yt/kanal/_baner.html", "w", encoding="utf-8").write(html)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": W, "height": H})
        await pg.goto("file:///home/claude/faceless/yt/kanal/_baner.html", wait_until="networkidle")
        await pg.evaluate("document.fonts.ready.then(()=>0)"); await pg.wait_for_timeout(400)
        await pg.screenshot(path="/home/claude/faceless/yt/kanal/baner-kanalu.png")
        await b.close()
asyncio.run(main())
print(SX0, SY0, SW, SH)
