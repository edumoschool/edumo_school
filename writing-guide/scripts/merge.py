"""Front cover + interior + back cover -> dist/Write_it_Right_Multilevel_Writing.pdf"""
from pathlib import Path
from pypdf import PdfReader, PdfWriter

DIST = Path(__file__).resolve().parent.parent / "dist"
cover, inner = PdfReader(DIST / "cover.pdf"), PdfReader(DIST / "interior.pdf")
w = PdfWriter()
w.add_page(cover.pages[0])
for p in inner.pages:
    w.add_page(p)
w.add_page(cover.pages[1])
out = DIST / "Write_it_Right_Multilevel_Writing.pdf"
with open(out, "wb") as f:
    w.write(f)
print(len(w.pages), "pages ->", out.name)
