"""Assemble the mock book: front cover (A3 design scaled to A4) + interior + back cover; also an A4 print spread.

Usage: python3 scripts/merge.py
"""
from pathlib import Path
from pypdf import PdfReader, PdfWriter, Transformation

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
A4 = (595.28, 841.89)


def scaled(page, factor):
    page.add_transformation(Transformation().scale(factor, factor))
    w, h = float(page.mediabox.width) * factor, float(page.mediabox.height) * factor
    page.mediabox.lower_left = (0, 0)
    page.mediabox.upper_right = (w, h)
    page.cropbox = page.mediabox
    return page


def main():
    cover = PdfReader(DIST / "Cover_front_back.pdf")
    f = A4[0] / float(cover.pages[0].mediabox.width)
    out = PdfWriter()
    out.add_page(scaled(cover.pages[0], f))
    for p in PdfReader(DIST / "mock_interior.pdf").pages:
        out.add_page(p)
    out.add_page(scaled(cover.pages[1], f))
    out.compress_identical_objects()
    with open(DIST / "Multilevel_Mock_Tests.pdf", "wb") as fh:
        out.write(fh)
    sp = PdfWriter()
    sp.add_page(scaled(PdfReader(DIST / "Cover_spread.pdf").pages[0], f))
    with open(DIST / "Mock_Cover_spread_A4.pdf", "wb") as fh:
        sp.write(fh)
    print(f"{len(out.pages)} pages -> dist/Multilevel_Mock_Tests.pdf; cover spread -> dist/Mock_Cover_spread_A4.pdf")


if __name__ == "__main__":
    main()
