"""
Python Data Types — Neon Light Theme, single scene, one category at a time
Manim Community v0.20.2
Voiceover uses manim_voiceover with Google Text‑to‑Speech (gTTS).

Install:
    pip install manim-voiceover gTTS

Render:
    manim -pql python_datatypes_neon.py DataTypesScene
    manim -pqh python_datatypes_neon.py DataTypesScene

Covers the 6 top-level Python data type categories, one at a time, each
with a runnable example on the left and a terminal-style "output" panel
on the right that fills in live as each print() line executes.
All animations are synchronised with detailed voiceover.
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
    "print": NEON_MAGENTA, "type": NEON_MAGENTA, "range": NEON_MAGENTA,
    "frozenset": NEON_MAGENTA, "True": NEON_YELLOW, "False": NEON_YELLOW,
}

# ------------------------------------------------------------- 6 categories --
SECTIONS = [
    {
        "subtitle": "1. Numeric Data Type",
        "description": "Classes: int, float, complex — for numbers",
        "filename": "numeric_demo.py",
        "code": [
            (0, "count = 15"),
            (0, "print(count, type(count))"),
            (0, "price = 4.5"),
            (0, "print(price, type(price))"),
            (0, "signal = 2 + 3j"),
            (0, "print(signal, type(signal))"),
        ],
        "outputs": [
            None, "15 <class 'int'>",
            None, "4.5 <class 'float'>",
            None, "(2+3j) <class 'complex'>",
        ],
        # Detailed voiceover for each line (including None lines)
        "voice_lines": [
            "Create a variable 'count' with the integer value 15.",
            "Print count and its type, showing it's an integer.",
            "Create 'price' with the float value 4.5.",
            "Print price and its type, showing it's a float.",
            "Create 'signal' with the complex number 2 plus 3j.",
            "Print signal and its type, showing it's a complex number.",
        ],
        "intro_voice": "Let's start with numeric data types. Python has three numeric types: integers, floats, and complex numbers.",
    },
    {
        "subtitle": "2. String Data Type",
        "description": "Class: str — a sequence of characters",
        "filename": "string_demo.py",
        "code": [
            (0, 'label = "Manim"'),
            (0, "print(label)"),
            (0, 'greeting = "Neon coding rocks"'),
            (0, "print(greeting)"),
        ],
        "outputs": [None, "Manim", None, "Neon coding rocks"],
        "voice_lines": [
            "Create a string variable 'label' with the value 'Manim'.",
            "Print the label.",
            "Create another string 'greeting' with a phrase.",
            "Print the greeting.",
        ],
        "intro_voice": "Now we look at strings, which are sequences of characters enclosed in quotes.",
    },
    {
        "subtitle": "3. Sequence Data Type",
        "description": "Classes: list, tuple, range — ordered collections",
        "filename": "sequence_demo.py",
        "code": [
            (0, 'colors = ["cyan", "magenta", "lime"]'),
            (0, "print(colors[0])"),
            (0, "print(colors[2])"),
            (0, 'point = ("origin", 0, 0)'),
            (0, "print(point[0])"),
            (0, "steps = range(3)"),
            (0, "print(list(steps))"),
        ],
        "outputs": [
            None, "cyan", "lime",
            None, "origin",
            None, "[0, 1, 2]",
        ],
        "voice_lines": [
            "Create a list 'colors' with three strings.",
            "Access and print the first element, which is 'cyan'.",
            "Access and print the third element, 'lime'.",
            "Create a tuple 'point' containing a string and two integers.",
            "Print the first element of the tuple, 'origin'.",
            "Create a range object from 0 to 2.",
            "Convert the range to a list and print it.",
        ],
        "intro_voice": "Sequences are ordered collections. Python has list, tuple, and range types.",
    },
    {
        "subtitle": "4. Mapping Data Type",
        "description": "Class: dict — key-value pairs",
        "filename": "mapping_demo.py",
        "code": [
            (0, 'city_temp = {"Delhi": 41, "Oslo": 5}'),
            (0, "print(city_temp)"),
            (0, 'print(city_temp["Oslo"])'),
        ],
        "outputs": [None, "{'Delhi': 41, 'Oslo': 5}", "5"],
        "voice_lines": [
            "Create a dictionary 'city_temp' with city names as keys and temperatures as values.",
            "Print the entire dictionary.",
            "Access and print the temperature for Oslo.",
        ],
        "intro_voice": "Dictionaries are mappings of key-value pairs. They are used to store data that can be looked up by a key.",
    },
    {
        "subtitle": "5. Boolean Data Type",
        "description": "Class: bool — True or False",
        "filename": "boolean_demo.py",
        "code": [
            (0, "is_ready = True"),
            (0, "print(is_ready, type(is_ready))"),
            (0, "print(5 > 3)"),
        ],
        "outputs": [None, "True <class 'bool'>", "True"],
        "voice_lines": [
            "Create a boolean variable 'is_ready' with value True.",
            "Print its value and type, confirming it's a boolean.",
            "Evaluate and print the expression 5 > 3, which returns True.",
        ],
        "intro_voice": "Booleans represent truth values: True or False. They are often the result of comparisons.",
    },
    {
        "subtitle": "6. Set Data Type",
        "description": "Classes: set, frozenset — unique, unordered items",
        "filename": "set_demo.py",
        "code": [
            (0, "ticket_ids = {203, 207, 201}"),
            (0, "print(ticket_ids)"),
            (0, "print(type(ticket_ids))"),
            (0, "locked_ids = frozenset(ticket_ids)"),
            (0, "print(type(locked_ids))"),
        ],
        "outputs": [
            None, "{201, 203, 207}", "<class 'set'>",
            None, "<class 'frozenset'>",
        ],
        "voice_lines": [
            "Create a set 'ticket_ids' with some integer values.",
            "Print the set (order may vary).",
            "Print its type, showing it's a set.",
            "Create a frozenset from the set, making it immutable.",
            "Print the type of the frozenset.",
        ],
        "intro_voice": "Sets store unique unordered items. Python also has frozenset, an immutable version.",
    },
]


class DataTypesScene(VoiceoverScene):
    def construct(self):
        # Set up voiceover service
        self.set_speech_service(GTTSService(lang="en"))

        self.camera.background_color = BG_COLOR
        self.section_mobjects = []
        self.main_title = self.build_main_title()

        for section in SECTIONS:
            self.run_data_type_section(**section)
            self.clear_section()

        self.closing()

    # ============================================================ shared --
    def track(self, mobj):
        self.section_mobjects.append(mobj)
        return mobj

    def clear_section(self):
        if self.section_mobjects:
            self.play(*[FadeOut(m) for m in self.section_mobjects], run_time=0.6)
            self.remove(*self.section_mobjects)
        self.section_mobjects = []

    def build_main_title(self):
        title = Text("Python Data Types", weight=BOLD, color=NEON_CYAN).scale(1.05)
        title.to_edge(UP, buff=0.5)
        underline = Underline(title, color=NEON_MAGENTA, buff=0.12)
        with self.voiceover(text="Welcome to this lesson on Python data types.") as tracker:
            self.play(Write(title), Create(underline), run_time=min(tracker.duration * 0.7, 1.0))
            self.wait(0.2)
        self.play(
            title.animate.scale(0.55).to_corner(UL, buff=0.35),
            FadeOut(underline),
            run_time=0.6,
        )
        return title

    def build_subtitle(self, text_str):
        sub = Text(text_str, font_size=28, color=NEON_MAGENTA, weight=BOLD)
        sub.to_edge(UP, buff=0.55)
        self.play(FadeIn(sub, shift=DOWN * 0.15), run_time=0.5)
        return sub

    def build_divider(self):
        divider = Line(UP * 3.2, DOWN * 3.2, stroke_color=NEON_CYAN, stroke_width=1.5)
        divider.set_opacity(0.25)
        return divider

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

    def highlight_line(self, idx, run_time=0.35):
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
    def build_terminal(self):
        width, height = 6.0, 4.4
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
        line = Text(text, font="Monospace", font_size=16, color=color)
        if line.width > self.output_max_w:
            line.scale(self.output_max_w / line.width)
        if self.output_lines:
            line.next_to(self.output_lines[-1], DOWN, buff=0.16, aligned_edge=LEFT)
        else:
            line.next_to(self.output_start, RIGHT, buff=0)
        self.output_lines.append(line)
        self.track(line)
        self.play(FadeIn(line, shift=RIGHT * 0.1), run_time=0.3)

    # ==================================================== per-category section --
    def run_data_type_section(self, subtitle, description, filename, code, outputs, voice_lines, intro_voice):
        # Intro voiceover for the category
        with self.voiceover(text=intro_voice) as tracker:
            sub = self.track(self.build_subtitle(subtitle))
            desc = Text(description, font_size=20, color=MUTED)
            max_w = 10.5
            if desc.width > max_w:
                desc.scale(max_w / desc.width)
            desc.next_to(sub, DOWN, buff=0.25)
            self.play(FadeIn(desc), run_time=0.4)
            self.track(desc)

        # Build divider, code panel, terminal (no voiceover for these)
        divider = self.build_divider()
        self.play(Create(divider), run_time=0.4)
        self.track(divider)

        code_panel, code_lines, code_numbers = self.build_code_panel(code, t2c=T2C, filename=filename)
        code_panel.to_edge(LEFT, buff=0.5)
        code_panel.align_to(desc, UP).shift(DOWN * 0.55)
        self.setup_code_geometry(code_lines, code_numbers)
        self.play(FadeIn(code_panel, shift=RIGHT * 0.2), run_time=0.6)
        self.track(code_panel)

        terminal = self.build_terminal()
        terminal.to_edge(RIGHT, buff=0.6)
        terminal.align_to(code_panel, UP)
        self.play(FadeIn(terminal, shift=RIGHT * 0.2), run_time=0.5)
        self.track(terminal)
        self.setup_terminal_geometry(terminal)

        # Now iterate through lines with voiceover for each
        for i in range(len(code)):
            # Voiceover for this line
            voice_text = voice_lines[i]
            with self.voiceover(text=voice_text) as tracker:
                # Highlight the line
                self.highlight_line(i)
                # If there is output, print it
                out = outputs[i]
                if out is not None:
                    # The voiceover already explains what the output is, but we can add a small pause
                    self.print_output(out)
                # The voiceover duration will control the pause; we don't need extra wait

        self.wait(0.8)

    # ------------------------------------------------------------- closing --
    def closing(self):
        closing_text = Text(
            "That covers Python's core data types!",
            weight=BOLD, color=NEON_GREEN,
        ).scale(0.9)
        closing_text.move_to(ORIGIN)
        with self.voiceover(text="That covers Python's core data types! You've learned about numbers, strings, sequences, mappings, booleans, and sets. Thanks for watching!") as tracker:
            self.play(Write(closing_text), run_time=min(tracker.duration * 0.7, 1.0))
            self.wait(1.5)
