"""
Why does C11 = M1 + M4 - M5 + M7 equal A11*B11 + A12*B21 ?

Expands the four products into their 12 raw terms, then cancels
opposite-sign pairs until only the two correct terms remain.
Target run time: ~42 seconds.

Render:  manim -qh strassen_cancellation.py StrassenCancellation
Preview: manim -pql strassen_cancellation.py StrassenCancellation

Uses Text (not MathTex) so no LaTeX install is required.
"""
from manim import *

# Sub-block names, e.g. a11 = A11
SUB = {"1": "₁", "2": "₂"}


def name(prefix, ij):
    return prefix + SUB[ij[0]] + SUB[ij[1]]


def term(sign, a, b):
    """Return a display string such as '+ a₁₁b₂₂'."""
    return f"{sign} {name('A', a)}{name('B', b)}"


# Each row: (label, [(sign, A-index, B-index), ...])
ROWS = [
    ("M₁", [("+", "11", "11"), ("+", "11", "22"), ("+", "22", "11"), ("+", "22", "22")]),
    ("M₄", [("+", "22", "21"), ("-", "22", "11")]),
    ("−M₅", [("-", "11", "22"), ("-", "12", "22")]),
    ("M₇", [("+", "12", "21"), ("+", "12", "22"), ("-", "22", "21"), ("-", "22", "22")]),
]

# Pairs of (row, col) that cancel each other
CANCEL_PAIRS = [
    ((0, 1), (2, 0)),  # A11B22
    ((0, 2), (1, 1)),  # A22B11
    ((0, 3), (3, 3)),  # A22B22
    ((1, 0), (3, 2)),  # A22B21
    ((2, 1), (3, 1)),  # A12B22
]
PAIR_COLOURS = [RED, ORANGE, PURPLE, TEAL, PINK]
SURVIVORS = [(0, 0), (3, 0)]  # A11B11 and A12B21


class StrassenCancellation(Scene):
    def construct(self):
        # ---- Title (0-5s) --------------------------------------------
        title = Text("Why do the sevens give the right answer?", font_size=34)
        goal = Text("C₁₁ = M₁ + M₄ − M₅ + M₇", font_size=40, color=YELLOW)
        goal.next_to(title, DOWN, buff=0.4)
        VGroup(title, goal).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(goal, shift=UP * 0.2), run_time=1)
        self.wait(2)

        # ---- Expand each product into raw terms (5-17s) ---------------
        grid = {}
        row_groups = []
        for r, (label, terms) in enumerate(ROWS):
            lab = Text(label + " =", font_size=30, color=BLUE_B)
            items = []
            for c, (s, a, b) in enumerate(terms):
                t = Text(term(s, a, b), font_size=28, font="Consolas")
                grid[(r, c)] = t
                items.append(t)
            line = VGroup(lab, *items).arrange(RIGHT, buff=0.35)
            row_groups.append(line)

        block = VGroup(*row_groups).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        block.next_to(goal, DOWN, buff=0.7)

        # Fix label column so rows line up nicely
        for line in row_groups:
            line.shift(LEFT * (line.get_left()[0] - block.get_left()[0]))

        for line in row_groups:
            self.play(FadeIn(line, shift=RIGHT * 0.3), run_time=2)
        note = Text(
            "12 terms. The answer only needs 2.", font_size=26, color=GREY_B
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note))
        self.wait(1.5)

        # ---- Cancel pairs (17-33s) ------------------------------------
        for (p, q), colour in zip(CANCEL_PAIRS, PAIR_COLOURS):
            t1, t2 = grid[p], grid[q]
            self.play(
                t1.animate.set_color(colour),
                t2.animate.set_color(colour),
                Indicate(t1, color=colour),
                Indicate(t2, color=colour),
                run_time=1.6,
            )
            self.play(
                Create(Cross(t1, stroke_color=colour, stroke_width=5)),
                Create(Cross(t2, stroke_color=colour, stroke_width=5)),
                t1.animate.set_opacity(0.2),
                t2.animate.set_opacity(0.2),
                run_time=1.6,
            )

        # ---- Survivors (33-42s) ---------------------------------------
        self.play(FadeOut(note))
        survivors = [grid[s] for s in SURVIVORS]
        self.play(
            *[Indicate(s, color=GREEN, scale_factor=1.3) for s in survivors],
            *[s.animate.set_color(GREEN) for s in survivors],
            run_time=1.5,
        )

        result = Text(
            "= A₁₁B₁₁ + A₁₂B₂₁", font_size=40, color=GREEN, font="Consolas"
        )
        result.next_to(block, DOWN, buff=0.6)
        caption = Text(
            "Exactly the classical C₁₁ - with one fewer multiplication per level",
            font_size=26,
            color=GREY_B,
        ).next_to(result, DOWN, buff=0.35)
        self.play(Write(result), run_time=1.5)
        self.play(FadeIn(caption))
        self.wait(5)
