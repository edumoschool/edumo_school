"""Merge the original Units 1-3 PDFs with the built Units 4-10 (+ answer key) into one book.

Usage: python3 scripts/merge.py
Needs the original PDFs in originals/ (see README) and dist/Unlock5_Units_4-10.pdf
(rendered with START_PAGE set so its page numbers continue after Unit 3).
The original pages get page numbers stamped in the same place and style as the built pages:
on the side with the blue strip, 20 mm in and 8 mm up; covers stay unnumbered.
"""
import io
import subprocess
import tempfile
from pathlib import Path

from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent.parent
ORIG = ROOT / "originals"
# (file, first page, last page, stamp numbers?) — 1-based, inclusive
PARTS = [
    (ORIG / "Book_Units_1-3.pdf", 1, 13, True),     # Unit 1 Conservation
    (ORIG / "Unit_2.pdf", 1, 15, True),             # Unit 2 Design (complete, with writing + speaking)
    (ORIG / "Book_Units_1-3.pdf", 26, 26, True),    # Unit 3 cover: Technology & Digital Life
    (ORIG / "Unit_3.pdf", 2, 11, True),             # Unit 3 pages
    (ROOT / "dist" / "Unit3_extra.pdf", 1, None, False),         # Unit 3 writing + speaking (built, numbered)
    (ROOT / "dist" / "Unlock5_Units_4-10.pdf", 1, None, False),  # Units 4-10 + answer key (built, numbered)
]
COVERS = {("Book_Units_1-3.pdf", 1), ("Unit_2.pdf", 1), ("Book_Units_1-3.pdf", 26)}
STRIP = (191, 217, 252)          # light-blue side strip


def strip_side(pdf, page_no):
    """'left' or 'right': which bottom corner carries the blue strip (left if neither)."""
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["pdftoppm", "-r", "12", "-png", "-f", str(page_no), "-l", str(page_no), str(pdf), f"{d}/p"],
                       check=True)
        im = Image.open(next(Path(d).glob("p*.png"))).convert("RGB")
    w, h = im.size

    def blue(x):
        r, g, b = im.getpixel((x, h - 3))
        return abs(r - STRIP[0]) + abs(g - STRIP[1]) + abs(b - STRIP[2]) < 60

    def plain(x):                # blue strip or white paper, not a photo
        return blue(x) or min(im.getpixel((x, h - 3))) > 235
    side = "right" if blue(w - 3) and not blue(2) else "left"
    x = round((20 if side == "left" else 277) * w / 297)
    return side, not plain(x)


def stamp(page, number, side, chip=False):
    w, h = float(page.mediabox.width), float(page.mediabox.height)
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(w, h))
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(HexColor("#6B7A99"))
    y = 8 * mm + 1
    if chip:                     # white tab so the number stays readable on top of a photo
        x0 = 20 * mm - 2 * mm if side == "left" else w - 20 * mm - 9 * mm
        c.setFillColor(HexColor("#FFFFFF"))
        c.roundRect(x0, y - 2 * mm, 11 * mm, 6.5 * mm, 1.5 * mm, stroke=0, fill=1)
        c.setFillColor(HexColor("#6B7A99"))
    if side == "left":
        c.drawString(20 * mm, y, str(number))
    else:
        c.drawRightString(w - 20 * mm, y, str(number))
    c.save()
    page.merge_page(PdfReader(buf).pages[0])


def main():
    out = PdfWriter()
    for f, a, b, number in PARTS:
        r = PdfReader(f)
        for i in range(a - 1, b or len(r.pages)):
            page = out.add_page(r.pages[i])
            if number and (f.name, i + 1) not in COVERS:
                stamp(page, len(out.pages), *strip_side(f, i + 1))
    out.compress_identical_objects()
    dest = ROOT / "dist" / "Unlock5_Units_1-10.pdf"
    with open(dest, "wb") as fh:
        out.write(fh)
    print(f"{len(out.pages)} pages -> {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
