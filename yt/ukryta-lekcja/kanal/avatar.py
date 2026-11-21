import sys, asyncio
sys.path.insert(0, "/home/claude/faceless/yt/odc1")
from engine import FONTS, CSS, DEFS, page
def svg(head, eye, ring):
    return f"""<svg class="ch" style="position:absolute;left:0;top:0" width="800" height="800" viewBox="0 0 800 800">
<path filter="url(#chalkp)" d="M400 78 a322 322 0 1 1 -0.1 0" fill="none" stroke="{ring}" stroke-width="10" stroke-linecap="round" stroke-dasharray="1880 140" opacity=".8"/>
<g transform="translate(400 405) scale(3.0) rotate(-6) translate(0 -59)">
<path d="M0 -10 a62 62 0 1 1 -0.1 0" fill="{head}"/>
<path d="M-34 84 L-48 128 L48 128 L34 84 Z" fill="{head}"/>
<ellipse cx="-19" cy="42" rx="9.5" ry="10.5" fill="{eye}"/><ellipse cx="25" cy="42" rx="9.5" ry="10.5" fill="{eye}"/></g></svg>"""
def body(head, eye, ring):
    return f"""<div class="b" style="width:800px;height:800px">{DEFS}<div class="board" style="background:radial-gradient(520px 520px at 50% 45%,#2b3132,#15191a 78%)"></div>
<div class="smudge" style="left:120px;top:90px;width:560px;height:260px"></div>
<div class="ch" style="position:absolute;inset:0">{svg(head, eye, ring)}</div><div class="dust"></div></div>"""
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": 800, "height": 800})
        for name, args in [("avatar-zolty", ("#F5C542", "#1d2122", "#EDEBE4")), ("avatar-kreda", ("#EDEBE4", "#1d2122", "#F5C542"))]:
            f = f"/home/claude/faceless/yt/kanal/_{name}.html"; open(f, "w", encoding="utf-8").write(page(FONTS, CSS, body(*args), 800, 800))
            await pg.goto(f"file://{f}", wait_until="networkidle"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=f"/home/claude/faceless/yt/kanal/{name}.png")
        await b.close()
asyncio.run(main())
