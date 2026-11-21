import math, asyncio, sys
sys.path.insert(0, "/home/claude/faceless/yt/odc1")
from engine import FONTS, CSS, DEFS, MASCOT, page, CH
R = math.pi / 180
def arm(a):
    ex, ey = math.sin(a[0]*R)*72, 175 + math.cos(a[0]*R)*72
    return f"M0 175 L{ex:.1f} {ey:.1f} L{ex+math.sin(a[1]*R)*68:.1f} {ey+math.cos(a[1]*R)*68:.1f}"
m = MASCOT.replace('<path id="mL"/>', f'<path d="{arm([-110,-118])}"/>').replace('<path id="mR"/>', f'<path d="{arm([63,-35])}"/>')
m = m.replace('<path id="lL"/>', '<path d="M0 330 L-43 471"/>').replace('<path id="lR"/>', '<path d="M0 330 L43 471"/>')
m = m.replace('<g id="mhead">', '<g id="mhead" transform="rotate(-4 0 128)">').replace('id="mascot"', 'id="mascot" style="left:990px;top:95px;transform:scale(0.98);transform-origin:160px 511px"')
body = f"""<div class="b" style="width:1280px;height:720px">{DEFS}<div class="board"></div>
<div class="smudge" style="left:600px;top:40px;width:600px;height:260px"></div>
<div class="tx ch cv" style="visibility:visible;left:70px;top:40px;font-size:190px;transform:rotate(-2deg)">OD</div>
<div class="tx ch cv y" style="visibility:visible;left:56px;top:235px;font-size:132px;transform:rotate(-2deg)">PONIEDZIAŁKU</div>
<svg class="lay" style="width:1280px;height:720px"><path filter="url(#chalkp)" d="M40 318 C280 300 560 326 840 296" stroke="#E07A6A" stroke-width="14" style="visibility:visible;fill:none;stroke-linecap:round"/></svg>
<div class="tx ch cv" style="visibility:visible;left:430px;top:400px;font-size:200px;transform:rotate(-4deg)">DZIŚ!</div>
{m}<div class="brand" style="right:40px;bottom:26px;font-size:40px">ukryta lekcja</div><div class="dust"></div></div>"""
html = page(FONTS, CSS, body, 1280, 720)
open("/home/claude/faceless/yt/odc1/paczka/_thumb.html", "w", encoding="utf-8").write(html)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": 1280, "height": 720})
        await pg.goto("file:///home/claude/faceless/yt/odc1/paczka/_thumb.html", wait_until="networkidle")
        await pg.evaluate("document.fonts.ready.then(()=>0)"); await pg.wait_for_timeout(300)
        await pg.screenshot(path="/home/claude/faceless/yt/odc1/paczka/miniaturka.jpg", type="jpeg", quality=92)
        await b.close()
asyncio.run(main())
