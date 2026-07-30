"""
Selection Sort — Neon Light Theme, with an IDE-style code walkthrough
Manim Community v0.20.2

Render:
    manim -pql selectionsort_neon.py SelectionSortScene      # quick preview
    manim -pqh selectionsort_neon.py SelectionSortScene      # high quality

Structure mirrors the Quick Sort scene for series consistency:
    1. Title intro
    2. A short "how it works" principle panel (bullet points), since the
       user asked for the basic working idea to be explained up front
    3. Split screen: IDE-style code (gutter line numbers + real
       indentation, no leading-space bbox issues) on the left, the live
       neon array on the right, with a full-row highlighter bar that
       tracks and pops the currently-executing line
    4. The animation is driven by a real selection sort implementation —
       every "current minimum" pick, comparison, and swap you see is the
       algorithm actually running.
"""

from manim import *

# ---------------------------------------------------------------- palette --
BG_COLOR = "#090913"
CARD_FILL = "#12121f"
NEON_CYAN = "#00fff0"
NEON_MAGENTA = "#ff2ee8"
NEON_YELLOW = "#faff00"
NEON_GREEN = "#39ff14"
TEXT_WHITE = "#f4f4ff"
MUTED = "#7a7a9c"
CODE_MUTED = "#9d9dc9"

LIFT = 0.55
CARD_SIZE = 0.55
CARD_GAP = 0.16

# --------------------------------------------------------- code, IDE-style --
GUTTER_W = 0.55
INDENT_W = 0.34
LINE_H = 0.40
CODE_FS = 20

ALL_LINES = [
    (0, "def selection_sort(a):"),
    (1, "n = len(a)"),
    (1, "for i in range(n - 1):"),
    (2, "min_idx = i"),
    (2, "for j in range(i + 1, n):"),
    (3, "if a[j] < a[min_idx]:"),
    (4, "min_idx = j"),
    (1, "a[i], a[min_idx] = a[min_idx], a[i]"),
]
(L_DEF, L_N, L_FOR_I, L_MIN_INIT, L_FOR_J, L_IF, L_UPDATE_MIN, L_SWAP) = range(8)

T2C = {
    "def": NEON_CYAN, "for": NEON_CYAN, "if": NEON_CYAN, "in": NEON_CYAN,
    "selection_sort": NEON_MAGENTA, "len": NEON_MAGENTA, "range": NEON_MAGENTA,
}

PRINCIPLE_BULLETS = [
    "Splits the array into a sorted part (left) and an unsorted part (right).",
    "Scans the unsorted part to find its smallest element.",
    "Swaps that smallest element into the next open spot in the sorted part.",
    "Repeats, shrinking the unsorted part by one each pass \u2014 O(n\u00b2) comparisons in total.",
]


class SelectionSortScene(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        data = [8, 3, 7, 4, 9, 1, 6, 2, 5]

        # ---------------------------------------------------------- intro --
        title = Text("Selection Sort", weight=BOLD, color=NEON_CYAN).scale(1.15)
        title.to_edge(UP, buff=0.5)
        underline = Underline(title, color=NEON_MAGENTA, buff=0.12)
        self.play(Write(title), Create(underline), run_time=1.0)
        self.wait(0.2)

        # ---------------------------------------------------- how it works --
        self.play(FadeOut(underline), run_time=0.3)
        principle_group = self.build_principle_panel()
        principle_group.next_to(title, DOWN, buff=0.6)
        self.play(
            LaggedStart(*[FadeIn(row, shift=UP * 0.15) for row in principle_group], lag_ratio=0.25),
            run_time=2.0,
        )
        self.wait(1.6)
        self.play(FadeOut(principle_group), run_time=0.5)

        self.play(
            title.animate.scale(0.5).to_corner(UL, buff=0.35),
            run_time=0.6,
        )

        legend = self.build_legend()
        legend.to_corner(UR, buff=0.35)
        self.play(FadeIn(legend, shift=DOWN * 0.2), run_time=0.5)

        divider = Line(UP * 3.2, DOWN * 3.2, stroke_color=NEON_CYAN, stroke_width=1.5)
        divider.set_opacity(0.25)
        self.play(Create(divider), run_time=0.4)

        # ------------------------------------------------------- code panel --
        code_panel, code_lines, code_numbers = self.build_code_panel()
        code_panel.to_edge(LEFT, buff=0.5)
        code_panel.align_to(title, UP).shift(DOWN * 0.9)

        self.code_lines = code_lines
        self.code_numbers = code_numbers
        self.line_marker = None
        self.code_right_edge = max(t.get_right()[0] for t in code_lines) + 0.15
        self.code_left_edge = min(n.get_left()[0] for n in code_numbers) - 0.12
        self.code_line_step = abs(code_lines[0].get_y() - code_lines[1].get_y())

        self.play(FadeIn(code_panel, shift=RIGHT * 0.2), run_time=0.6)

        # ------------------------------------------------------ build array --
        bars, labels, idx_labels, array_group = self.build_array(data)
        array_group.shift(RIGHT * 3.55 + UP * 1.0)

        self.play(LaggedStart(*[GrowFromCenter(b) for b in bars], lag_ratio=0.08), run_time=1.1)
        self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.08), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(l) for l in idx_labels], lag_ratio=0.08), run_time=0.6)

        self.status_text = Text("Starting Selection Sort...", font_size=24, color=MUTED)
        self.status_text.next_to(array_group, DOWN, buff=0.7)
        self.play(FadeIn(self.status_text), run_time=0.4)
        self.wait(0.3)

        # ------------------------------------------------------- algorithm --
        self.bars = bars
        self.labels = labels
        self.values = data[:]
        self.positions = [b.get_center() for b in bars]
        self.sorted_flags = [False] * len(data)
        self.array_group = array_group

        self.run_selection_sort()

        # ---------------------------------------------------------- outro --
        self.set_status("Array fully sorted!", NEON_GREEN)
        self.play(
            *[
                self.bars[i].animate.set_stroke(NEON_GREEN, width=5).set_fill(NEON_GREEN, opacity=0.18)
                for i in range(len(data))
            ],
            run_time=0.8,
        )
        finale = Text("Sorted!", weight=BOLD, color=NEON_GREEN)
        finale.next_to(array_group, DOWN, buff=0.7)
        self.play(FadeOut(self.status_text), Write(finale), run_time=0.7)
        self.wait(1.6)

    # ---------------------------------------------------------------- UI --
    def build_principle_panel(self):
        rows = VGroup()
        for text_str in PRINCIPLE_BULLETS:
            dot = Dot(radius=0.06, color=NEON_MAGENTA)
            txt = Text(text_str, font_size=24, color=TEXT_WHITE)
            dot.next_to(txt, LEFT, buff=0.25)
            rows.add(VGroup(dot, txt))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        max_w = 10.5
        if rows.width > max_w:
            rows.scale(max_w / rows.width)
        return rows

    def build_legend(self):
        rows = [
            (NEON_YELLOW, "Current Min"),
            (NEON_MAGENTA, "Comparing"),
            (NEON_GREEN, "Sorted"),
        ]
        items = VGroup()
        for color, label in rows:
            chip = RoundedRectangle(corner_radius=0.05, width=0.24, height=0.24,
                                     stroke_color=color, stroke_width=3,
                                     fill_color=color, fill_opacity=0.25)
            text = Text(label, font_size=18, color=TEXT_WHITE)
            text.next_to(chip, RIGHT, buff=0.15)
            items.add(VGroup(chip, text))
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        return items

    def build_code_panel(self):
        line_mobs = VGroup()
        number_mobs = VGroup()

        for i, (indent, code) in enumerate(ALL_LINES):
            text = Text(code, font="Monospace", font_size=CODE_FS, color=TEXT_WHITE, t2c=T2C)
            num = Text(str(i + 1), font="Monospace", font_size=CODE_FS - 3, color=CODE_MUTED)

            x_text = GUTTER_W + indent * INDENT_W
            x_num_right = GUTTER_W - 0.14
            y = -i * LINE_H

            text.next_to([x_text, y, 0], RIGHT, buff=0)
            num.next_to([x_num_right, y, 0], LEFT, buff=0)

            line_mobs.add(text)
            number_mobs.add(num)

        gutter_top = number_mobs[0].get_top()[1] + 0.12
        gutter_bottom = number_mobs[-1].get_bottom()[1] - 0.12
        gutter_line = Line(
            [GUTTER_W - 0.05, gutter_top, 0], [GUTTER_W - 0.05, gutter_bottom, 0],
            stroke_color=CODE_MUTED, stroke_width=1,
        )
        gutter_line.set_opacity(0.4)

        header = Text("selection_sort.py", font_size=18, color=CODE_MUTED, weight=BOLD)
        header.next_to([0, LINE_H * 0.95, 0], RIGHT, buff=0)

        panel = VGroup(header, number_mobs, gutter_line, line_mobs)

        max_w, max_h = 6.3, 6.6
        scale_factor = min(max_w / panel.width, max_h / panel.height, 1.0)
        if scale_factor < 1.0:
            panel.scale(scale_factor)

        return panel, line_mobs, number_mobs

    def build_array(self, data):
        n = len(data)
        total_width = n * CARD_SIZE + (n - 1) * CARD_GAP
        start_x = -total_width / 2 + CARD_SIZE / 2

        bars, labels, idx_labels = VGroup(), VGroup(), VGroup()
        for i, val in enumerate(data):
            x = start_x + i * (CARD_SIZE + CARD_GAP)
            card = RoundedRectangle(
                corner_radius=0.1, width=CARD_SIZE, height=CARD_SIZE,
                stroke_color=NEON_CYAN, stroke_width=3.5,
                fill_color=CARD_FILL, fill_opacity=1,
            )
            card.move_to([x, 0, 0])

            num = Text(str(val), font_size=22, color=TEXT_WHITE, weight=BOLD)
            num.move_to(card.get_center())

            idx = Text(str(i), font_size=14, color=MUTED)
            idx.next_to(card, DOWN, buff=0.16)

            bars.add(card)
            labels.add(num)
            idx_labels.add(idx)

        group = VGroup(bars, labels, idx_labels)
        return bars, labels, idx_labels, group

    def set_status(self, msg, color=TEXT_WHITE):
        new_text = Text(msg, font_size=24, color=color)
        new_text.move_to(self.status_text)
        self.play(Transform(self.status_text, new_text), run_time=0.3)

    # ------------------------------------------------------- code highlight --
    def highlight_line(self, idx, run_time=0.3):
        line = self.code_lines[idx]
        h = self.code_line_step * 0.88
        y_center = line.get_y()
        box = Rectangle(
            width=self.code_right_edge - self.code_left_edge,
            height=h,
            stroke_color=NEON_YELLOW, stroke_width=2,
            fill_color=NEON_YELLOW, fill_opacity=0.10,
        )
        box.move_to([(self.code_left_edge + self.code_right_edge) / 2, y_center, 0])

        if self.line_marker is None:
            box.set_stroke(opacity=0)
            box.set_fill(opacity=0)
            self.line_marker = box
            self.add(self.line_marker)
            self.play(
                self.line_marker.animate.set_stroke(opacity=1).set_fill(opacity=0.10),
                Indicate(line, color=NEON_YELLOW, scale_factor=1.06),
                run_time=run_time,
            )
        else:
            self.play(
                self.line_marker.animate.move_to(box.get_center()),
                Indicate(line, color=NEON_YELLOW, scale_factor=1.06),
                run_time=run_time,
            )

    # ---------------------------------------------------------- algorithm --
    def run_selection_sort(self):
        n = len(self.values)
        self.highlight_line(L_DEF)
        self.highlight_line(L_N)

        for i in range(n - 1):
            self.highlight_line(L_FOR_I)
            self.highlight_line(L_MIN_INIT)
            min_idx = i
            self.set_status(f"Assume {self.values[i]} is the minimum", NEON_YELLOW)
            self.highlight_min(min_idx)

            for j in range(i + 1, n):
                self.highlight_line(L_FOR_J)
                self.highlight_line(L_IF)
                self.set_status(f"Comparing {self.values[j]} with current min {self.values[min_idx]}", NEON_MAGENTA)
                self.flash_compare(j)
                if self.values[j] < self.values[min_idx]:
                    self.highlight_line(L_UPDATE_MIN)
                    self.unhighlight_min(min_idx)
                    min_idx = j
                    self.set_status(f"New minimum found: {self.values[min_idx]}", NEON_YELLOW)
                    self.highlight_min(min_idx)
                self.unflash_compare(j)

            self.highlight_line(L_SWAP)
            if min_idx != i:
                self.set_status(f"Swap {self.values[i]} and {self.values[min_idx]} into place", NEON_MAGENTA)
                self.swap(i, min_idx)
            else:
                self.set_status(f"{self.values[i]} is already in place", MUTED)
            self.mark_sorted(i)

        self.mark_sorted(n - 1)

    # ------------------------------------------------------------ visuals --
    def highlight_min(self, idx):
        self.play(
            self.bars[idx].animate.set_stroke(NEON_YELLOW, width=5).set_fill(NEON_YELLOW, opacity=0.16),
            run_time=0.3,
        )

    def unhighlight_min(self, idx):
        if not self.sorted_flags[idx]:
            self.play(
                self.bars[idx].animate.set_stroke(NEON_CYAN, width=3.5).set_fill(CARD_FILL, opacity=1),
                run_time=0.25,
            )

    def flash_compare(self, j):
        if self.sorted_flags[j]:
            return
        self.play(self.bars[j].animate.set_stroke(NEON_MAGENTA, width=5), run_time=0.22)
        self.wait(0.06)

    def unflash_compare(self, j):
        if self.sorted_flags[j]:
            return
        self.play(self.bars[j].animate.set_stroke(NEON_CYAN, width=3.5), run_time=0.18)

    def mark_sorted(self, idx):
        self.sorted_flags[idx] = True
        self.play(
            self.bars[idx].animate.set_stroke(NEON_GREEN, width=4.5).set_fill(NEON_GREEN, opacity=0.16),
            run_time=0.28,
        )

    def swap(self, i, j):
        if i == j:
            return
        pos_i, pos_j = self.positions[i], self.positions[j]
        bar_i, bar_j = self.bars[i], self.bars[j]
        lab_i, lab_j = self.labels[i], self.labels[j]

        lift_i = pos_i + UP * LIFT
        lift_j = pos_j + UP * LIFT

        self.play(
            bar_i.animate.move_to(lift_i), lab_i.animate.move_to(lift_i),
            bar_j.animate.move_to(lift_j), lab_j.animate.move_to(lift_j),
            run_time=0.22,
        )
        self.play(
            bar_i.animate.move_to([pos_j[0], lift_i[1], 0]),
            lab_i.animate.move_to([pos_j[0], lift_i[1], 0]),
            bar_j.animate.move_to([pos_i[0], lift_j[1], 0]),
            lab_j.animate.move_to([pos_i[0], lift_j[1], 0]),
            run_time=0.26,
        )
        self.play(
            bar_i.animate.move_to(pos_j), lab_i.animate.move_to(pos_j),
            bar_j.animate.move_to(pos_i), lab_j.animate.move_to(pos_i),
            run_time=0.22,
        )

        self.bars[i], self.bars[j] = bar_j, bar_i
        self.labels[i], self.labels[j] = lab_j, lab_i
        self.values[i], self.values[j] = self.values[j], self.values[i]
