"""
Python Operators — Neon Light Theme, single scene, one category at a time
Manim Community v0.20.2
Voiceover uses manim_voiceover with Google Text‑to‑Speech (gTTS).

Install:
    pip install manim-voiceover gTTS

Render:
    manim -pql python_operators_neon.py OperatorsScene
    manim -pqh python_operators_neon.py OperatorsScene

Structure:
    Intro   — what an operator/operand is, plus a preview of every
              category covered (as requested, before diving into any of them)
    1. Arithmetic Operators
    2. Relational Operators
    3. Logical Operators
    4. Bitwise Operators
    5. Assignment Operators
    6. Ternary Operator
    7. Identity Operators
    Outro   — thanks for watching + like / share / subscribe

Each operator category gets a code panel (IDE-style gutter + real
indentation) on the left and a neon terminal panel on the right that
fills in with real print() output as each line highlights — same
"example + output" pairing used in the data types video. Screen clears
gracefully between every section. Voiceover is synchronised using
tracker.duration.
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
    "print": NEON_MAGENTA,
    "and": NEON_CYAN, "or": NEON_CYAN, "not": NEON_CYAN,
    "is": NEON_CYAN, "if": NEON_CYAN, "else": NEON_CYAN,
    "True": NEON_YELLOW, "False": NEON_YELLOW,
}

CATEGORY_NAMES = [
    "Arithmetic", "Relational", "Logical", "Bitwise",
    "Assignment", "Ternary", "Identity",
]

# Voiceover texts for each line and intro for each section
SECTIONS = [
    {
        "subtitle": "1. Arithmetic Operators",
        "description": "Basic math: +  -  *  /  //  %  **",
        "filename": "arithmetic_demo.py",
        "code": [
            (0, "x = 18"),
            (0, "y = 5"),
            (0, 'print("Add:", x + y)'),
            (0, 'print("Sub:", x - y)'),
            (0, 'print("Mul:", x * y)'),
            (0, 'print("Div:", x / y)'),
            (0, 'print("FloorDiv:", x // y)'),
            (0, 'print("Mod:", x % y)'),
            (0, 'print("Power:", x ** y)'),
        ],
        "outputs": [
            None, None,
            "Add: 23", "Sub: 13", "Mul: 90", "Div: 3.6",
            "FloorDiv: 3", "Mod: 3", "Power: 1889568",
        ],
        "intro_voice": "Arithmetic operators perform mathematical operations. Let's see addition, subtraction, multiplication, division, floor division, modulus, and exponentiation.",
        "voice_lines": [
            "Assign x = 18.",
            "Assign y = 5.",
            "Print the sum of x and y.",
            "Print the difference.",
            "Print the product.",
            "Print the quotient as a float.",
            "Print floor division, which gives the integer part of the quotient.",
            "Print the remainder (modulus).",
            "Print x raised to the power of y.",
        ],
    },
    {
        "subtitle": "2. Relational Operators",
        "description": "Compare two values: >  <  ==  !=  >=  <=",
        "filename": "relational_demo.py",
        "code": [
            (0, "p = 21"),
            (0, "q = 9"),
            (0, "print(p > q)"),
            (0, "print(p < q)"),
            (0, "print(p == q)"),
            (0, "print(p != q)"),
            (0, "print(p >= q)"),
            (0, "print(p <= q)"),
        ],
        "outputs": [None, None, "True", "False", "False", "True", "True", "False"],
        "intro_voice": "Relational operators compare two values and return a boolean. We'll check greater than, less than, equality, inequality, greater than or equal, and less than or equal.",
        "voice_lines": [
            "Assign p = 21.",
            "Assign q = 9.",
            "Print whether p is greater than q. This is True.",
            "Print whether p is less than q, which is False.",
            "Print if p equals q, False.",
            "Print if p is not equal to q, True.",
            "Print if p is greater than or equal to q, True.",
            "Print if p is less than or equal to q, False.",
        ],
    },
    {
        "subtitle": "3. Logical Operators",
        "description": "Combine conditions: and  or  not",
        "filename": "logical_demo.py",
        "code": [
            (0, "ready = True"),
            (0, "done = False"),
            (0, "print(ready and done)"),
            (0, "print(ready or done)"),
            (0, "print(not ready)"),
        ],
        "outputs": [None, None, "False", "True", "False"],
        "intro_voice": "Logical operators let you combine boolean conditions. We have 'and', 'or', and 'not'.",
        "voice_lines": [
            "Set 'ready' to True.",
            "Set 'done' to False.",
            "'ready and done' is False because both must be True.",
            "'ready or done' is True because at least one is True.",
            "'not ready' flips the value, so it becomes False.",
        ],
    },
    {
        "subtitle": "4. Bitwise Operators",
        "description": "Operate on bits: &  |  ~  ^  >>  <<",
        "filename": "bitwise_demo.py",
        "code": [
            (0, "m = 12"),
            (0, "n = 5"),
            (0, "print(m & n)"),
            (0, "print(m | n)"),
            (0, "print(~m)"),
            (0, "print(m ^ n)"),
            (0, "print(m >> 1)"),
            (0, "print(m << 1)"),
        ],
        "outputs": [None, None, "4", "13", "-13", "9", "6", "24"],
        "intro_voice": "Bitwise operators work at the bit level. We have AND, OR, NOT, XOR, right shift, and left shift.",
        "voice_lines": [
            "Assign m = 12.",
            "Assign n = 5.",
            "Print bitwise AND of 12 and 5. Result is 4.",
            "Print bitwise OR, result 13.",
            "Print bitwise NOT of 12, gives -13.",
            "Print bitwise XOR, result 9.",
            "Print right shift by 1, which divides by 2: 6.",
            "Print left shift by 1, which multiplies by 2: 24.",
        ],
    },
    {
        "subtitle": "5. Assignment Operators",
        "description": "Assign & update: =  +=  -=  *=  <<=",
        "filename": "assignment_demo.py",
        "code": [
            (0, "base = 8"),
            (0, "total = base"),
            (0, "print(total)"),
            (0, "total += base"),
            (0, "print(total)"),
            (0, "total -= base"),
            (0, "print(total)"),
            (0, "total *= base"),
            (0, "print(total)"),
            (0, "total <<= base"),
            (0, "print(total)"),
        ],
        "outputs": [
            None, None, "8", None, "16", None, "8", None, "64", None, "16384",
        ],
        "intro_voice": "Assignment operators not only assign but also perform an operation. We'll see =, +=, -=, *=, and <<=.",
        "voice_lines": [
            "Set base = 8.",
            "Set total = base, so total is 8.",
            "Print total: 8.",
            "total += base adds 8 to total, making 16.",
            "Print total: 16.",
            "total -= base subtracts 8, back to 8.",
            "Print total: 8.",
            "total *= base multiplies by 8, getting 64.",
            "Print total: 64.",
            "total <<= base left shifts by 8 bits (multiply by 256), giving 16384.",
            "Print total: 16384.",
        ],
    },
    {
        "subtitle": "6. Ternary Operator",
        "description": "One line: value_if_true if condition else value_if_false",
        "filename": "ternary_demo.py",
        "code": [
            (0, "p, q = 14, 9"),
            (0, "smaller = p if p < q else q"),
            (0, "print(smaller)"),
        ],
        "outputs": [None, None, "9"],
        "intro_voice": "The ternary operator is a concise way to assign one of two values based on a condition.",
        "voice_lines": [
            "Assign p=14 and q=9.",
            "If p is less than q, take p, else take q. Since 14 < 9 is false, smaller becomes 9.",
            "Print smaller: 9.",
        ],
    },
    {
        "subtitle": "7. Identity Operators",
        "description": "Same object in memory: is  is not",
        "filename": "identity_demo.py",
        "code": [
            (0, "j = 17"),
            (0, "k = 29"),
            (0, "m = j"),
            (0, "print(j is not k)"),
            (0, "print(j is m)"),
        ],
        "outputs": [None, None, None, "True", "True"],
        "intro_voice": "Identity operators check if two variables reference the same object in memory. We have 'is' and 'is not'.",
        "voice_lines": [
            "Assign j = 17.",
            "Assign k = 29.",
            "Assign m = j, so m references the same object as j.",
            "j is not k is True because they are different objects.",
            "j is m is True because both point to the same object.",
        ],
    },
]


class OperatorsScene(VoiceoverScene):
    def construct(self):
        # Set up voiceover service
        self.set_speech_service(GTTSService(lang="en"))

        self.camera.background_color = BG_COLOR
        self.section_mobjects = []
        self.main_title = self.build_main_title()

        self.section_intro()
        self.clear_section()

        for section in SECTIONS:
            self.run_operator_section(**section)
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

    def build_main_title(self):
        title = Text("Python Operators", weight=BOLD, color=NEON_CYAN).scale(1.1)
        title.to_edge(UP, buff=0.5)
        underline = Underline(title, color=NEON_MAGENTA, buff=0.12)
        with self.voiceover(text="Welcome to this lesson on Python operators.") as tracker:
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

    def build_bullet_list(self, lines, color=NEON_MAGENTA, font_size=22):
        rows = VGroup()
        for text_str in lines:
            dot = Dot(radius=0.06, color=color)
            txt = Text(text_str, font_size=font_size, color=TEXT_WHITE)
            dot.next_to(txt, LEFT, buff=0.25)
            rows.add(VGroup(dot, txt))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        max_w = 10.8
        if rows.width > max_w:
            rows.scale(max_w / rows.width)
        return rows

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

        max_w, max_h = 6.2, 6.0
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

    def highlight_line(self, idx, run_time=0.32):
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
        width, height = 6.0, 4.6
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
            line.next_to(self.output_lines[-1], DOWN, buff=0.14, aligned_edge=LEFT)
        else:
            line.next_to(self.output_start, RIGHT, buff=0)
        self.output_lines.append(line)
        self.track(line)
        self.play(FadeIn(line, shift=RIGHT * 0.1), run_time=0.28)

    # ==================================================================== intro --
    def section_intro(self):
        with self.voiceover(text="What are operators? Operators are special symbols that perform operations on values. The values an operator works on are called its operands. Python groups its operators into several categories.") as tracker:
            subtitle = self.track(self.build_subtitle("What Are Operators?"))
            bullets = self.build_bullet_list([
                "Operators are special symbols that perform operations on values.",
                "The values an operator works on are called its operands.",
                "Python groups its operators into several categories:",
            ])
            bullets.next_to(subtitle, DOWN, buff=0.5)
            self.play(
                LaggedStart(*[FadeIn(row, shift=UP * 0.15) for row in bullets], lag_ratio=0.3),
                run_time=min(tracker.duration * 0.6, 1.8),
            )
            self.track(bullets)
            self.wait(0.4)

        chips = VGroup(*[self.make_chip(name) for name in CATEGORY_NAMES])
        chips.arrange_in_grid(rows=2, cols=4, buff=0.35)
        chips.next_to(bullets, DOWN, buff=0.6)
        max_w = 11.5
        if chips.width > max_w:
            chips.scale(max_w / chips.width)
        with self.voiceover(text="We will cover Arithmetic, Relational, Logical, Bitwise, Assignment, Ternary, and Identity operators.") as tracker:
            self.play(LaggedStart(*[GrowFromCenter(c) for c in chips], lag_ratio=0.12), run_time=min(tracker.duration * 0.8, 1.8))
            self.track(chips)
            self.wait(0.5)

    def make_chip(self, label):
        box = RoundedRectangle(corner_radius=0.12, width=2.4, height=0.65,
                                stroke_color=NEON_CYAN, stroke_width=2.5,
                                fill_color=CARD_FILL, fill_opacity=1)
        text = Text(label, font_size=18, color=TEXT_WHITE, weight=BOLD)
        text.move_to(box.get_center())
        return VGroup(box, text)

    # ==================================================== per-category section --
    def run_operator_section(self, subtitle, description, filename, code, outputs, intro_voice, voice_lines):
        # Intro voice for this category
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

        # Ite through lines with voice
  # Iterate through lines with voiceover
        for i in range(len(code)):
            voice_text = voice_lines[i]
            with self.voiceover(text=voice_text) as tracker:
                self.highlight_line(i)
                out = outputs[i]
                if out is not None:
                    self.print_output(out)
                # The voiceover duration will control the pause; no extra wait

        self.wait(0.7)

    # ==================================================================== outro --
    def section_outro(self):
        with self.voiceover(text="Thanks for watching! If you found this helpful, please like, share, and subscribe for more visual Python lessons.") as tracker:
            thanks = Text("Thanks for Watching!", weight=BOLD, color=NEON_CYAN).scale(1.1)
            thanks.move_to(UP * 1.6)
            self.play(Write(thanks), run_time=min(tracker.duration * 0.4, 1.0))
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
                run_time=min(tracker.duration * 0.5, 1.2),
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
