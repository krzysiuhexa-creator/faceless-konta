"""Paczka: napisy-pl.srt, opis.txt (rozdziały + źródła), miniaturka.jpg"""
import re, os, asyncio
from boards import build
from engine import FR, CSS, DEFS, FONTS, page, Y, P
from boards import eiffel, tag

OUT = "/home/claude/bangla-yt/odc2/paczka"
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
chap = [(0, "Ktoś sprzedał Wieżę Eiffla"), (BD[5].start, "Kim był Victor Lustig"), (BD[8].start, "Plan"),
        (BD[15].start, "Haczyk i łapówka"), (BD[21].start, "Drugi raz"), (BD[26].start, "Ameryka i Al Capone"), (BD[34].start, "Koniec")]
for (t1, _), (t2, n) in zip(chap, chap[1:]): assert t2 - t1 >= 10, n
chapters = "\n".join(f"{mmss(t)} {n}" for t, n in chap)

opis = f"""W 1925 roku w Paryżu ktoś sprzedał Wieżę Eiffla. Na złom. Problem: wieża nie była jego. A potem zrobił to drugi raz. Historia Victora Lustiga, „hrabiego”, którego nazywano najgładszym oszustem w historii: od fałszywego ministerstwa i hotelu Crillon, przez pożyczkę od Ala Capone, aż po Alcatraz.

Fakty podajemy wprost. Legendy oznaczamy jako „podobno” albo „według relacji”. Tam, gdzie źródła się różnią (kwoty, druga sprzedaż), mówimy to otwarcie.

{chapters}

Źródła:
• Smithsonian Magazine: The Smoothest Con Man That Ever Lived
• Smithsonian Magazine: The Man Who Sold the Eiffel Tower. Twice.
• Tour Eiffel (oficjalna strona wieży): Who sold the Eiffel Tower? oraz historia ratunku dzięki radiu
• The Mob Museum: The long con of underworld grifter „Count” Victor Lustig
• The Hustle: The con man who sold the Eiffel Tower — twice
• Mental Floss: Smooth Operator
• Wikipedia: Victor Lustig

Wszystkie rysunki są nasze. Lustig i Al Capone to rysunkowe ikonki, nie portrety.

Znasz kogoś, kto zawsze mówi, że jego nikt nie oszuka? Wyślij mu ten odcinek.
W następnym odcinku „Dziwnych historii”: armia, która wypowiedziała wojnę ptakom. I przegrała.

Nie wiem, ale bangla (chyba).

#historia #ciekawostki #wiezaeiffla #oszustwo #dziwnehistorie
"""
tytul = "Ten facet sprzedał Wieżę Eiffla. Dwa razy."
tagi = ("Victor Lustig, Wieża Eiffla, sprzedał Wieżę Eiffla, oszust, największy oszust w historii, Al Capone, Alcatraz, "
        "ciekawostki historyczne, dziwne historie, historia oszustwa, Paryż 1925, con man, nie wiem ale bangla")
open(f"{OUT}/opis.txt", "w", encoding="utf-8").write(f"TYTUŁ:\n{tytul}\n\nOPIS:\n{opis}\nTAGI:\n{tagi}\n")

# ── miniaturka 1280x720 (rysowana w 1920x1080, zmniejszana) ──
body = f"""<div class="f" style="background:radial-gradient(1100px 800px at 70% 60%,#2a2f37,#111317 70%)">{DEFS}
<div style="position:absolute;left:0;top:0;width:1920px;height:1080px;opacity:.5;background-image:linear-gradient(rgba(255,255,255,.04) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.04) 2px,transparent 2px);background-size:60px 60px"></div>
<div style="position:absolute;left:1120px;top:60px;transform:rotate(4deg)">{eiffel(980)}</div>
<div style="position:absolute;left:1300px;top:470px;transform:rotate(12deg)">{tag("NA SPRZEDAŻ", Y, "#111", 62)}</div>
<div class="big" style="position:absolute;left:70px;top:90px;font-size:200px;color:#fff;transform:rotate(-4deg);text-shadow:0 14px 0 #000">SPRZEDAŁ</div>
<div class="big" style="position:absolute;left:90px;top:300px;font-size:150px;color:#fff;transform:rotate(-4deg);text-shadow:0 14px 0 #000">WIEŻĘ EIFFLA</div>
<div class="big" style="position:absolute;left:110px;top:480px;font-size:330px;color:{Y};transform:rotate(-6deg);text-shadow:0 16px 0 #000">×2<span style="color:{P}">?!</span></div>
<div class="chyba" style="position:absolute;left:820px;top:860px;font-size:80px;padding:10px 44px;border-radius:60px;transform:rotate(-8deg)">(chyba)</div>
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
