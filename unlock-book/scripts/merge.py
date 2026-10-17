"""Merge the original Units 1-3 PDFs with the built Units 4-10 (+ answer key) into one book.

Usage: python3 scripts/merge.py
Needs the original PDFs in originals/ (see README) and dist/Unlock5_Units_4-10.pdf
(rendered with START_PAGE set so its page numbers continue after Unit 3).
"""
from pathlib import Path
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parent.parent
ORIG = ROOT / "originals"
# (file, first page, last page) — 1-based, inclusive
PARTS = [
    (ORIG / "Book_Units_1-3.pdf", 1, 13),     # Unit 1 Conservation
    (ORIG / "Unit_2.pdf", 1, 15),             # Unit 2 Design (complete, with writing + speaking)
    (ORIG / "Book_Units_1-3.pdf", 26, 26),    # Unit 3 cover: Technology & Digital Life
    (ORIG / "Unit_3.pdf", 2, 11),             # Unit 3 pages
    (ROOT / "dist" / "Unlock5_Units_4-10.pdf", 1, None),   # Units 4-10 + answer key for Units 1-10
]


def main():
    out = PdfWriter()
    for f, a, b in PARTS:
        r = PdfReader(f)
        for i in range(a - 1, b or len(r.pages)):
            out.add_page(r.pages[i])
    out.compress_identical_objects()
    dest = ROOT / "dist" / "Unlock5_Units_1-10.pdf"
    with open(dest, "wb") as fh:
        out.write(fh)
    print(f"{len(out.pages)} pages -> {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
