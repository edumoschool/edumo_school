"""Book cover in the Impulse mockup style (white + blue band, 3D hero, Uzbek girih ornaments).

Usage: python3 scripts/cover.py      -> dist/cover_pages.html (front + back, A3) and dist/cover_spread.html
Then:  node scripts/cover_render.js  -> dist/Cover_front_back.pdf and dist/Cover_spread.pdf
"""
import base64
from pathlib import Path

import qrcode
import qrcode.image.svg

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / "assets" / "brand"
DIST = ROOT / "dist"
CHANNEL = "https://t.me/multilevel_express"
SPINE_MM = 10          # ~155 pages on 80 g/m² paper; adjust to the printer's spine width


def uri(p, mime="image/png"):
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def qr():
    img = qrcode.make(CHANNEL, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=1)
    return img.to_string(encoding="unicode")


# Uzbek girih ornament: 8-point stars (two squares) linked by a lattice, tiled as an SVG pattern.
GIRIH = """<svg class="pat" xmlns="http://www.w3.org/2000/svg"><defs>
<pattern id="g{id}" width="64" height="64" patternUnits="userSpaceOnUse" patternTransform="scale({scale})">
 <g fill="none" stroke="{col}" stroke-width="1.6" stroke-linejoin="round">
  <rect x="20" y="20" width="24" height="24"/><rect x="20" y="20" width="24" height="24" transform="rotate(45 32 32)"/>
  <circle cx="32" cy="32" r="6"/>
  <path d="M32 15 L32 0 M32 49 L32 64 M15 32 L0 32 M49 32 L64 32"/>
  <path d="M0 0 L8 8 M64 0 L56 8 M0 64 L8 56 M64 64 L56 56"/>
  <path d="M8 8 L14 0 M8 8 L0 14 M56 8 L50 0 M56 8 L64 14 M8 56 L0 50 M8 56 L14 64 M56 56 L64 50 M56 56 L50 64"/>
 </g></pattern></defs><rect width="100%" height="100%" fill="url(#g{id})"/></svg>"""


def girih(i, col="rgba(255,255,255,.13)", scale=1.0):
    return GIRIH.format(id=i, col=col, scale=scale)


# a single large ornamental rosette (islimi-style 8/16-point star) for accents
ROSETTE = """<svg class="{cls}" viewBox="-100 -100 200 200" xmlns="http://www.w3.org/2000/svg">
 <g fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round">
  <rect x="-62" y="-62" width="124" height="124"/><rect x="-62" y="-62" width="124" height="124" transform="rotate(45)"/>
  <rect x="-44" y="-44" width="88" height="88" transform="rotate(22.5)"/><rect x="-44" y="-44" width="88" height="88" transform="rotate(67.5)"/>
  <circle r="30"/><circle r="94"/>
  <path d="M0 -30 C14 -14 14 14 0 30 C-14 14 -14 -14 0 -30Z"/>
  <path d="M-30 0 C-14 -14 14 -14 30 0 C14 14 -14 14 -30 0Z"/>
 </g></svg>"""


def rosette(cls, col, sw=2.2):
    return ROSETTE.format(cls=cls, col=col, sw=sw)


def border_band(i):
    """A thin ornamental border row (repeating stars) like a suzani/girih frieze."""
    return f"""<svg class="frieze" xmlns="http://www.w3.org/2000/svg"><defs>
<pattern id="f{i}" width="40" height="40" patternUnits="userSpaceOnUse">
 <g fill="none" stroke="#fff" stroke-width="1.6" opacity=".55">
  <rect x="12" y="12" width="16" height="16"/><rect x="12" y="12" width="16" height="16" transform="rotate(45 20 20)"/>
  <path d="M0 20 L6 20 M34 20 L40 20"/><circle cx="20" cy="20" r="3" fill="#fff" stroke="none"/></g></pattern></defs>
<rect width="100%" height="100%" fill="url(#f{i})"/></svg>"""


def front():
    return f"""<div class="front">
 <img class="logo" src="{uri(BRAND / 'logo_blue.png')}" alt="Impulse Learning Center">
 <div class="badge">C1 · Advanced</div>
 <div class="band">{girih(1)}<img class="hero" src="{uri(BRAND / 'hero.png')}" alt="">
  {rosette('ros r1', 'rgba(255,255,255,.22)')}{rosette('ros r2', 'rgba(255,255,255,.16)')}
  <div class="frieze-wrap">{border_band(1)}</div></div>
 <div class="ttl">
  <p class="pre">Milliy sertifikat · CEFR</p>
  <h1>Multilevel</h1>
  <p class="sub">B2 darajadan <b>C1 darajaga qadar</b></p>
  <p class="skills">Reading · Listening · Writing · Speaking</p>
  </div>
 {rosette('ros r3', 'rgba(47,91,234,.10)', 1.6)}
</div>"""


def back():
    return f"""<div class="back">
 <p class="bpre">Multilevel · C1 Advanced</p>
 <img class="bicon" src="{uri(BRAND / 'icon_blue.png')}" alt="">
 <p class="bdesc">10 units of academic reading and writing — articles, vocabulary, grammar for writing and academic
 skills — with real <b>Multilevel (CEFR)</b> exam practice in reading, listening, writing and speaking, plus a full answer key.</p>
 <div class="bband">{girih(2)}<div class="frieze-wrap top">{border_band(2)}</div>
  <p class="btag">B2 darajadan <b>C1 darajaga qadar</b></p>
  <div class="bqr"><div class="q">{qr()}</div><div><b>Audio</b><span>t.me/multilevel_express</span></div></div>
  <p class="social"><svg viewBox="0 0 24 24"><path fill="#fff" d="M21.5 3.6 2.9 10.8c-1.3.5-1.3 1.2-.2 1.6l4.8 1.5 1.8 5.6c.2.6.4.8.8.8.4 0 .6-.2.9-.5l2.3-2.2 4.8 3.5c.9.5 1.5.2 1.7-.8l3.2-15c.3-1.3-.5-1.9-1.5-1.5zM9 13.6l9.2-5.8c.5-.3.8-.1.4.2l-7.6 6.9-.3 3.3L9 13.6z"/></svg>
   <svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="#fff" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="none" stroke="#fff" stroke-width="2"/><circle cx="17.3" cy="6.7" r="1.2" fill="#fff"/></svg>
   impulse_learning_center</p></div>
</div>"""


def spine():
    return f"""<div class="spine">{girih(3, 'rgba(255,255,255,.10)', .5)}
 <span class="sp1">Multilevel</span><span class="sp2">C1 · Advanced</span>
 <img class="spicon" src="{uri(BRAND / 'icon_white.png')}" alt=""></div>"""


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--blue:#2F5BEA;--blue2:#1A3FC4;--navy:#0D2A8A;--ink:#0B1A4A}
body{font-family:"Manrope",sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact;background:#fff}
.sheet{position:relative;overflow:hidden;page-break-after:always;background:#F3F5F9}
.pat{position:absolute;inset:0;width:100%;height:100%}
.front,.back{position:absolute;top:0;width:297mm;height:420mm;overflow:hidden;background:linear-gradient(180deg,#F7F8FB,#ECEFF5)}
/* ----- front ----- */
.logo{position:absolute;left:24mm;top:24mm;width:78mm}
.badge{position:absolute;right:24mm;top:24mm;background:linear-gradient(120deg,#3A6BF2,#1F48D6);color:#fff;font:700 15pt "Unbounded";padding:3.2mm 7mm;
  border-radius:3mm}
.band{position:absolute;left:0;right:0;top:66mm;height:190mm;overflow:hidden;
  background:linear-gradient(120deg,#3A6BF2 0%,#1F48D6 45%,#0F2C9C 100%);
  clip-path:path('M 0 70 C 260 -40, 600 40, 1123 0 L 1123 718 L 0 718 Z')}
.hero{position:absolute;right:2mm;top:12mm;width:215mm;filter:drop-shadow(0 4mm 6mm rgba(5,20,90,.35))}
.ros{position:absolute}
.r1{width:92mm;left:-26mm;top:58mm}
.r2{width:46mm;left:62mm;top:20mm}
.r3{width:150mm;right:-55mm;bottom:-55mm}
.frieze-wrap{position:absolute;left:0;right:0;bottom:6mm;height:10mm}
.frieze-wrap.top{top:5mm;bottom:auto;transform:none}
.frieze{width:100%;height:100%}
.ttl{position:absolute;left:24mm;right:24mm;top:268mm}
.pre{font:300 24pt "Unbounded";color:#7EA0F5;letter-spacing:.01em}
.ttl h1{font:800 74pt/1 "Unbounded";color:var(--blue2);letter-spacing:-.01em;margin:2mm 0 6mm}
.sub{font:300 17pt "Unbounded";color:#5C6A8E}
.sub b{font-weight:500;color:var(--ink)}
.skills{font:600 13pt "Manrope";color:var(--blue2);margin-top:7mm;letter-spacing:.04em}
.units{font:400 11pt "JetBrains Mono",monospace;color:#8A94AE;letter-spacing:.32em;margin-top:9mm}
/* ----- back ----- */
.bpre{position:absolute;left:0;right:0;top:46mm;text-align:center;font:300 20pt "Unbounded";color:var(--blue)}
.bicon{position:absolute;left:50%;top:76mm;width:100mm;transform:translateX(-50%)}
.bdesc{position:absolute;left:44mm;right:44mm;top:232mm;text-align:center;font:500 12.5pt/1.6 "Manrope";color:#4A5675}
.bdesc b{color:var(--blue2)}
.bband{position:absolute;left:0;right:0;bottom:0;height:120mm;overflow:hidden;
  background:linear-gradient(120deg,#3A6BF2,#0F2C9C);clip-path:polygon(0 18%,100% 0,100% 100%,0 100%)}
.btag{position:absolute;left:24mm;top:44mm;font:300 18pt "Unbounded";color:#CFDBFF}
.btag b{font-weight:600;color:#fff}
.bqr{position:absolute;right:24mm;top:36mm;display:flex;gap:4mm;align-items:center;color:#fff}
.bqr .q{width:34mm;height:34mm;background:#fff;border-radius:2.5mm;padding:2mm}
.bqr .q svg{width:100%;height:100%;display:block}
.bqr b{display:block;font:700 13pt "Unbounded"}
.bqr span{font:500 9.5pt "Manrope";opacity:.85}
.social{position:absolute;left:0;right:0;bottom:16mm;text-align:center;color:#fff;font:600 12pt "Manrope";
  display:flex;align-items:center;justify-content:center;gap:2.5mm}
.social svg{width:6mm;height:6mm}
/* ----- spine ----- */
.spine{position:absolute;top:0;height:420mm;background:linear-gradient(180deg,#2F5BEA,#0F2C9C);overflow:hidden}
.spine span{position:absolute;left:50%;transform:translateX(-50%) rotate(90deg);transform-origin:center;white-space:nowrap;color:#fff}
.sp1{top:120mm;font:800 15pt "Unbounded"}
.sp2{top:300mm;font:400 10pt "Manrope";opacity:.85}
.spicon{position:absolute;left:50%;bottom:16mm;width:6.5mm;transform:translateX(-50%)}
"""

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@300;400;500;600;700;800'
         '&family=Manrope:wght@400;500;600;700&family=JetBrains+Mono:wght@400&display=block" rel="stylesheet">')


def doc(body, page_w):
    return (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>@page{{size:{page_w}mm 420mm;margin:0}}'
            f'{CSS}</style></head><body>{body}</body></html>')


def main():
    DIST.mkdir(exist_ok=True)
    pages = (f'<section class="sheet" style="width:297mm;height:420mm">{front()}</section>'
             f'<section class="sheet" style="width:297mm;height:420mm">{back().replace("class=\"back\"", "class=\"back\" style=\"left:0\"")}</section>')
    (DIST / "cover_pages.html").write_text(doc(pages, 297), encoding="utf-8")
    w = 297 * 2 + SPINE_MM
    spread = (f'<section class="sheet" style="width:{w}mm;height:420mm">'
              f'{back().replace("class=\"back\"", "class=\"back\" style=\"left:0\"")}'
              f'{spine().replace("class=\"spine\"", f"class=\"spine\" style=\"left:297mm;width:{SPINE_MM}mm\"")}'
              f'{front().replace("class=\"front\"", f"class=\"front\" style=\"left:{297 + SPINE_MM}mm\"")}</section>')
    (DIST / "cover_spread.html").write_text(doc(spread, w), encoding="utf-8")
    print("dist/cover_pages.html, dist/cover_spread.html")


if __name__ == "__main__":
    main()
