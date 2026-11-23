import math, asyncio, sys
sys.path.insert(0, "/home/claude/faceless/yt/odc2")
from engine import FONTS, CSS, DEFS, MASCOT, page, CH
R = math.pi / 180
def arm(a):
    ex, ey = math.sin(a[0]*R)*72, 175 + math.cos(a[0]*R)*72
    return f"M0 175 L{ex:.1f} {ey:.1f} L{ex+math.sin(a[1]*R)*68:.1f} {ey+math.cos(a[1]*R)*68:.1f}"
m = MASCOT.replace('<path id="mL"/>', f'<path d="{arm([-63,35])}"/>').replace('<path id="mR"/>', f'<path d="{arm([54,200])}"/>')
m = m.replace('<path id="lL"/>', '<path d="M0 330 L-43 471"/>').replace('<path id="lR"/>', '<path d="M0 330 L43 471"/>')
m = m.replace('<g id="mhead">', '<g id="mhead" transform="rotate(8 0 128)">').replace('id="mascot"', 'id="mascot" style="left:900px;top:120px;transform:scale(1.0);transform-origin:160px 511px"')
import random
random.seed(5)
gr = " ".join(f"M{random.uniform(20,980):.0f} {random.uniform(380,700):.0f} l{random.uniform(-5,5):.0f} -{random.uniform(14,26):.0f}" for _ in range(170))
body = f"""<div class="b" style="width:1280px;height:720px">{DEFS}<div class="board"></div>
<div class="smudge" style="left:600px;top:40px;width:600px;height:260px"></div>
<svg class="lay" style="width:1280px;height:720px"><g filter="url(#chalkp)" style="fill:none;stroke-linecap:round">
<path d="{gr}" stroke="#EDEBE4" stroke-width="4" opacity=".75" style="visibility:visible"/>
<path d="M0 560 C400 600 760 660 1080 700" stroke="rgba(237,235,228,.28)" stroke-width="70" style="visibility:visible"/>
<path d="M1020 690 C860 580 640 470 330 410" stroke="rgba(245,197,66,.45)" stroke-width="60" style="visibility:visible"/>
</g></svg>
<div class="tx ch cv y" style="visibility:visible;left:60px;top:20px;font-size:230px;transform:rotate(-3deg)">ZNOWU?</div>
<div class="tx ch cv" style="visibility:visible;left:70px;top:250px;font-size:84px;transform:rotate(-2deg)">stare nawyki wracają</div>
{m}<div class="brand" style="right:40px;bottom:26px;font-size:40px">ukryta lekcja</div><div class="dust"></div></div>"""
html = page(FONTS, CSS, body, 1280, 720)
open("/home/claude/faceless/yt/odc2/paczka/_thumb.html", "w", encoding="utf-8").write(html)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": 1280, "height": 720})
        await pg.goto("file:///home/claude/faceless/yt/odc2/paczka/_thumb.html", wait_until="networkidle")
        await pg.evaluate("document.fonts.ready.then(()=>0)"); await pg.wait_for_timeout(300)
        await pg.screenshot(path="/home/claude/faceless/yt/odc2/paczka/miniaturka.jpg", type="jpeg", quality=92)
        await b.close()
asyncio.run(main())
