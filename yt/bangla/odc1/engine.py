"""Silnik animacji „Nie wiem, ale bangla” (16:9). Plansza = HTML + JS setT(t); render: Playwright → JPEG → ffmpeg."""
import json, os, subprocess, sys
sys.path.insert(0, "/home/claude/faceless-konta/tools")
from templates import links, page

W, H, FPS = 1920, 1080, 30
Y, P, G = "#FFD21F", "#FF4FA0", "#9aa0a8"
RED, GREEN = "#ff3b3b", "#2BE38B"
FONTS = links(["poppins/900-italic.css", "poppins/800.css", "poppins/800-italic.css", "poppins/600.css"])
OUT = "/home/claude/bangla-yt/odc1"
TL = json.load(open(f"{OUT}/timeline.json", encoding="utf-8"))
FR = {f["id"]: f for f in TL["frags"]}


# ─────────── czas ───────────
def _ci(fid, phrase, occ=0):
    t = FR[fid]["text"]; i = -1
    for _ in range(occ + 1):
        i = t.index(phrase, i + 1)
    return i

def _tc(fid, i):
    f = FR[fid]
    for c0, c1, t0, t1 in f["map"]:
        if c0 <= i < c1:
            return t0 + (t1 - t0) * (i - c0) / max(1, c1 - c0)
    return f["t1"]

def A(fid, phrase=None, occ=0):
    """moment, w którym lektor zaczyna mówić frazę"""
    if phrase is None: return FR[fid]["t0"]
    return round(_tc(fid, _ci(fid, phrase, occ)), 3)

def E(fid, phrase=None, occ=0):
    """moment, w którym lektor kończy frazę"""
    if phrase is None: return FR[fid]["t1"]
    i = _ci(fid, phrase, occ) + len(phrase)
    return round(_tc(fid, max(0, i - 1)) + 0.05, 3)


# ─────────── CSS / JS ───────────
CSS = f"""
body{{margin:0;background:#111317}}
.f{{width:1920px;height:1080px;position:relative;overflow:hidden;background:#111317;font-family:Poppins;color:#fff}}
#bg{{position:absolute;inset:0;background:radial-gradient(1200px 700px at 60% 58%,rgba(255,255,255,.07),transparent 70%)}}
#grid{{position:absolute;left:0;top:250px;width:1920px;height:830px;opacity:.55;
  background-image:linear-gradient(rgba(255,255,255,.035) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.035) 2px,transparent 2px);background-size:60px 60px}}
#cam{{position:absolute;inset:0}}
.bar{{position:absolute;left:0;right:0;top:0;height:250px;background:#0a0b0d;z-index:50}}
.bar:after{{content:"";position:absolute;left:0;right:0;bottom:-6px;height:6px;background:linear-gradient(90deg,{Y} 0 33%,{P} 33% 66%,#fff 66%);opacity:.9}}
#hb{{position:absolute;inset:0}}
.h{{position:absolute;left:90px;top:40px;font-weight:900;font-style:italic;font-size:118px;line-height:1;text-transform:uppercase;letter-spacing:-2px;white-space:nowrap;display:inline-block}}
.h .w{{display:inline-block;margin-right:.22em}}
.sub{{position:absolute;left:96px;top:180px;font-weight:600;font-size:40px;color:#e9e9e9;white-space:nowrap}}
.chip{{position:absolute;right:70px;top:44px;font-weight:800;font-size:26px;letter-spacing:2px;color:{G};text-transform:uppercase}}
.chip b{{color:{P};font-weight:900;font-style:italic;margin-right:10px}}
.src{{position:absolute;left:60px;bottom:40px;font-weight:600;font-size:26px;color:{G};letter-spacing:1px;z-index:40;text-transform:uppercase}}
.badge{{position:absolute;right:70px;bottom:40px;width:96px;height:96px;border-radius:50%;background:{Y};color:#111;font-weight:900;font-style:italic;font-size:52px;display:flex;align-items:center;justify-content:center;box-shadow:0 6px 0 #000;z-index:40}}
.logo{{position:absolute;right:190px;bottom:62px;font-weight:900;font-style:italic;font-size:34px;color:#fff;opacity:.85;z-index:40}}
.grain{{position:absolute;inset:0;opacity:.10;mix-blend-mode:overlay;z-index:90;pointer-events:none;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}}
#dim{{position:absolute;left:0;right:0;top:250px;bottom:0;background:#000;opacity:0;z-index:30;pointer-events:none}}
#flash{{position:absolute;inset:0;background:#fff;opacity:0;z-index:95;pointer-events:none}}
.el{{position:absolute;will-change:transform,opacity}}
.chyba{{padding:8px 26px;border-radius:30px;background:{P};color:#fff;font-weight:900;font-style:italic;font-size:44px;box-shadow:0 6px 0 #000;white-space:nowrap}}
.card{{background:#1c1f25;border-radius:34px;border:6px solid #fff;box-shadow:0 10px 0 #000;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
.pill{{background:#1c1f25;border:5px solid #fff;border-radius:60px;box-shadow:0 8px 0 #000;padding:14px 34px;font-weight:800;font-size:40px;text-transform:uppercase;white-space:nowrap}}
.ypill{{background:{Y};color:#111;border-radius:60px;box-shadow:0 8px 0 #000;padding:14px 38px;font-weight:900;font-style:italic;font-size:46px;text-transform:uppercase;white-space:nowrap}}
.emo{{font-family:'Noto Color Emoji';line-height:1;filter:drop-shadow(4px 0 0 #fff) drop-shadow(-4px 0 0 #fff) drop-shadow(0 4px 0 #fff) drop-shadow(0 -4px 0 #fff) drop-shadow(0 9px 0 #000)}}
.emo.flat{{filter:none}}
.lab{{font-weight:800;font-size:44px;margin-top:14px;text-transform:uppercase;line-height:1.1}}
.stamp{{border:10px solid {RED};color:{RED};font-weight:900;font-style:italic;font-size:92px;padding:6px 34px;border-radius:16px;letter-spacing:2px;white-space:nowrap;background:rgba(17,19,23,.55)}}
.big{{font-weight:900;font-style:italic;text-transform:uppercase;line-height:1;white-space:nowrap;letter-spacing:-2px;text-shadow:0 10px 0 #000}}
.txt{{font-weight:800;font-size:44px;line-height:1.25;white-space:nowrap}}
.mute{{color:{G}}}
svg.lay{{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible}}
svg [data-a]{{transform-box:fill-box;transform-origin:center}}
.eyes{{transform-box:fill-box;transform-origin:center}}
"""

DEFS = """<svg width="0" height="0" style="position:absolute"><defs>
<filter id="stk" x="-30%" y="-30%" width="160%" height="160%"><feMorphology in="SourceAlpha" operator="dilate" radius="9" result="d"/>
<feFlood flood-color="#fff"/><feComposite in2="d" operator="in" result="w"/><feOffset in="d" dy="11" result="sd"/>
<feFlood flood-color="#000"/><feComposite in2="sd" operator="in" result="s"/>
<feMerge><feMergeNode in="s"/><feMergeNode in="w"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="10" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs></svg>"""

JS = r"""
const S=window.SCENE;const cl=(v,a=0,b=1)=>Math.min(b,Math.max(a,v));
const eo=u=>1-Math.pow(1-u,3), eio=u=>u<.5?4*u*u*u:1-Math.pow(-2*u+2,3)/2, ein=u=>u*u*u;
const back=(u,c=1.9)=>1+(c+1)*Math.pow(u-1,3)+c*Math.pow(u-1,2);
let ELS=[],DR=[],CN=[],WD=[],EY=[],CAM,HB,DIM,FL;
function init(){
 CAM=document.getElementById('cam');HB=document.getElementById('hb');DIM=document.getElementById('dim');FL=document.getElementById('flash');
 const h=document.querySelector('.h');if(h){let fs=118;while(h.getBoundingClientRect().width>S.hmax&&fs>56){fs-=2;h.style.fontSize=fs+'px'}}
 document.querySelectorAll('[data-a]').forEach((e,i)=>{const d=e.dataset;ELS.push({e,svg:e instanceof SVGElement,a:d.a,t:+d.t,d:+(d.d||.4),o:d.o?+d.o:1e9,od:+(d.od||.3),oa:d.oa||'fade',
   i:(d.i||'').split(' ').filter(Boolean),r:+(d.r||0),s:+(d.s||1),c:d.c==='1',seed:i*1.37+.3,sk:d.sk?d.sk.split(',').map(p=>p.split(':').map(Number)):null});
   if(d.og)e.style.transformOrigin=d.og;});
 document.querySelectorAll('[data-draw]').forEach(p=>{const L=p.getTotalLength();p.style.strokeDasharray=L+' '+L;DR.push({p,L,t:+p.dataset.t,d:+p.dataset.d,o:p.dataset.o?+p.dataset.o:1e9})});
 document.querySelectorAll('[data-count]').forEach(e=>CN.push({e,f:+e.dataset.from,to:+e.dataset.to,t:+e.dataset.t,d:+e.dataset.d,fmt:e.dataset.fmt||'#'}));
 document.querySelectorAll('.w').forEach(e=>WD.push({e,t:+e.dataset.t}));
 document.querySelectorAll('.eyes').forEach((e,i)=>EY.push({e,ph:i*.83+.4}));
}
function setT(t){
 for(const o of ELS){
  let op=1,dx=0,dy=0,sc=o.s,sx=1,sy=1,r=o.r,clip=null;const u=cl((t-o.t)/o.d);
  switch(o.a){
   case 'pop': sc=o.s*Math.max(0,back(u,2.4));op=cl(u*5);break;
   case 'drop': dy=-150*(1-back(u,1.6));op=cl(u*4);break;
   case 'sl': dx=-260*(1-eo(u));op=cl(u*3);break;
   case 'sr': dx=260*(1-eo(u));op=cl(u*3);break;
   case 'su': dy=180*(1-eo(u));op=cl(u*3);break;
   case 'sd': dy=-180*(1-eo(u));op=cl(u*3);break;
   case 'stamp': sc=o.s*(1+1.7*Math.pow(1-u,2));op=cl(u*3.5);break;
   case 'fade': op=eo(u);break;
   case 'zoom': sc=o.s*(.6+.4*eo(u));op=eo(u);break;
   case 'wipe': clip=`inset(-20% ${100*(1-eio(u))}% -20% -5%)`;break;
   case 'wipel': clip=`inset(-20% -5% -20% ${100*(1-eio(u))}%)`;break;
   case 'wipeu': clip=`inset(${100*(1-eio(u))}% -5% -5% -5%)`;break;
   case 'growx': sx=eo(u);break;
   case 'growy': sy=eo(u);break;
   case 'none': break;
  }
  if(t<o.t)op=0;
  if(o.sk){let v=o.s;for(const [tk,sv] of o.sk){const q=cl((t-tk)/.32);if(q>0)v=v+(sv-v)*back(q,2.2)}sc=sc/o.s*v}
  if(t>=o.o){const q=cl((t-o.o)/o.od);
   if(o.oa==='fade')op*=1-q;else if(o.oa==='pop'){sc*=Math.max(0,1-ein(q));op*=1-cl((q-.7)/.3)}
   else if(o.oa==='up'){dy-=140*eio(q);op*=1-q}else if(o.oa==='left'){dx-=420*ein(q);op*=1-q}
   else if(o.oa==='right'){dx+=420*ein(q);op*=1-q}else if(o.oa==='down'){dy+=220*ein(q);op*=1-q}}
  const k=cl((t-o.t-o.d)/.35),ph=t+o.seed;
  for(const i of o.i){
   if(i==='bob')dy+=k*7*Math.sin(ph*2*Math.PI*.9);
   else if(i==='float')dy+=k*12*Math.sin(ph*2*Math.PI*.42);
   else if(i==='wig')r+=k*3.2*Math.sin(ph*2*Math.PI*1.1);
   else if(i==='sway')r+=k*6*Math.sin(ph*2*Math.PI*.45);
   else if(i==='pulse')sc*=1+k*.04*Math.sin(ph*2*Math.PI*1.25);
   else if(i==='breathe'){sy*=1+k*.025*Math.sin(ph*2*Math.PI*.55);}
   else if(i==='jit'){dx+=k*2.5*Math.sin(t*61+o.seed*5);dy+=k*2*Math.cos(t*47+o.seed*3)}
   else if(i==='drive'){dy+=k*3*Math.abs(Math.sin(ph*2*Math.PI*3.2))}
   else if(i==='blinkop'){op*=.55+.45*Math.abs(Math.sin(ph*2*Math.PI*1.6))}
   else if(i==='spin'){r+=k*(t-o.t)*40}
  }
  const tr=`${o.c?'translate(-50%,-50%) ':''}translate(${dx.toFixed(2)}px,${dy.toFixed(2)}px) rotate(${r.toFixed(2)}deg) scale(${(sc*sx).toFixed(4)},${(sc*sy).toFixed(4)})`;
  o.e.style.transform=tr;o.e.style.opacity=op.toFixed(3);if(clip!==null||o.a.startsWith('wipe'))o.e.style.clipPath=clip||'none';
 }
 for(const d of DR){const u=cl((t-d.t)/d.d);d.p.style.strokeDashoffset=(d.L*(1-eio(u))).toFixed(2);
   d.p.style.opacity=t<d.t?0:(t>=d.o?1-cl((t-d.o)/.3):1)}
 for(const c of CN){const u=cl((t-c.t)/c.d);const v=Math.round(c.f+(c.to-c.f)*eo(u));c.e.textContent=c.fmt.replace('#',v)}
 for(const w of WD){const u=cl((t-w.t)/.24);w.e.style.transform=`translateY(${(-60*(1-back(u,1.8))).toFixed(1)}px) scale(${(1+.35*(1-eo(u))).toFixed(3)})`;w.e.style.opacity=cl(u*4)}
 for(const e of EY){const m=(t+e.ph)%3.3;e.e.style.transform=`scaleY(${m<.13?.12:1})`}
 // kamera
 let z=1+S.push*cl(t/S.dur),dx=0,dy=0,op=1,hop=1;
 for(const [tp,a] of S.punch){if(t>=tp)z+=a*eo(cl((t-tp)/.16))}
 for(const [ts,a] of S.shakes){const p=t-ts;if(p>=0&&p<.7){const e=Math.exp(-p/.13);dx+=a*e*Math.sin(p*95);dy+=a*e*Math.cos(p*81)}}
 if(S.whipIn&&t<.26){const u=eo(t/.26);dx+=170*(1-u);op=cl(t/.14);hop=cl(t/.12)}
 if(S.whipOut&&t>S.dur-.17){const u=cl((t-(S.dur-.17))/.17);dx-=200*ein(u);op=1-u;hop=1-u}
 CAM.style.transform=`translate(${dx.toFixed(2)}px,${dy.toFixed(2)}px) scale(${z.toFixed(4)})`;CAM.style.opacity=op;HB.style.opacity=hop;
 let g=0,dm=0;for(const [a,b,v0,v1] of S.gray){if(t>=a)g=v0+(v1-v0)*eio(cl((t-a)/Math.max(.01,b-a)))}
 for(const [a,b,v0,v1] of S.dim){if(t>=a)dm=v0+(v1-v0)*eio(cl((t-a)/Math.max(.01,b-a)))}
 CAM.style.filter=g>0.001?`grayscale(${g.toFixed(3)})`:'none';DIM.style.opacity=dm;
 let fl=0;for(const tf of S.flash){const p=t-tf;if(p>=0)fl=Math.max(fl,.42*Math.exp(-p/.07))}FL.style.opacity=fl.toFixed(3);
}
"""


# ─────────── elementy ───────────
SND = {"pop": "pop", "drop": "pop", "sl": "swish", "sr": "swish", "su": "swish", "sd": "swish", "stamp": "stamp",
       "zoom": "swish", "wipe": "swipe", "wipel": "swipe", "wipeu": "swipe", "growx": "swipe", "growy": "rise", "fade": None, "none": None}


class Board:
    def __init__(self, fid, head, sub="", color=Y, chip="", src="", push=0.035, origin=(960, 640)):
        self.fid, self.name = fid, f"b{fid:02d}"
        self.head, self.sub, self.color, self.chip, self.src = head, sub, color, chip, src
        self.items, self.ev = [], []
        self.push, self.origin = push, origin
        self.punch, self.shakes, self.flash, self.gray, self.dim = [], [], [], [], []
        self.start = 0.0 if fid == 1 else round(FR[fid]["t0"] - 0.3, 3)
        self.end = round(FR[fid + 1]["t0"] - 0.3, 3) if fid + 1 in FR else None
        self.head_t = self.start + (0.12 if fid > 1 else 0.35)

    # pozycjonowany element HTML; (x,y) = środek
    def el(self, inner, x, y, t, a="pop", d=None, out=None, od=0.3, oa="fade", idle="", rot=0, s=1.0, cls="", style="",
           z=5, og=None, sk=None, snd=True, sx=None, c=True):
        d = d if d is not None else {"pop": 0.42, "stamp": 0.2, "drop": 0.5, "wipe": 0.45, "fade": 0.4}.get(a, 0.38)
        attrs = f'data-a="{a}" data-t="__T{t}__" data-d="{d}" data-r="{rot}" data-s="{s}" data-c="{1 if c else 0}"'
        if out is not None: attrs += f' data-o="__T{out}__" data-od="{od}" data-oa="{oa}"'
        if idle: attrs += f' data-i="{idle}"'
        if og: attrs += f' data-og="{og}"'
        if sk: attrs += ' data-sk="' + ",".join(f"__T{tt}__:{v}" for tt, v in sk) + '"'
        pos = f"left:{x}px;top:{y}px;" if c else f"left:{x}px;top:{y}px;"
        self.items.append(f'<div class="el {cls}" style="{pos}z-index:{z};{style}" {attrs}>{inner}</div>')
        if snd:
            k = SND.get(a) if snd is True else snd
            if k: self.ev.append((k, t, x))
        if out is not None and snd and oa in ("left", "right", "up", "down", "pop"): self.ev.append(("swish_s", out, x))
        if sk and snd:
            for tt, v in sk: self.ev.append(("pop", tt, x))
        return self

    def svg(self, s, t=None, d=None, snd="marker", x=960):
        """surowy fragment SVG (ścieżki z data-draw itp.) na pełnym płótnie"""
        self.items.append(f'<svg class="lay" style="z-index:4">{s}</svg>')
        if t is not None and snd: self.ev.append((snd, t, x, d or 0.5))
        return self

    def draw(self, d, t, du, color="#fff", w=8, dash=None, x=960, z=4, out=None, head=False, snd="marker"):
        """rysowana linia; dash → przerywana (przez maskę)"""
        oid = f"m{self.fid}_{len(self.items)}"
        o = f' data-o="__T{out}__"' if out is not None else ""
        if dash:
            s = (f'<defs><mask id="{oid}" maskUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080"><path d="{d}" fill="none" stroke="#fff" stroke-width="{w + 16}" stroke-linecap="round" stroke-linejoin="round" data-draw="1" data-t="__T{t}__" data-d="{du}"{o}/></mask></defs>'
                 f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-dasharray="{dash}" stroke-linecap="round" mask="url(#{oid})"/>')
        else:
            s = f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" data-draw="1" data-t="__T{t}__" data-d="{du}"{o}/>'
        self.items.append(f'<svg class="lay" style="z-index:{z}">{s}</svg>')
        if snd: self.ev.append((snd, t, x, du))
        return self

    def count(self, x, y, frm, to, t, du, fmt="#", size=200, color=Y, cls="big", a="pop", z=6):
        inner = f'<span data-count="1" data-from="{frm}" data-to="{to}" data-t="__T{t}__" data-d="{du}" data-fmt="{fmt}">{fmt.replace("#", str(frm))}</span>'
        self.el(inner, x, y, t, a=a, cls=cls, style=f"font-size:{size}px;color:{color}", z=z)
        self.ev.append(("ticks", t, x, du))
        return self

    def shake(self, t, amp=10, thud=True):
        self.shakes.append([t, amp])
        if thud: self.ev.append(("boom", t, 960, min(1.0, amp / 14)))
        return self

    def sfx(self, kind, t, x=960, *extra):
        self.ev.append((kind, t, x) + tuple(extra)); return self

    # ── HTML ──
    def html(self):
        off = self.start
        import re
        fix = lambda s: re.sub(r"__T(-?[\d.]+)__", lambda m: f"{float(m.group(1)) - off:.3f}", s)
        loc = lambda v: round(v - off, 3)
        words = self.head.split(" ")
        ht = "".join(f'<span class="w" data-t="{loc(self.head_t) + 0.075 * i:.3f}">{w}</span>' for i, w in enumerate(words))
        sub = (f'<div class="sub el" style="left:96px;top:180px" data-a="fade" data-t="{loc(self.head_t) + 0.25:.3f}" data-d="0.35" data-c="0">{self.sub}</div>'
               if self.sub else "")
        chip = f'<div class="chip">{self.chip}</div>' if self.chip else ""
        src = f'<div class="src">{self.src}</div>' if self.src else ""
        cfg = dict(dur=round(self.end - off, 3), push=self.push, punch=[[loc(a), b] for a, b in self.punch],
                   shakes=[[loc(a), b] for a, b in self.shakes], flash=[loc(a) for a in self.flash],
                   gray=[[loc(a), loc(b), c, d] for a, b, c, d in self.gray], dim=[[loc(a), loc(b), c, d] for a, b, c, d in self.dim],
                   whipIn=self.fid > 1, whipOut=self.fid < max(FR), hmax=1360 if self.chip else 1720)
        body = f"""<div class="f">{DEFS}<div id="bg"></div><div id="grid"></div>
<div id="cam" style="transform-origin:{self.origin[0]}px {self.origin[1]}px">{fix("".join(self.items))}</div><div id="dim"></div>
<div class="bar"><div id="hb"><div class="h" style="color:{self.color}">{ht}</div>{fix(sub)}{chip}</div></div>
{src}<div class="logo">nie wiem, ale bangla</div><div class="badge">?!</div><div class="grain"></div><div id="flash"></div></div>
<script>window.SCENE={json.dumps(cfg)};{JS}</script>"""
        return page(FONTS, CSS, body, W, H)

    def events(self):
        ev = [("whip", self.start + 0.02, 1200)] if self.fid > 1 else []
        ev.append(("hit", self.head_t, 400))
        for t, a in self.punch: ev.append(("swish_s", t, 960))
        for t in self.flash: ev.append(("snap", t, 960))
        return ev + self.ev


# ─────────── grafiki (oryginalne rysunki) ───────────
def bear_head(helmet=True, cub=False, mood="ok", size=300):
    fur, dark, mz = ("#a06a35", "#7b4a22", "#e0b88a") if cub else ("#8b5a2b", "#6e4220", "#d2a679")
    ey = 20 if cub else 16
    if mood == "sleepy":
        eyes = '<path d="M-68 -6 Q-50 4 -32 -6 M32 -6 Q50 4 68 -6" stroke="#111" stroke-width="9" fill="none" stroke-linecap="round"/>'
    elif mood == "sad":
        eyes = (f'<g class="eyes"><circle cx="-50" cy="-4" r="{ey}" fill="#111"/><circle cx="50" cy="-4" r="{ey}" fill="#111"/>'
                f'<circle cx="-44" cy="-10" r="5" fill="#fff"/><circle cx="56" cy="-10" r="5" fill="#fff"/></g>'
                '<path d="M-76 -30 L-32 -44 M76 -30 L32 -44" stroke="#3a2412" stroke-width="8" stroke-linecap="round"/>')
    else:
        eyes = (f'<g class="eyes"><circle cx="-50" cy="-8" r="{ey}" fill="#111"/><circle cx="50" cy="-8" r="{ey}" fill="#111"/>'
                f'<circle cx="-44" cy="-14" r="{5 + (2 if cub else 0)}" fill="#fff"/><circle cx="56" cy="-14" r="{5 + (2 if cub else 0)}" fill="#fff"/></g>')
    mouth = ('<path d="M-18 76 Q0 66 18 76" stroke="#1a1110" stroke-width="7" fill="none" stroke-linecap="round"/>' if mood == "sad"
             else '<path d="M-16 74 Q0 90 16 74" stroke="#1a1110" stroke-width="7" fill="none" stroke-linecap="round"/>')
    hel = ('<path d="M-118 -40 C-110 -150 110 -150 118 -40 Z" fill="#55652f"/><rect x="-140" y="-52" width="280" height="26" rx="13" fill="#46552a"/>'
           '<path d="M-60 -112 Q0 -128 60 -112" stroke="#6f8240" stroke-width="8" fill="none" stroke-linecap="round"/>') if helmet else ""
    return f"""<svg width="{size}" height="{size}" viewBox="-170 -170 340 340" style="overflow:visible;display:block"><g filter="url(#stk)">
<circle cx="-92" cy="-70" r="44" fill="{dark}"/><circle cx="92" cy="-70" r="44" fill="{dark}"/><circle cx="-92" cy="-70" r="22" fill="{mz}"/><circle cx="92" cy="-70" r="22" fill="{mz}"/>
<ellipse cx="0" cy="10" rx="138" ry="124" fill="{fur}"/><ellipse cx="0" cy="62" rx="66" ry="50" fill="{mz}"/><ellipse cx="0" cy="38" rx="26" ry="18" fill="#1a1110"/>
{mouth}{eyes}{hel}</g></svg>"""


def bear_body(helmet=True, carry="crate", size=520):
    """cały miś na tylnych łapach; carry: crate | shell | none"""
    fur, dark, mz = "#8b5a2b", "#6e4220", "#d2a679"
    hel = ('<path d="M-118 -40 C-110 -150 110 -150 118 -40 Z" fill="#55652f"/><rect x="-140" y="-52" width="280" height="26" rx="13" fill="#46552a"/>') if helmet else ""
    head = f"""<g transform="translate(0,-205) scale(.78)"><circle cx="-92" cy="-70" r="44" fill="{dark}"/><circle cx="92" cy="-70" r="44" fill="{dark}"/>
<circle cx="-92" cy="-70" r="22" fill="{mz}"/><circle cx="92" cy="-70" r="22" fill="{mz}"/><ellipse cx="0" cy="10" rx="138" ry="124" fill="{fur}"/>
<ellipse cx="0" cy="62" rx="66" ry="50" fill="{mz}"/><ellipse cx="0" cy="38" rx="26" ry="18" fill="#1a1110"/>
<path d="M-16 74 Q0 90 16 74" stroke="#1a1110" stroke-width="7" fill="none" stroke-linecap="round"/>
<g class="eyes"><circle cx="-50" cy="-8" r="16" fill="#111"/><circle cx="50" cy="-8" r="16" fill="#111"/><circle cx="-44" cy="-14" r="5" fill="#fff"/><circle cx="56" cy="-14" r="5" fill="#fff"/></g>{hel}</g>"""
    legs = f'<rect x="-108" y="150" width="78" height="120" rx="36" fill="{dark}"/><rect x="30" y="150" width="78" height="120" rx="36" fill="{dark}"/>'
    body = f'<ellipse cx="0" cy="40" rx="135" ry="160" fill="{fur}"/><ellipse cx="0" cy="70" rx="80" ry="105" fill="{mz}"/>'
    if carry == "crate":
        load = ('<g transform="translate(0,40) rotate(-3)"><rect x="-130" y="-70" width="260" height="150" rx="10" fill="#b8843f"/>'
                '<rect x="-130" y="-70" width="260" height="150" rx="10" fill="none" stroke="#7a5524" stroke-width="10"/>'
                '<path d="M-130 -20 H130 M-130 30 H130" stroke="#7a5524" stroke-width="8"/>'
                '<text x="0" y="16" text-anchor="middle" font-family="Poppins" font-weight="900" font-size="34" fill="#2a1a0a">AMUNICJA</text></g>'
                f'<circle cx="-138" cy="40" r="34" fill="{dark}"/><circle cx="138" cy="40" r="34" fill="{dark}"/>')
        arms = f'<rect x="-175" y="-60" width="64" height="130" rx="30" fill="{dark}" transform="rotate(18 -143 -60)"/><rect x="111" y="-60" width="64" height="130" rx="30" fill="{dark}" transform="rotate(-18 143 -60)"/>'
    elif carry == "shell":
        load = ('<g transform="translate(60,10) rotate(-35)"><rect x="-38" y="-60" width="76" height="190" rx="8" fill="#c9a24a"/>'
                '<path d="M-38 -60 Q-38 -150 0 -175 Q38 -150 38 -60 Z" fill="#9aa0a8"/><rect x="-38" y="110" width="76" height="22" fill="#a07f2e"/></g>'
                f'<circle cx="-12" cy="-28" r="34" fill="{dark}"/><circle cx="104" cy="58" r="34" fill="{dark}"/>')
        arms = f'<rect x="-150" y="-50" width="64" height="140" rx="30" fill="{dark}" transform="rotate(-40 -118 -50)"/><rect x="100" y="-70" width="64" height="120" rx="30" fill="{dark}" transform="rotate(30 132 -70)"/>'
    else:
        load = ""
        arms = f'<rect x="-178" y="-40" width="64" height="160" rx="30" fill="{dark}" transform="rotate(14 -146 -40)"/><rect x="114" y="-40" width="64" height="160" rx="30" fill="{dark}" transform="rotate(-14 146 -40)"/>'
    return f"""<svg width="{size}" height="{size}" viewBox="-260 -360 520 650" style="overflow:visible;display:block"><g filter="url(#stk)">{legs}{arms}{body}{head}{load}</g></svg>"""


def emo(ch, size=170, flat=False):
    return f'<div class="emo{" flat" if flat else ""}" style="font-size:{size}px">{ch}</div>'


def card(inner, w, h, border="#fff", style=""):
    return f'<div class="card" style="width:{w}px;height:{h}px;border-color:{border};{style}">{inner}</div>'


# ─────────── mapa (uproszczona) ───────────
PLACES = {"Szkocja": (-3.2, 55.9), "Edynburg": (-3.2, 55.95), "Duns": (-2.35, 55.78), "Monte Cassino": (13.8, 41.5),
          "Włochy": (13.8, 41.5), "Egipt": (31.2, 30.0), "Palestyna": (35.2, 31.8), "Syria": (36.3, 33.5), "Irak": (44.4, 33.3),
          "Iran": (51.4, 35.7), "Polska": (21.0, 52.2), "Kraków": (19.9, 50.06), "Poznań": (16.9, 52.4), "ZSRR": (58.0, 47.0)}

def proj(view):
    lo0, lo1, la0, la1, x0, x1, y0, y1 = view
    def f(lo, la):
        return x0 + (lo - lo0) / (lo1 - lo0) * (x1 - x0), y1 - (la - la0) / (la1 - la0) * (y1 - y0)
    return f

WORLD = proj((-8, 60, 25, 60, 160, 1820, 300, 980))


# ─────────── render ───────────
async def open_board(b, board):
    pg = await b.new_page(viewport={"width": W, "height": H})
    pg.on("pageerror", lambda e: print("JS ERR", board.name, e, flush=True))
    f = f"{OUT}/sceny/_{board.name}.html"
    open(f, "w", encoding="utf-8").write(board.html())
    await pg.goto(f"file://{f}", wait_until="networkidle")
    await pg.evaluate("document.fonts.ready.then(()=>0)")
    await pg.wait_for_timeout(250)
    await pg.evaluate("init()")
    return pg

async def stills(boards, spec, out_dir):
    from playwright.async_api import async_playwright
    res = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        for bd in boards:
            if bd.name not in spec: continue
            pg = await open_board(b, bd)
            for t in spec[bd.name]:
                await pg.evaluate(f"setT({t - bd.start})")
                p = f"{out_dir}/kadr_{bd.name}_{t:06.2f}.jpg"
                await pg.screenshot(path=p, type="jpeg", quality=80); res.append(p)
            await pg.close()
        await b.close()
    return res

async def render_board(board):
    from playwright.async_api import async_playwright
    f0, f1 = int(round(board.start * FPS)), int(round(board.end * FPS))
    tmp, dst = f"{OUT}/sceny/scena_{board.name}.tmp.mp4", f"{OUT}/sceny/scena_{board.name}.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg",
                           "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
                           "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await open_board(b, board)
        for i in range(f0, f1):
            await pg.evaluate(f"setT({i / FPS - board.start:.5f})")
            ff.stdin.write(await pg.screenshot(type="jpeg", quality=92))
        await b.close()
    ff.stdin.close()
    if ff.wait() == 0:
        os.replace(tmp, dst); print("ok", board.name, f1 - f0, flush=True)
    else:
        print("FAIL", board.name, flush=True)
