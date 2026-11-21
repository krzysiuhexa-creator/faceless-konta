"""Avatar 800x800 (2 wersje) i baner 2560x1440 kanału „Nie wiem, ale bangla (chyba)”."""
import sys, asyncio
sys.path.insert(0, "/home/claude/bangla-yt/odc1")
from engine import CSS, DEFS, FONTS, page, bear_head, Y, P, G
OUT = "/home/claude/bangla-yt/kanal"
GRAIN = """<div style="position:absolute;inset:0;opacity:.10;mix-blend-mode:overlay;background-image:url(&quot;data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>&quot;)"></div>"""
GRID = 'background-image:linear-gradient(rgba(255,255,255,.04) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.04) 2px,transparent 2px);background-size:{s}px {s}px'

# ── avatary ──
A1 = f"""<div style="position:relative;width:800px;height:800px;background:{Y};overflow:hidden;font-family:Poppins">
<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-weight:900;font-style:italic;font-size:500px;color:#111;letter-spacing:-20px;line-height:1;transform:translate(-10px,-18px) rotate(-6deg);text-shadow:0 18px 0 rgba(0,0,0,.18)">?!</div>{GRAIN}</div>"""
A2 = f"""<div style="position:relative;width:800px;height:800px;background:radial-gradient(520px 520px at 50% 45%,#2a2f37,#111317 75%);overflow:hidden;font-family:Poppins">
<div style="position:absolute;inset:0;{GRID.format(s=50)}"></div>
<div style="position:absolute;left:50%;top:50%;width:560px;height:560px;margin:-300px 0 0 -280px;border-radius:50%;background:{Y};box-shadow:0 22px 0 #000;display:flex;align-items:center;justify-content:center;transform:rotate(-8deg)">
<div style="font-weight:900;font-style:italic;font-size:330px;color:#111;letter-spacing:-14px;line-height:1;transform:translate(-8px,-12px)">?!</div></div>
<div style="position:absolute;left:50%;bottom:92px;transform:translateX(-50%) rotate(-6deg);background:{P};color:#fff;font-weight:900;font-style:italic;font-size:76px;padding:6px 38px;border-radius:60px;box-shadow:0 10px 0 #000;white-space:nowrap">(chyba)</div>{GRAIN}</div>"""

# ── baner ──
W, H = 2560, 1440
SX, SY, SW, SH = (W - 1546) // 2, (H - 423) // 2, 1546, 423
def emo(ch, x, y, size, rot=0, op=1):
    return f'<div class="emo" style="position:absolute;left:{x}px;top:{y}px;font-size:{size}px;transform:translate(-50%,-50%) rotate({rot}deg);opacity:{op}">{ch}</div>'
def pill(txt, x, y, rot, bg, fg="#111", size=44, op=1):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;transform:translate(-50%,-50%) rotate({rot}deg);background:{bg};color:{fg};font-weight:900;font-style:italic;'
            f'font-size:{size}px;padding:10px 32px;border-radius:50px;box-shadow:0 8px 0 #000;white-space:nowrap;opacity:{op}">{txt}</div>')
def q(x, y, size, rot, color, op=0.9):
    return f'<div style="position:absolute;left:{x}px;top:{y}px;transform:translate(-50%,-50%) rotate({rot}deg);font-weight:900;font-style:italic;font-size:{size}px;color:{color};text-shadow:0 10px 0 #000;opacity:{op}">?</div>'
# ozdoby poza bezpiecznym pasem (widać na komputerze i TV)
deco = "".join([
    emo("🤯", 230, 260, 150, -10), emo("🌍", 470, 1180, 140, 8), emo("🐙", 2330, 300, 140, 10), emo("🚀", 2120, 1190, 140, -14),
    emo("👽", 1280, 180, 110, 6), emo("🧠", 820, 210, 110, -8), emo("🗞️", 1760, 215, 110, 9), emo("💸", 1000, 1250, 110, -6),
    emo("🦖", 2400, 900, 130, -6), emo("🍕", 150, 760, 120, 12), emo("📼", 1560, 1265, 100, 8),
    pill("PODOBNO", 540, 430, -8, "#3a4450", "#fff", 46), pill("SERIO?!", 2050, 430, 7, "#3EE6C1", "#111", 50),
    pill("CIEKAWOSTKA", 330, 1010, 6, "#7CFF4F", "#111", 42), pill("NEWS DNIA", 2260, 1040, -7, "#FF8A3D", "#111", 46),
    pill("DZIWNE HISTORIE", 1300, 1300, -3, "#fff", "#111", 46),
    q(2470, 640, 170, 14, P), q(110, 470, 150, -12, Y), q(1900, 1330, 120, -8, "#3EE6C1"), q(680, 1330, 110, 10, P),
])
route = f'<svg style="position:absolute;left:0;top:0" width="{W}" height="{H}"><path d="M60 1360 C420 1180 520 1320 860 1230 S1500 1370 1720 1290 S2300 1180 2520 1330" fill="none" stroke="rgba(255,255,255,.35)" stroke-width="8" stroke-dasharray="26 18" stroke-linecap="round"/>' \
        f'<path d="M80 90 C500 150 700 40 1100 110 S1900 40 2480 120" fill="none" stroke="rgba(255,210,31,.35)" stroke-width="8" stroke-dasharray="26 18" stroke-linecap="round"/></svg>'
tx = SX + 330
B = f"""<div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;font-family:Poppins;color:#fff;background:radial-gradient(1500px 800px at 50% 50%,#262a31,#111317 72%)">{DEFS}
<div style="position:absolute;inset:0;{GRID.format(s=64)}"></div>{route}{deco}
<div style="position:absolute;left:{SX + 140}px;top:{SY + SH // 2}px;width:270px;height:270px;margin:-135px 0 0 -135px;border-radius:50%;background:{Y};color:#111;box-shadow:0 12px 0 #000;display:flex;align-items:center;justify-content:center;transform:rotate(-8deg)">
<div style="font-weight:900;font-style:italic;font-size:160px;letter-spacing:-8px;line-height:1;transform:translate(-4px,-6px)">?!</div></div>
<div id="t1" style="position:absolute;left:{tx}px;top:{SY + 18}px;font-weight:900;font-style:italic;font-size:138px;line-height:1;letter-spacing:-3px;text-shadow:0 10px 0 #000;white-space:nowrap">NIE WIEM,</div>
<div id="t2" style="position:absolute;left:{tx}px;top:{SY + 158}px;font-weight:900;font-style:italic;font-size:138px;line-height:1;letter-spacing:-3px;color:{Y};text-shadow:0 10px 0 #000;white-space:nowrap">ALE BANGLA</div>
<div id="ch" style="position:absolute;left:{tx + 720}px;top:{SY + 40}px;transform:rotate(-7deg);background:{P};color:#fff;font-weight:900;font-style:italic;font-size:64px;padding:8px 36px;border-radius:60px;box-shadow:0 8px 0 #000;white-space:nowrap">(chyba)</div>
<div id="tg" style="position:absolute;left:{tx + 6}px;top:{SY + 330}px;font-weight:600;font-size:48px;color:#e9e9e9;white-space:nowrap">dziwne historie, które brzmią jak żart</div>
<div style="position:absolute;left:0;right:0;top:{SY + SH + 30}px;height:0"></div>{GRAIN}
<div id="safe" style="display:none;position:absolute;left:{SX}px;top:{SY}px;width:{SW}px;height:{SH}px;outline:4px solid #f00"></div></div>"""

async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        for name, body, w, h in [("avatar-zolty", A1, 800, 800), ("avatar-ciemny", A2, 800, 800), ("baner-kanalu", B, W, H)]:
            f = f"{OUT}/_{name}.html"; open(f, "w", encoding="utf-8").write(page(FONTS, CSS, body, w, h))
            pg = await b.new_page(viewport={"width": w, "height": h})
            await pg.goto(f"file://{f}", wait_until="networkidle"); await pg.evaluate("document.fonts.ready.then(()=>0)"); await pg.wait_for_timeout(400)
            await pg.screenshot(path=f"{OUT}/{name}.png")
            if name == "baner-kanalu":
                box = await pg.evaluate("""()=>['t1','t2','ch','tg'].map(i=>{const r=document.getElementById(i).getBoundingClientRect();return [i,Math.round(r.left),Math.round(r.right),Math.round(r.top),Math.round(r.bottom)]})""")
                print("bezpieczny pas x", SX, SX + SW, "y", SY, SY + SH); print(box)
                await pg.evaluate("document.getElementById('safe').style.display='block'")
                await pg.screenshot(path=f"{OUT}/_podglad-z-pasem.png")
            await pg.close()
        await b.close()
asyncio.run(main())
