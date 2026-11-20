"""Buduje grafiki i payloady Metricool z pliku spec JSON.

Użycie:  python3 tools/build.py posts/2026-11-21/spec.json
Wynik:   posts/<data>/mm/*.png, posts/<data>/bangla/*.png, posts/<data>/metricool.json, posts/<data>/podglad.png
         i lista ostrzeżeń o tekście, który wychodzi poza bezpieczny obszar (wtedy skróć tekst i zbuduj ponownie).
"""
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image
from playwright.sync_api import sync_playwright

import templates as T

REPO_RAW = "https://raw.githubusercontent.com/krzysiuhexa-creator/faceless-konta/main/"
BLOG = {("mm", "pl"): 8253009, ("mm", "en"): 8253033, ("bangla", "pl"): 8252917}
TZ = "Europe/Warsaw"

# JS: najniższy punkt treści (bez stopki, znaczka, źródła itp.) – do wykrywania przepełnienia
CHECK_JS = """() => {
  const skip = '.ft,.pill,.src,.swipe,.disc,.cta,.stat,.fade,.ph,.dots';
  let maxB = 0, maxR = 0;
  document.querySelectorAll('.s *').forEach(el => {
    if (el.closest(skip)) return;
    if (!el.childNodes.length || [...el.childNodes].every(n => n.nodeType !== 3 || !n.textContent.trim())) return;
    const r = el.getBoundingClientRect();
    maxB = Math.max(maxB, r.bottom); maxR = Math.max(maxR, r.right);
  });
  return {bottom: maxB, right: maxR};
}"""
LIMIT = {"mm": 1170, "mm_bars": 1235, "mm_stat": 1000, "mm_why": 1000, "bangla": 1130}


def info(text, media, date, time, kind="POST"):
    return json.dumps({
        "autoPublish": True, "draft": True, "descendants": [], "firstCommentText": "", "hasNotReadNotes": False,
        "media": media, "mediaAltText": [], "providers": [{"network": "instagram"}],
        "publicationDate": {"dateTime": f"{date}T{time}:00", "timezone": TZ},
        "shortener": False, "smartLinkData": {"ids": []}, "text": text, "instagramData": {"type": kind},
    }, ensure_ascii=False)


def main(spec_path):
    spec_path = Path(spec_path).resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    day = spec["date"]
    out = spec_path.parent
    tmp = out / "_html"
    tmp.mkdir(parents=True, exist_ok=True)
    jobs = []      # (relpath, html, w, h, transparent, limit_key)
    posts = []     # payloady Metricool
    photos = []    # nakładki do zdjęć

    for p in spec["posts"]:
        t, slug = p["type"], p["slug"]
        if t == "mm_carousel":
            for lang in ("pl", "en"):
                d = p[lang]
                n = len(d["slides"])
                files = []
                for i, sl in enumerate(d["slides"], 1):
                    rel = f"mm/{slug}-{lang}-{i}.png"
                    lk = "mm_stat" if sl.get("stat") else {"why": "mm_why", "bars": "mm_bars"}.get(sl["kind"], "mm")
                    jobs.append((rel, T.mm_slide(lang, d, sl, i, n), T.W, T.H, False, lk))
                    files.append(rel)
                posts.append({"account": f"mm-{lang}", "blogId": BLOG[("mm", lang)], "time": p["time"], "slug": slug,
                              "files": files, "caption": d["caption"]})
        elif t == "mm_numbers":
            for lang in ("pl", "en"):
                d = p[lang]
                rel = f"mm/{slug}-{lang}.png"
                jobs.append((rel, T.mm_numbers(lang, d), T.W, T.H, False, None))
                posts.append({"account": f"mm-{lang}", "blogId": BLOG[("mm", lang)], "time": p["time"], "slug": slug,
                              "files": [rel], "caption": d["caption"]})
        elif t == "bangla_carousel":
            n = len(p["slides"])
            files = []
            for i, sl in enumerate(p["slides"], 1):
                rel = f"bangla/{slug}-{i}.png"
                lk = None if sl["kind"] == "cover" else "bangla"
                jobs.append((rel, T.bangla_slide(p, sl, i, n), T.W, T.H, False, lk))
                files.append(rel)
            posts.append({"account": "bangla", "blogId": BLOG[("bangla", "pl")], "time": p["time"], "slug": slug,
                          "files": files, "caption": p["caption"]})
        elif t == "bangla_photo":
            for prev, suf, tr in ((False, "nakladka", True), (True, "podglad", False)):
                rel = f"bangla/zdjecie-{slug}-{suf}.png"
                jobs.append((rel, T.bangla_photo(p, preview=prev), T.W, T.H, tr, None))
            photos.append({"slug": slug, "overlay": f"bangla/zdjecie-{slug}-nakladka.png",
                           "preview": f"bangla/zdjecie-{slug}-podglad.png", "caption": p["caption"],
                           "photo_hint": p.get("photo_hint", "")})
        else:
            raise SystemExit(f"Nieznany typ posta: {t}")

    warnings = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        for rel, html, w, h, transparent, lk in jobs:
            f = tmp / (rel.replace("/", "__") + ".html")
            f.write_text(html, encoding="utf-8")
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.goto(f"file://{f}")
            pg.wait_for_load_state("networkidle")
            pg.evaluate("document.fonts.ready")
            dst = out / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            if lk:
                m = pg.evaluate(CHECK_JS)
                if m["bottom"] > LIMIT[lk] or m["right"] > w - 40:
                    warnings.append(f"{rel}: tekst za nisko/szeroko (dół {m['bottom']:.0f}px, limit {LIMIT[lk]}; prawo {m['right']:.0f}px)")
            pg.screenshot(path=str(dst), omit_background=transparent)
            pg.close()
        b.close()

    # payloady Metricool
    mc = []
    for po in posts:
        media = [REPO_RAW + f"posts/{day}/{x}" for x in po["files"]]
        mc.append({"account": po["account"], "slug": po["slug"], "blogId": str(po["blogId"]),
                   "date": datetime.fromisoformat(f"{day}T{po['time']}:00").replace(tzinfo=ZoneInfo(TZ)).isoformat(), "info": info(po["caption"], media, day, po["time"])})
    (out / "metricool.json").write_text(json.dumps(mc, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "zdjecia.json").write_text(json.dumps(photos, ensure_ascii=False, indent=1), encoding="utf-8")

    # podgląd dnia: pierwsze slajdy wszystkich postów
    firsts = [out / po["files"][0] for po in posts] + [out / ph["preview"] for ph in photos]
    if firsts:
        s = 0.3
        w, h = int(1080 * s), int(1350 * s)
        cols = 4
        rows = (len(firsts) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * (w + 12) + 12, rows * (h + 12) + 12), "#05070D")
        for j, fp in enumerate(firsts):
            sheet.paste(Image.open(fp).convert("RGB").resize((w, h)), (12 + (j % cols) * (w + 12), 12 + (j // cols) * (h + 12)))
        sheet.save(out / "podglad.png")

    for f in tmp.glob("*.html"):
        f.unlink()
    tmp.rmdir()
    print(json.dumps({"posts": len(mc), "photos": len(photos), "warnings": warnings}, ensure_ascii=False, indent=1))
    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
