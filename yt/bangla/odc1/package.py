"""Paczka: napisy-pl.srt, opis.txt (rozdziały + źródła), miniaturka.jpg"""
import re, os, asyncio
from boards import build
from engine import FR, CSS, DEFS, FONTS, page, bear_body, Y, P

OUT = "/home/claude/bangla-yt/odc1/paczka"
os.makedirs(OUT, exist_ok=True)
bs = build(); BD = {b.fid: b for b in bs}

def tc(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{min(999, int(round((s - int(s)) * 1000))):03d}"

def tchar(fid, c):
    for cs, ce, ts, te in FR[fid]["map"]:
        if cs <= c <= ce: return ts + (c - cs) / max(1, ce - cs) * (te - ts)
    return FR[fid]["t1"]

subs = []
for fid in sorted(FR):
    txt = FR[fid]["text"]; parts = []
    for m in re.finditer(r"[^.?!…:]+[.?!…:]*\s*", txt):
        seg = m.group(0)
        if len(seg.strip()) > 56:
            cur = ""
            for p in re.split(r"(?<=,)\s+", seg):
                if len(cur) + len(p) > 56 and cur: parts.append(cur); cur = p + " "
                else: cur += p + " "
            if cur.strip(): parts.append(cur)
        else: parts.append(seg)
    merged = []
    for p in parts:
        if merged and len(merged[-1].strip()) + len(p.strip()) <= 28: merged[-1] = merged[-1].rstrip() + " " + p
        else: merged.append(p)
    c = 0
    for p in merged:
        pc = p.strip()
        if not pc: continue
        c0 = txt.index(pc, c); c1 = c0 + len(pc); c = c1
        t0, t1 = tchar(fid, c0), tchar(fid, c1)
        if t1 - t0 < 0.9: t1 = t0 + 0.9
        line = pc
        if len(line) > 40:
            words, l1 = line.split(), ""
            while words and len(l1) + len(words[0]) < len(line) / 2 + 4: l1 += words.pop(0) + " "
            line = l1.strip() + "\n" + " ".join(words)
        subs.append([t0, t1, line])
for i in range(len(subs) - 1):
    subs[i][1] = min(subs[i][1], subs[i + 1][0] - 0.02)
with open(f"{OUT}/napisy-pl.srt", "w", encoding="utf-8") as f:
    for i, (a, b, l) in enumerate(subs, 1): f.write(f"{i}\n{tc(a)} --> {tc(b)}\n{l}\n\n")

def mmss(t): t = int(t); return f"{t // 60}:{t % 60:02d}"
chap = [(0, "Kapral, który był niedźwiedziem"), (BD[5].start, "Skąd się wziął Wojtek"), (BD[13].start, "Życie w wojsku"),
        (BD[16].start, "Szeregowy Wojtek"), (BD[20].start, "Monte Cassino"), (BD[24].start, "Po wojnie"), (BD[32].start, "Dziś")]
chapters = "\n".join(f"{mmss(t)} {n}" for t, n in chap)

opis = f"""W polskiej armii służył kapral, który pił piwo, jadł papierosy i mocował się z kolegami dla zabawy. I był niedźwiedziem. Historia Wojtka: od irańskiej drogi w 1942 roku, przez Monte Cassino, aż do zoo w Edynburgu.

Fakty podajemy wprost. Legendy oznaczamy jako „podobno” albo „według relacji”.

{chapters}

Źródła:
• Encyclopaedia Britannica: Wojtek the Bear. https://www.britannica.com/print/article/2226582
• British Library, European studies blog: Wojtek, the soldier bear from the Polish Army. https://www.bl.uk/stories/blogs/posts/wojtek-the-soldier-bear-from-the-polish-army
• BBC Wildlife (Discover Wildlife): Wojtek bear. https://www.discoverwildlife.com/animal-facts/mammals/wojtek-bear
• ANSA: The fairy tale of Wojtek, the bear who became a soldier. https://www.ansa.it/nuova_europa/en/news/sections/news/2014/05/14/the-fairy-tale-of-wojtek-the-bear-who-became-a-soldier_1de489cc-96a8-40e2-abef-2a118f883dbc.html
• Irish Farmers Journal: Heroic animals, Wojtek the happy warrior. https://www.farmersjournal.ie/life/features/heroic-animals-wojtek-the-happy-warrior-566457
• Wikipedia: Wojtek (bear). https://en.wikipedia.org/wiki/Wojtek_(bear)

Mapy są uproszczone. Wszystkie rysunki (w tym znak kompanii) są nasze, rysunkowe.

Znasz kogoś, kto musi to usłyszeć? Wyślij mu ten odcinek.
W następnym odcinku „Dziwnych historii”: facet, który sprzedał Wieżę Eiffla.

Nie wiem, ale bangla (chyba).

#historia #ciekawostki #wojtek #montecassino #dziwnehistorie
"""
tytul = "Ten polski kapral pił piwo, jadł papierosy i był niedźwiedziem"
tagi = ("niedźwiedź Wojtek, kapral Wojtek, Wojtek niedźwiedź, Monte Cassino, armia Andersa, II Korpus Polski, historia Polski, "
        "ciekawostki historyczne, dziwne historie, II wojna światowa, niedźwiedź żołnierz, Edinburgh Zoo, soldier bear, nie wiem ale bangla")
open(f"{OUT}/opis.txt", "w", encoding="utf-8").write(f"TYTUŁ:\n{tytul}\n\nOPIS:\n{opis}\nTAGI:\n{tagi}\n")

# ── miniaturka 1280x720 (rysowana w 1920x1080, zmniejszana) ──
body = f"""<div class="f" style="background:radial-gradient(1100px 800px at 70% 60%,#2a2f37,#111317 70%)">{DEFS}
<div style="position:absolute;left:0;top:0;width:1920px;height:1080px;opacity:.5;background-image:linear-gradient(rgba(255,255,255,.04) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.04) 2px,transparent 2px);background-size:60px 60px"></div>
<div style="position:absolute;left:1020px;top:110px;transform:scale(1.62);transform-origin:0 0">{bear_body(True, "shell", 520)}</div>
<div class="big" style="position:absolute;left:70px;top:120px;font-size:225px;color:{Y};transform:rotate(-5deg);text-shadow:0 14px 0 #000">KAPRAL<span style="color:{P}">?!</span></div>
<div style="position:absolute;left:100px;top:470px;transform:rotate(-3deg);background:#fff;color:#111;font-weight:900;font-style:italic;font-size:88px;line-height:1.08;padding:18px 44px;border-radius:22px;box-shadow:0 12px 0 #000;white-space:nowrap">PIŁ PIWO,<br>JADŁ PAPIEROSY</div>
<div class="chyba" style="position:absolute;left:640px;top:800px;font-size:90px;padding:12px 46px;border-radius:60px;transform:rotate(-8deg)">(chyba)</div>
<div class="grain"></div></div>"""
open(f"{OUT}/_thumb.html", "w", encoding="utf-8").write(page(FONTS, CSS, body, 1920, 1080))

async def thumb():
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": 1920, "height": 1080})
        await pg.goto(f"file://{OUT}/_thumb.html", wait_until="networkidle"); await pg.evaluate("document.fonts.ready.then(()=>0)"); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f"{OUT}/_thumb_full.png")
        await b.close()
asyncio.run(thumb())
os.system(f"ffmpeg -loglevel error -y -i {OUT}/_thumb_full.png -vf scale=1280:720:flags=lanczos -q:v 2 {OUT}/miniaturka.jpg")
print(len(subs), "napisów;", chapters.replace("\n", " | "))
