"""Szablon kont storytellingowych (styl długich karuzel: zdjęcie u góry, tekst szeryfowy na czerni).
1080x1350. Teksty mogą zawierać proste HTML: <i>…</i> (puenta kursywą), <b>…</b>, <br>, <mark>…</mark> (akcent).

Rodzaje slajdów (sl["kind"]):
  photo  – zdjęcie u góry (img, pos), tekst na dole. Na okładce większa czcionka.
  text   – sama czerń z delikatnym ziarnem, tekst wyśrodkowany (oddech między zdjęciami).
  number – duża liczba/porównanie (big, label, opcjonalnie big2/label2) + tekst.
  punch  – okładka „krzykliwa”: zdjęcie + wersaliki Oswald z akcentem <mark>.
"""
from templates import links, page, W, H

ST_FONTS = links(["crimson-pro/400.css", "crimson-pro/400-italic.css", "crimson-pro/600.css",
                  "crimson-pro/600-italic.css", "oswald/600.css", "oswald/700.css"])

ST_CSS = """
:root{--acc:#F5C542}
body{background:#000;color:#F4F1EA;font-family:'Crimson Pro',serif}
.s{position:relative;width:1080px;height:1350px;overflow:hidden;background:#000}
.img{position:absolute;left:0;top:0;width:1080px;height:var(--ih,880px);background-size:cover;background-position:var(--pos,center)}
.fade{position:absolute;left:0;top:0;width:1080px;height:var(--ih,880px);
  background:linear-gradient(180deg,rgba(0,0,0,0) 45%,rgba(0,0,0,.55) 72%,#000 100%)}
.grain{position:absolute;inset:0;opacity:.07;mix-blend-mode:screen;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
.vig{position:absolute;inset:0;background:radial-gradient(900px 700px at 50% 45%,rgba(40,36,30,.35),transparent 70%)}
.txt{position:absolute;left:70px;right:70px;bottom:118px;text-align:center}
.txt p{font-size:var(--fs,50px);line-height:1.17;font-weight:400;letter-spacing:-.2px;text-shadow:0 2px 18px rgba(0,0,0,.6)}
.txt p+p{margin-top:.62em}
.txt i{font-style:italic;color:#E9E2D2}
.txt b{font-weight:600}
.txt mark{background:none;color:var(--acc)}
.mid{top:0;bottom:0;display:flex;flex-direction:column;justify-content:center}
.cnt{position:absolute;right:46px;bottom:38px;font-size:26px;color:#8C877C;letter-spacing:1px}
.swipe{position:absolute;left:50%;bottom:46px;transform:translateX(-50%);width:90px;height:2px;background:#6E6A62}
.swipe:after{content:"";position:absolute;right:-2px;top:-5px;border:6px solid transparent;border-left:10px solid #6E6A62}
.nums{display:flex;justify-content:center;gap:90px;margin-bottom:56px}
.num{text-align:center}
.num .v{font-size:200px;line-height:.9;font-weight:600;color:#F4F1EA}
.num .v.dim{color:#6E6A62}
.num .l{margin-top:18px;font-size:34px;line-height:1.15;color:#B7B0A2;max-width:380px}
.punch .txt{bottom:120px}
.punch h1{font-family:'Oswald',sans-serif;font-weight:700;text-transform:uppercase;font-size:var(--fs,74px);
  line-height:1.04;letter-spacing:.5px;color:#fff}
.punch h1 mark{background:none;color:var(--acc)}
"""


def _ps(text):
    return "".join(f"<p>{t}</p>" for t in (text if isinstance(text, list) else [text]))


def story_slide(p, sl, i, n):
    k = sl.get("kind", "photo")
    acc = p.get("accent", "#F5C542")
    cnt = f'<div class="cnt">{i}/{n}</div>'
    sw = '<div class="swipe"></div>' if i == 1 else ""
    if k in ("photo", "punch"):
        ih = sl.get("ih", 900 if i == 1 else 860)
        img = (f'<div class="img" style="--ih:{ih}px;--pos:{sl.get("pos","center")};'
               f'background-image:url(\'file://{sl["img"]}\')"></div><div class="fade" style="--ih:{ih}px"></div>')
        if k == "punch":
            body = f'{img}<div class="txt"><h1>{sl["text"]}</h1></div>'
            return page(ST_FONTS, ST_CSS, f'<div class="s punch" style="--acc:{acc};--fs:{sl.get("fs",74)}px">{body}<div class="grain"></div>{sw}{cnt}</div>')
        fs = sl.get("fs", 60 if i == 1 else 50)
        body = f'{img}<div class="txt" style="--fs:{fs}px">{_ps(sl["text"])}</div>'
    elif k == "number":
        cols = [(sl["big"], sl.get("label", ""), "")]
        if sl.get("big2"):
            cols.append((sl["big2"], sl.get("label2", ""), "dim"))
        nums = "".join(f'<div class="num"><div class="v {c}">{v}</div><div class="l">{l}</div></div>' for v, l, c in cols)
        body = (f'<div class="vig"></div><div class="txt mid" style="--fs:{sl.get("fs",50)}px">'
                f'<div class="nums">{nums}</div>{_ps(sl.get("text", []))}</div>')
    else:  # text
        body = f'<div class="vig"></div><div class="txt mid" style="--fs:{sl.get("fs",54)}px">{_ps(sl["text"])}</div>'
    return page(ST_FONTS, ST_CSS, f'<div class="s" style="--acc:{acc}">{body}<div class="grain"></div>{sw}{cnt}</div>')


# ───────── STYL ŁĄCZONY (Mental Aspect × Doktor Niedźwiedź) ─────────
# Każdy slajd: czarno-białe zdjęcie na całą wysokość, zejście w czerń, kreska z nazwą konta,
# 1–3 zdania wąskim grubym krojem (Anton), »» w prawym dolnym rogu, licznik w lewym.
# sl: img, pos, text (str lub lista), opcjonalnie fs, dark (0–1: przyciemnienie całego zdjęcia), zoom (np. 1.6 = zbliżenie; pos = punkt zbliżenia),
#     big/label/big2/label2 (slajd z liczbami), noimg (czarne tło).
AS_FONTS = links(["anton/400.css", "crimson-pro/600-italic.css"])
AS_CSS = """
:root{--acc:#F5C542}
body{background:#000;color:#fff;font-family:'Anton',sans-serif}
.s{position:relative;width:1080px;height:1350px;overflow:hidden;background:#000}
.img{position:absolute;inset:0;background-size:var(--bs,cover);background-position:var(--pos,center);
  filter:grayscale(1) contrast(1.12) brightness(var(--br,1))}
.fade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 38%,rgba(0,0,0,.72) 60%,#000 76%)}
.grain{position:absolute;inset:0;opacity:.06;mix-blend-mode:screen;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
.box{position:absolute;left:64px;right:64px;bottom:118px;text-align:center}
.box.mid{top:0;bottom:0;display:flex;flex-direction:column;justify-content:center}
.div{display:flex;align-items:center;gap:22px;margin-bottom:30px}
.div:before,.div:after{content:"";flex:1;height:3px;background:#fff}
.div span{font-size:30px;letter-spacing:3px;line-height:1}
.t p{font-size:var(--fs,64px);line-height:1.12;letter-spacing:.3px}
.t p+p{margin-top:.45em}
.t mark{background:var(--acc);color:#000;padding:0 .18em;border-radius:6px}
.t em{font-style:normal;color:var(--acc)}
.nums{display:flex;justify-content:center;gap:110px;margin-bottom:40px}
.num .v{font-size:230px;line-height:.95}
.num .v.dim{color:#7a7a7a}
.num .l{margin-top:8px;font-size:34px;line-height:1.15;color:#cfcfcf;max-width:360px}
.chev{position:absolute;right:50px;bottom:38px;font-size:54px;letter-spacing:-2px;line-height:1}
.cnt{position:absolute;left:56px;bottom:50px;font-size:28px;color:#9a9a9a;letter-spacing:1px}
"""


def aspect_slide(p, sl, i, n):
    name = p.get("name", "NAZWA KONTA")
    acc = p.get("accent", "#F5C542")
    img = ""
    if sl.get("img") and not sl.get("noimg"):
        bs = f'{int(sl["zoom"]*125)}% auto' if sl.get("zoom") else "cover"
        img = (f'<div class="img" style="--pos:{sl.get("pos","center")};--br:{1-sl.get("dark",0)};--bs:{bs};'
               f'background-image:url(\'file://{sl["img"]}\')"></div><div class="fade"></div>')
    nums = ""
    if sl.get("big"):
        cols = [(sl["big"], sl.get("label", ""), "")] + ([(sl["big2"], sl.get("label2", ""), "dim")] if sl.get("big2") else [])
        nums = '<div class="nums">' + "".join(
            f'<div class="num"><div class="v {c}">{v}</div><div class="l">{l}</div></div>' for v, l, c in cols) + "</div>"
    mid = " mid" if not img else ""
    body = (f'{img}<div class="box{mid}"><div class="div"><span>{name}</span></div>{nums}'
            f'<div class="t" style="--fs:{sl.get("fs",64)}px">{_ps(sl.get("text", []))}</div></div>')
    chev = '<div class="chev">›››</div>' if i < n else ""
    cnt = f'<div class="cnt">{i}/{n}</div>' if n > 1 else ""  # karta (1 slajd) bez licznika
    return page(AS_FONTS, AS_CSS, f'<div class="s" style="--acc:{acc}">{body}<div class="grain"></div>{chev}{cnt}</div>')
