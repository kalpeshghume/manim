"""
Python Lists — Neon Light Theme, in-depth, with voiceover.
Manim Community v0.20.2
Voiceover uses manim_voiceover with Google Text‑to‑Speech (gTTS).

Install:
    pip install manim-voiceover gTTS

Render:
    manim -pql python_lists_neon.py ListsScene
    manim -pqh python_lists_neon.py ListsScene
"""

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

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

# --------------------------------------------------------- code, IDE-style --
GUTTER_W = 0.55
INDENT_W = 0.34
LINE_H = 0.40
CODE_FS = 20

T2C = {
    "for": NEON_CYAN, "while": NEON_CYAN, "not": NEON_CYAN, "True": NEON_YELLOW,
    "print": NEON_MAGENTA, "del": NEON_CYAN, "enumerate": NEON_MAGENTA,
    "len": NEON_MAGENTA, "max": NEON_MAGENTA, "min": NEON_MAGENTA,
    "sum": NEON_MAGENTA, "sorted": NEON_MAGENTA, "list": NEON_MAGENTA,
}


class ListsScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en"))

        self.camera.background_color = BG_COLOR
        self.section_mobjects = []
        self.build_main_title()

        self.section_intro()
        self.clear_section()

        self.section_characteristics()
        self.clear_section()

        self.section_creating()
        self.clear_section()

        self.section_accessing()
        self.clear_section()

        self.section_slicing()
        self.clear_section()

        self.section_updating()
        self.clear_section()

        self.section_adding()
        self.clear_section()

        self.section_removing()
        self.clear_section()

        self.section_operations()
        self.clear_section()

        self.section_methods_reference()
        self.clear_section()

        self.section_builtin_functions()
        self.clear_section()

        self.section_traversing()
        self.clear_section()

        self.section_outro()

    # ============================================================ shared --
    def track(self, mobj):
        self.section_mobjects.append(mobj)
        return mobj

    def clear_section(self):
        if self.section_mobjects:
            self.play(*[FadeOut(m) for m in self.section_mobjects], run_time=0.6)
            self.remove(*self.section_mobjects)
        self.section_mobjects = []

    def set_top_y(self, mobject, y):
        mobject.shift(UP * (y - mobject.get_top()[1]))

    def build_main_title(self):
        title = Text("Python Lists", weight=BOLD, color=NEON_CYAN).scale(1.2)
        title.move_to(ORIGIN)
        underline = Underline(title, color=NEON_MAGENTA, buff=0.12)
        with self.voiceover(text="Hi friends! Welcome to this comprehensive lesson on Python lists. Let's jump right in!") as tracker:
            self.play(Write(title), Create(underline), run_time=min(tracker.duration * 0.7, 1.2))
            self.wait(0.2)
        self.play(FadeOut(title), FadeOut(underline), run_time=0.5)

    def build_subtitle(self, text_str):
        sub = Text(text_str, font_size=27, color=NEON_MAGENTA, weight=BOLD)
        sub.to_edge(UP, buff=0.55)
        self.play(FadeIn(sub, shift=DOWN * 0.15), run_time=0.5)
        return sub

    def build_desc(self, text_str):
        desc = Text(text_str, font_size=20, color=MUTED)
        max_w = 10.5
        if desc.width > max_w:
            desc.scale(max_w / desc.width)
        return desc

    def build_bullet_list(self, lines, color=NEON_MAGENTA, font_size=22):
        rows = VGroup()
        for text_str in lines:
            dot = Dot(radius=0.06, color=color)
            txt = Text(text_str, font_size=font_size, color=TEXT_WHITE)
            dot.next_to(txt, LEFT, buff=0.25)
            rows.add(VGroup(dot, txt))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        max_w = 10.8
        if rows.width > max_w:
            rows.scale(max_w / rows.width)
        return rows

    def build_divider(self):
        divider = Line(UP * 3.2, DOWN * 3.2, stroke_color=NEON_CYAN, stroke_width=1.5)
        divider.set_opacity(0.25)
        return divider

    def make_chip(self, label):
        text = Text(label, font_size=17, color=TEXT_WHITE, weight=BOLD)
        box = RoundedRectangle(corner_radius=0.1, width=text.width + 0.45, height=0.6,
                                stroke_color=NEON_CYAN, stroke_width=2.3,
                                fill_color=CARD_FILL, fill_opacity=1)
        text.move_to(box.get_center())
        return VGroup(box, text)

    def make_badge(self, label, color):
        text = Text(label, font_size=15, color=color, weight=BOLD)
        box = RoundedRectangle(corner_radius=0.08, width=text.width + 0.4, height=0.42,
                                stroke_color=color, stroke_width=2,
                                fill_color=CARD_FILL, fill_opacity=1)
        text.move_to(box.get_center())
        return VGroup(box, text)

    def build_code_panel(self, lines, t2c=None, filename="code.py"):
        t2c = t2c or {}
        line_mobs = VGroup()
        number_mobs = VGroup()

        for i, (indent, code) in enumerate(lines):
            text = Text(code, font="Monospace", font_size=CODE_FS, color=TEXT_WHITE, t2c=t2c)
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

        header = Text(filename, font_size=18, color=CODE_MUTED, weight=BOLD)
        header.next_to([0, LINE_H * 0.95, 0], RIGHT, buff=0)

        panel = VGroup(header, number_mobs, gutter_line, line_mobs)

        max_w, max_h = 6.2, 5.6
        scale_factor = min(max_w / panel.width, max_h / panel.height, 1.0)
        if scale_factor < 1.0:
            panel.scale(scale_factor)

        return panel, line_mobs, number_mobs

    def setup_code_geometry(self, code_lines, code_numbers):
        self.code_lines = code_lines
        self.code_numbers = code_numbers
        self.line_marker = None
        self.code_right_edge = max(t.get_right()[0] for t in code_lines) + 0.15
        self.code_left_edge = min(n.get_left()[0] for n in code_numbers) - 0.12
        if len(code_lines) > 1:
            self.code_line_step = abs(code_lines[0].get_y() - code_lines[1].get_y())
        else:
            self.code_line_step = LINE_H

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
            self.track(self.line_marker)
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

    # ------------------------------------------------------- output terminal --
    def build_terminal(self, height=4.4):
        width = 6.0
        body = RoundedRectangle(
            corner_radius=0.15, width=width, height=height,
            stroke_color=NEON_GREEN, stroke_width=2.5,
            fill_color="#050508", fill_opacity=1,
        )
        top_bar = Rectangle(width=width, height=0.4, fill_color=CARD_FILL, fill_opacity=1, stroke_width=0)
        top_bar.move_to(body.get_top() + DOWN * 0.2)
        dots = VGroup(*[Dot(radius=0.055, color=c) for c in ["#ff5f56", "#ffbd2e", "#27c93f"]])
        dots.arrange(RIGHT, buff=0.12)
        dots.move_to(top_bar.get_left() + RIGHT * 0.35)
        label = Text("output", font_size=14, color=CODE_MUTED)
        label.move_to(top_bar.get_center())
        return VGroup(body, top_bar, dots, label)

    def setup_terminal_geometry(self, terminal):
        body, top_bar = terminal[0], terminal[1]
        self.output_lines = []
        self.output_start = [body.get_left()[0] + 0.3, top_bar.get_bottom()[1] - 0.3, 0]
        self.output_max_w = body.width - 0.6

    def print_output(self, text, color=NEON_GREEN):
        line = Text(text, font="Monospace", font_size=15, color=color)
        if line.width > self.output_max_w:
            line.scale(self.output_max_w / line.width)
        if self.output_lines:
            line.next_to(self.output_lines[-1], DOWN, buff=0.13, aligned_edge=LEFT)
        else:
            line.next_to(self.output_start, RIGHT, buff=0)
        self.output_lines.append(line)
        self.track(line)
        self.play(FadeIn(line, shift=RIGHT * 0.1), run_time=0.25)

    # -------------------------------------------------- list-block visuals --
    def build_list_row(self, values, start_index=0, show_neg=False, cell_w=1.05, cell_h=0.7, fs=17):
        n = len(values)
        cells = VGroup()
        idx_labels = VGroup()
        neg_labels = VGroup()
        for i, val in enumerate(values):
            cell = Rectangle(width=cell_w, height=cell_h, stroke_color=NEON_CYAN, stroke_width=2.6,
                              fill_color=CARD_FILL, fill_opacity=1)
            cell.move_to(RIGHT * i * cell_w)
            text = Text(str(val), font_size=fs, color=TEXT_WHITE, weight=BOLD)
            max_w = cell_w - 0.15
            if text.width > max_w:
                text.scale(max_w / text.width)
            text.move_to(cell.get_center())
            cells.add(VGroup(cell, text))

            idx = Text(str(start_index + i), font_size=13, color=NEON_YELLOW)
            idx.next_to(cell, DOWN, buff=0.12)
            idx_labels.add(idx)

            if show_neg:
                neg = Text(str(i - n), font_size=13, color=NEON_MAGENTA)
                neg.next_to(cell, UP, buff=0.12)
                neg_labels.add(neg)

        row = VGroup(cells, idx_labels)
        if show_neg:
            row.add(neg_labels)
        max_w_total = 12.0
        if row.width > max_w_total:
            row.scale(max_w_total / row.width)
        return row, cells, idx_labels, (neg_labels if show_neg else VGroup())

    def flash_cells(self, cells, indices, color=NEON_YELLOW):
        boxes = [cells[i][0] for i in indices]
        self.play(*[b.animate.set_stroke(color, width=4.5) for b in boxes], run_time=0.28)
        self.wait(0.15)
        self.play(*[b.animate.set_stroke(NEON_CYAN, width=2.6) for b in boxes], run_time=0.22)

    def replace_list_row(self, old_row, new_values, show_neg=False):
        anchor = old_row.get_center()
        self.play(FadeOut(old_row), run_time=0.3)
        if not new_values:
            box = RoundedRectangle(corner_radius=0.1, width=2.3, height=0.7,
                                    stroke_color=MUTED, stroke_width=2.3,
                                    fill_color=CARD_FILL, fill_opacity=1)
            text = Text("[ ]  empty", font_size=16, color=MUTED)
            text.move_to(box.get_center())
            new_row = VGroup(box, text)
            new_row.move_to(anchor)
            self.play(FadeIn(new_row, scale=1.1), run_time=0.5)
            return new_row, VGroup(), VGroup(), VGroup()
        new_row, cells, idx_labels, neg_labels = self.build_list_row(new_values, show_neg=show_neg)
        new_row.move_to(anchor)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.08), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(l) for l in idx_labels], lag_ratio=0.08), run_time=0.4)
        return new_row, cells, idx_labels, neg_labels

    def swap_row(self, old_row, new_values, show_neg=False):
        new_row, cells, idx_labels, neg_labels = self.replace_list_row(old_row, new_values, show_neg=show_neg)
        if old_row in self.section_mobjects:
            self.section_mobjects.remove(old_row)
        self.track(new_row)
        return new_row, cells, idx_labels, neg_labels

    def start_block_section(self, subtitle_text, values, show_neg=False):
        sub = self.track(self.build_subtitle(subtitle_text))
        row, cells, idx_labels, neg_labels = self.build_list_row(values, show_neg=show_neg)
        row.next_to(sub, DOWN, buff=0.4)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.1), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(l) for l in idx_labels], lag_ratio=0.1), run_time=0.6)
        if show_neg:
            self.play(LaggedStart(*[FadeIn(l) for l in neg_labels], lag_ratio=0.1), run_time=0.6)
        self.track(row)
        return sub, row, cells, idx_labels, neg_labels

    # ==================================================================== intro --
    def section_intro(self):
        subtitle = self.track(self.build_subtitle("Introduction to Lists"))

        bullets = self.build_bullet_list([
            "A list stores multiple values in a single variable.",
            "Values are written inside square brackets, comma-separated.",
            "A list can hold any mix of data types, even other lists.",
        ])
        bullets.next_to(subtitle, DOWN, buff=0.4)

        with self.voiceover(text="Hi everyone! Let's begin our journey with Python lists. A list is a container that can hold multiple values in one variable. You write them inside square brackets, separated by commas. And the best part? You can mix different data types, including other lists!") as tracker:
            self.play(
                LaggedStart(*[FadeIn(r, shift=UP * 0.15) for r in bullets], lag_ratio=0.25),
                run_time=min(tracker.duration * 0.6, 1.6),
            )
            self.track(bullets)

        values = [88, "A+", 91.5, [7, 8]]
        row, cells, idx_labels, _ = self.build_list_row(values)
        row.next_to(bullets, DOWN, buff=0.5)
        with self.voiceover(text="Here's an example list called 'scores' – it has an integer, a string, a float, and even a nested list. Each item has an index number underneath, starting from zero.") as tracker:
            self.play(LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.12), run_time=min(tracker.duration * 0.8, 1.2))
            self.play(LaggedStart(*[FadeIn(l) for l in idx_labels], lag_ratio=0.12), run_time=0.6)
            self.track(row)

        caption = Text('scores = [88, "A+", 91.5, [7, 8]]', font="Monospace", font_size=18, color=NEON_CYAN)
        caption.next_to(row, DOWN, buff=0.4)
        with self.voiceover(text="In Python code, we write it like this. Notice the square brackets and commas.") as tracker:
            self.play(FadeIn(caption), run_time=0.4)
            self.track(caption)
            self.wait(0.3)

    # ============================================================ characteristics --
    def section_characteristics(self):
        sub = self.track(self.build_subtitle("Characteristics of Lists"))
        desc = self.build_desc("Five defining traits, shown one at a time:")
        desc.next_to(sub, DOWN, buff=0.25)
        self.play(FadeIn(desc), run_time=0.4)
        self.track(desc)

        divider = self.build_divider()
        self.play(Create(divider), run_time=0.4)
        self.track(divider)

        code = [
            (0, "nums = [4, 9, 2]"),
            (0, "print(nums[0])"),
            (0, "nums[1] = 99"),
            (0, "print(nums)"),
            (0, 'mix = [5, "Go", 3.3]'),
            (0, "print(mix)"),
            (0, "dup = [4, 9, 4, 9]"),
            (0, "print(dup)"),
            (0, "nest = [[1, 2], [3, 4]]"),
            (0, "print(nest)"),
        ]
        outputs = [
            None, "4", None, "[4, 99, 2]", None, "[5, 'Go', 3.3]",
            None, "[4, 9, 4, 9]", None, "[[1, 2], [3, 4]]",
        ]
        badge_map = {
            1: ("ORDERED", NEON_CYAN), 3: ("MUTABLE", NEON_YELLOW),
            5: ("HETEROGENEOUS", NEON_MAGENTA), 7: ("DUPLICATES OK", NEON_GREEN),
            9: ("NESTED", NEON_CYAN),
        }

        panel, code_lines, code_numbers = self.build_code_panel(code, t2c=T2C, filename="characteristics_demo.py")
        panel.to_edge(LEFT, buff=0.5)
        panel.align_to(desc, UP).shift(DOWN * 0.55)
        self.setup_code_geometry(code_lines, code_numbers)
        self.play(FadeIn(panel, shift=RIGHT * 0.2), run_time=0.6)
        self.track(panel)

        terminal = self.build_terminal()
        terminal.to_edge(RIGHT, buff=0.6)
        terminal.align_to(panel, UP)
        self.play(FadeIn(terminal, shift=RIGHT * 0.2), run_time=0.5)
        self.track(terminal)
        self.setup_terminal_geometry(terminal)

        # Voice lines for each code line
        voice_lines = [
            "We create a list called 'nums' with three integers.",
            "Access the first element using index 0 – we get 4.",
            "Now we update the second element (index 1) to 99. Lists are mutable!",
            "Print the list – it has changed.",
            "Create a mixed list: an integer, a string, and a float.",
            "Print it – heterogeneous data is allowed.",
            "Create a list with duplicate values.",
            "Print it – duplicates are fine.",
            "Create a nested list – each inner list has two numbers.",
            "Print the nested structure."
        ]
        current_badge = None
        for i in range(len(code)):
            with self.voiceover(text=voice_lines[i]) as tracker:
                self.highlight_line(i)
                if outputs[i] is not None:
                    self.print_output(outputs[i])
                if i in badge_map:
                    label, color = badge_map[i]
                    if current_badge is not None:
                        self.play(FadeOut(current_badge), run_time=0.2)
                        self.section_mobjects.remove(current_badge)
                    badge = self.make_badge(label, color)
                    badge.next_to(terminal, DOWN, buff=0.3)
                    self.play(FadeIn(badge, scale=1.1), run_time=0.35)
                    self.track(badge)
                    current_badge = badge
        self.wait(0.3)

    # ==================================================================== creating --
    def section_creating(self):
        code = [
            (0, "empty_list = []"),
            (0, "scores = [72, 88, 95, 61]"),
            (0, 'mixed = [3, "Nova", 6.5, True]'),
            (0, "print(empty_list)"),
            (0, "print(scores)"),
            (0, "print(mixed)"),
        ]
        outputs = [None, None, None, "[]", "[72, 88, 95, 61]", "[3, 'Nova', 6.5, True]"]
        voice_lines = [
            "Create an empty list with square brackets.",
            "Create a list of integers called 'scores'.",
            "Create a mixed list with different types.",
            "Print the empty list.",
            "Print the scores list.",
            "Print the mixed list."
        ]
        self.run_code_section_with_voice(
            "Creating Lists",
            "Square brackets, comma-separated values",
            code, outputs, "creating_demo.py", voice_lines
        )

    # ==================================================================== accessing --
    def section_accessing(self):
        sub, row, cells, idx_labels, neg_labels = self.start_block_section(
            "Accessing List Elements", [72, 88, 95, 61, 79], show_neg=True
        )

        code = [
            (0, "scores = [72, 88, 95, 61, 79]"),
            (0, "print(scores[0])"),
            (0, "print(scores[3])"),
            (0, "print(scores[-1])"),
            (0, "print(scores[-2])"),
            (0, "matrix = [[1, 2], [3, 4]]"),
            (0, "print(matrix[1][0])"),
        ]
        outputs = [None, "72", "61", "79", "61", None, "3"]
        highlight_targets = {1: [0], 2: [3], 3: [4], 4: [3]}
        voice_lines = [
            "We have a list of five numbers.",
            "Access index 0 – get the first element.",
            "Access index 3 – that's the fourth element.",
            "Use a negative index -1 to get the last element.",
            "Negative -2 gives the second last element.",
            "Here's a nested list – matrix.",
            "Access the first element of the second inner list – we get 3."
        ]

        panel, code_lines, code_numbers = self.build_code_panel(code, t2c=T2C, filename="access_demo.py")
        panel.to_edge(LEFT, buff=0.5)
        self.set_top_y(panel, row.get_bottom()[1] - 0.35)
        self.setup_code_geometry(code_lines, code_numbers)
        self.play(FadeIn(panel, shift=RIGHT * 0.2), run_time=0.6)
        self.track(panel)

        terminal = self.build_terminal(height=3.8)
        terminal.to_edge(RIGHT, buff=0.6)
        self.set_top_y(terminal, row.get_bottom()[1] - 0.35)
        self.play(FadeIn(terminal, shift=RIGHT * 0.2), run_time=0.5)
        self.track(terminal)
        self.setup_terminal_geometry(terminal)

        for i in range(len(code)):
            with self.voiceover(text=voice_lines[i]) as tracker:
                self.highlight_line(i)
                if i in highlight_targets:
                    self.flash_cells(cells, highlight_targets[i], NEON_YELLOW)
                if outputs[i] is not None:
                    self.print_output(outputs[i])
        self.wait(0.3)

    # ==================================================================== slicing --
    def section_slicing(self):
        sub, row, cells, idx_labels, _ = self.start_block_section(
            "List Slicing", [72, 88, 95, 61, 79]
        )

        code = [
            (0, "scores = [72, 88, 95, 61, 79]"),
            (0, "print(scores[1:4])"),
            (0, "print(scores[:3])"),
            (0, "print(scores[::2])"),
            (0, "print(scores[::-1])"),
        ]
        outputs = [None, "[88, 95, 61]", "[72, 88, 95]", "[72, 95, 79]", "[79, 61, 95, 88, 72]"]
        highlight_targets = {1: [1, 2, 3], 2: [0, 1, 2], 3: [0, 2, 4], 4: [0, 1, 2, 3, 4]}
        voice_lines = [
            "We start with the same list.",
            "Slicing from index 1 to 3 (excluding 4) gives us three elements.",
            "Slicing from the beginning up to index 3 gives the first three.",
            "Using a step of 2 gives every second element.",
            "A negative step reverses the entire list."
        ]

        panel, code_lines, code_numbers = self.build_code_panel(code, t2c=T2C, filename="slicing_demo.py")
        panel.to_edge(LEFT, buff=0.5)
        self.set_top_y(panel, row.get_bottom()[1] - 0.35)
        self.setup_code_geometry(code_lines, code_numbers)
        self.play(FadeIn(panel, shift=RIGHT * 0.2), run_time=0.6)
        self.track(panel)

        terminal = self.build_terminal(height=3.8)
        terminal.to_edge(RIGHT, buff=0.6)
        self.set_top_y(terminal, row.get_bottom()[1] - 0.35)
        self.play(FadeIn(terminal, shift=RIGHT * 0.2), run_time=0.5)
        self.track(terminal)
        self.setup_terminal_geometry(terminal)

        for i in range(len(code)):
            with self.voiceover(text=voice_lines[i]) as tracker:
                self.highlight_line(i)
                if i in highlight_targets:
                    self.flash_cells(cells, highlight_targets[i], NEON_MAGENTA)
                if outputs[i] is not None:
                    self.print_output(outputs[i])
        self.wait(0.3)

    # ==================================================================== updating --
    def section_updating(self):
        sub, row, cells, idx_labels, _ = self.start_block_section(
            "Updating Lists", [72, 88, 95, 61, 79]
        )

        code = [
            (0, "scores = [72, 88, 95, 61, 79]"),
            (0, "scores[2] = 100"),
            (0, "print(scores)"),
            (0, "scores[0], scores[4] = 80, 85"),
            (0, "print(scores)"),
        ]
        outputs = [None, None, "[72, 88, 100, 61, 79]", None, "[80, 88, 100, 61, 85]"]
        voice_lines = [
            "Our list.",
            "Update the third element (index 2) to 100.",
            "Print the modified list.",
            "Simultaneously update the first and last elements.",
            "Print the final updated list."
        ]

        panel, code_lines, code_numbers = self.build_code_panel(code, t2c=T2C, filename="update_demo.py")
        panel.to_edge(LEFT, buff=0.5)
        self.set_top_y(panel, row.get_bottom()[1] - 0.35)
        self.setup_code_geometry(code_lines, code_numbers)
        self.play(FadeIn(panel, shift=RIGHT * 0.2), run_time=0.6)
        self.track(panel)

        terminal = self.build_terminal(height=3.8)
        terminal.to_edge(RIGHT, buff=0.6)
        self.set_top_y(terminal, row.get_bottom()[1] - 0.35)
        self.play(FadeIn(terminal, shift=RIGHT * 0.2), run_time=0.5)
        self.track(terminal)
        self.setup_terminal_geometry(terminal)

        for i in range(len(code)):
            with self.voiceover(text=voice_lines[i]) as tracker:
                self.highlight_line(i)
                if i == 1:
                    self.flash_cells(cells, [2], NEON_YELLOW)
                    row, cells, idx_labels, _ = self.swap_row(row, [72, 88, 100, 61, 79])
                if i == 3:
                    self.flash_cells(cells, [0, 4], NEON_YELLOW)
                    row, cells, idx_labels, _ = self.swap_row(row, [80, 88, 100, 61, 85])
                if outputs[i] is not None:
                    self.print_output(outputs[i])
        self.wait(0.3)

    # ==================================================================== adding --
    def section_adding(self):
        sub, row, cells, idx_labels, _ = self.start_block_section(
            "Adding Elements", [72, 88, 95]
        )

        code = [
            (0, "scores = [72, 88, 95]"),
            (0, "scores.append(61)"),
            (0, "print(scores)"),
            (0, "scores.insert(1, 99)"),
            (0, "print(scores)"),
            (0, "scores.extend([50, 45])"),
            (0, "print(scores)"),
        ]
        outputs = [
            None, None, "[72, 88, 95, 61]", None, "[72, 99, 88, 95, 61]",
            None, "[72, 99, 88, 95, 61, 50, 45]",
        ]
        voice_lines = [
            "Start with three numbers.",
            "Append 61 to the end.",
            "Print – it's added.",
            "Insert 99 at index 1.",
            "Print – 99 is now in second position.",
            "Extend the list by adding two more numbers.",
            "Print the final extended list."
        ]

        panel, code_lines, code_numbers = self.build_code_panel(code, t2c=T2C, filename="adding_demo.py")
        panel.to_edge(LEFT, buff=0.5)
        self.set_top_y(panel, row.get_bottom()[1] - 0.35)
        self.setup_code_geometry(code_lines, code_numbers)
        self.play(FadeIn(panel, shift=RIGHT * 0.2), run_time=0.6)
        self.track(panel)

        terminal = self.build_terminal(height=3.8)
        terminal.to_edge(RIGHT, buff=0.6)
        self.set_top_y(terminal, row.get_bottom()[1] - 0.35)
        self.play(FadeIn(terminal, shift=RIGHT * 0.2), run_time=0.5)
        self.track(terminal)
        self.setup_terminal_geometry(terminal)

        for i in range(len(code)):
            with self.voiceover(text=voice_lines[i]) as tracker:
                self.highlight_line(i)
                if i == 1:
                    row, cells, idx_labels, _ = self.swap_row(row, [72, 88, 95, 61])
                if i == 3:
                    row, cells, idx_labels, _ = self.swap_row(row, [72, 99, 88, 95, 61])
                if i == 5:
                    row, cells, idx_labels, _ = self.swap_row(row, [72, 99, 88, 95, 61, 50, 45])
                if outputs[i] is not None:
                    self.print_output(outputs[i])
        self.wait(0.3)

    # ==================================================================== removing --
    def section_removing(self):
        sub, row, cells, idx_labels, _ = self.start_block_section(
            "Removing Elements", [72, 99, 88, 95, 61]
        )

        code = [
            (0, "scores = [72, 99, 88, 95, 61]"),
            (0, "scores.remove(88)"),
            (0, "print(scores)"),
            (0, "scores.pop(0)"),
            (0, "print(scores)"),
            (0, "del scores[1]"),
            (0, "print(scores)"),
            (0, "scores.clear()"),
            (0, "print(scores)"),
        ]
        outputs = [
            None, None, "[72, 99, 95, 61]", None, "[99, 95, 61]",
            None, "[99, 61]", None, "[]",
        ]
        voice_lines = [
            "Start with five elements.",
            "Remove the value 88 – it finds and deletes it.",
            "Print the list – 88 is gone.",
            "Pop the first element (index 0).",
            "Print – first element is removed.",
            "Use del to delete the element at index 1.",
            "Print – now only two remain.",
            "Clear everything – empty the list.",
            "Print the empty list."
        ]

        panel, code_lines, code_numbers = self.build_code_panel(code, t2c=T2C, filename="removing_demo.py")
        panel.to_edge(LEFT, buff=0.5)
        self.set_top_y(panel, row.get_bottom()[1] - 0.35)
        self.setup_code_geometry(code_lines, code_numbers)
        self.play(FadeIn(panel, shift=RIGHT * 0.2), run_time=0.6)
        self.track(panel)

        terminal = self.build_terminal(height=3.8)
        terminal.to_edge(RIGHT, buff=0.6)
        self.set_top_y(terminal, row.get_bottom()[1] - 0.35)
        self.play(FadeIn(terminal, shift=RIGHT * 0.2), run_time=0.5)
        self.track(terminal)
        self.setup_terminal_geometry(terminal)

        for i in range(len(code)):
            with self.voiceover(text=voice_lines[i]) as tracker:
                self.highlight_line(i)
                if i == 1:
                    row, cells, idx_labels, _ = self.swap_row(row, [72, 99, 95, 61])
                if i == 3:
                    row, cells, idx_labels, _ = self.swap_row(row, [99, 95, 61])
                if i == 5:
                    row, cells, idx_labels, _ = self.swap_row(row, [99, 61])
                if i == 7:
                    row, cells, idx_labels, _ = self.swap_row(row, [])
                if outputs[i] is not None:
                    self.print_output(outputs[i])
        self.wait(0.3)

    # ==================================================================== operations --
    def section_operations(self):
        sub = self.track(self.build_subtitle("List Operations"))
        desc = self.build_desc("Concatenation, repetition, membership & iteration")
        desc.next_to(sub, DOWN, buff=0.25)
        self.play(FadeIn(desc), run_time=0.4)
        self.track(desc)

        divider = self.build_divider()
        self.play(Create(divider), run_time=0.4)
        self.track(divider)

        code = [
            (0, "a = [1, 2, 3]"),
            (0, "b = [4, 5]"),
            (0, "print(a + b)"),
            (0, "print(a * 2)"),
            (0, "print(3 in a)"),
            (0, "print(9 not in a)"),
            (0, "for item in a:"),
            (1, "print(item)"),
        ]
        voice_lines = [
            "List a with three numbers.",
            "List b with two numbers.",
            "Concatenate a and b – we get a combined list.",
            "Repeat a twice using the multiplication operator.",
            "Check if 3 is a member of a – True.",
            "Check if 9 is not in a – True.",
            "Iterate through the list using a for loop.",
            "Print each item on a new line."
        ]

        panel, code_lines, code_numbers = self.build_code_panel(code, t2c=T2C, filename="operations_demo.py")
        panel.to_edge(LEFT, buff=0.5)
        panel.align_to(desc, UP).shift(DOWN * 0.55)
        self.setup_code_geometry(code_lines, code_numbers)
        self.play(FadeIn(panel, shift=RIGHT * 0.2), run_time=0.6)
        self.track(panel)

        terminal = self.build_terminal()
        terminal.to_edge(RIGHT, buff=0.6)
        terminal.align_to(panel, UP)
        self.play(FadeIn(terminal, shift=RIGHT * 0.2), run_time=0.5)
        self.track(terminal)
        self.setup_terminal_geometry(terminal)

        # We'll handle each line with voiceover
        for i in range(6):
            with self.voiceover(text=voice_lines[i]) as tracker:
                self.highlight_line(i)
                out = [None, None, "[1, 2, 3, 4, 5]", "[1, 2, 3, 1, 2, 3]", "True", "True"][i]
                if out is not None:
                    self.print_output(out)

        # For the loop, we'll do separate voiceover for each iteration
        with self.voiceover(text=voice_lines[6]) as tracker:
            self.highlight_line(6)
        for val in [1, 2, 3]:
            with self.voiceover(text=f"Printing {val}.") as tracker:
                self.highlight_line(7)
                self.print_output(str(val))
        self.wait(0.3)

    # ============================================================ methods reference --
    def section_methods_reference(self):
        sub = self.track(self.build_subtitle("Built-in List Methods"))
        desc = self.build_desc("A quick reference, then the ones we haven't used yet:")
        desc.next_to(sub, DOWN, buff=0.25)
        self.play(FadeIn(desc), run_time=0.4)
        self.track(desc)

        names = ["append()", "extend()", "insert()", "remove()", "pop()", "clear()",
                 "index()", "count()", "sort()", "reverse()", "copy()"]
        chips = VGroup(*[self.make_chip(n) for n in names])
        chips.arrange_in_grid(rows=3, cols=4, buff=0.3)
        chips.next_to(desc, DOWN, buff=0.35)
        max_w = 12.0
        if chips.width > max_w:
            chips.scale(max_w / chips.width)
        with self.voiceover(text="Here are the most common list methods: append, extend, insert, remove, pop, clear, index, count, sort, reverse, and copy. We'll now see the ones we haven't covered yet.") as tracker:
            self.play(LaggedStart(*[GrowFromCenter(c) for c in chips], lag_ratio=0.06), run_time=min(tracker.duration * 0.8, 1.4))
            self.track(chips)
            self.wait(0.3)

        self.play(FadeOut(chips), run_time=0.4)
        self.section_mobjects.remove(chips)

        code = [
            (0, "scores = [72, 61, 95, 61, 88]"),
            (0, "print(scores.index(95))"),
            (0, "print(scores.count(61))"),
            (0, "scores.sort()"),
            (0, "print(scores)"),
            (0, "scores.reverse()"),
            (0, "print(scores)"),
            (0, "backup = scores.copy()"),
            (0, "print(backup)"),
        ]
        outputs = [
            None, "2", "2", None, "[61, 61, 72, 88, 95]",
            None, "[95, 88, 72, 61, 61]", None, "[95, 88, 72, 61, 61]",
        ]
        voice_lines = [
            "We have a list with duplicates.",
            "Find the index of value 95 – it's at position 2.",
            "Count how many times 61 appears – it's 2.",
            "Sort the list in ascending order.",
            "Print the sorted list.",
            "Reverse the sorted list.",
            "Print the reversed list.",
            "Create a copy of the list.",
            "Print the copy – it's identical."
        ]

        divider = self.build_divider()
        self.play(Create(divider), run_time=0.4)
        self.track(divider)

        panel, code_lines, code_numbers = self.build_code_panel(code, t2c=T2C, filename="methods_demo.py")
        panel.to_edge(LEFT, buff=0.5)
        panel.align_to(desc, UP).shift(DOWN * 0.55)
        self.setup_code_geometry(code_lines, code_numbers)
        self.play(FadeIn(panel, shift=RIGHT * 0.2), run_time=0.6)
        self.track(panel)

        terminal = self.build_terminal()
        terminal.to_edge(RIGHT, buff=0.6)
        terminal.align_to(panel, UP)
        self.play(FadeIn(terminal, shift=RIGHT * 0.2), run_time=0.5)
        self.track(terminal)
        self.setup_terminal_geometry(terminal)

        for i in range(len(code)):
            with self.voiceover(text=voice_lines[i]) as tracker:
                self.highlight_line(i)
                if outputs[i] is not None:
                    self.print_output(outputs[i])
        self.wait(0.3)

    # ============================================================ builtin functions --
    def section_builtin_functions(self):
        code = [
            (0, "nums = [14, 6, 27, 9]"),
            (0, "print(len(nums))"),
            (0, "print(max(nums))"),
            (0, "print(min(nums))"),
            (0, "print(sum(nums))"),
            (0, "print(sorted(nums))"),
            (0, 'print(list("abc"))'),
        ]
        outputs = [None, "4", "27", "6", "56", "[6, 9, 14, 27]", "['a', 'b', 'c']"]
        voice_lines = [
            "We have a list of numbers.",
            "Find the length using len() – it's 4.",
            "Find the maximum value – 27.",
            "Find the minimum value – 6.",
            "Sum all numbers – total is 56.",
            "Sorted returns a new sorted list.",
            "Convert a string to a list of characters."
        ]
        self.run_code_section_with_voice(
            "Built-in Functions with Lists",
            "len(), max(), min(), sum(), sorted(), list()",
            code, outputs, "builtin_functions_demo.py", voice_lines
        )

    # ==================================================================== traversing --
    def section_traversing(self):
        sub = self.track(self.build_subtitle("Traversing Lists"))
        desc = self.build_desc("for loop, while loop, and enumerate()")
        desc.next_to(sub, DOWN, buff=0.25)
        self.play(FadeIn(desc), run_time=0.4)
        self.track(desc)

        divider = self.build_divider()
        self.play(Create(divider), run_time=0.4)
        self.track(divider)

        code = [
            (0, 'items = ["pen", "book", "bag"]'),
            (0, "for x in items:"),
            (1, "print(x)"),
            (0, "i = 0"),
            (0, "while i < len(items):"),
            (1, "print(items[i])"),
            (1, "i += 1"),
            (0, "for idx, val in enumerate(items):"),
            (1, "print(idx, val)"),
        ]
        voice_lines = [
            "We have a list of items.",
            "Start a for loop to go through each item.",
            "Print the current item.",
            "Initialize index i to 0 for the while loop.",
            "Set up a while loop to iterate using an index.",
            "Print the item at current index.",
            "Increment the index.",
            "Use enumerate to get both index and value.",
            "Print index and value together."
        ]

        panel, code_lines, code_numbers = self.build_code_panel(code, t2c=T2C, filename="traversing_demo.py")
        panel.to_edge(LEFT, buff=0.5)
        panel.align_to(desc, UP).shift(DOWN * 0.55)
        self.setup_code_geometry(code_lines, code_numbers)
        self.play(FadeIn(panel, shift=RIGHT * 0.2), run_time=0.6)
        self.track(panel)

        terminal = self.build_terminal(height=5.2)
        terminal.to_edge(RIGHT, buff=0.6)
        terminal.align_to(panel, UP)
        self.play(FadeIn(terminal, shift=RIGHT * 0.2), run_time=0.5)
        self.track(terminal)
        self.setup_terminal_geometry(terminal)

        items = ["pen", "book", "bag"]

        # For loop
        with self.voiceover(text=voice_lines[0]) as tracker:
            self.highlight_line(0)
        with self.voiceover(text=voice_lines[1]) as tracker:
            self.highlight_line(1)
        for val in items:
            with self.voiceover(text=f"Print {val}.") as tracker:
                self.highlight_line(2)
                self.print_output(val)

        # While loop
        with self.voiceover(text=voice_lines[3]) as tracker:
            self.highlight_line(3)
        with self.voiceover(text=voice_lines[4]) as tracker:
            self.highlight_line(4)
        for val in items:
            with self.voiceover(text=voice_lines[5]) as tracker:
                self.highlight_line(5)
                self.print_output(val)
            with self.voiceover(text=voice_lines[6]) as tracker:
                self.highlight_line(6)

        # Enumerate
        with self.voiceover(text=voice_lines[7]) as tracker:
            self.highlight_line(7)
        for idx, val in enumerate(items):
            with self.voiceover(text=voice_lines[8]) as tracker:
                self.highlight_line(8)
                self.print_output(f"{idx} {val}")

        self.wait(0.3)

    # -------------------------------------------------------- shared code runner --
    def run_code_section_with_voice(self, subtitle_text, desc_text, code, outputs, filename, voice_lines):
        sub = self.track(self.build_subtitle(subtitle_text))
        desc = self.build_desc(desc_text)
        desc.next_to(sub, DOWN, buff=0.25)
        self.play(FadeIn(desc), run_time=0.4)
        self.track(desc)

        divider = self.build_divider()
        self.play(Create(divider), run_time=0.4)
        self.track(divider)

        panel, code_lines, code_numbers = self.build_code_panel(code, t2c=T2C, filename=filename)
        panel.to_edge(LEFT, buff=0.5)
        panel.align_to(desc, UP).shift(DOWN * 0.55)
        self.setup_code_geometry(code_lines, code_numbers)
        self.play(FadeIn(panel, shift=RIGHT * 0.2), run_time=0.6)
        self.track(panel)

        terminal = self.build_terminal()
        terminal.to_edge(RIGHT, buff=0.6)
        terminal.align_to(panel, UP)
        self.play(FadeIn(terminal, shift=RIGHT * 0.2), run_time=0.5)
        self.track(terminal)
        self.setup_terminal_geometry(terminal)

        for i in range(len(code)):
            with self.voiceover(text=voice_lines[i]) as tracker:
                self.highlight_line(i)
                if outputs[i] is not None:
                    self.print_output(outputs[i])
        self.wait(0.3)

    # ==================================================================== outro --
    def section_outro(self):
        with self.voiceover(text="That's all for today, friends! I hope you now feel confident with Python lists. If you enjoyed this lesson, please like, share, and subscribe. See you in the next one!") as tracker:
            thanks = Text("Thanks for Watching!", weight=BOLD, color=NEON_CYAN).scale(1.1)
            thanks.move_to(UP * 1.6)
            self.play(Write(thanks), run_time=min(tracker.duration * 0.3, 1.0))
            self.track(thanks)

            tagline = Text(
                "Like, Share & Subscribe for more visual Python learning",
                font_size=22, color=MUTED,
            )
            max_w = 11.0
            if tagline.width > max_w:
                tagline.scale(max_w / tagline.width)
            tagline.next_to(thanks, DOWN, buff=0.4)
            self.play(FadeIn(tagline), run_time=0.6)
            self.track(tagline)

            buttons = VGroup(
                self.make_outro_button("LIKE", NEON_MAGENTA),
                self.make_outro_button("SHARE", NEON_GREEN),
                self.make_outro_button("SUBSCRIBE", NEON_YELLOW),
            )
            buttons.arrange(RIGHT, buff=0.6)
            buttons.next_to(tagline, DOWN, buff=0.7)
            self.play(
                LaggedStart(*[GrowFromCenter(b) for b in buttons], lag_ratio=0.25),
                run_time=min(tracker.duration * 0.4, 1.2),
            )
            self.play(*[Indicate(b, scale_factor=1.1, color=NEON_CYAN) for b in buttons], run_time=0.6)
            self.track(buttons)
            self.wait(0.5)

    def make_outro_button(self, label, color):
        box = RoundedRectangle(corner_radius=0.15, width=2.7, height=0.8,
                                stroke_color=color, stroke_width=3,
                                fill_color=CARD_FILL, fill_opacity=1)
        text = Text(label, font_size=22, color=color, weight=BOLD)
        text.move_to(box.get_center())
        return VGroup(box, text)