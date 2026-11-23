"""Silnik plansz „Ukryta Lekcja" – tablica, kreda, maskotka, kamera. Czasy w elementach są absolutne (sekundy odcinka)."""
import sys, os, math, json, subprocess, asyncio
sys.path.insert(0, "/home/claude/faceless-konta/tools")
from templates import links, page

W, H, FPS = 1920, 1080, 30
FONTS = links(["caveat/700.css", "kalam/400.css", "kalam/700.css"])
CH, YL, RED = "#EDEBE4", "#F5C542", "#E07A6A"
GROUND, MX = 860, 1580

CSS = """
body{margin:0;background:#15191a}
.b{width:1920px;height:1080px;position:relative;overflow:hidden;background:#15191a;font-family:'Kalam',cursive;color:#EDEBE4}
#cam{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0}
.board{position:absolute;inset:0;background:radial-gradient(1200px 700px at 50% 45%,#262b2c,#15191a 75%)}
.dust{position:absolute;inset:0;opacity:.16;mix-blend-mode:screen;pointer-events:none;
 background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.75' numOctaves='3'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .55 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
.smudge{position:absolute;border-radius:50%;background:rgba(255,255,255,.05);filter:blur(40px)}
#resid{position:absolute;inset:0}
#resid i{position:absolute;display:block;height:120px;border-radius:60px;background:rgba(255,255,255,.035);filter:blur(18px)}
#content{position:absolute;inset:0}
.ch{filter:url(#chalk)}
.tx{position:absolute;white-space:nowrap;line-height:1.2;visibility:hidden;transform-origin:0 50%}
.cv{font-family:'Caveat';font-weight:700;line-height:1}
.y{color:#F5C542} .r{color:#E07A6A}
.dim{opacity:.72}
.box{position:absolute;visibility:hidden;border:6px solid #EDEBE4;border-radius:14px}
.box.yb{border-color:#F5C542}
.bub{position:absolute;visibility:hidden;white-space:nowrap;border:5px solid #EDEBE4;border-radius:44px;padding:10px 34px;font-size:46px;line-height:1.25}
.vig{position:absolute;inset:0;visibility:hidden;background:radial-gradient(900px 560px at 45% 50%,rgba(0,0,0,0) 35%,rgba(0,0,0,.62) 100%)}
.streak{position:absolute;visibility:hidden;width:70px;border-radius:40px;background:rgba(237,235,228,.10);filter:blur(10px)}
.cell{position:absolute;visibility:hidden;width:62px;height:62px;border:5px solid #EDEBE4;border-radius:8px;opacity:.8}
svg.lay{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible}
svg.lay path{fill:none;stroke-linecap:round;stroke-linejoin:round;visibility:hidden}
.bar{position:absolute;transform-origin:50% 100%;visibility:hidden;border:7px solid #EDEBE4;border-bottom:none;
 background:repeating-linear-gradient(-45deg,rgba(237,235,228,.16) 0 6px,transparent 6px 22px)}
.bar.yb{border-color:#F5C542;background:repeating-linear-gradient(-45deg,rgba(245,197,66,.22) 0 6px,transparent 6px 22px)}
.wipe{position:absolute;height:34px;border-radius:20px;visibility:hidden;
 background:linear-gradient(90deg,rgba(237,235,228,.0),rgba(237,235,228,.24) 6%,rgba(237,235,228,.16) 75%,rgba(237,235,228,0));filter:blur(3px)}
#mascot{position:absolute;overflow:visible;transform-origin:160px 511px}
#sponge{position:absolute;left:0;top:0;width:260px;height:120px;display:none;border-radius:16px;
 background:linear-gradient(180deg,#8a6a48,#6f5236 70%,#4a4a48 70%,#5b5a56);box-shadow:0 10px 26px rgba(0,0,0,.45)}
#sponge:after{content:"";position:absolute;left:18px;right:18px;top:16px;height:10px;border-radius:6px;background:rgba(255,255,255,.12)}
.brand{position:absolute;right:70px;bottom:46px;font-family:'Caveat';font-weight:700;font-size:44px;letter-spacing:2px;opacity:.75;color:#F5C542}
#fade{position:absolute;inset:0;background:#000;opacity:0;pointer-events:none}
"""

DEFS = """<svg width="0" height="0" style="position:absolute">
<filter id="chalk"><feTurbulence type="fractalNoise" baseFrequency="1.2" numOctaves="2" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="3"/><feComponentTransfer><feFuncA type="table" tableValues="0 .85 .95"/></feComponentTransfer></filter>
<filter id="chalkp" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2320" height="1480"><feTurbulence type="fractalNoise" baseFrequency="1.2" numOctaves="2" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="3"/><feComponentTransfer><feFuncA type="table" tableValues="0 .85 .95"/></feComponentTransfer></filter></svg>"""

RESID = "".join(f'<i style="left:{x}px;top:{y}px;width:{w}px"></i>' for x, y, w in
                [(120, 170, 1250), (90, 330, 1350), (140, 500, 1200), (100, 660, 1300), (160, 820, 1150)])

MASCOT = f"""<svg id="mascot" class="ch" width="320" height="560" viewBox="-160 -40 320 560">
<g stroke="{CH}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" fill="none">
<g id="mhead"><path d="M0 -10 a62 62 0 1 1 -0.1 0" fill="{CH}" stroke="none"/>
<path d="M-34 84 L-48 128 L48 128 L34 84 Z" fill="{CH}" stroke="none"/>
<g id="eyes"><ellipse id="e1" cx="-22" cy="44" rx="9" ry="9" fill="#1d2122" stroke="none"/><ellipse id="e2" cx="22" cy="44" rx="9" ry="9" fill="#1d2122" stroke="none"/></g></g>
<path d="M0 128 L0 330"/><path id="mL"/><path id="mR"/><path id="lL"/><path id="lR"/>
<path id="chalkst" stroke-width="10" stroke-linecap="butt" stroke="#ffffff" visibility="hidden"/></g></svg>"""

JS = r"""
const E=window.SCENE;
const ease=x=>x<=0?0:x>=1?1:x*x*(3-2*x);
const cl=x=>x<0?0:x>1?1:x;
const lerp=(a,b,q)=>a+(b-a)*q;
const eob=x=>{const c1=1.9,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const R=Math.PI/180, L1=72, L2=68, SX=0, SY=175;
const P={
 hips:{L:[-63,35],R:[63,-35],h:0}, hang:{L:[-10,-4],R:[10,4],h:0},
 pointL:{L:[-128,-122],R:[12,4],h:-4}, pointLlow:{L:[-98,-92],R:[12,4],h:-3}, pointDown:{L:[-48,-52],R:[63,-35],h:-10},
 shrug:{L:[-72,-150],R:[72,150],h:8}, idea:{L:[-63,35],R:[125,165],h:-3},
 think:{L:[-63,35],R:[54,200],h:6}, facepalm:{L:[-12,-5],R:[140,206],h:-9},
 wow:{L:[-118,-155],R:[118,155],h:0}, wave:{L:[-63,35],R:[110,160],h:4},
 heart:{L:[-63,35],R:[20,200],h:4}, give:{L:[-98,-92],R:[63,-35],h:-3},
 trip:{L:[-140,-150],R:[70,125],h:12,rot:-28}, down:{L:[-165,-178],R:[165,178],h:0,rot:-84}
};
let items,byId={},widths=new Map(),content,sponge,resid,fade,cam,mascot,mL,mR,lL,lR,mhead,eyes,e1,e2,chalkst;
function init(){
  items=[...document.querySelectorAll('[data-k]')];
  for(const el of items){
    if(el.dataset.id) byId[el.dataset.id]=el;
    el._base=parseFloat(getComputedStyle(el).opacity)||1;
    if(el.dataset.k==='w'||el.dataset.k==='p') widths.set(el,el.offsetWidth||el.getBoundingClientRect().width);
    if(el.dataset.k==='d'){el.setAttribute('pathLength','1');el.style.strokeDasharray='1 1';el._len=el.getTotalLength();}
  }
  const g=id=>document.getElementById(id);
  content=g('content');sponge=g('sponge');resid=g('resid');fade=g('fade');cam=g('cam');mascot=g('mascot');
  mL=g('mL');mR=g('mR');lL=g('lL');lR=g('lR');mhead=g('mhead');eyes=g('eyes');e1=g('e1');e2=g('e2');chalkst=g('chalkst');
}
function prog(el,t){return cl((t-(+el.dataset.t0))/(+el.dataset.du));}
function tipOf(id,t){ const el=byId[id]; const q=prog(el,t);
  if(el.dataset.k==='d'){const p=el.getPointAtLength(q*el._len);return [p.x,p.y,q];}
  return [el.offsetLeft+q*widths.get(el), el.offsetTop+el.offsetHeight*0.6, q]; }
function angPts(a){const ex=SX+Math.sin(a[0]*R)*L1, ey=SY+Math.cos(a[0]*R)*L1;return [ex,ey,ex+Math.sin(a[1]*R)*L2,ey+Math.cos(a[1]*R)*L2];}
function ik(tx,ty){ const vx=tx-SX,vy=ty-SY; let d=Math.hypot(vx,vy); d=Math.max(Math.abs(L1-L2)+1,Math.min(d,L1+L2-1));
  const an=Math.atan2(vy,vx), a=Math.acos((L1*L1+d*d-L2*L2)/(2*L1*d));
  const c1=[SX+L1*Math.cos(an+a),SY+L1*Math.sin(an+a)], c2=[SX+L1*Math.cos(an-a),SY+L1*Math.sin(an-a)];
  const el=c1[1]>c2[1]?c1:c2; return [el[0],el[1],SX+d*Math.cos(an),SY+d*Math.sin(an)]; }
function mstate(t){
  let x=E.mx0, walking=false, w=0, phi=0, dir=0;
  for(const m of E.moves){ const [a,b,x0,x1]=m;
    if(t>=b){x=x1;continue} if(t>=a){const q=ease((t-a)/(b-a)); x=lerp(x0,x1,q); walking=true; dir=Math.sign(x1-x0);
      w=Math.min(1,(t-a)/0.15,(b-t)/0.15); phi=Math.abs(x-x0)/110*2*Math.PI;} break; }
  let jy=0; for(const j of E.jumps){const u=(t-j)/0.45; if(u>0&&u<1) jy=-85*Math.sin(Math.PI*u);}
  return {x,walking,w:Math.max(0,w),phi,dir,jy};
}
function spec(k,t,ms){
  if(k[1]==='ik'){ const [tx,ty,q]=tipOf(k[2],t); const top=E.mtop+ms.yoff;
    let lx=tx-ms.x, ly=ty-top-40; if(q>0&&q<1) ly+=5*Math.sin(t*70);
    if(k[3]==='R') return {L:{a:P.hips.L},R:{p:ik(lx,ly)},h:-5,rot:0,name:'ik',hand:'R'};
    return {L:{p:ik(lx,ly)},R:{a:P.hips.R},h:-5,rot:0,name:'ik',hand:'L'}; }
  const p=P[k[1]]; return {L:{a:p.L},R:{a:p.R},h:p.h,rot:p.rot||0,name:k[1]};
}
function blendArm(A,B,b){ if(b>=1) return B; if(b<=0) return A; if(A.a&&B.a) return {a:[lerp(A.a[0],B.a[0],b),lerp(A.a[1],B.a[1],b)]};
  const pa=A.p||angPts(A.a), pb=B.p||angPts(B.a); return {p:pa.map((v,i)=>lerp(v,pb[i],b))}; }
function poseAt(t,ms){ const ks=E.poses; let i=0; while(i+1<ks.length&&ks[i+1][0]<=t) i++;
  const cur=spec(ks[i],t,ms); if(i===0) return Object.assign(cur,{b:1});
  const pr=spec(ks[i-1],t,ms), b=ease((t-ks[i][0])/0.3);
  return {L:blendArm(pr.L,cur.L,b),R:blendArm(pr.R,cur.R,b),h:lerp(pr.h,cur.h,b),rot:lerp(pr.rot,cur.rot,b),name:cur.name,hand:cur.hand,b}; }
function pathArm(A){const p=A.p||angPts(A.a);return [`M${SX} ${SY} L${p[0].toFixed(1)} ${p[1].toFixed(1)} L${p[2].toFixed(1)} ${p[3].toFixed(1)}`,p];}
function camAt(t){ let s=1,cx=960,cy=540;
  for(const k of E.cam){ if(t<k[0]) break; const q=ease((t-k[0])/(k[4]||0.5)); s=lerp(s,k[1],q); cx=lerp(cx,k[2],q); cy=lerp(cy,k[3],q); }
  let tx=960-cx*s, ty=540-cy*s; tx=Math.min(0,Math.max(1920-1920*s,tx)); ty=Math.min(0,Math.max(1080-1080*s,ty));
  for(const sh of E.shakes){ const u=(t-sh[0])/0.35; if(u>=0&&u<1){ const a=sh[1]*(1-u)*(1-u); tx+=a*Math.sin(t*93); ty+=a*Math.cos(t*71); } }
  return [tx,ty,s]; }
function setT(t){
  const T=E.T0+t;
  for(const el of items){ const k=el.dataset.k, q=prog(el,t), r=+(el.dataset.r||0), cx=el.dataset.cx?'translateX(-50%) ':'';
    let op=1;
    if(k==='w'){ if(q<=0){el.style.visibility='hidden';continue} el.style.visibility='visible';
      const x=q*(widths.get(el)+70); const m=q>=1?'none':`linear-gradient(90deg,#000 ${x-60}px,transparent ${x}px)`;
      el.style.webkitMaskImage=m; el.style.maskImage=m; el.style.transform=`${cx}rotate(${r}deg)`; }
    else if(k==='p'||k==='c'){ if(q<=0){el.style.visibility='hidden';continue} el.style.visibility='visible';
      const sc=1.7-0.7*eob(q); el.style.transform=`${cx}rotate(${r}deg) scale(${sc.toFixed(4)})`; op=Math.min(1,q*4);
      if(k==='c') el.textContent=(el.dataset.pre||'')+Math.round(ease(cl((t-(+el.dataset.t0))/(+el.dataset.cd)))*(+el.dataset.to))+(el.dataset.suf||''); }
    else if(k==='f'){ if(q<=0){el.style.visibility='hidden';continue} el.style.visibility='visible'; op=ease(q); if(cx||r) el.style.transform=`${cx}rotate(${r}deg)`; }
    else if(k==='d'){ el.style.visibility=q<=0?'hidden':'visible'; el.style.strokeDashoffset=(1-q).toFixed(4); }
    else if(k==='g'){ el.style.visibility=q<=0?'hidden':'visible'; el.style.transform=`scaleY(${ease(q).toFixed(4)})`; }
    if(el.dataset.out){ const qo=cl((t-(+el.dataset.out))/(+(el.dataset.od||0.4))); op*=1-qo; }
    el.style.opacity=(op*el._base).toFixed(3);
  }
  const ms=mstate(t); ms.yoff=ms.jy-7*Math.abs(Math.sin(ms.phi))*ms.w+3.5*Math.sin(T*2*Math.PI/2.6);
  const p=poseAt(t,ms); const sw=2*Math.sin(T*2.1);
  if(p.L.a) p.L.a=[p.L.a[0]-sw,p.L.a[1]-sw]; if(p.R.a) p.R.a=[p.R.a[0]+sw,p.R.a[1]+sw];
  if(ms.w>0 && (p.name==='hips'||p.name==='hang') && p.b>=1 && p.L.a && p.R.a){ const s=Math.sin(ms.phi);
    const wl=[-24+16*s,-34+18*s], wr=[24+16*s,34+18*s];
    p.L={a:[lerp(p.L.a[0],wl[0],ms.w),lerp(p.L.a[1],wl[1],ms.w)]}; p.R={a:[lerp(p.R.a[0],wr[0],ms.w),lerp(p.R.a[1],wr[1],ms.w)]}; }
  const [dL,pl]=pathArm(p.L),[dR,pr]=pathArm(p.R); mL.setAttribute('d',dL); mR.setAttribute('d',dR);
  if(p.name==='ik'&&p.b>0.6){ const pp=p.hand==='R'?pr:pl; const ex=pp[0],ey=pp[1],hx=pp[2],hy=pp[3],n=Math.hypot(hx-ex,hy-ey)||1;
    chalkst.setAttribute('d',`M${hx.toFixed(1)} ${hy.toFixed(1)} L${(hx+(hx-ex)/n*20).toFixed(1)} ${(hy+(hy-ey)/n*20).toFixed(1)}`); chalkst.setAttribute('visibility','visible'); }
  else chalkst.setAttribute('visibility','hidden');
  const inAir=ms.jy<-5; const la=ms.w>0?24*Math.sin(ms.phi)*ms.w-17*(1-ms.w):(inAir?-8:-17);
  const ra=ms.w>0?-24*Math.sin(ms.phi)*ms.w+17*(1-ms.w):(inAir?8:17);
  lL.setAttribute('d',`M0 330 L${(Math.sin(la*R)*148).toFixed(1)} ${(330+Math.cos(la*R)*148).toFixed(1)}`);
  lR.setAttribute('d',`M0 330 L${(Math.sin(ra*R)*148).toFixed(1)} ${(330+Math.cos(ra*R)*148).toFixed(1)}`);
  const h=p.h+1.5*Math.sin(T*1.3)+3*Math.sin(2*ms.phi)*ms.w;
  mhead.setAttribute('transform',`rotate(${h.toFixed(2)} 0 128)`);
  let ed=0; if(ms.walking) ed=6*ms.dir; else if(['pointL','pointLlow','pointDown','give'].includes(p.name)||(p.name==='ik'&&p.hand!=='R')) ed=-6; else if(p.name==='wave'||(p.name==='ik'&&p.hand==='R')) ed=4;
  eyes.setAttribute('transform',`translate(${ed} 0)`);
  const bl=(T%3.9)<0.13?0.15:1; e1.setAttribute('ry',9*bl); e2.setAttribute('ry',9*bl);
  mascot.style.left=(ms.x-160).toFixed(1)+'px'; mascot.style.top=(E.mtop+ms.yoff).toFixed(1)+'px';
  mascot.style.transform=`rotate(${(p.rot||0).toFixed(2)}deg)`;
  if(E.erase){ const [a,b]=E.erase, q=(t-a)/(b-a);
    if(q>0&&q<1){ const qe=ease(q)*0.35+q*0.65, X=-260+qe*(1920+520), Y=560+300*Math.sin(q*Math.PI*2*5.5);
      sponge.style.display='block';
      sponge.style.transform=`translate(${(X-130).toFixed(1)}px,${(Y-60).toFixed(1)}px) rotate(${(-8+5*Math.sin(q*47)).toFixed(2)}deg)`;
      const m=`linear-gradient(90deg,transparent ${X-30}px,#000 ${X+90}px)`; content.style.webkitMaskImage=m; content.style.maskImage=m;
      if(!E.residStatic){const m2=`linear-gradient(90deg,#000 ${X-30}px,transparent ${X+90}px)`;resid.style.webkitMaskImage=m2;resid.style.maskImage=m2;}
    } else { sponge.style.display='none';
      if(q>=1){content.style.visibility='hidden'; if(!E.residStatic){resid.style.webkitMaskImage='none';resid.style.maskImage='none'}}
      else {content.style.visibility='visible';content.style.webkitMaskImage='none';content.style.maskImage='none';
        if(!E.residStatic){resid.style.webkitMaskImage='linear-gradient(#0000,#0000)';resid.style.maskImage='linear-gradient(#0000,#0000)'}} }
  } else if(!E.residStatic){resid.style.webkitMaskImage='linear-gradient(#0000,#0000)';resid.style.maskImage='linear-gradient(#0000,#0000)'}
  const [tx,ty,s]=camAt(t); cam.style.transform=`translate(${tx.toFixed(2)}px,${ty.toFixed(2)}px) scale(${s.toFixed(4)})`;
  let o=0; if(E.fadeIn) o=Math.max(o,1-cl(t/E.fadeIn)); if(E.fadeOut) o=Math.max(o,cl((t-(E.dur-E.fadeOut))/E.fadeOut));
  fade.style.opacity=o.toFixed(3);
}
"""

# ─────────── elementy (czasy absolutne; __T0__ podmieniane przy budowie) ───────────
_rot = [0.6, -0.5, 0.3, -0.8, 0.5, -0.3, 0.8, -0.6, 0.2, -0.4]
_ri = [0]
def _r():
    _ri[0] += 1
    return _rot[_ri[0] % len(_rot)]

def _attrs(t0, du, out=None, od=0.4, id=None, cx=False, r=None):
    s = f' data-t0="__T{t0:.3f}__" data-du="{du}"'
    if out is not None: s += f' data-out="__T{out:.3f}__" data-od="{od}"'
    if id: s += f' data-id="{id}"'
    if cx: s += ' data-cx="1"'
    if r is not None: s += f' data-r="{r}"'
    return s

def T(txt, x, y, t0, du=None, size=80, cls="", cv=False, id=None, out=None, cx=False, snd=True):
    du = du or max(0.3, round(len(txt) * 0.032, 2))
    c = "tx ch " + ("cv " if cv else "") + cls
    w = len(txt) * size * (0.42 if cv else 0.5)
    return dict(k="html", t=t0, s=f'<div class="{c}" data-k="w"{_attrs(t0, du, out, 0.4, id, cx, _r() if size >= 60 else 0)} style="left:{x}px;top:{y}px;font-size:{size}px">{txt}</div>',
                ev=("write", t0, du, x if cx else x + w / 2, size) if snd else None)

def POP(txt, x, y, t0, size=120, cls="", cv=True, du=0.32, out=None, cx=False, thud=1.0):
    c = "tx ch " + ("cv " if cv else "") + cls
    return dict(k="html", t=t0, s=f'<div class="{c}" data-k="p"{_attrs(t0, du, out, 0.4, None, cx, _r())} style="left:{x}px;top:{y}px;font-size:{size}px">{txt}</div>',
                ev=("thud", t0 + 0.05, thud, x) if thud else None)

def D(d, t0, du, color=CH, w=9, id=None, x=900, out=None, snd="draw"):
    return dict(k="svg", t=t0, s=f'<path filter="url(#chalkp)" data-k="d"{_attrs(t0, du, out, 0.4, id)} d="{d}" stroke="{color}" stroke-width="{w}"/>',
                ev=(snd, t0, du, x) if snd else None)

def BAR(x, base, w, h, t0, du, yellow=False, out=None):
    return dict(k="html", t=t0, s=f'<div class="bar ch{" yb" if yellow else ""}" data-k="g"{_attrs(t0, du, out)} style="left:{x}px;top:{base-h}px;width:{w}px;height:{h}px"></div>',
                ev=("draw", t0, du, x + w / 2))

def CNT(x, y, to, t0, cd, size=110, pre="+", suf="%", out=None):
    return dict(k="html", t=t0, s=f'<div class="tx ch cv y" data-k="c"{_attrs(t0, 0.3, out)} data-cd="{cd}" data-to="{to}" data-pre="{pre}" data-suf="{suf}" data-r="-2" style="left:{x}px;top:{y}px;font-size:{size}px"></div>',
                ev=("ticks", t0, cd, x + 100))

def WIPE(x, y, w, t0, du=0.4):
    return dict(k="html", t=t0, s=f'<div class="wipe" data-k="w"{_attrs(t0, du)} style="left:{x}px;top:{y}px;width:{w}px"></div>',
                ev=("rub", t0, du, x + w / 2))

def BOX(x, y, w, h, t0, du=0.6, yellow=False, out=None, inner="", style=""):
    return dict(k="html", t=t0, s=f'<div class="box ch{" yb" if yellow else ""}" data-k="w"{_attrs(t0, du, out)} style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{style}">{inner}</div>',
                ev=("draw", t0, du, x + w / 2))

def BUB(txt, x, y, t0, du=None, out=None, cls=""):
    du = du or max(0.4, round(len(txt) * 0.03, 2))
    return dict(k="html", t=t0, s=f'<div class="bub ch {cls}" data-k="w"{_attrs(t0, du, out)} style="left:{x}px;top:{y}px">{txt}</div>',
                ev=("write", t0, du, x + 200, 46))

def FADE(cls, t0, du, style="", out=None, snd=None, x=900):
    return dict(k="html", t=t0, s=f'<div class="{cls}" data-k="f"{_attrs(t0, du, out)} style="{style}"></div>',
                ev=(snd, t0, du, x) if snd else None)

def CELL(x, y, t0, out=None):
    return dict(k="html", t=t0, s=f'<div class="cell ch" data-k="f"{_attrs(t0, 0.15, out)} style="left:{x}px;top:{y}px"></div>', ev=None)

# ─────────── ikony kredą ───────────
def ell(cx, cy, rx, ry):
    return f"M{cx - rx} {cy} a{rx} {ry} 0 1 1 {2 * rx} 0 a{rx} {ry} 0 1 1 {-2 * rx} 0"
def brain(cx, cy):
    return [f"M{cx-70} {cy+10} C{cx-95} {cy-10} {cx-80} {cy-55} {cx-45} {cy-55} C{cx-35} {cy-80} {cx+5} {cy-80} {cx+10} {cy-60} C{cx+35} {cy-80} {cx+80} {cy-60} {cx+70} {cy-25} C{cx+100} {cy-5} {cx+85} {cy+40} {cx+50} {cy+40} C{cx+40} {cy+60} {cx-5} {cy+60} {cx-10} {cy+40} C{cx-40} {cy+60} {cx-85} {cy+45} {cx-70} {cy+10} Z",
            f"M{cx} {cy-62} C{cx-12} {cy-30} {cx+12} {cy} {cx} {cy+42} M{cx-52} {cy-20} C{cx-32} {cy-32} {cx-30} {cy} {cx-14} {cy+6} M{cx+24} {cy-36} C{cx+50} {cy-26} {cx+40} {cy+6} {cx+62} {cy+10}"]
def barchart(cx, cy):
    return [f"M{cx-75} {cy-65} L{cx-75} {cy+50} L{cx+80} {cy+50}",
            f"M{cx-52} {cy+50} L{cx-52} {cy+12} L{cx-26} {cy+12} L{cx-26} {cy+50} M{cx-8} {cy+50} L{cx-8} {cy-18} L{cx+18} {cy-18} L{cx+18} {cy+50} M{cx+36} {cy+50} L{cx+36} {cy-50} L{cx+62} {cy-50} L{cx+62} {cy+50}"]
def steps(cx, cy):
    return [f"M{cx-80} {cy+50} L{cx-80} {cy+18} L{cx-28} {cy+18} L{cx-28} {cy-14} L{cx+24} {cy-14} L{cx+24} {cy-46} L{cx+80} {cy-46} L{cx+80} {cy+50} Z",
            f"M{cx-62} {cy-12} L{cx+8} {cy-72} M{cx-18} {cy-72} L{cx+8} {cy-72} L{cx+6} {cy-46}"]
def magnifier(cx, cy, r=46):
    return [ell(cx, cy, r, r), f"M{cx+r*0.72:.0f} {cy+r*0.72:.0f} L{cx+r*1.7:.0f} {cy+r*1.7:.0f}"]
def calendar(x, y, w, h):
    return [f"M{x} {y} L{x+w} {y} L{x+w} {y+h} L{x} {y+h} Z", f"M{x} {y+h*0.28:.0f} L{x+w} {y+h*0.28:.0f} M{x+w*0.3:.0f} {y-16} L{x+w*0.3:.0f} {y+16} M{x+w*0.7:.0f} {y-16} L{x+w*0.7:.0f} {y+16}"]
def tree(cx, cy):
    return [f"M{cx} {cy-70} L{cx-40} {cy-20} L{cx-20} {cy-20} L{cx-55} {cy+25} L{cx+55} {cy+25} L{cx+20} {cy-20} L{cx+40} {cy-20} Z M{cx-10} {cy+25} L{cx-10} {cy+50} L{cx+10} {cy+50} L{cx+10} {cy+25}"]
def suitcase(cx, cy):
    return [f"M{cx-65} {cy-30} L{cx+65} {cy-30} L{cx+65} {cy+50} L{cx-65} {cy+50} Z M{cx-25} {cy-30} L{cx-25} {cy-55} L{cx+25} {cy-55} L{cx+25} {cy-30} M{cx-65} {cy+5} L{cx+65} {cy+5}"]
def cake(cx, cy):
    return [f"M{cx-60} {cy+50} L{cx-60} {cy} L{cx+60} {cy} L{cx+60} {cy+50} Z M{cx-60} {cy+20} C{cx-30} {cy+35} {cx+30} {cy+5} {cx+60} {cy+20} M{cx} {cy} L{cx} {cy-32}",
            f"M{cx} {cy-38} C{cx-11} {cy-48} {cx-3} {cy-60} {cx} {cy-68} C{cx+4} {cy-58} {cx+11} {cy-48} {cx} {cy-38}"]
def sprout(cx, cy):
    return [f"M{cx} {cy+30} L{cx} {cy-12} M{cx} {cy} C{cx-30} {cy-5} {cx-36} {cy-30} {cx-30} {cy-36} C{cx-10} {cy-36} {cx} {cy-16} {cx} {cy} M{cx} {cy-12} C{cx+26} {cy-16} {cx+36} {cy-42} {cx+30} {cy-46} C{cx+10} {cy-46} {cx} {cy-26} {cx} {cy-12}"]
def plane(cx, cy):
    return [f"M{cx-80} {cy} L{cx+80} {cy-52} L{cx+22} {cy+56} L{cx} {cy+12} Z M{cx} {cy+12} L{cx+80} {cy-52}"]
def check(x, y, s=1.0):
    return f"M{x} {y} L{x+12*s:.0f} {y+14*s:.0f} L{x+36*s:.0f} {y-20*s:.0f}"
def cross(x, y, s=1.0):
    return f"M{x} {y} L{x+30*s:.0f} {y+30*s:.0f} M{x+30*s:.0f} {y} L{x} {y+30*s:.0f}"
def arrow_up(x, y, h):
    return f"M{x} {y} L{x} {y-h} M{x-24} {y-h+28} L{x} {y-h} L{x+24} {y-h+28}"
def arrow_r(x1, y, x2):
    return f"M{x1} {y} L{x2} {y} M{x2-28} {y-20} L{x2} {y} L{x2-28} {y+20}"
def star(cx, cy, r=46, ri=19):
    pts = [f"{cx + (r if i % 2 == 0 else ri) * math.cos(-math.pi / 2 + i * math.pi / 5):.1f} {cy + (r if i % 2 == 0 else ri) * math.sin(-math.pi / 2 + i * math.pi / 5):.1f}" for i in range(10)]
    return "M" + " L".join(pts) + " Z"
def smooth(pts):
    d = f"M{pts[0][0]} {pts[0][1]}"
    for i in range(len(pts) - 1):
        p0 = pts[max(i - 1, 0)]; p1 = pts[i]; p2 = pts[i + 1]; p3 = pts[min(i + 2, len(pts) - 1)]
        d += f" C{p1[0] + (p2[0] - p0[0]) / 6:.1f} {p1[1] + (p2[1] - p0[1]) / 6:.1f} {p2[0] - (p3[0] - p1[0]) / 6:.1f} {p2[1] - (p3[1] - p1[1]) / 6:.1f} {p2[0]} {p2[1]}"
    return d
def arc(cx, cy, r, a1, a2, head=True):
    p = lambda a: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
    x1, y1 = p(a1); x2, y2 = p(a2)
    d = f"M{x1:.1f} {y1:.1f} A{r} {r} 0 0 1 {x2:.1f} {y2:.1f}"
    if head:
        ta = math.radians(a2 + 90)  # kierunek styczny
        for da in (150, -150):
            hx = x2 + 26 * math.cos(ta + math.radians(da)); hy = y2 + 26 * math.sin(ta + math.radians(da))
            d += f" M{x2:.1f} {y2:.1f} L{hx:.1f} {hy:.1f}"
    return d
def icon(paths, t0, du_each=0.45, color=CH, w=8, x=900, gap=0.05, out=None):
    res, t = [], t0
    for p in paths:
        res.append(D(p, t, du_each, color, w, x=x, out=out)); t += du_each + gap
    return res

# ─────────── budowa sceny ───────────
class Board:
    def __init__(self, name, start, end, items, poses=None, moves=None, cam=None, shakes=None, jumps=None, sfx=None,
                 erase=None, fadeIn=0, fadeOut=0, resid_static=True):
        self.name, self.start, self.end = name, start, end
        self.items = [i for i in items if i]
        self.poses = poses or [[start, "hips"]]
        if self.poses[0][0] > start: self.poses.insert(0, [start, "hips"])
        self.moves, self.cam, self.shakes, self.jumps = moves or [], cam or [], shakes or [], jumps or []
        self.sfx, self.erase, self.fadeIn, self.fadeOut, self.resid_static = sfx or [], erase, fadeIn, fadeOut, resid_static
        # pilnuj ciągłości: maskotka wraca na MX w hips, kamera na 1.0 przed ścieraniem
        for m in self.moves: assert m[1] <= end, (name, m)
        if self.moves: assert self.moves[-1][3] == MX, (name, "maskotka nie wraca")
        lim = erase[0] if erase else end
        if self.poses[-1][1] != "hips" and name != "outro": self.poses.append([lim - 0.55, "hips"])
        if self.cam and (self.cam[-1][1] != 1.0) and name != "outro": self.cam.append([lim - 0.7, 1.0, 960, 540, 0.5])

    def html(self):
        off = self.start
        def fix(s):
            import re
            return re.sub(r"__T(-?[\d.]+)__", lambda m: f"{max(0.05, float(m.group(1)) - off):.3f}", s)
        loc = lambda v: round(v - off, 3)
        cfg = dict(T0=round(off, 3), dur=round(self.end - off, 3), erase=[loc(self.erase[0]), loc(self.erase[1])] if self.erase else None,
                   fadeIn=self.fadeIn, fadeOut=self.fadeOut, residStatic=self.resid_static,
                   poses=[[loc(p[0])] + p[1:] for p in sorted(self.poses, key=lambda p: p[0])],
                   moves=[[loc(a), loc(b), x0, x1] for a, b, x0, x1 in self.moves], jumps=[loc(j) for j in self.jumps],
                   shakes=[[loc(a), m] for a, m in self.shakes], cam=[[loc(c[0])] + c[1:] for c in self.cam], mx0=MX, mtop=GROUND - 511)
        hi = fix("".join(i["s"] for i in self.items if i["k"] == "html"))
        si = fix("".join(i["s"] for i in self.items if i["k"] == "svg"))
        body = f"""<div class="b">{DEFS}<div id="cam"><div class="board"></div>
<div class="smudge" style="left:900px;top:80px;width:700px;height:300px"></div><div class="smudge" style="left:100px;top:700px;width:600px;height:260px"></div>
<div id="resid">{RESID}</div><div id="content">{hi}<svg class="lay">{si}</svg></div>{MASCOT}<div id="sponge"></div></div>
<div class="brand">ukryta lekcja</div><div class="dust"></div><div id="fade"></div></div>
<script>window.SCENE={json.dumps(cfg)};{JS}</script>"""
        return page(FONTS, CSS, body, W, H)

    def events(self):
        ev = [i["ev"] for i in self.items if i.get("ev")]
        if self.erase: ev.append(("erase", self.erase[0], self.erase[1] - self.erase[0]))
        for a, b, x0, x1 in self.moves:
            last = 0
            for i in range(1, 401):
                u = i / 400; q = u * u * (3 - 2 * u); d = abs(x1 - x0) * q
                if d // 55 > last:
                    last = d // 55; ev.append(("step", a + (b - a) * u, min(max(x0 + (x1 - x0) * q, 0), 1920)))
        for j in self.jumps: ev += [("whoosh", j - 0.02, 0.3, 1300), ("thud", j + 0.45, 0.55, 1500)]
        for t, m in self.shakes:
            if not any(e[0] == "thud" and abs(e[1] - t) < 0.15 for e in ev): ev.append(("thud", t, min(1.0, m / 8), 960))
        for c in self.cam: ev.append(("whoosh", c[0], c[4] if len(c) > 4 else 0.5, 960))
        return ev + list(self.sfx)

async def open_board(b, board, out_dir):
    pg = await b.new_page(viewport={"width": W, "height": H})
    pg.on("pageerror", lambda e: print("JS ERR", board.name, e, flush=True))
    f = f"{out_dir}/_{board.name}.html"
    open(f, "w", encoding="utf-8").write(board.html())
    await pg.goto(f"file://{f}", wait_until="networkidle")
    await pg.evaluate("document.fonts.ready.then(()=>0)")
    await pg.wait_for_timeout(250)
    await pg.evaluate("init()")
    return pg

async def stills(boards, spec, out_dir):
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        res = []
        for bd in boards:
            if bd.name not in spec: continue
            pg = await open_board(b, bd, out_dir)
            for t in spec[bd.name]:
                await pg.evaluate(f"setT({t - bd.start})")
                p = f"{out_dir}/kadr_{bd.name}_{t:.1f}.jpg"
                await pg.screenshot(path=p, type="jpeg", quality=80); res.append(p)
            await pg.close()
        await b.close()
    return res

async def render_board(board, out_dir):
    from playwright.async_api import async_playwright
    f0, f1 = int(round(board.start * FPS)), int(round(board.end * FPS))
    tmp, dst = f"{out_dir}/scena_{board.name}.tmp.mp4", f"{out_dir}/scena_{board.name}.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg",
                           "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                           "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await open_board(b, board, out_dir)
        for i in range(f0, f1):
            await pg.evaluate(f"setT({i / FPS - board.start:.5f})")
            ff.stdin.write(await pg.screenshot(type="jpeg", quality=92))
        await b.close()
    ff.stdin.close()
    if ff.wait() == 0:
        os.replace(tmp, dst); print("ok", board.name, f1 - f0, flush=True)
    else:
        print("FAIL", board.name, flush=True)
