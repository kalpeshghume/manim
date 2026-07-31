python3 << 'PY'
from pathlib import Path

code = r'''"""
Python Data Types — Neon Light Theme, single progressive scene
Manim Community v0.20.2

Render:
    manim -pql python_data_types_neon.py PythonDataTypesScene
    manim -pqh python_data_types_neon.py PythonDataTypesScene

One continuous Scene. Topics in order, screen cleared between each:

  1. Overview of Data Types
  2. Numeric   (int, float, complex)
  3. String
  4. Sequence  (list, tuple, range)
  5. Mapping   (dict)
  6. Boolean
  7. Set
  8. Outro

Only ONE Scene subclass — required by some online Manim runners.
All example names/values are original (not copied from Programiz or similar).
Layouts keep content inside frame margins to avoid cropping/overlap.
"""

from manim import *

# ---------------------------------------------------------------- palette --
BG_COLOR = "#090913"
CARD_FILL = "#12121f"
NEON_CYAN = "#00fff0"
NEON_MAGENTA = "#ff2ee8"
NEON_YELLOW = "#faff00"
NEON_GREEN = "#39ff14"
GC_RED = "#ff3860"
TEXT_WHITE = "#f4f4ff"
MUTED = "#7a7a9c"
CODE_MUTED = "#9d9dc9"

# --------------------------------------------------------- code, IDE-style --
GUTTER_W = 0.50
INDENT_W = 0.30
LINE_H = 0.38
CODE_FS = 18


class PythonDataTypesScene(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        self.section_mobjects = []
        self.line_marker = None
        self.main_title = self.build_main_title()

        self.section_overview()
        self.clear_section()

        self.section_numeric()
        self.clear_section()

        self.section_string()
        self.clear_section()

        self.section_sequence()
        self.clear_section()

        self.section_mapping()
        self.clear_section()

        self.section_boolean()
        self.clear_section()

        self.section_set()
        self.clear_section()

        self.section_outro()

    # ============================================================ shared --
    def track(self, mobj):
        self.section_mobjects.append(mobj)
        return mobj

    def clear_section(self):
        present = [m for m in self.section_mobjects if m in self.mobjects]
        if present:
            self.play(*[FadeOut(m) for m in present], run_time=0.55)
        self.section_mobjects = []
        self.line_marker = None
        self.wait(0.25)

    def build_main_title(self):
        title = Text("Python Data Types", weight=BOLD, color=NEON_CYAN).scale(1.1)
        title.to_edge(UP, buff=0.45)
        underline = Underline(title, color=NEON_MAGENTA, buff=0.10)
        self.play(Write(title), Create(underline), run_time=1.0)
        self.wait(0.15)
        self.play(
            title.animate.scale(0.48).to_corner(UL, buff=0.30),
            FadeOut(underline),
            run_time=0.55,
        )
        return title

    def build_subtitle(self, text_str):
        sub = Text(text_str, font_size=26, color=NEON_MAGENTA, weight=BOLD)
        sub.to_edge(UP, buff=0.50)
        self.play(FadeIn(sub, shift=DOWN * 0.12), run_time=0.45)
        return sub

    def build_legend(self, rows):
        items = VGroup()
        for color, label in rows:
            chip = RoundedRectangle(
                corner_radius=0.05, width=0.22, height=0.22,
                stroke_color=color, stroke_width=2.5,
                fill_color=color, fill_opacity=0.25,
            )
            text = Text(label, font_size=16, color=TEXT_WHITE)
            text.next_to(chip, RIGHT, buff=0.12)
            items.add(VGroup(chip, text))
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        return items

    def build_divider(self):
        divider = Line(UP * 3.0, DOWN * 3.0, stroke_color=NEON_CYAN, stroke_width=1.4)
        divider.set_opacity(0.22)
        return divider

    def build_code_panel(self, lines, filename="demo.py"):
        line_mobs = VGroup()
        number_mobs = VGroup()

        for i, (indent, code) in enumerate(lines):
            text = Text(code, font="Monospace", font_size=CODE_FS, color=TEXT_WHITE)
            num = Text(str(i + 1), font="Monospace", font_size=CODE_FS - 3, color=CODE_MUTED)
            x_text = GUTTER_W + indent * INDENT_W
            x_num_right = GUTTER_W - 0.12
            y = -i * LINE_H
            text.next_to([x_text, y, 0], RIGHT, buff=0)
            num.next_to([x_num_right, y, 0], LEFT, buff=0)
            line_mobs.add(text)
            number_mobs.add(num)

        gutter_top = number_mobs[0].get_top()[1] + 0.10
        gutter_bottom = number_mobs[-1].get_bottom()[1] - 0.10
        gutter_line = Line(
            [GUTTER_W - 0.04, gutter_top, 0],
            [GUTTER_W - 0.04, gutter_bottom, 0],
            stroke_color=CODE_MUTED, stroke_width=1,
        )
        gutter_line.set_opacity(0.35)

        header = Text(filename, font_size=16, color=CODE_MUTED, weight=BOLD)
        header.next_to([0, LINE_H * 0.90, 0], RIGHT, buff=0)

        panel = VGroup(header, number_mobs, gutter_line, line_mobs)
        max_w, max_h = 6.0, 5.8
        scale_factor = min(max_w / panel.width, max_h / panel.height, 1.0)
        if scale_factor < 1.0:
            panel.scale(scale_factor)
        return panel, line_mobs, number_mobs

    def setup_code_geometry(self, code_lines, code_numbers):
        self.code_lines = code_lines
        self.code_numbers = code_numbers
        self.line_marker = None
        self.code_right_edge = max(t.get_right()[0] for t in code_lines) + 0.12
        self.code_left_edge = min(n.get_left()[0] for n in code_numbers) - 0.10
        if len(code_lines) > 1:
            self.code_line_step = abs(code_lines[0].get_y() - code_lines[1].get_y())
        else:
            self.code_line_step = LINE_H

    def highlight_line(self, idx, run_time=0.30):
        line = self.code_lines[idx]
        h = self.code_line_step * 0.86
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
            self.track(self.line_marker)
            self.play(
                self.line_marker.animate.set_stroke(opacity=1).set_fill(opacity=0.10),
                Indicate(line, color=NEON_YELLOW, scale_factor=1.04),
                run_time=run_time,
            )
        else:
            self.play(
                self.line_marker.animate.move_to(box.get_center()),
                Indicate(line, color=NEON_YELLOW, scale_factor=1.04),
                run_time=run_time,
            )

    def make_output_card(self, lines, title="Output"):
        """Right-side output panel with title + result lines."""
        header = Text(title, font_size=18, color=NEON_CYAN, weight=BOLD)
        body_rows = VGroup()
        for ln in lines:
            body_rows.add(Text(ln, font="Monospace", font_size=17, color=TEXT_WHITE))
        body_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        inner = VGroup(header, body_rows).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        box = SurroundingRectangle(
            inner, color=NEON_CYAN, buff=0.28, stroke_width=2,
            corner_radius=0.12,
        )
        box.set_fill(CARD_FILL, opacity=1)
        card = VGroup(box, inner)
        return card

    def make_type_chip(self, label, color):
        chip = RoundedRectangle(
            corner_radius=0.10, width=2.4, height=0.55,
            stroke_color=color, stroke_width=2.5,
            fill_color=CARD_FILL, fill_opacity=1,
        )
        txt = Text(label, font_size=18, color=color, weight=BOLD)
        txt.move_to(chip.get_center())
        return VGroup(chip, txt)

    # =================================================== 1. OVERVIEW --
    def section_overview(self):
        subtitle = self.track(self.build_subtitle("1. What are Data Types?"))

        intro = Text(
            "Data types tell Python what kind of value a variable holds.",
            font_size=22, color=TEXT_WHITE,
        )
        intro.next_to(subtitle, DOWN, buff=0.45)
        intro.set_x(0)
        self.play(FadeIn(intro, shift=UP * 0.1), run_time=0.5)
        self.track(intro)

        # 6 category cards in 2 rows
        cats = [
            ("Numeric", "int  float  complex", NEON_GREEN),
            ("String", "str", NEON_CYAN),
            ("Sequence", "list  tuple  range", NEON_YELLOW),
            ("Mapping", "dict", NEON_MAGENTA),
            ("Boolean", "bool", NEON_GREEN),
            ("Set", "set  frozenset", NEON_CYAN),
        ]
        cards = VGroup()
        for title, detail, color in cats:
            head = Text(title, font_size=20, color=color, weight=BOLD)
            body = Text(detail, font_size=15, color=MUTED)
            inner = VGroup(head, body).arrange(DOWN, buff=0.12)
            box = SurroundingRectangle(
                inner, color=color, buff=0.22, stroke_width=2.2, corner_radius=0.10,
            )
            box.set_fill(CARD_FILL, opacity=1)
            cards.add(VGroup(box, inner))

        row1 = VGroup(*cards[:3]).arrange(RIGHT, buff=0.45)
        row2 = VGroup(*cards[3:]).arrange(RIGHT, buff=0.45)
        grid = VGroup(row1, row2).arrange(DOWN, buff=0.40)
        grid.next_to(intro, DOWN, buff=0.55)
        grid.set_x(0)

        # scale if needed to stay on screen
        if grid.width > 12.5:
            grid.scale(12.5 / grid.width)

        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in cards], lag_ratio=0.12),
            run_time=1.6,
        )
        self.track(grid)
        self.wait(1.4)

    # =================================================== 2. NUMERIC --
    def section_numeric(self):
        subtitle = self.track(self.build_subtitle("2. Numeric Types"))

        bullets = VGroup(
            Text("•  int     — whole numbers of any size", font_size=20, color=TEXT_WHITE),
            Text("•  float   — numbers with a decimal point", font_size=20, color=TEXT_WHITE),
            Text("•  complex — real + imaginary parts  (a + bj)", font_size=20, color=TEXT_WHITE),
        )
        bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        bullets.next_to(subtitle, DOWN, buff=0.40).to_edge(LEFT, buff=0.55)
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in bullets], lag_ratio=0.18), run_time=1.0)
        self.track(bullets)

        divider = self.build_divider()
        self.play(Create(divider), run_time=0.3)
        self.track(divider)

        code_lines = [
            (0, "points = 150"),
            (0, "ratio = 3.75"),
            (0, "wave = 2 + 5j"),
            (0, "print(type(points))"),
            (0, "print(type(ratio))"),
            (0, "print(type(wave))"),
        ]
        code_panel, clines, cnums = self.build_code_panel(code_lines, "numeric_demo.py")
        code_panel.to_edge(LEFT, buff=0.45)
        code_panel.shift(DOWN * 0.55)
        self.setup_code_geometry(clines, cnums)
        self.play(FadeIn(code_panel, shift=RIGHT * 0.15), run_time=0.5)
        self.track(code_panel)

        # right side: type chips that appear one by one
        chips = VGroup(
            self.make_type_chip("int", NEON_GREEN),
            self.make_type_chip("float", NEON_YELLOW),
            self.make_type_chip("complex", NEON_MAGENTA),
        )
        chips.arrange(DOWN, buff=0.35)
        chips.move_to([3.6, 0.3, 0])

        outputs = [
            '<class \'int\'>',
            '<class \'float\'>',
            '<class \'complex\'>',
        ]

        for i, (chip, out) in enumerate(zip(chips, outputs)):
            self.highlight_line(i)
            self.wait(0.15)
            self.highlight_line(i + 3)
            out_txt = Text(out, font="Monospace", font_size=16, color=MUTED)
            out_txt.next_to(chip, RIGHT, buff=0.25)
            self.play(FadeIn(chip, shift=LEFT * 0.1), FadeIn(out_txt), run_time=0.4)
            self.track(chip)
            self.track(out_txt)

        self.wait(1.0)

    # =================================================== 3. STRING --
    def section_string(self):
        subtitle = self.track(self.build_subtitle("3. String Type"))

        note = Text(
            "A string is a sequence of characters, written in quotes.",
            font_size=20, color=TEXT_WHITE,
        )
        note.next_to(subtitle, DOWN, buff=0.40)
        note.set_x(0)
        self.play(FadeIn(note), run_time=0.45)
        self.track(note)

        divider = self.build_divider()
        self.play(Create(divider), run_time=0.3)
        self.track(divider)

        code_lines = [
            (0, 'city = "Aurora"'),
            (0, "tag = 'code-lab'"),
            (0, "print(city)"),
            (0, "print(tag)"),
            (0, "print(type(city))"),
        ]
        code_panel, clines, cnums = self.build_code_panel(code_lines, "string_demo.py")
        code_panel.to_edge(LEFT, buff=0.45)
        code_panel.shift(DOWN * 0.35)
        self.setup_code_geometry(clines, cnums)
        self.play(FadeIn(code_panel, shift=RIGHT * 0.15), run_time=0.5)
        self.track(code_panel)

        out_card = self.make_output_card([
            "Aurora",
            "code-lab",
            "<class 'str'>",
        ])
        out_card.move_to([3.5, 0.4, 0])

        for i in range(5):
            self.highlight_line(i)
            if i == 2:
                self.play(FadeIn(out_card), run_time=0.45)
                self.track(out_card)
            self.wait(0.25)

        self.wait(0.9)

    # =================================================== 4. SEQUENCE --
    def section_sequence(self):
        subtitle = self.track(self.build_subtitle("4. Sequence Types"))

        intro = Text(
            "Sequences store ordered collections of items.",
            font_size=20, color=TEXT_WHITE,
        )
        intro.next_to(subtitle, DOWN, buff=0.35)
        intro.set_x(0)
        self.play(FadeIn(intro), run_time=0.4)
        self.track(intro)

        # three mini cards: list / tuple / range
        defs = [
            ("list", "[ ]  mutable", NEON_GREEN,
             'skills = ["design", "code", "test"]'),
            ("tuple", "( )  immutable", NEON_YELLOW,
             'coords = (12, 8, 3)'),
            ("range", "range(start, stop)", NEON_MAGENTA,
             "steps = range(0, 5)"),
        ]

        cards = VGroup()
        for title, trait, color, example in defs:
            head = Text(title, font_size=22, color=color, weight=BOLD)
            trait_t = Text(trait, font_size=15, color=MUTED)
            ex = Text(example, font="Monospace", font_size=15, color=TEXT_WHITE)
            inner = VGroup(head, trait_t, ex).arrange(DOWN, buff=0.14)
            box = SurroundingRectangle(
                inner, color=color, buff=0.22, stroke_width=2.2, corner_radius=0.10,
            )
            box.set_fill(CARD_FILL, opacity=1)
            cards.add(VGroup(box, inner))

        cards.arrange(RIGHT, buff=0.35)
        cards.next_to(intro, DOWN, buff=0.40)
        cards.set_x(0)
        if cards.width > 12.8:
            cards.scale(12.8 / cards.width)

        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards], lag_ratio=0.2),
            run_time=1.2,
        )
        self.track(cards)

        # live demo for list access
        demo_note = Text("Access by index  →  skills[0]  returns  \"design\"", font_size=18, color=NEON_CYAN)
        demo_note.next_to(cards, DOWN, buff=0.50)
        demo_note.set_x(0)
        self.play(FadeIn(demo_note, shift=UP * 0.08), run_time=0.45)
        self.track(demo_note)
        self.wait(1.3)

    # =================================================== 5. MAPPING --
    def section_mapping(self):
        subtitle = self.track(self.build_subtitle("5. Mapping Type — dict"))

        note = Text(
            "A dictionary stores data as key → value pairs.",
            font_size=20, color=TEXT_WHITE,
        )
        note.next_to(subtitle, DOWN, buff=0.38)
        note.set_x(0)
        self.play(FadeIn(note), run_time=0.4)
        self.track(note)

        divider = self.build_divider()
        self.play(Create(divider), run_time=0.3)
        self.track(divider)

        code_lines = [
            (0, "player = {"),
            (1, '"name": "Nova",'),
            (1, '"level": 7,'),
            (1, '"active": True,'),
            (0, "}"),
            (0, 'print(player["name"])'),
            (0, "print(type(player))"),
        ]
        code_panel, clines, cnums = self.build_code_panel(code_lines, "dict_demo.py")
        code_panel.to_edge(LEFT, buff=0.45)
        code_panel.shift(DOWN * 0.25)
        self.setup_code_geometry(clines, cnums)
        self.play(FadeIn(code_panel, shift=RIGHT * 0.15), run_time=0.5)
        self.track(code_panel)

        # visual key-value cards on the right
        pairs = [
            ("name", "Nova", NEON_MAGENTA),
            ("level", "7", NEON_YELLOW),
            ("active", "True", NEON_GREEN),
        ]
        kv_cards = VGroup()
        for key, val, color in pairs:
            k = Text(key, font="Monospace", font_size=16, color=color, weight=BOLD)
            arrow = Text("→", font_size=16, color=MUTED)
            v = Text(val, font="Monospace", font_size=16, color=TEXT_WHITE)
            row = VGroup(k, arrow, v).arrange(RIGHT, buff=0.18)
            box = SurroundingRectangle(row, color=color, buff=0.16, stroke_width=1.8, corner_radius=0.08)
            box.set_fill(CARD_FILL, opacity=1)
            kv_cards.add(VGroup(box, row))
        kv_cards.arrange(DOWN, buff=0.28)
        kv_cards.move_to([3.5, 0.9, 0])

        for i in range(5):
            self.highlight_line(i)
        self.play(
            LaggedStart(*[FadeIn(c, shift=LEFT * 0.1) for c in kv_cards], lag_ratio=0.15),
            run_time=0.9,
        )
        self.track(kv_cards)

        self.highlight_line(5)
        out1 = Text('Nova', font="Monospace", font_size=18, color=NEON_CYAN)
        out1.next_to(kv_cards, DOWN, buff=0.45)
        self.play(FadeIn(out1), run_time=0.35)
        self.track(out1)

        self.highlight_line(6)
        out2 = Text("<class 'dict'>", font="Monospace", font_size=16, color=MUTED)
        out2.next_to(out1, DOWN, buff=0.20)
        self.play(FadeIn(out2), run_time=0.35)
        self.track(out2)
        self.wait(1.0)

    # =================================================== 6. BOOLEAN --
    def section_boolean(self):
        subtitle = self.track(self.build_subtitle("6. Boolean Type"))

        note = Text(
            "Booleans hold only two values:  True  or  False.",
            font_size=20, color=TEXT_WHITE,
        )
        note.next_to(subtitle, DOWN, buff=0.38)
        note.set_x(0)
        self.play(FadeIn(note), run_time=0.4)
        self.track(note)

        divider = self.build_divider()
        self.play(Create(divider), run_time=0.3)
        self.track(divider)

        code_lines = [
            (0, "ready = True"),
            (0, "paused = False"),
            (0, "print(ready)"),
            (0, "print(type(paused))"),
            (0, "print(5 > 2)"),
        ]
        code_panel, clines, cnums = self.build_code_panel(code_lines, "bool_demo.py")
        code_panel.to_edge(LEFT, buff=0.45)
        code_panel.shift(DOWN * 0.30)
        self.setup_code_geometry(clines, cnums)
        self.play(FadeIn(code_panel, shift=RIGHT * 0.15), run_time=0.5)
        self.track(code_panel)

        # two big True / False cards
        true_card = self._bool_card("True", NEON_GREEN)
        false_card = self._bool_card("False", GC_RED)
        bool_group = VGroup(true_card, false_card).arrange(RIGHT, buff=0.50)
        bool_group.move_to([3.5, 1.1, 0])

        self.highlight_line(0)
        self.play(GrowFromCenter(true_card), run_time=0.4)
        self.track(true_card)

        self.highlight_line(1)
        self.play(GrowFromCenter(false_card), run_time=0.4)
        self.track(false_card)

        self.highlight_line(2)
        out1 = Text("True", font="Monospace", font_size=18, color=NEON_GREEN)
        out1.move_to([3.5, -0.4, 0])
        self.play(FadeIn(out1), run_time=0.3)
        self.track(out1)

        self.highlight_line(3)
        out2 = Text("<class 'bool'>", font="Monospace", font_size=16, color=MUTED)
        out2.next_to(out1, DOWN, buff=0.18)
        self.play(FadeIn(out2), run_time=0.3)
        self.track(out2)

        self.highlight_line(4)
        out3 = Text("5 > 2  →  True", font="Monospace", font_size=17, color=NEON_YELLOW)
        out3.next_to(out2, DOWN, buff=0.22)
        self.play(FadeIn(out3), run_time=0.35)
        self.track(out3)
        self.wait(1.0)

    def _bool_card(self, label, color):
        box = RoundedRectangle(
            corner_radius=0.12, width=2.2, height=0.85,
            stroke_color=color, stroke_width=3,
            fill_color=CARD_FILL, fill_opacity=1,
        )
        txt = Text(label, font_size=26, color=color, weight=BOLD)
        txt.move_to(box.get_center())
        return VGroup(box, txt)

    # =================================================== 7. SET --
    def section_set(self):
        subtitle = self.track(self.build_subtitle("7. Set Type"))

        note = Text(
            "A set holds unique items — no duplicates, no fixed order.",
            font_size=20, color=TEXT_WHITE,
        )
        note.next_to(subtitle, DOWN, buff=0.38)
        note.set_x(0)
        self.play(FadeIn(note), run_time=0.4)
        self.track(note)

        divider = self.build_divider()
        self.play(Create(divider), run_time=0.3)
        self.track(divider)

        code_lines = [
            (0, "badges = {10, 20, 10, 30}"),
            (0, "print(badges)"),
            (0, "print(type(badges))"),
        ]
        code_panel, clines, cnums = self.build_code_panel(code_lines, "set_demo.py")
        code_panel.to_edge(LEFT, buff=0.45)
        code_panel.shift(DOWN * 0.20)
        self.setup_code_geometry(clines, cnums)
        self.play(FadeIn(code_panel, shift=RIGHT * 0.15), run_time=0.5)
        self.track(code_panel)

        # visual unique items
        items = VGroup()
        for val, color in [("10", NEON_GREEN), ("20", NEON_YELLOW), ("30", NEON_MAGENTA)]:
            circ = Circle(radius=0.38, stroke_color=color, stroke_width=2.5, fill_color=CARD_FILL, fill_opacity=1)
            lbl = Text(val, font_size=20, color=TEXT_WHITE, weight=BOLD)
            lbl.move_to(circ.get_center())
            items.add(VGroup(circ, lbl))
        items.arrange(RIGHT, buff=0.35)
        items.move_to([3.5, 1.0, 0])

        self.highlight_line(0)
        self.play(
            LaggedStart(*[GrowFromCenter(it) for it in items], lag_ratio=0.2),
            run_time=0.9,
        )
        self.track(items)

        dup_note = Text("duplicate 10 is dropped", font_size=15, color=MUTED)
        dup_note.next_to(items, DOWN, buff=0.30)
        self.play(FadeIn(dup_note), run_time=0.35)
        self.track(dup_note)

        self.highlight_line(1)
        out1 = Text("{10, 20, 30}", font="Monospace", font_size=18, color=NEON_CYAN)
        out1.next_to(dup_note, DOWN, buff=0.35)
        self.play(FadeIn(out1), run_time=0.35)
        self.track(out1)

        self.highlight_line(2)
        out2 = Text("<class 'set'>", font="Monospace", font_size=16, color=MUTED)
        out2.next_to(out1, DOWN, buff=0.18)
        self.play(FadeIn(out2), run_time=0.3)
        self.track(out2)
        self.wait(1.1)

    # =================================================== 8. OUTRO --
    def section_outro(self):
        thanks = Text("Thanks for Watching!", weight=BOLD, color=NEON_CYAN).scale(1.1)
        thanks.move_to(UP * 1.2)
        self.play(Write(thanks), run_time=0.9)
        self.track(thanks)

        summary = Text(
            "Numeric  ·  String  ·  Sequence  ·  Mapping  ·  Boolean  ·  Set",
            font_size=18, color=MUTED,
        )
        summary.next_to(thanks, DOWN, buff=0.45)
        self.play(FadeIn(summary), run_time=0.5)
        self.track(summary)

        buttons = VGroup(
            self._outro_btn("LIKE", NEON_MAGENTA),
            self._outro_btn("SUBSCRIBE", NEON_YELLOW),
            self._outro_btn("SHARE", NEON_GREEN),
        )
        buttons.arrange(RIGHT, buff=0.50)
        buttons.next_to(summary, DOWN, buff=0.70)
        self.play(
            LaggedStart(*[GrowFromCenter(b) for b in buttons], lag_ratio=0.2),
            run_time=1.0,
        )
        self.play(*[Indicate(b, scale_factor=1.08, color=NEON_CYAN) for b in buttons], run_time=0.55)
        self.track(buttons)
        self.wait(1.8)

    def _outro_btn(self, label, color):
        box = RoundedRectangle(
            corner_radius=0.14, width=2.5, height=0.75,
            stroke_color=color, stroke_width=2.8,
            fill_color=CARD_FILL, fill_opacity=1,
        )
        txt = Text(label, font_size=20, color=color, weight=BOLD)
        txt.move_to(box.get_center())
        return VGroup(box, txt)
'''

path = Path("/home/workdir/artifacts/python_data_types_neon.py")
path.write_text(code)
print("Written", path.stat().st_size, "bytes")
import re
print(re.findall(r'class \w+\(.*Scene', path.read_text()))
PY
