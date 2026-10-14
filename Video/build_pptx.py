"""Builds Strassen.pptx from the downloaded Wikimedia images. Run: python build_pptx.py"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from PIL import Image
import os

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = lambda n: os.path.join(HERE, "images", n)

NAVY = RGBColor(0x1B, 0x2A, 0x49)
ACCENT = RGBColor(0xE0, 0x5A, 0x2B)
GREEN = RGBColor(0x2E, 0x8B, 0x57)
GREY = RGBColor(0x55, 0x55, 0x55)
LIGHT = RGBColor(0xF2, 0xF4, 0xF8)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]


def add_text(slide, text, x, y, w, h, size=20, bold=False, color=NAVY,
             align=PP_ALIGN.LEFT, font="Calibri"):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    lines = text if isinstance(text, list) else [text]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = line
        r.font.size, r.font.bold, r.font.name = Pt(size), bold, font
        r.font.color.rgb = color
        p.space_after = Pt(8)
    return tb


def new_slide(title, notes="", segment=""):
    s = prs.slides.add_slide(BLANK)
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(1.1))
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()
    add_text(s, title, 0.5, 0.18, 12.3, 0.8, size=32, bold=True, color=RGBColor(255, 255, 255))
    if segment:
        add_text(s, segment, 10.3, 7.05, 3, 0.35, size=11, color=GREY, align=PP_ALIGN.RIGHT)
    s.notes_slide.notes_text_frame.text = notes
    return s


def add_image(slide, name, x, y, max_w, max_h, caption=None):
    w, h = Image.open(IMG(name)).size
    scale = min(max_w / w, max_h / h)
    iw, ih = w * scale, h * scale
    ox, oy = x + (max_w - iw) / 2, y + (max_h - ih) / 2
    slide.shapes.add_picture(IMG(name), Inches(ox), Inches(oy), Inches(iw), Inches(ih))
    if caption:
        add_text(slide, caption, x, oy + ih + 0.05, max_w, 0.5, size=11, color=GREY,
                 align=PP_ALIGN.CENTER)


def add_table(slide, rows, x, y, w, col_w, row_h=0.45, size=16):
    t = slide.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y),
                               Inches(w), Inches(row_h * len(rows))).table
    for c, cw in enumerate(col_w):
        t.columns[c].width = Inches(cw)
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = t.cell(r, c)
            cell.text = str(val)
            para = cell.text_frame.paragraphs[0]
            para.font.size = Pt(size)
            para.font.bold = r == 0
            para.font.name = "Calibri"
            para.font.color.rgb = RGBColor(255, 255, 255) if r == 0 else NAVY
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY if r == 0 else (LIGHT if r % 2 else RGBColor(255, 255, 255))
    return t


# ---------------------------------------------------------------- Segment 1
s = new_slide("Strassen's Algorithm: beating n³", segment="Segment 1 - Problem",
              notes="IMAGE: Photo of Volker Strassen at his Knuth Prize lecture (David Eppstein, "
                    "CC BY-SA 3.0, Wikimedia Commons: File:Strassen_Knuth_Prize_lecture.jpg).\n"
                    "Open with the hook: everyone assumed you needed n³ multiplications until 1969.")
add_text(s, ["Fast matrix multiplication", "Volker Strassen, 1969",
             "“Gaussian elimination is not optimal”", "Numerische Mathematik 13, 354-356"],
         0.6, 1.8, 6.5, 3.5, size=26)
add_image(s, "strassen_portrait.jpg", 7.3, 1.5, 5.5, 5.2,
          "Volker Strassen, Knuth Prize lecture. Photo: David Eppstein, CC BY-SA 3.0")

s = new_slide("The problem: multiplying two n × n matrices", segment="Segment 1 - Problem",
              notes="IMAGE: left, native table showing the n³ triple-loop count; right, text on where "
                    "matrix multiplication is used (graphics, ML, solving linear systems, graph algorithms).\n"
                    "Say: C[i,j] = sum over k of A[i,k]*B[k,j]. n² outputs, each is n multiplies -> n³.")
add_text(s, ["C[i][j] = Σₖ A[i][k] · B[k][j]",
             "n² entries in C, each needs n multiplications  →  n³ multiplications",
             "Used everywhere: neural networks, graphics, solving linear systems, graph algorithms",
             "For 60 years nobody thought you could do better."],
         0.6, 1.5, 6.2, 5, size=24)
add_table(s, [["n", "Classical n³ multiplications"],
              ["2", "8"], ["10", "1,000"], ["100", "1,000,000"],
              ["1,024", "1,073,741,824"]], 7.2, 2.0, 5.6, [1.4, 4.2], size=20)

# ---------------------------------------------------------------- Segment 2
s = new_slide("Idea 1: divide and conquer on blocks", segment="Segment 2 - How it works",
              notes="IMAGE: native shapes - three 2x2 block grids (A, B, C) drawn in PowerPoint with the "
                    "blocks colour-coded: A11 blue, A12 orange, A21 green, A22 purple (same for B and C).\n"
                    "Split each matrix into four n/2 x n/2 blocks. The obvious recursion needs 8 block "
                    "multiplications -> T(n)=8T(n/2)+O(n^2) = O(n^3). No gain.")
COLS = [RGBColor(0x4A, 0x90, 0xD9), RGBColor(0xE0, 0x9A, 0x2B), RGBColor(0x3C, 0xA8, 0x6B), RGBColor(0x8E, 0x5B, 0xC4)]


def grid(slide, letter, x, y, cell=0.9):
    for i in range(4):
        r, c = divmod(i, 2)
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x + c * cell), Inches(y + r * cell),
                                     Inches(cell), Inches(cell))
        box.fill.solid()
        box.fill.fore_color.rgb = COLS[i]
        box.line.color.rgb = RGBColor(255, 255, 255)
        tf = box.text_frame
        tf.text = f"{letter}{r + 1}{c + 1}"
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        tf.paragraphs[0].font.size = Pt(22)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)


grid(s, "A", 0.6, 1.8)
add_text(s, "×", 2.55, 2.2, 0.6, 0.8, size=40, bold=True, color=GREY, align=PP_ALIGN.CENTER)
grid(s, "B", 3.1, 1.8)
add_text(s, "=", 5.05, 2.2, 0.6, 0.8, size=40, bold=True, color=GREY, align=PP_ALIGN.CENTER)
grid(s, "C", 5.6, 1.8)
add_text(s, "Each block is (n/2 × n/2)", 0.6, 3.8, 6.5, 0.5, size=18, color=GREY)
add_text(s, ["Naive recursion: 8 block products", "T(n) = 8T(n/2) + Θ(n²) = Θ(n³)"],
         0.6, 4.6, 6.5, 1.6, size=24, bold=True, color=ACCENT)
add_text(s, ["C₁₁ = A₁₁B₁₁ + A₁₂B₂₁",
             "C₁₂ = A₁₁B₁₂ + A₁₂B₂₂",
             "C₂₁ = A₂₁B₁₁ + A₂₂B₂₁",
             "C₂₂ = A₂₁B₁₂ + A₂₂B₂₂",
             "8 half-size multiplications  →  still n³",
             "Additions are cheap (n² work). Multiplications are what recurse."],
         7.6, 1.5, 5.4, 5.2, size=24)

s = new_slide("Idea 2: seven products instead of eight", segment="Segment 2 - How it works",
              notes="IMAGE: Strassen_algorithm.svg (Cyp, CC BY-SA 3.0, Wikimedia Commons). Left column = "
                    "the 8 products of the naive method, columns M1..M7 = Strassen's seven; summing the "
                    "coloured columns reproduces the left column.\n"
                    "Read the seven products, then the four recombinations. Cue the manim animation to "
                    "show WHY the combos cancel.")
add_image(s, "strassen_diagram.png", 0.4, 1.2, 12.5, 2.7,
          "Each column M₁…M₇ is one product. Cyp, CC BY-SA 3.0")
add_text(s, ["M₁ = (A₁₁ + A₂₂)(B₁₁ + B₂₂)", "M₂ = (A₂₁ + A₂₂) B₁₁", "M₃ = A₁₁ (B₁₂ − B₂₂)",
             "M₄ = A₂₂ (B₂₁ − B₁₁)"], 0.6, 3.95, 6.2, 1.8, size=19)
add_text(s, ["M₅ = (A₁₁ + A₁₂) B₂₂", "M₆ = (A₂₁ − A₁₁)(B₁₁ + B₁₂)", "M₇ = (A₁₂ − A₂₂)(B₂₁ + B₂₂)"],
         6.9, 3.95, 6.2, 1.8, size=19)
add_text(s, ["C₁₁ = M₁ + M₄ − M₅ + M₇     C₁₂ = M₃ + M₅     C₂₁ = M₂ + M₄     "
             "C₂₂ = M₁ − M₂ + M₃ + M₆"],
         0.5, 5.85, 12.4, 0.6, size=22, bold=True, color=ACCENT)
add_text(s, "7 multiplications, 18 additions/subtractions of half-size blocks. Trade one expensive "
            "multiply for a handful of cheap adds.", 0.5, 6.4, 12.3, 0.6, size=18, color=GREY)
# ---------------------------------------------------------------- Segment 5
s = new_slide("Why the complexity is n^log₂7", segment="Segment 5 - Complexity",
              notes="IMAGE: native table of the recursion tree level by level (no external image).\n"
                    "Level k has 7^k subproblems each of size n/2^k. Multiplication work only appears at "
                    "the leaves: 7^(log2 n) = n^(log2 7). Addition work per level is 7^k (n/2^k)² = "
                    "n² (7/4)^k, a growing geometric series dominated by the last level, so additions "
                    "never change the exponent.")
add_text(s, ["T(n) = 7 · T(n/2) + Θ(n²)", "Master theorem: a = 7, b = 2, n^log₂7 ≈ n^2.807 > n²",
             "→ the leaves dominate:  T(n) = Θ(n^log₂7) ≈ Θ(n^2.807)"],
         0.5, 1.3, 12.3, 1.8, size=26, bold=True, color=ACCENT)
add_table(s, [["Level k", "Subproblems 7ᵏ", "Block size n/2ᵏ", "Add. work per level"],
              ["0", "1", "n", "n²"],
              ["1", "7", "n/2", "7/4 · n²"],
              ["2", "49", "n/4", "(7/4)² · n²"],
              ["…", "…", "…", "…"],
              ["log₂ n", "7^log₂n = n^log₂7", "1", "(7/4)^log₂n · n² = n^log₂7"]],
          0.5, 3.2, 12.3, [1.7, 3.5, 3.0, 4.1], row_h=0.5, size=18)
add_text(s, "Each level saves 1/8 of the multiplications; across log₂n levels that compounds: "
            "(7/8)^log₂n = n^(−0.193). For n = 1024: 7¹⁰ ≈ 2.8 × 10⁸ vs 1024³ ≈ 1.07 × 10⁹.",
         0.5, 6.3, 12.3, 0.9, size=20, color=GREY)

s = new_slide("Classical vs Strassen: multiplications at the leaves",
              segment="Segment 5 - Complexity",
              notes="IMAGE: native comparison table. Computed values: n³ vs 7^log2(n) for n powers of two. "
                    "Emphasise the gap grows without bound but only pays off once n is large enough to "
                    "amortise the extra additions.")
add_table(s, [["n", "Classical n³", "Strassen 7^log₂n", "Ratio"],
              ["16", "4,096", "2,401", "1.7×"],
              ["256", "16,777,216", "5,764,801", "2.9×"],
              ["1,024", "1,073,741,824", "282,475,249", "3.8×"],
              ["8,192", "5.5 × 10¹¹", "9.7 × 10¹⁰", "5.7×"]],
          0.8, 1.7, 11.7, [2.0, 3.5, 3.7, 2.5], row_h=0.7, size=24)
add_text(s, ["Recurrence only counts multiplications at full depth. Real implementations stop early "
             "(see the code) and switch to classical multiplication below a threshold."],
         0.8, 5.5, 11.7, 1.2, size=22, color=GREY)

# ---------------------------------------------------------------- Segment 6
s = new_slide("Constraints and practical limits", segment="Segment 6 - Constraints",
              notes="IMAGE: two-column text slide (valid vs limits); no external image.\n"
                    "Validity: needs a ring (subtraction). Fails for Boolean and min-plus semirings. "
                    "Square power-of-two by padding. Exact for integers; floats lose some stability.")
add_text(s, ["WHEN IT APPLIES", "• Needs subtraction: any ring (ints, reals, mod p)",
             "• NOT for boolean or min-plus semirings (no subtraction)",
             "• Squares of size 2ᵏ; otherwise pad with zeros",
             "• Exact over integers; rounding error only matters with floats"],
         0.5, 1.5, 6.1, 5, size=22)
add_text(s, ["PRACTICAL LIMITS", "• 18 extra block additions per level: slower for small n",
             "• Extra memory: temporaries, padding up to 4× elements",
             "• Cache and vectorised BLAS favour classical code",
             "• Break-even: roughly n ≈ 500-1000+ (Huang et al. 2016 saw ~20% gains at n=512)"],
         6.9, 1.5, 6.0, 5, size=22)

# ---------------------------------------------------------------- Segment 7
s = new_slide("Extra research 1: numerical stability", segment="Segment 7 - Extras",
              notes="IMAGE: native table of error-bound comparison.\n"
                    "Classical multiplication has a componentwise error bound; Strassen's is only "
                    "normwise (Higham; Webb Miller 1975). Demmel, Dumitriu, Holtz and Kleinberg proved "
                    "that fast matrix multiplication algorithms are 'stable' in a normwise sense, so the "
                    "loss is a worse constant, not a catastrophe.")
add_table(s, [["", "Classical", "Strassen"],
              ["Error bound", "Componentwise", "Normwise only"],
              ["Badly scaled rows/cols", "Handled well", "Can lose accuracy"],
              ["Growth with depth", "None", "Constant grows with recursion levels"],
              ["Theory (Demmel et al. 2007)", "Stable", "Stable in the normwise sense"]],
          0.6, 1.6, 12.1, [3.8, 3.8, 4.5], row_h=0.7, size=22)
add_text(s, "Mitigations: stop recursing early (the threshold), and scale rows/columns "
            "before multiplying.", 0.6, 5.6, 12.1, 1, size=22, color=GREY)

s = new_slide("Extra research 2: is 7 optimal? What came next", segment="Segment 7 - Extras",
              notes="IMAGE: MatrixMultComplexity_svg.svg (Jochen Burghardt, CC BY-SA 4.0, Wikimedia "
                    "Commons) - the improvement of the exponent omega over time from 3 down to ~2.37.\n"
                    "Hopcroft & Kerr 1971 and Winograd 1971: 7 multiplications is optimal for 2x2. "
                    "AlphaTensor (Fawzi et al., Nature 2022) found 47 multiplications for 4x4 over GF(2), "
                    "beating 49 = 7x7 from Strassen applied twice. Alman et al. 2024: omega < 2.371339.")
add_image(s, "omega_timeline.png", 0.3, 1.3, 6.4, 5.5,
          "Exponent ω over time. J. Burghardt, CC BY-SA 4.0")
add_text(s, ["• Hopcroft & Kerr (1971), Winograd (1971): 7 is optimal for 2×2",
             "• Winograd's variant: 15 additions instead of 18",
             "• AlphaTensor (DeepMind, 2022): 47 multiplications for 4×4 over GF(2) vs 49",
             "• Best known exponent today: ω < 2.371339 (Alman et al., 2024)",
             "• Those record algorithms are galactic - never used in practice"],
         6.9, 1.5, 6.1, 5.3, size=21)

s = new_slide("References", segment="Segment 7 - Outro",
              notes="IMAGE: none, text only. Keep on screen for the final seconds.")
add_text(s, [
    "VIDEOS",
    "• ByteQuest, 'Strassen Algorithm Visually Explained' - youtube.com/watch?v=2IgZuVGwEb0",
    "• Sagar Choudhary, 'Strassen's Matrix Multiplication | Faster Matrix Multiplication Explained "
    "with Example' - youtube.com/watch?v=cGmfchtOJi4",
    "ARTICLES",
    "• Wikipedia, 'Strassen algorithm' - en.wikipedia.org/wiki/Strassen_algorithm",
    "• Wikipedia, 'Computational complexity of matrix multiplication' - en.wikipedia.org/wiki/"
    "Computational_complexity_of_matrix_multiplication",
    "• GeeksforGeeks, 'Matrix Multiplication / Strassen's' - geeksforgeeks.org/strassens-matrix-multiplication/",
    "RESEARCH",
    "• Strassen (1969), Numerische Mathematik 13:354-356",
    "• Demmel, Dumitriu, Holtz, Kleinberg, 'Fast matrix multiplication is stable' - arxiv.org/abs/math/0603207",
    "• Fawzi et al., AlphaTensor, Nature 610 (2022) - nature.com/articles/s41586-022-05172-4",
    "• Alman et al., 'More Asymmetry Yields Faster Matrix Multiplication' - arxiv.org/abs/2404.16349",
    "IMAGES: Wikimedia Commons (CC BY-SA 3.0/4.0, CC0) - see slide notes",
], 0.5, 1.3, 12.4, 5.9, size=15)

prs.save(os.path.join(HERE, "Strassen.pptx"))
print("saved")
