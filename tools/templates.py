"""Szablony grafik: Market Minute (mm) i Nie wiem, ale bangla (bangla). 1080x1350 px.
Teksty mogą zawierać proste HTML: <b>…</b>, <br>, &nbsp;. Emoji w Bangla owijamy automatycznie."""
from pathlib import Path

FS = Path(__file__).resolve().parent / "node_modules" / "@fontsource"
W, H = 1080, 1350


def links(spec):
    return "".join(f'<link rel="stylesheet" href="file://{FS}/{f}">' for f in spec)


MM_FONTS = links(["space-grotesk/400.css", "space-grotesk/500.css", "space-grotesk/700.css",
                  "jetbrains-mono/500.css", "jetbrains-mono/700.css"])
BG_FONTS = links(["poppins/600.css", "poppins/700.css", "poppins/800-italic.css", "poppins/900-italic.css"])


def page(head, css, body, w=W, h=H):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">{head}<style>*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{w}px;height:{h}px;overflow:hidden}}{css}</style></head><body>{body}</body></html>"""


# ───────────────────────── MARKET MINUTE ─────────────────────────
MM_CSS = """
:root{--bg:#0A0E13;--panel:#111821;--line:#1F2A36;--text:#F2F5F7;--muted:#8796A8;--up:#2BE38B;--down:#FF5A5F}
body{background:var(--bg);color:var(--text);font-family:'Space Grotesk',sans-serif}
.s{position:relative;width:1080px;height:1350px;padding:84px 84px 0 84px;
   background:radial-gradient(900px 600px at 85% -10%,rgba(43,227,139,.10),transparent 60%),var(--bg)}
.hd{display:flex;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;gap:18px;font-weight:700;font-size:30px;letter-spacing:3px}
.brand small{font-size:20px;color:var(--bg);background:var(--up);padding:4px 10px;border-radius:8px;letter-spacing:1px;margin-left:6px}
.tag{font-family:'JetBrains Mono';font-weight:500;font-size:24px;color:var(--muted);letter-spacing:1px}
.tag b{color:var(--up);font-weight:700}
.kicker{margin-top:120px;font-family:'JetBrains Mono';font-weight:700;font-size:30px;color:var(--up);letter-spacing:4px}
h1{margin-top:22px;font-size:84px;line-height:1.02;font-weight:700;letter-spacing:-1.5px}
h2{margin-top:110px;font-size:66px;line-height:1.05;font-weight:700;letter-spacing:-1px}
.big{margin-top:70px;font-family:'JetBrains Mono';font-weight:700;font-size:190px;line-height:1;color:var(--up);letter-spacing:-6px}
.big.dn{color:var(--down)}
.biglbl{margin-top:14px;font-size:34px;color:var(--muted)}
ul{list-style:none;margin-top:56px}
li{position:relative;padding-left:50px;font-size:48px;line-height:1.25;margin-bottom:42px}
li:before{content:"";position:absolute;left:0;top:20px;width:22px;height:22px;border-radius:5px;background:var(--up)}
li b{color:var(--up)}
.ft{position:absolute;left:84px;right:84px;bottom:64px;display:flex;justify-content:space-between;align-items:flex-end;
    font-family:'JetBrains Mono';font-size:22px;color:var(--muted)}
.dots{display:flex;gap:10px}.dots i{display:block;width:44px;height:6px;border-radius:3px;background:var(--line)}
.dots i.on{background:var(--up)}
.swipe{position:absolute;right:84px;bottom:130px;font-size:30px;color:var(--muted)}
.bars{margin-top:70px;display:flex;align-items:flex-end;gap:70px;height:560px;padding:0 30px;border-bottom:3px solid var(--line)}
.bar{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%}
.bar .v{font-family:'JetBrains Mono';font-weight:700;font-size:46px;margin-bottom:18px}
.bar .r{width:100%;border-radius:14px 14px 0 0}
.lbls{display:flex;gap:70px;padding:0 30px;margin-top:18px}.lbls div{flex:1;text-align:center;font-size:30px;color:var(--muted)}
.note{margin-top:54px;padding:30px 34px;border:2px solid var(--line);border-radius:22px;font-size:36px;line-height:1.3;background:var(--panel)}
.note b{color:var(--up)}
.quote{margin-top:60px;font-size:64px;line-height:1.16;font-weight:500}
.quote b{color:var(--up);font-weight:700}
.cta{position:absolute;left:84px;right:84px;bottom:200px;font-size:40px;line-height:1.35;color:var(--text);padding-top:34px;border-top:2px solid var(--line)}
.cta b{color:var(--up)}
.disc{position:absolute;left:84px;bottom:150px;font-size:26px;color:var(--muted)}
.rows{margin-top:20px;border-top:2px solid var(--line)}
.row{display:flex;justify-content:space-between;align-items:baseline;padding:22px 0;border-bottom:2px solid var(--line);font-size:34px}
.row span{color:var(--muted)}
.row b{font-family:'JetBrains Mono';font-weight:700;font-size:40px}
.dn{color:var(--down)}.upc{color:var(--up)}
.price{margin-top:24px;font-family:'Space Grotesk';font-weight:700;font-size:170px;letter-spacing:-4px;line-height:1}
.stat{position:absolute;left:84px;right:84px;bottom:190px;padding:40px 44px;border-radius:26px;background:var(--panel);border:2px solid var(--line)}
.stat .n{font-family:'Space Grotesk';font-weight:700;font-size:130px;line-height:1;color:var(--up);letter-spacing:-3px}
.stat .t{margin-top:12px;font-size:34px;color:var(--muted)}
.chart{margin-top:30px;display:block}
"""

MM_LOGO = """<svg viewBox="0 0 100 100" width="{s}" height="{s}">
<rect x="0" y="0" width="100" height="100" rx="24" fill="#2BE38B"/>
<rect x="44" y="9" width="12" height="8" rx="2" fill="#0A0E13"/>
<circle cx="50" cy="56" r="31" fill="none" stroke="#0A0E13" stroke-width="7"/>
<polyline points="31,66 43,56 52,61 68,43" fill="none" stroke="#0A0E13" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
<polyline points="59,42 68,43 67,52" fill="none" stroke="#0A0E13" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

MM_HANDLE = {"pl": "@marketminute.pl", "en": "@marketminuteng"}
MM_DISC = {"pl": "Informacja, nie porada inwestycyjna.", "en": "Information, not financial advice."}
MM_SWIPE = {"pl": "Przesuń →", "en": "Swipe →"}
MM_CTA = {"pl": "Obserwuj <b>@marketminute.pl</b>: rynek w minutę, codziennie.",
          "en": "Follow <b>@marketminuteng</b>: markets in a minute, every day."}


def _mm_header(lang, tag, date):
    badge = "<small>PL</small>" if lang == "pl" else ""
    return f"""<div class="hd"><div class="brand">{MM_LOGO.format(s=64)}MARKET MINUTE{badge}</div>
<div class="tag"><b>{tag}</b> · {date}</div></div>"""


def _mm_footer(lang, src, i, n):
    dots = "".join(f'<i class="{"on" if k == i else ""}"></i>' for k in range(1, n + 1)) if n > 1 else ""
    return f"""<div class="ft"><div>{MM_HANDLE[lang]}<br>{src}</div><div class="dots">{dots}</div></div>"""


def mm_slide(lang, p, sl, i, n):
    """p: dane posta w danym języku (tag, date, src); sl: slajd."""
    hd = _mm_header(lang, p["tag"], p["date"])
    ft = _mm_footer(lang, p["src"], i, n)
    k = sl["kind"]
    if k == "cover":
        dn = " dn" if sl.get("down") else ""
        big = f'<div class="big{dn}">{sl["big"]}</div><div class="biglbl">{sl.get("big_label", "")}</div>' if sl.get("big") else ""
        sw = f'<div class="swipe">{MM_SWIPE[lang]}</div>' if n > 1 else ""
        body = f'{hd}<div class="kicker">{sl.get("kicker", "")}</div><h1>{sl["title"]}</h1>{big}{sw}'
    elif k == "bullets":
        stat = ""
        if sl.get("stat"):
            stat = f'<div class="stat"><div class="n">{sl["stat"]}</div><div class="t">{sl.get("stat_label", "")}</div></div>'
        body = f'{hd}<h2>{sl["title"]}</h2><ul>{"".join(f"<li>{x}</li>" for x in sl["items"])}</ul>{stat}'
    elif k == "bars":
        a, b = float(sl["a"]), float(sl["b"])
        mx = max(a, b) or 1
        ha, hb = a / mx * 430, b / mx * 430
        ca, cb = ("#2A3644", "#2BE38B") if b >= a else ("#2BE38B", "#FF5A5F")
        note = f'<div class="note">{sl["note"]}</div>' if sl.get("note") else ""
        body = f"""{hd}<h2>{sl["title"]}</h2>
<div class="bars"><div class="bar"><div class="v" style="color:#8796A8">{sl["a_value"]}</div><div class="r" style="height:{ha:.0f}px;background:{ca}"></div></div>
<div class="bar"><div class="v" style="color:{cb}">{sl["b_value"]}</div><div class="r" style="height:{hb:.0f}px;background:{cb}"></div></div></div>
<div class="lbls"><div>{sl["a_label"]}</div><div>{sl["b_label"]}</div></div>{note}"""
    elif k == "why":
        body = f"""{hd}<h2>{sl["title"]}</h2><div class="quote">{sl["text"]}</div>
<div class="cta">{MM_CTA[lang]}</div><div class="disc">{MM_DISC[lang]}</div>"""
    else:
        raise ValueError(f"nieznany slajd mm: {k}")
    return page(MM_FONTS, MM_CSS, f'<div class="s">{body}{ft}</div>')


def mm_numbers(lang, p):
    """Karta liczbowa (np. Bitcoin w liczbach). p: tag,date,kicker,value,value_label,rows[[label,value,cls]],src, chart{points,labels} opcjonalnie."""
    chart = ""
    c = p.get("chart")
    if c:
        pts = [float(x) for x in c["points"]]
        lo, hi = min(pts), max(pts)
        pad = (hi - lo) * 0.15 or 1
        lo, hi = lo - pad, hi + pad
        n = len(pts)
        xs = [30 + j * (852 / (n - 1)) for j in range(n)] if n > 1 else [456]
        ys = [30 + (hi - v) / (hi - lo) * 170 for v in pts]
        col = "#FF5A5F" if pts[-1] < pts[0] else "#2BE38B"
        poly = " ".join(f"{x:.0f},{y:.0f}" for x, y in zip(xs, ys))
        circ = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="11" fill="{col}"/>' for x, y in zip(xs, ys))
        labs = c.get("labels", [])
        lx = [0] + [x for x in xs[1:-1]] + [912] if n > 1 else [456]
        an = ["start"] + ["middle"] * (n - 2) + ["end"] if n > 1 else ["middle"]
        lt = "".join(f'<text x="{x:.0f}" y="245" text-anchor="{a}" fill="#8796A8" font-size="26" font-family="Space Grotesk">{l}</text>'
                     for x, a, l in zip(lx, an, labs))
        chart = f'<svg class="chart" width="912" height="260" viewBox="0 0 912 260"><polyline points="{poly}" fill="none" stroke="{col}" stroke-width="6" stroke-linejoin="round"/>{circ}{lt}</svg>'
    rows = "".join(f'<div class="row"><span>{a}</span><b class="{cl}">{b}</b></div>' for a, b, cl in p.get("rows", []))
    body = f"""{_mm_header(lang, p["tag"], p["date"])}
<div class="kicker" style="margin-top:56px">{p["kicker"]}</div>
<div class="price">{p["value"]}</div><div class="biglbl">{p.get("value_label", "")}</div>
{chart}<div class="rows">{rows}</div>
{_mm_footer(lang, p["src"] + " · " + MM_DISC[lang], 1, 1)}"""
    return page(MM_FONTS, MM_CSS, f'<div class="s">{body}</div>')


def mm_avatar():
    body = f"""<div style="width:1080px;height:1080px;display:flex;align-items:center;justify-content:center;
background:radial-gradient(700px 700px at 50% 40%,#13202A,#0A0E13)">{MM_LOGO.format(s=620)}</div>"""
    return page(MM_FONTS, MM_CSS, body, 1080, 1080)


# ───────────────────────── NIE WIEM, ALE BANGLA ─────────────────────────
BG_CSS = """
:root{--bg:#0B0F1A;--band:#05070D;--acc:#FFD21F;--pink:#FF4FA0;--w:#FFFFFF;--muted:#9AA3B5}
body{background:var(--bg);color:var(--w);font-family:'Poppins',sans-serif}
.e{font-family:'Noto Color Emoji';font-style:normal}
.s{position:relative;width:1080px;height:1350px;overflow:hidden;
   background:radial-gradient(700px 520px at 50% 72%,rgba(255,210,31,.16),transparent 70%),linear-gradient(#0E1424,#0B0F1A)}
.s.o{background:transparent}
.band{position:relative;background:var(--band);padding:70px 60px 34px;text-align:center}
.band:after{content:"";position:absolute;left:0;right:0;bottom:-60px;height:60px;background:linear-gradient(var(--band),transparent)}
.h{font-weight:900;font-style:italic;text-transform:uppercase;color:var(--acc);font-size:76px;line-height:1.02;letter-spacing:-1px;text-shadow:0 4px 0 rgba(0,0,0,.35)}
.sub{margin-top:14px;font-weight:800;font-style:italic;text-transform:uppercase;font-size:44px;line-height:1.08}
.swipe{margin-top:18px;font-weight:800;font-style:italic;text-transform:uppercase;font-size:30px}
.swipe b{color:var(--acc);font-weight:900}
.pill{position:absolute;left:50%;bottom:58px;transform:translateX(-50%);display:flex;align-items:center;gap:14px;background:#FFD21F;color:#111;
      border-radius:60px;padding:10px 30px 10px 12px;font-weight:800;font-size:28px;white-space:nowrap;box-shadow:0 6px 0 rgba(0,0,0,.35)}
.pill .m{width:52px;height:52px;border-radius:50%;background:#111;color:#FFD21F;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:26px}
.pill .c{background:var(--pink);color:#fff;border-radius:30px;padding:2px 12px;font-size:20px;transform:rotate(-5deg)}
.src{position:absolute;left:44px;bottom:150px;font-weight:800;font-style:italic;text-transform:uppercase;font-size:22px;line-height:1.3}
.src span{display:block;font-weight:600;font-style:normal;color:#D9DEE8}
.circ{position:absolute;border-radius:50%;border:10px solid #fff;background:#1A2236;display:flex;align-items:center;justify-content:center;box-shadow:0 18px 40px rgba(0,0,0,.45)}
.tag{position:absolute;background:#fff;color:#111;font-weight:800;border-radius:18px;padding:12px 22px;font-size:30px;box-shadow:0 8px 0 rgba(0,0,0,.35);white-space:nowrap}
.big{position:absolute;font-weight:900;font-style:italic;color:#111;background:var(--acc);border-radius:26px;padding:6px 34px 14px;font-size:130px;line-height:1;letter-spacing:-4px;box-shadow:0 12px 0 rgba(0,0,0,.4);white-space:nowrap}
.rows{position:absolute;left:60px;right:60px;display:flex;flex-direction:column;gap:26px}
.row{display:flex;align-items:center;gap:28px;background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.12);border-radius:26px;padding:22px 28px}
.row .ic{flex:none;width:118px;height:118px;border-radius:50%;border:6px solid #fff;background:#1A2236;display:flex;align-items:center;justify-content:center;font-size:58px}
.row .t{font-size:40px;line-height:1.22;font-weight:600}
.row .t b{color:var(--acc);font-weight:800}
.bars{position:absolute;left:60px;right:60px;display:flex;flex-direction:column;gap:30px}
.bar{display:flex;align-items:center;justify-content:space-between;border-radius:24px;padding:26px 34px;font-weight:900;font-style:italic;font-size:62px}
.bar small{font-weight:700;font-style:normal;font-size:30px;text-align:right;line-height:1.2}
.note{position:absolute;left:60px;right:60px;font-size:38px;line-height:1.3;font-weight:600;text-align:center}
.note b{color:var(--acc);font-weight:800}
.cta{position:absolute;left:60px;right:60px;text-align:center;font-weight:900;font-style:italic;text-transform:uppercase;font-size:50px;line-height:1.08}
.cta small{display:block;margin-top:14px;font-weight:600;font-style:normal;text-transform:none;font-size:30px;color:var(--muted)}
.fade{position:absolute;left:0;right:0;bottom:0;height:380px;background:linear-gradient(transparent,rgba(5,7,13,.92))}
.ph{position:absolute;left:0;right:0;top:470px;bottom:0;background:repeating-linear-gradient(45deg,#2A3146 0 30px,#232A3D 30px 60px);
    display:flex;align-items:center;justify-content:center;font-weight:800;font-size:44px;color:#C9D0DE;text-align:center}
"""


def _e(x):
    return f'<span class="e">{x}</span>'


def _bg_pill():
    return '<div class="pill"><div class="m">?!</div>NIE WIEM, ALE BANGLA<span class="c">(chyba)</span></div>'


def _bg_src(t):
    return f'<div class="src">Źródło:<span>{t}</span></div>'


def _bg_band(h, sub="", swipe=True, hsize=None):
    hs = f' style="font-size:{hsize}px"' if hsize else ""
    sw = '<div class="swipe"><b>»</b> Przesuń w prawo <b>»</b></div>' if swipe else ""
    sb = f'<div class="sub">{sub}</div>' if sub else ""
    return f'<div class="band"><div class="h"{hs}>{h}</div>{sb}{sw}</div>'


def _hsize(text, base):
    n = len(text)
    return base if n <= 40 else (70 if n <= 60 else 62)


def bangla_slide(p, sl, i, n):
    acc = f'<style>:root{{--acc:{p.get("accent", "#FFD21F")}}}</style>'
    k = sl["kind"]
    if k == "cover":
        tags = sl.get("tags", [])[:3]
        pos = [("left:60px;top:640px;transform:rotate(-6deg)"), ("right:50px;top:700px;transform:rotate(6deg)"), ("left:50px;top:850px;transform:rotate(3deg)")]
        tg = "".join(f'<div class="tag" style="{pos[j]}">{_e(em)} {tx}</div>' for j, (em, tx) in enumerate(tags))
        big = f'<div class="big" style="left:50%;top:925px;transform:translateX(-50%) rotate(-5deg)">{sl["big"]}</div>' if sl.get("big") else ""
        emo = f'<div class="circ" style="left:320px;top:590px;width:440px;height:440px;font-size:230px">{_e(sl.get("emoji", "🤯"))}</div>'
        body = f'{_bg_band(sl["title"], sl.get("sub", ""), swipe=n > 1, hsize=_hsize(sl["title"], 76))}{emo}{tg}{big}'
    elif k == "rows":
        rows = "".join(f'<div class="row"><div class="ic">{_e(em)}</div><div class="t">{tx}</div></div>' for em, tx in sl["rows"])
        cta = ""
        if sl.get("cta"):
            cta = f'<div class="cta" style="top:{300 + 175 * len(sl["rows"]) + 60}px">{sl["cta"]}<small>{sl.get("cta_small", "")}</small></div>'
        body = f'{_bg_band(sl["title"], sl.get("sub", ""), swipe=False, hsize=96 if len(sl["title"]) < 16 else 80)}<div class="rows" style="top:300px">{rows}</div>{cta}'
    elif k == "bars":
        bars = ""
        for val, lab, hl in sl["bars"]:
            st = "background:var(--acc);color:#111" if hl else "background:#1A2236;border:3px solid rgba(255,255,255,.2)"
            bars += f'<div class="bar" style="{st}">{val}<small>{lab}</small></div>'
        note = f'<div class="note" style="top:{400 + 190 * len(sl["bars"]) + 20}px">{sl["note"]}</div>' if sl.get("note") else ""
        body = f'{_bg_band(sl["title"], sl.get("sub", ""), swipe=False, hsize=90)}<div class="bars" style="top:400px">{bars}</div>{note}'
    else:
        raise ValueError(f"nieznany slajd bangla: {k}")
    return page(BG_FONTS, BG_CSS, f'{acc}<div class="s">{body}{_bg_src(p["src"])}{_bg_pill()}</div>')


def bangla_photo(p, preview=False):
    """Nakładka na zdjęcie (przezroczysty środek). preview=True: z kratką 'tu wrzucasz zdjęcie'."""
    acc = f'<style>:root{{--acc:{p.get("accent", "#FFD21F")}}}</style>'
    ph = '<div class="ph">TU WRZUCASZ<br>SWOJE ZDJĘCIE</div>' if preview else ""
    inner = f'{_bg_band(p["title"], p.get("sub", ""), swipe=p.get("swipe", False), hsize=_hsize(p["title"], 76))}<div class="fade"></div>{_bg_src(p["src"])}{_bg_pill()}'
    return page(BG_FONTS, BG_CSS + "body{background:transparent}", f'{acc}<div class="s o">{ph}{inner}</div>')
