"""
Python Dictionaries — Neon Light Theme, in-depth, with voiceover.
Manim Community v0.20.2
Voiceover uses manim_voiceover with Google Text‑to‑Speech (gTTS).

Install:
    pip install manim-voiceover gTTS

Render:
    manim -pql python_dict_neon.py DictScene
    manim -pqh python_dict_neon.py DictScene
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
    "for": NEON_CYAN, "not": NEON_CYAN, "True": NEON_YELLOW, "False": NEON_YELLOW,
    "print": NEON_MAGENTA, "del": NEON_CYAN, "list": NEON_MAGENTA,
}


class DictScene(VoiceoverScene):
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

        self.section_adding()
        self.clear_section()

        self.section_updating()
        self.clear_section()

        self.section_removing()
        self.clear_section()

        self.section_iterating()
        self.clear_section()

        self.section_membership()
        self.clear_section()

        self.section_methods()
        self.clear_section()

        self.section_keyvalue()
        self.clear_section()

        self.section_unique_keys()
        self.clear_section()

        self.section_nested()
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
        title = Text("Python Dictionaries", weight=BOLD, color=NEON_CYAN).scale(1.2)
        title.move_to(ORIGIN)
        underline = Underline(title, color=NEON_MAGENTA, buff=0.12)
        with self.voiceover(text="Hi friends! Welcome to this comprehensive lesson on Python dictionaries. Let's dive right in!") as tracker:
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

    def build_legend(self, rows):
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

    # -------------------------------------------------- dict-block visuals --
    def _fmt(self, x):
        return f"'{x}'" if isinstance(x, str) else str(x)

    def build_dict_cell(self, key, value, cell_w=1.9, half_h=0.5):
        key_box = Rectangle(width=cell_w, height=half_h, stroke_color=NEON_MAGENTA, stroke_width=2.4,
                             fill_color=CARD_FILL, fill_opacity=1)
        val_box = Rectangle(width=cell_w, height=half_h, stroke_color=NEON_CYAN, stroke_width=2.4,
                             fill_color=CARD_FILL, fill_opacity=1)
        val_box.next_to(key_box, DOWN, buff=0)
        key_text = Text(self._fmt(key), font_size=15, color=NEON_MAGENTA, weight=BOLD)
        val_text = Text(self._fmt(value), font_size=15, color=TEXT_WHITE)
        max_w = cell_w - 0.18
        if key_text.width > max_w:
            key_text.scale(max_w / key_text.width)
        if val_text.width > max_w:
            val_text.scale(max_w / val_text.width)
        key_text.move_to(key_box.get_center())
        val_text.move_to(val_box.get_center())
        return VGroup(key_box, val_box, key_text, val_text)

    def build_dict_row(self, pairs, cell_w=1.9):
        cells = VGroup()
        for i, (k, v) in enumerate(pairs):
            cell = self.build_dict_cell(k, v, cell_w=cell_w)
            cell.move_to(RIGHT * i * cell_w)
            cells.add(cell)
        row = VGroup(cells)
        max_w_total = 12.5
        if row.width > max_w_total:
            row.scale(max_w_total / row.width)
        return row, cells

    def flash_dict_cell(self, cells, index, part="both", color=NEON_YELLOW):
        cell = cells[index]
        boxes = []
        if part in ("key", "both"):
            boxes.append(cell[0])
        if part in ("value", "both"):
            boxes.append(cell[1])
        self.play(*[b.animate.set_stroke(color, width=4.2) for b in boxes], run_time=0.26)
        self.wait(0.12)
        restore = []
        for b in boxes:
            orig = NEON_MAGENTA if b is cell[0] else NEON_CYAN
            restore.append(b.animate.set_stroke(orig, width=2.4))
        self.play(*restore, run_time=0.2)

    def replace_dict_row(self, old_row, new_pairs):
        anchor = old_row.get_center()
        self.play(FadeOut(old_row), run_time=0.3)
        if not new_pairs:
            box = RoundedRectangle(corner_radius=0.1, width=2.5, height=0.9,
                                    stroke_color=MUTED, stroke_width=2.3,
                                    fill_color=CARD_FILL, fill_opacity=1)
            text = Text("{ }  empty", font_size=16, color=MUTED)
            text.move_to(box.get_center())
            new_row = VGroup(box, text)
            new_row.move_to(anchor)
            self.play(FadeIn(new_row, scale=1.1), run_time=0.5)
            return new_row, VGroup()
        new_row, cells = self.build_dict_row(new_pairs)
        new_row.move_to(anchor)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.1), run_time=0.7)
        return new_row, cells

    def swap_dict_row(self, old_row, new_pairs):
        new_row, cells = self.replace_dict_row(old_row, new_pairs)
        if old_row in self.section_mobjects:
            self.section_mobjects.remove(old_row)
        self.track(new_row)
        return new_row, cells

    def start_dict_block_section(self, subtitle_text, pairs, legend_rows=None):
        sub = self.track(self.build_subtitle(subtitle_text))

        if legend_rows is None:
            legend_rows = [(NEON_MAGENTA, "Key"), (NEON_CYAN, "Value")]
        legend = self.build_legend(legend_rows)
        legend.to_corner(UR, buff=0.35)
        self.play(FadeIn(legend, shift=DOWN * 0.2), run_time=0.5)
        self.track(legend)

        row, cells = self.build_dict_row(pairs)
        row.next_to(sub, DOWN, buff=0.45)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.15), run_time=1.1)
        self.track(row)
        return sub, row, cells

    # ==================================================================== intro --
    def section_intro(self):
        subtitle = self.track(self.build_subtitle("Introduction to Dictionaries"))
        bullets = self.build_bullet_list([
            "A dictionary stores data as key: value pairs.",
            "Each key maps directly to its own value — no",
            "counting positions like a list, just look up the key.",
        ])
        bullets.next_to(subtitle, DOWN, buff=0.4)

        with self.voiceover(text=(
            "Alright friends! A dictionary is a way to store data as key-value pairs. "
            "Instead of counting positions like you do with a list, you can just look up the key directly. "
            "It's like a real dictionary – you look up a word and find its definition."
        )) as tracker:
            self.play(
                LaggedStart(*[FadeIn(r, shift=UP * 0.15) for r in bullets], lag_ratio=0.25),
                run_time=min(tracker.duration * 0.6, 1.6),
            )
            self.track(bullets)

        pairs = [(101, "Coffee"), (102, "Tea"), (103, "Juice")]
        row, cells = self.build_dict_row(pairs)
        row.next_to(bullets, DOWN, buff=0.5)
        with self.voiceover(text="Here's a simple example: a menu that maps item IDs to beverage names. You'll see the key in magenta and the value in white.") as tracker:
            self.play(LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.15), run_time=min(tracker.duration * 0.8, 1.4))
            self.track(row)

        legend_note = Text("top = key (magenta)     bottom = value (white)", font_size=16, color=MUTED)
        legend_note.next_to(row, DOWN, buff=0.35)
        self.play(FadeIn(legend_note), run_time=0.4)
        self.track(legend_note)

        caption = Text('menu = {101: "Coffee", 102: "Tea", 103: "Juice"}',
                        font="Monospace", font_size=16, color=NEON_CYAN)
        caption.next_to(legend_note, DOWN, buff=0.3)
        with self.voiceover(text="In Python, we write this dictionary as menu equals open curly brace, 101 colon Coffee, comma, 102 colon Tea, and so on. Easy, right?") as tracker:
            self.play(FadeIn(caption), run_time=0.5)
            self.track(caption)
            self.wait(0.5)

    # ============================================================ characteristics --
    def section_characteristics(self):
        sub, row, cells = self.start_dict_block_section(
            "Characteristics of Dictionaries", [("name", "Zara"), ("age", 21)]
        )

        code = [
            (0, 'info = {"name": "Zara", "age": 21}'),
            (0, 'print(info["name"])'),
            (0, 'info["age"] = 22'),
            (0, "print(info)"),
            (0, 'info["age"] = 30'),
            (0, "print(info)"),
            (0, 'mixed = {1: "one", "two": 2}'),
            (0, "print(mixed)"),
        ]
        outputs = [
            None, "Zara", None, "{'name': 'Zara', 'age': 22}",
            None, "{'name': 'Zara', 'age': 30}", None, "{1: 'one', 'two': 2}",
        ]
        badge_map = {
            1: ("INDEXED BY KEY", NEON_CYAN), 3: ("MUTABLE", NEON_YELLOW),
            5: ("UNIQUE KEYS", NEON_MAGENTA), 7: ("HETEROGENEOUS", NEON_GREEN),
        }
        flash_map = {1: (0, "key"), 2: (1, "value"), 4: (1, "value")}

        panel, code_lines, code_numbers = self.build_code_panel(code, t2c=T2C, filename="characteristics_demo.py")
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

        current_badge = None

        line_voices = [
            "We create a dictionary with two keys: 'name' and 'age'.",
            "Look! We can access the value using the key inside square brackets.",
            "Now let's change the age to 22 – dictionaries are mutable.",
            "See the updated dictionary.",
            "And again, we update the same key to 30.",
            "Print it – the value has changed.",
            "Dictionaries can hold different types – here we have integer and string keys.",
            "And the output shows both."
        ]
        for i in range(len(code)):
            voice_text = line_voices[i] if i < len(line_voices) else ""
            with self.voiceover(text=voice_text) as tracker:
                self.highlight_line(i)
                if i in flash_map:
                    idx, part = flash_map[i]
                    self.flash_dict_cell(cells, idx, part, NEON_YELLOW)
                if i == 2:
                    row, cells = self.swap_dict_row(row, [("name", "Zara"), ("age", 22)])
                if i == 4:
                    row, cells = self.swap_dict_row(row, [("name", "Zara"), ("age", 30)])
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
        self.wait(0.5)

    # ==================================================================== creating --
    def section_creating(self):
        code = [
            (0, "empty_dict = {}"),
            (0, 'profile_one = {"name": "Zara", "age": 21, "city": "Lisbon"}'),
            (0, 'profile_two = dict(name="Kai", age=19, city="Osaka")'),
            (0, "print(empty_dict)"),
            (0, "print(profile_one)"),
            (0, "print(profile_two)"),
        ]
        outputs = [
            None, None, None, "{}",
            "{'name': 'Zara', 'age': 21, 'city': 'Lisbon'}",
            "{'name': 'Kai', 'age': 19, 'city': 'Osaka'}",
        ]
        voice_lines = [
            "We start with an empty dictionary using curly braces.",
            "Now we create a dictionary with three entries using the literal syntax.",
            "Alternatively, you can use the dict() constructor with keyword arguments – both ways are fine.",
            "Print the empty dictionary.",
            "Print profile one – see the key-value pairs.",
            "And profile two – identical structure."
        ]
        self.run_simple_code_section(
            "Creating a Dictionary",
            "Curly braces with key: value pairs, or dict()",
            code, outputs, "creating_demo.py", voice_lines
        )

    # ==================================================================== accessing --
    def section_accessing(self):
        sub, row, cells = self.start_dict_block_section(
            "Accessing Dictionary Items", [("name", "Zara"), ("level", 12), ("score", 340)]
        )

        code = [
            (0, 'player = {"name": "Zara", "level": 12, "score": 340}'),
            (0, 'print(player["name"])'),
            (0, 'print(player["level"])'),
            (0, 'print(player.get("score"))'),
            (0, 'print(player.get("rank"))'),
        ]
        outputs = [None, "Zara", "12", "340", "None"]
        flash_map = {1: 0, 2: 1, 3: 2}
        voice_lines = [
            "We define a player dictionary.",
            "We use square brackets to access the name – simple and fast.",
            "Now we get the level.",
            "There's also a safe method called get – it works the same for existing keys.",
            "But if the key doesn't exist, get returns None instead of raising an error – very handy!"
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
                if i in flash_map:
                    self.flash_dict_cell(cells, flash_map[i], "both", NEON_YELLOW)
                if outputs[i] is not None:
                    self.print_output(outputs[i])
        note = Text("get() returns None instead of erroring on a missing key", font_size=15, color=MUTED)
        note.next_to(terminal, DOWN, buff=0.25)
        if note.width > terminal.width:
            note.scale(terminal.width / note.width)
        with self.voiceover(text="So always prefer get when you're not sure if a key exists – it's safer.") as tracker:
            self.play(FadeIn(note), run_time=0.4)
            self.track(note)
            self.wait(0.3)

    # ==================================================================== adding --
    def section_adding(self):
        sub, row, cells = self.start_dict_block_section("Adding Items to a Dictionary", [("name", "Zara"), ("level", 12)])

        code = [
            (0, 'player = {"name": "Zara", "level": 12}'),
            (0, "print(player)"),
            (0, 'player["score"] = 340'),
            (0, "print(player)"),
        ]
        outputs = [None, "{'name': 'Zara', 'level': 12}", None, "{'name': 'Zara', 'level': 12, 'score': 340}"]
        voice_lines = [
            "We have a player with name and level.",
            "Print it – two items.",
            "Now we add a new key 'score' by simply assigning a value to it.",
            "Print again – the dictionary has grown!"
        ]

        panel, code_lines, code_numbers = self.build_code_panel(code, t2c=T2C, filename="adding_demo.py")
        panel.to_edge(LEFT, buff=0.5)
        self.set_top_y(panel, row.get_bottom()[1] - 0.35)
        self.setup_code_geometry(code_lines, code_numbers)
        self.play(FadeIn(panel, shift=RIGHT * 0.2), run_time=0.6)
        self.track(panel)

        terminal = self.build_terminal(height=3.6)
        terminal.to_edge(RIGHT, buff=0.6)
        self.set_top_y(terminal, row.get_bottom()[1] - 0.35)
        self.play(FadeIn(terminal, shift=RIGHT * 0.2), run_time=0.5)
        self.track(terminal)
        self.setup_terminal_geometry(terminal)

        for i in range(len(code)):
            with self.voiceover(text=voice_lines[i]) as tracker:
                self.highlight_line(i)
                if i == 2:
                    row, cells = self.swap_dict_row(row, [("name", "Zara"), ("level", 12), ("score", 340)])
                if outputs[i] is not None:
                    self.print_output(outputs[i])
        self.wait(0.3)

    # ==================================================================== updating --
    def section_updating(self):
        sub, row, cells = self.start_dict_block_section(
            "Updating Dictionary Items", [("name", "Zara"), ("level", 12), ("score", 340)]
        )

        code = [
            (0, 'player = {"name": "Zara", "level": 12, "score": 340}'),
            (0, 'player["level"] = 13'),
            (0, 'player["score"] = 410'),
            (0, "print(player)"),
        ]
        outputs = [None, None, None, "{'name': 'Zara', 'level': 13, 'score': 410}"]
        voice_lines = [
            "Here's our player.",
            "We can update the level by reassigning.",
            "Similarly, we update the score.",
            "Print it – the values have changed."
        ]

        panel, code_lines, code_numbers = self.build_code_panel(code, t2c=T2C, filename="update_demo.py")
        panel.to_edge(LEFT, buff=0.5)
        self.set_top_y(panel, row.get_bottom()[1] - 0.35)
        self.setup_code_geometry(code_lines, code_numbers)
        self.play(FadeIn(panel, shift=RIGHT * 0.2), run_time=0.6)
        self.track(panel)

        terminal = self.build_terminal(height=3.6)
        terminal.to_edge(RIGHT, buff=0.6)
        self.set_top_y(terminal, row.get_bottom()[1] - 0.35)
        self.play(FadeIn(terminal, shift=RIGHT * 0.2), run_time=0.5)
        self.track(terminal)
        self.setup_terminal_geometry(terminal)

        for i in range(len(code)):
            with self.voiceover(text=voice_lines[i]) as tracker:
                self.highlight_line(i)
                if i == 1:
                    self.flash_dict_cell(cells, 1, "value", NEON_YELLOW)
                    row, cells = self.swap_dict_row(row, [("name", "Zara"), ("level", 13), ("score", 340)])
                if i == 2:
                    self.flash_dict_cell(cells, 2, "value", NEON_YELLOW)
                    row, cells = self.swap_dict_row(row, [("name", "Zara"), ("level", 13), ("score", 410)])
                if outputs[i] is not None:
                    self.print_output(outputs[i])
        self.wait(0.3)

    # ==================================================================== removing --
    def section_removing(self):
        sub, row, cells = self.start_dict_block_section(
            "Removing Dictionary Items",
            [("name", "Zara"), ("score", 410), ("region", "EU")],
        )

        code = [
            (0, 'player = {"name": "Zara", "score": 410, "region": "EU"}'),
            (0, 'del player["region"]'),
            (0, "print(player)"),
            (0, 'removed = player.pop("score")'),
            (0, "print(player)"),
            (0, "print(removed)"),
            (0, "last_item = player.popitem()"),
            (0, "print(player)"),
            (0, "print(last_item)"),
            (0, "player.clear()"),
            (0, "print(player)"),
        ]
        outputs = [
            None, None, "{'name': 'Zara', 'score': 410}",
            None, "{'name': 'Zara'}", "410",
            None, "{}", "('name', 'Zara')",
            None, "{}",
        ]
        voice_lines = [
            "We start with three keys.",
            "Use 'del' to remove the 'region' key.",
            "Now the dictionary is smaller.",
            "Pop removes the key and returns its value.",
            "After pop, only 'name' is left.",
            "Here's the popped value.",
            "popitem() removes and returns the last inserted key-value pair.",
            "Now the dictionary is empty.",
            "popitem returns a tuple of key and value.",
            "clear() empties everything at once.",
            "And we get an empty dictionary."
        ]

        panel, code_lines, code_numbers = self.build_code_panel(code, t2c=T2C, filename="removing_demo.py")
        panel.to_edge(LEFT, buff=0.5)
        self.set_top_y(panel, row.get_bottom()[1] - 0.35)
        self.setup_code_geometry(code_lines, code_numbers)
        self.play(FadeIn(panel, shift=RIGHT * 0.2), run_time=0.6)
        self.track(panel)

        terminal = self.build_terminal(height=4.6)
        terminal.to_edge(RIGHT, buff=0.6)
        self.set_top_y(terminal, row.get_bottom()[1] - 0.35)
        self.play(FadeIn(terminal, shift=RIGHT * 0.2), run_time=0.5)
        self.track(terminal)
        self.setup_terminal_geometry(terminal)

        for i in range(len(code)):
            with self.voiceover(text=voice_lines[i]) as tracker:
                self.highlight_line(i)
                if i == 1:
                    row, cells = self.swap_dict_row(row, [("name", "Zara"), ("score", 410)])
                if i == 3:
                    row, cells = self.swap_dict_row(row, [("name", "Zara")])
                if i == 6:
                    row, cells = self.swap_dict_row(row, [])
                if outputs[i] is not None:
                    self.print_output(outputs[i])
        self.wait(0.3)

    # ==================================================================== iterating --
    def section_iterating(self):
        sub, row, cells = self.start_dict_block_section(
            "Iterating Through a Dictionary",
            [("name", "Zara"), ("level", 13), ("score", 410)],
        )

        code = [
            (0, 'player = {"name": "Zara", "level": 13, "score": 410}'),
            (0, "for key in player:"),
            (1, "value = player[key]"),
            (1, 'print(key, "->", value)'),
        ]
        outputs = [None, None, None, None]
        voice_lines = [
            "Here's our player.",
            "We can loop over the dictionary to get each key.",
            "For each key, we retrieve its value.",
            "And then print both key and value."
        ]

        panel, code_lines, code_numbers = self.build_code_panel(code, t2c=T2C, filename="iterating_demo.py")
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

        with self.voiceover(text=voice_lines[0]) as tracker:
            self.highlight_line(0)
        with self.voiceover(text=voice_lines[1]) as tracker:
            self.highlight_line(1)

        pairs = [("name", "Zara"), ("level", 13), ("score", 410)]
        for i, (k, v) in enumerate(pairs):
            with self.voiceover(text=f"Now we get '{k}' and print its value.") as tracker:
                self.highlight_line(2)
                self.flash_dict_cell(cells, i, "both", NEON_YELLOW)
                self.highlight_line(3)
                self.print_output(f"{k} -> {v}")
        self.wait(0.3)

    # ==================================================================== membership --
    def section_membership(self):
        code = [
            (0, 'player = {"name": "Zara", "level": 13}'),
            (0, 'print("name" in player)'),
            (0, 'print("rank" in player)'),
            (0, 'print("rank" not in player)'),
        ]
        outputs = [None, "True", "False", "True"]
        voice_lines = [
            "We have a player dictionary.",
            "We can check if a key exists using 'in' – 'name' is present, so True.",
            "'rank' is not there, so False.",
            "We can also check the opposite with 'not in' – it returns True."
        ]
        self.run_simple_code_section(
            "Checking Key Existence (in / not in)",
            "Test whether a key exists before using it",
            code, outputs, "membership_demo.py", voice_lines
        )

    # ==================================================================== methods --
    def section_methods(self):
        sub = self.track(self.build_subtitle("Dictionary Methods"))
        desc = self.build_desc("A quick reference, then the ones we haven't used yet:")
        desc.next_to(sub, DOWN, buff=0.25)
        self.play(FadeIn(desc), run_time=0.4)
        self.track(desc)

        names = ["get()", "update()", "copy()", "pop()", "popitem()", "clear()", "keys()", "values()"]
        chips = VGroup(*[self.make_chip(n) for n in names])
        chips.arrange_in_grid(rows=2, cols=4, buff=0.3)
        chips.next_to(desc, DOWN, buff=0.35)
        max_w = 12.0
        if chips.width > max_w:
            chips.scale(max_w / chips.width)
        with self.voiceover(text="Here are the most common dictionary methods: get, update, copy, pop, popitem, clear, keys, and values.") as tracker:
            self.play(LaggedStart(*[GrowFromCenter(c) for c in chips], lag_ratio=0.08), run_time=min(tracker.duration * 0.8, 1.4))
            self.track(chips)
            self.wait(0.3)

        self.play(FadeOut(chips), run_time=0.4)
        self.section_mobjects.remove(chips)

        code = [
            (0, 'player = {"name": "Zara", "level": 13}'),
            (0, 'player.update({"score": 410, "level": 14})'),
            (0, "print(player)"),
            (0, "backup = player.copy()"),
            (0, "print(backup)"),
            (0, "print(list(player.keys()))"),
            (0, "print(list(player.values()))"),
        ]
        outputs = [
            None, None, "{'name': 'Zara', 'level': 14, 'score': 410}",
            None, "{'name': 'Zara', 'level': 14, 'score': 410}",
            "['name', 'level', 'score']", "['Zara', 14, 410]",
        ]
        voice_lines = [
            "We start with a simple player dictionary.",
            "Update lets us add a new key and update an existing one in one go.",
            "Print it – both changes applied.",
            "Copy creates a shallow copy.",
            "Print the copy – identical.",
            "Keys returns a view of all keys; we convert it to a list.",
            "And values gives us the list of all values."
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

    # ==================================================================== key-value --
    def section_keyvalue(self):
        sub, row, cells = self.start_dict_block_section(
            "Dictionary Key-Value Pairs", [("book", "Dune"), ("author", "Herbert")]
        )

        desc = self.build_desc("Every entry is one unit: a key bound to its value")
        desc.next_to(row, DOWN, buff=0.4)
        self.play(FadeIn(desc), run_time=0.4)
        self.track(desc)

        with self.voiceover(text="Now, each entry is a single unit – a key and its corresponding value. They always come together.") as tracker:
            self.flash_dict_cell(cells, 0, "key", NEON_MAGENTA)
            note1 = Text('"book" is the key', font_size=16, color=NEON_MAGENTA)
            note1.next_to(desc, DOWN, buff=0.35)
            self.play(FadeIn(note1), run_time=0.4)
            self.track(note1)
            self.wait(0.3)

        with self.voiceover(text="The value is the data associated with that key, like 'Dune' for the book key.") as tracker:
            self.flash_dict_cell(cells, 0, "value", NEON_CYAN)
            note2 = Text('"Dune" is the value stored under it', font_size=16, color=NEON_CYAN)
            note2.next_to(note1, DOWN, buff=0.25)
            self.play(FadeIn(note2), run_time=0.4)
            self.track(note2)
            self.wait(0.5)

    # ==================================================================== unique keys --
    def section_unique_keys(self):
        sub, row, cells = self.start_dict_block_section("Unique Keys", [("volume", 5)])

        code = [
            (0, "settings = {}"),
            (0, 'settings["volume"] = 5'),
            (0, 'settings["volume"] = 9'),
            (0, "print(settings)"),
        ]
        outputs = [None, None, None, "{'volume': 9}"]
        voice_lines = [
            "We begin with an empty dictionary.",
            "We add a key 'volume' with value 5.",
            "Now we assign again to the same key with value 9.",
            "Print it – the old value is gone and replaced."
        ]

        panel, code_lines, code_numbers = self.build_code_panel(code, t2c=T2C, filename="unique_keys_demo.py")
        panel.to_edge(LEFT, buff=0.5)
        self.set_top_y(panel, row.get_bottom()[1] - 0.35)
        self.setup_code_geometry(code_lines, code_numbers)
        self.play(FadeIn(panel, shift=RIGHT * 0.2), run_time=0.6)
        self.track(panel)

        terminal = self.build_terminal(height=3.4)
        terminal.to_edge(RIGHT, buff=0.6)
        self.set_top_y(terminal, row.get_bottom()[1] - 0.35)
        self.play(FadeIn(terminal, shift=RIGHT * 0.2), run_time=0.5)
        self.track(terminal)
        self.setup_terminal_geometry(terminal)

        with self.voiceover(text=voice_lines[0]) as tracker:
            self.highlight_line(0)
        with self.voiceover(text=voice_lines[1]) as tracker:
            self.highlight_line(1)
        note = Text("Same key assigned again — no duplicate entry is made,", font_size=16, color=MUTED)
        note2 = Text("the old value is simply overwritten.", font_size=16, color=MUTED)
        note_group = VGroup(note, note2).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        note_group.next_to(terminal, DOWN, buff=0.25)
        if note_group.width > terminal.width + 1:
            note_group.scale((terminal.width + 1) / note_group.width)
        with self.voiceover(text="Remember, keys must be unique. If you reuse a key, the new value overwrites the old one.") as tracker:
            self.play(FadeIn(note_group), run_time=0.4)
            self.track(note_group)

        with self.voiceover(text=voice_lines[2]) as tracker:
            self.highlight_line(2)
            self.flash_dict_cell(cells, 0, "value", NEON_YELLOW)
            row, cells = self.swap_dict_row(row, [("volume", 9)])
        with self.voiceover(text=voice_lines[3]) as tracker:
            self.highlight_line(3)
            self.print_output(outputs[3])
        self.wait(0.3)

    # ==================================================================== nested --
    def section_nested(self):
        sub = self.track(self.build_subtitle("Nested Dictionaries"))
        desc = self.build_desc("A value inside a dictionary can be another dictionary")
        desc.next_to(sub, DOWN, buff=0.3)
        self.play(FadeIn(desc), run_time=0.4)
        self.track(desc)

        outer_cell = self.build_dict_cell("grades", "{...}", cell_w=2.4)
        outer_cell.next_to(desc, DOWN, buff=0.5)
        with self.voiceover(text="Now for something cool – a dictionary can hold another dictionary as its value.") as tracker:
            self.play(GrowFromCenter(outer_cell), run_time=0.6)
            self.track(outer_cell)

        inner_row, inner_cells = self.build_dict_row([("math", 92), ("art", 88)], cell_w=1.9)
        inner_row.next_to(outer_cell, DOWN, buff=0.6)
        arrow = Arrow(outer_cell.get_bottom(), inner_row.get_top(), buff=0.1,
                      color=NEON_MAGENTA, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        self.play(Create(arrow), run_time=0.4)
        with self.voiceover(text="Here, the key 'grades' points to another dictionary containing subject scores.") as tracker:
            self.play(LaggedStart(*[GrowFromCenter(c) for c in inner_cells], lag_ratio=0.15), run_time=min(tracker.duration * 0.8, 1.2))
            self.track(VGroup(arrow, inner_row))
            self.wait(0.3)

        code = [
            (0, 'student = {"name": "Zara", "grades": {"math": 92, "art": 88}}'),
            (0, 'print(student["grades"])'),
            (0, 'print(student["grades"]["math"])'),
        ]
        outputs = [None, "{'math': 92, 'art': 88}", "92"]
        voice_lines = [
            "We define a nested dictionary.",
            "Access the inner dictionary by its key.",
            "And then we can chain brackets to get a specific value inside."
        ]

        panel, code_lines, code_numbers = self.build_code_panel(code, t2c=T2C, filename="nested_demo.py")
        panel.to_edge(LEFT, buff=0.5)
        self.set_top_y(panel, inner_row.get_bottom()[1] - 0.4)
        self.setup_code_geometry(code_lines, code_numbers)
        self.play(FadeIn(panel, shift=RIGHT * 0.2), run_time=0.6)
        self.track(panel)

        terminal = self.build_terminal(height=2.8)
        terminal.to_edge(RIGHT, buff=0.6)
        self.set_top_y(terminal, inner_row.get_bottom()[1] - 0.4)
        self.play(FadeIn(terminal, shift=RIGHT * 0.2), run_time=0.5)
        self.track(terminal)
        self.setup_terminal_geometry(terminal)

        for i in range(len(code)):
            with self.voiceover(text=voice_lines[i]) as tracker:
                self.highlight_line(i)
                if i == 2:
                    self.flash_dict_cell(inner_cells, 0, "both", NEON_YELLOW)
                if outputs[i] is not None:
                    self.print_output(outputs[i])
        self.wait(0.3)

    # -------------------------------------------------------- shared code runner --
    def run_simple_code_section(self, subtitle_text, desc_text, code, outputs, filename, voice_lines):
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
            voice_text = voice_lines[i] if i < len(voice_lines) else ""
            with self.voiceover(text=voice_text) as tracker:
                self.highlight_line(i)
                if outputs[i] is not None:
                    self.print_output(outputs[i])
        self.wait(0.3)

    # ==================================================================== outro --
    def section_outro(self):
        with self.voiceover(text="That's all for today, friends! I hope you enjoyed this journey into Python dictionaries. If you found it helpful, please like, share, and subscribe. See you in the next lesson!") as tracker:
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