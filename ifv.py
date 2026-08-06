"""
Python if Statements — Neon Light Theme, single scene, with voiceover.
Manim Community v0.20.2
Voiceover uses manim_voiceover with Google Text‑to‑Speech (gTTS).

Install:
    pip install manim-voiceover gTTS

Render:
    manim -pql python_if_statements_neon.py IfStatementsScene
    manim -pqh python_if_statements_neon.py IfStatementsScene

Voiceover synchronised with animations using tracker.duration.
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
    "if": NEON_CYAN, "else": NEON_CYAN,
    "print": NEON_MAGENTA, "True": NEON_YELLOW, "False": NEON_YELLOW,
}
# NOTE: "elif" is intentionally NOT a separate key here — "elif" contains
# "if" as a substring, and having both as t2c keys makes Manim's colorizer
# find two overlapping color rules for the same characters and raise
# "Ambiguous style" even though both rules specify the same color. The
# "if" key alone still colors the "if" portion inside every "elif".


class IfStatementsScene(VoiceoverScene):
    def construct(self):
        # Set up voiceover service
        self.set_speech_service(GTTSService(lang="en"))

        self.camera.background_color = BG_COLOR
        self.section_mobjects = []
        self.main_title = self.build_main_title()

        self.section_intro()
        self.clear_section()

        self.section_if()
        self.clear_section()

        self.section_if_else()
        self.clear_section()

        self.section_elif()
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

    def build_main_title(self):
        title = Text("Python if Statements", weight=BOLD, color=NEON_CYAN).scale(1.0)
        title.to_edge(UP, buff=0.5)
        underline = Underline(title, color=NEON_MAGENTA, buff=0.12)
        with self.voiceover(text="Welcome to this lesson on Python if statements.") as tracker:
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
            line.next_to(self.output_lines[-1], DOWN, buff=0.14, aligned_edge=LEFT)
        else:
            line.next_to(self.output_start, RIGHT, buff=0)
        self.output_lines.append(line)
        self.track(line)
        self.play(FadeIn(line, shift=RIGHT * 0.1), run_time=0.28)

    # ------------------------------------------------------- flowchart nodes --
    def make_terminal_node(self, label):
        box = Ellipse(width=1.8, height=0.6, stroke_color=NEON_CYAN, stroke_width=2.8,
                       fill_color=CARD_FILL, fill_opacity=1)
        text = Text(label, font_size=16, color=TEXT_WHITE, weight=BOLD)
        text.move_to(box.get_center())
        return VGroup(box, text)

    def make_process(self, label):
        box = RoundedRectangle(corner_radius=0.1, width=2.4, height=0.62,
                                stroke_color=NEON_MAGENTA, stroke_width=2.8,
                                fill_color=CARD_FILL, fill_opacity=1)
        text = Text(label, font_size=15, color=TEXT_WHITE)
        max_w = box.width - 0.25
        if text.width > max_w:
            text.scale(max_w / text.width)
        text.move_to(box.get_center())
        return VGroup(box, text)

    def make_decision(self, label):
        diamond = Polygon(UP * 0.52, RIGHT * 1.35, DOWN * 0.52, LEFT * 1.35,
                           stroke_color=NEON_YELLOW, stroke_width=2.8,
                           fill_color=CARD_FILL, fill_opacity=1)
        text = Text(label, font_size=14, color=TEXT_WHITE, weight=BOLD)
        max_w = 2.3
        if text.width > max_w:
            text.scale(max_w / text.width)
        text.move_to(diamond.get_center())
        return VGroup(diamond, text)

    def flow_arrow(self, start_pt, end_pt, color, label=None, label_offset=None):
        arrow = Arrow(start_pt, end_pt, buff=0.08, color=color, stroke_width=2.8,
                       max_tip_length_to_length_ratio=0.18)
        group = VGroup(arrow)
        if label:
            lbl = Text(label, font_size=15, color=color, weight=BOLD)
            offset = label_offset if label_offset is not None else UP * 0.25
            lbl.move_to(arrow.get_center() + offset)
            group.add(lbl)
        return group

    def clamp_flowchart(self, group, max_w=12.5, max_h=6.5):
        scale_factor = min(max_w / group.width, max_h / group.height, 1.0)
        if scale_factor < 1.0:
            group.scale(scale_factor)
        return group

    # ---------------------------------------------------- 4 flowchart builders --
    def build_if_flowchart(self):
        start = self.make_terminal_node("Start")
        decision = self.make_decision("speed > 80?")
        yes_box = self.make_process("print warning")
        done_box = self.make_process("print done")
        end = self.make_terminal_node("End")

        start.move_to(UP * 2.9)
        decision.move_to(UP * 1.8)
        yes_box.move_to(UP * 0.5 + LEFT * 2.8)
        done_box.move_to(DOWN * 0.7)
        end.move_to(DOWN * 1.9)

        arrows = VGroup(
            self.flow_arrow(start.get_bottom(), decision.get_top(), NEON_CYAN),
            self.flow_arrow(decision.get_left(), yes_box.get_top(), NEON_GREEN, "Yes", LEFT * 0.35),
            self.flow_arrow(decision.get_right(), done_box.get_right(), NEON_MAGENTA, "No", RIGHT * 0.35 + UP * 0.2),
            self.flow_arrow(yes_box.get_bottom(), done_box.get_top(), NEON_CYAN),
            self.flow_arrow(done_box.get_bottom(), end.get_top(), NEON_CYAN),
        )
        group = VGroup(start, decision, yes_box, done_box, end, arrows)
        self.clamp_flowchart(group)
        trace = [start, decision, yes_box, done_box, end]
        return group, trace

    def build_ifelse_flowchart(self):
        start = self.make_terminal_node("Start")
        decision = self.make_decision("age >= 18?")
        yes_box = self.make_process("Eligible to vote")
        no_box = self.make_process("Not yet eligible")
        end = self.make_terminal_node("End")

        start.move_to(UP * 2.6)
        decision.move_to(UP * 1.5)
        yes_box.move_to(UP * 0.1 + LEFT * 2.8)
        no_box.move_to(UP * 0.1 + RIGHT * 2.8)
        end.move_to(DOWN * 1.3)

        arrows = VGroup(
            self.flow_arrow(start.get_bottom(), decision.get_top(), NEON_CYAN),
            self.flow_arrow(decision.get_left(), yes_box.get_top(), NEON_GREEN, "Yes", LEFT * 0.35),
            self.flow_arrow(decision.get_right(), no_box.get_top(), NEON_MAGENTA, "No", RIGHT * 0.35),
            self.flow_arrow(yes_box.get_bottom(), end.get_left() + UP * 0.15, NEON_CYAN),
            self.flow_arrow(no_box.get_bottom(), end.get_right() + UP * 0.15, NEON_CYAN),
        )
        group = VGroup(start, decision, yes_box, no_box, end, arrows)
        self.clamp_flowchart(group)
        trace = [start, decision, no_box, end]
        return group, trace

    def build_elif_flowchart(self):
        start = self.make_terminal_node("Start")
        d1 = self.make_decision("temp > 30?")
        hot_box = self.make_process("Hot")
        d2 = self.make_decision("temp > 15?")
        mild_box = self.make_process("Mild")
        cold_box = self.make_process("Cold")
        end = self.make_terminal_node("End")

        start.move_to(UP * 3.3)
        d1.move_to(UP * 2.2)
        hot_box.move_to(UP * 2.2 + LEFT * 3.0)
        d2.move_to(UP * 0.8)
        mild_box.move_to(UP * 0.8 + LEFT * 3.0)
        cold_box.move_to(DOWN * 0.5)
        end.move_to(DOWN * 1.9)

        arrows = VGroup(
            self.flow_arrow(start.get_bottom(), d1.get_top(), NEON_CYAN),
            self.flow_arrow(d1.get_left(), hot_box.get_right(), NEON_GREEN, "Yes", UP * 0.28),
            self.flow_arrow(d1.get_bottom(), d2.get_top(), NEON_MAGENTA, "No", RIGHT * 0.4),
            self.flow_arrow(d2.get_left(), mild_box.get_right(), NEON_GREEN, "Yes", UP * 0.28),
            self.flow_arrow(d2.get_bottom(), cold_box.get_top(), NEON_MAGENTA, "No", RIGHT * 0.4),
            self.flow_arrow(hot_box.get_bottom(), end.get_left() + UP * 0.15, NEON_CYAN),
            self.flow_arrow(mild_box.get_bottom(), end.get_left() + UP * 0.05, NEON_CYAN),
            self.flow_arrow(cold_box.get_bottom(), end.get_top(), NEON_CYAN),
        )
        group = VGroup(start, d1, hot_box, d2, mild_box, cold_box, end, arrows)
        self.clamp_flowchart(group)
        trace = [start, d1, d2, cold_box, end]
        return group, trace

    def build_nested_flowchart(self):
        start = self.make_terminal_node("Start")
        d1 = self.make_decision("is_member?")
        d2 = self.make_decision("weight <= 5?")
        standard_box = self.make_process("Standard shipping")
        free_box = self.make_process("Free shipping")
        discount_box = self.make_process("Discounted shipping")
        end = self.make_terminal_node("End")

        start.move_to(UP * 3.3)
        d1.move_to(UP * 2.2)
        d2.move_to(UP * 0.9 + LEFT * 2.2)
        standard_box.move_to(UP * 0.9 + RIGHT * 3.0)
        free_box.move_to(DOWN * 0.5 + LEFT * 3.6)
        discount_box.move_to(DOWN * 0.5 + LEFT * 0.4)
        end.move_to(DOWN * 1.9)

        arrows = VGroup(
            self.flow_arrow(start.get_bottom(), d1.get_top(), NEON_CYAN),
            self.flow_arrow(d1.get_left(), d2.get_top(), NEON_GREEN, "Yes", LEFT * 0.35),
            self.flow_arrow(d1.get_right(), standard_box.get_top(), NEON_MAGENTA, "No", RIGHT * 0.35),
            self.flow_arrow(d2.get_left(), free_box.get_top(), NEON_GREEN, "Yes", LEFT * 0.35),
            self.flow_arrow(d2.get_right(), discount_box.get_top(), NEON_MAGENTA, "No", RIGHT * 0.35),
            self.flow_arrow(free_box.get_bottom(), end.get_left() + UP * 0.15, NEON_CYAN),
            self.flow_arrow(discount_box.get_bottom(), end.get_bottom() + DOWN * 0.15, NEON_CYAN),
            self.flow_arrow(standard_box.get_bottom(), end.get_right() + UP * 0.15, NEON_CYAN),
        )
        group = VGroup(start, d1, d2, standard_box, free_box, discount_box, end, arrows)
        self.clamp_flowchart(group)
        trace = [start, d1, d2, free_box, end]
        return group, trace

    # ==================================================================== intro --
    def section_intro(self):
        with self.voiceover(text=(
            "In programming, you often need to make decisions. "
            "Python's if statements allow your program to execute different blocks of code based on certain conditions. "
            "In this lesson, we'll cover four variations: the simple if, if-else, if-elif-else, and nested if statements."
        )) as tracker:
            subtitle = self.track(self.build_subtitle("Why Use if Statements?"))

            bullets = self.build_bullet_list([
                "An if statement lets your program make decisions.",
                "It runs a block of code only when a condition is True.",
                "Python offers a few variations for different needs:",
            ])
            bullets.next_to(subtitle, DOWN, buff=0.5)
            self.play(
                LaggedStart(*[FadeIn(row, shift=UP * 0.15) for row in bullets], lag_ratio=0.3),
                run_time=min(tracker.duration * 0.5, 1.8),
            )
            self.track(bullets)
            self.wait(0.4)

            chips = VGroup(*[self.make_chip(c) for c in ["if", "if...else", "if...elif...else", "Nested if"]])
            chips.arrange(RIGHT, buff=0.4)
            chips.next_to(bullets, DOWN, buff=0.6)
            max_w = 11.5
            if chips.width > max_w:
                chips.scale(max_w / chips.width)
            self.play(LaggedStart(*[GrowFromCenter(c) for c in chips], lag_ratio=0.15), run_time=min(tracker.duration * 0.4, 1.5))
            self.track(chips)
            self.wait(0.5)

    def make_chip(self, label):
        text = Text(label, font_size=18, color=TEXT_WHITE, weight=BOLD)
        box = RoundedRectangle(corner_radius=0.12, width=text.width + 0.5, height=0.65,
                                stroke_color=NEON_CYAN, stroke_width=2.5,
                                fill_color=CARD_FILL, fill_opacity=1)
        text.move_to(box.get_center())
        return VGroup(box, text)

# ================================================================= 1. if --
    def section_if(self):
        sub = self.track(self.build_subtitle("1. if Statement"))
        desc = self.build_desc("Runs a block only when the condition is True")
        desc.next_to(sub, DOWN, buff=0.25)
        self.play(FadeIn(desc), run_time=0.4)
        self.track(desc)

        flowchart, trace_nodes = self.build_if_flowchart()
        flowchart.next_to(desc, DOWN, buff=0.35)

        with self.voiceover(text=(
            "The simplest if statement has a condition and a block. "
            "If the condition is true, the block executes; if false, it's skipped. "
            "Here's a flowchart. We start, check if speed is greater than 80. "
            "For our example, speed is 82, so the condition is true, we take the yes path, "
            "print a warning, then continue to the end."
        )) as tracker:
            self.play(Create(flowchart), run_time=min(tracker.duration * 0.5, 1.8))
            self.track(flowchart)

            for node in trace_nodes:
                self.play(Indicate(node, color=NEON_GREEN, scale_factor=1.08), run_time=0.25)

            caption = self.build_caption("speed = 82  ->  condition True  ->  warning printed")
            caption.next_to(flowchart, DOWN, buff=0.3)
            self.play(FadeIn(caption), run_time=0.4)
            self.track(caption)
            self.wait(0.3)

        self.play(FadeOut(flowchart), FadeOut(caption), run_time=0.5)
        self.section_mobjects.remove(flowchart)
        self.section_mobjects.remove(caption)

        code = [
            (0, "speed = 82"),
            (0, "if speed > 80:"),
            (1, 'print("Warning: over the limit!")'),
            (0, 'print("Speed check complete.")'),
        ]
        outputs = [None, None, "Warning: over the limit!", "Speed check complete."]
        self.run_code_beat(
            desc, code, outputs, exec_order=[0, 1, 2, 3], skip=[],
            filename="if_demo.py",
            voice_text=(
                "Now let's see the Python code. We set speed to 82. "
                "The if statement checks the condition. Since it's true, the print inside runs, "
                "then the final print runs. The condition is false for other values, but here we see the true path."
            )
        )

    # ============================================================ 2. if-else --
    def section_if_else(self):
        sub = self.track(self.build_subtitle("2. if...else Statement"))
        desc = self.build_desc("Chooses between two alternatives")
        desc.next_to(sub, DOWN, buff=0.25)
        self.play(FadeIn(desc), run_time=0.4)
        self.track(desc)

        flowchart, trace_nodes = self.build_ifelse_flowchart()
        flowchart.next_to(desc, DOWN, buff=0.35)

        with self.voiceover(text=(
            "The if-else statement adds an alternative. If condition is true, one block runs; "
            "if false, the else block runs. Our example: age is 15, condition 'age >= 18' is false, "
            "so we take the no path and print 'Not yet eligible'."
        )) as tracker:
            self.play(Create(flowchart), run_time=min(tracker.duration * 0.5, 1.8))
            self.track(flowchart)

            for node in trace_nodes:
                self.play(Indicate(node, color=NEON_GREEN, scale_factor=1.08), run_time=0.25)

            caption = self.build_caption("age = 15  ->  condition False  ->  else branch runs")
            caption.next_to(flowchart, DOWN, buff=0.3)
            self.play(FadeIn(caption), run_time=0.4)
            self.track(caption)
            self.wait(0.3)

        self.play(FadeOut(flowchart), FadeOut(caption), run_time=0.5)
        self.section_mobjects.remove(flowchart)
        self.section_mobjects.remove(caption)

        code = [
            (0, "age = 15"),
            (0, "if age >= 18:"),
            (1, 'print("Eligible to vote")'),
            (0, "else:"),
            (1, 'print("Not yet eligible")'),
        ]
        outputs = [None, None, None, None, "Not yet eligible"]
        self.run_code_beat(
            desc, code, outputs, exec_order=[0, 1, 3, 4], skip=[2],
            filename="if_else_demo.py",
            voice_text=(
                "In code, we set age to 15. The if condition fails, so we skip the if block "
                "and go to the else block, printing the else message."
            )
        )

    # ========================================================== 3. elif --
    def section_elif(self):
        sub = self.track(self.build_subtitle("3. if...elif...else Statement"))
        desc = self.build_desc("Chooses between more than two alternatives")
        desc.next_to(sub, DOWN, buff=0.25)
        self.play(FadeIn(desc), run_time=0.4)
        self.track(desc)

        flowchart, trace_nodes = self.build_elif_flowchart()
        flowchart.next_to(desc, DOWN, buff=0.3)

        with self.voiceover(text=(
            "When you have multiple conditions, use if-elif-else. It checks each condition in order until one is true. "
            "Here temperature is 3. First check: temp > 30? false. Then elif temp > 15? also false. "
            "So we go to else and print 'Cold'."
        )) as tracker:
            self.play(Create(flowchart), run_time=min(tracker.duration * 0.5, 1.8))
            self.track(flowchart)

            for node in trace_nodes:
                self.play(Indicate(node, color=NEON_GREEN, scale_factor=1.08), run_time=0.25)

            caption = self.build_caption("temp = 3  ->  both conditions False  ->  else runs (Cold)")
            caption.next_to(flowchart, DOWN, buff=0.25)
            self.play(FadeIn(caption), run_time=0.4)
            self.track(caption)
            self.wait(0.3)

        self.play(FadeOut(flowchart), FadeOut(caption), run_time=0.5)
        self.section_mobjects.remove(flowchart)
        self.section_mobjects.remove(caption)

        code = [
            (0, "temp = 3"),
            (0, "if temp > 30:"),
            (1, 'print("Hot")'),
            (0, "elif temp > 15:"),
            (1, 'print("Mild")'),
            (0, "else:"),
            (1, 'print("Cold")'),
        ]
        outputs = [None, None, None, None, None, None, "Cold"]
        self.run_code_beat(
            desc, code, outputs, exec_order=[0, 1, 3, 5, 6], skip=[2, 4],
            filename="elif_demo.py",
            voice_text=(
                "We set temp to 3. The first if fails, the elif fails, so the else block executes, printing 'Cold'. "
                "The other branches are skipped, and you can see them dimmed."
            )
        )

    # ========================================================= 4. nested if --
    def section_nested(self):
        sub = self.track(self.build_subtitle("4. Nested if Statement"))
        desc = self.build_desc("An if statement inside another if statement")
        desc.next_to(sub, DOWN, buff=0.25)
        self.play(FadeIn(desc), run_time=0.4)
        self.track(desc)

        flowchart, trace_nodes = self.build_nested_flowchart()
        flowchart.next_to(desc, DOWN, buff=0.3)

        with self.voiceover(text=(
            "A nested if is an if inside another if. This allows more complex logic. "
            "Our example: is_member is True, so we go inside the outer if. "
            "Then we check weight <= 5, which is true, so we go to free shipping."
        )) as tracker:
            self.play(Create(flowchart), run_time=min(tracker.duration * 0.5, 1.8))
            self.track(flowchart)

            for node in trace_nodes:
                self.play(Indicate(node, color=NEON_GREEN, scale_factor=1.08), run_time=0.25)

            caption = self.build_caption("member=True, weight=4  ->  inner True  ->  Free shipping")
            caption.next_to(flowchart, DOWN, buff=0.25)
            self.play(FadeIn(caption), run_time=0.4)
            self.track(caption)
            self.wait(0.3)

        self.play(FadeOut(flowchart), FadeOut(caption), run_time=0.5)
        self.section_mobjects.remove(flowchart)
        self.section_mobjects.remove(caption)

        code = [
            (0, "is_member = True"),
            (0, "weight = 4"),
            (0, "if is_member:"),
            (1, "if weight <= 5:"),
            (2, 'print("Free shipping")'),
            (1, "else:"),
            (2, 'print("Discounted shipping")'),
            (0, "else:"),
            (1, 'print("Standard shipping")'),
        ]
        outputs = [None, None, None, None, "Free shipping", None, None, None, None]
        self.run_code_beat(
            desc, code, outputs,
            exec_order=[0, 1, 2, 3, 4], skip=[5, 6, 7, 8],
            filename="nested_if_demo.py",
            voice_text=(
                "We set is_member to True and weight to 4. The outer if passes, "
                "then the inner if passes, so we print 'Free shipping'. The other branches are skipped and dimmed."
            )
        )

    # -------------------------------------------------------- shared helpers --
    def build_desc(self, text_str):
        desc = Text(text_str, font_size=20, color=MUTED)
        max_w = 10.5
        if desc.width > max_w:
            desc.scale(max_w / desc.width)
        return desc

    def build_caption(self, text_str):
        cap = Text(text_str, font_size=18, color=NEON_GREEN)
        max_w = 11.0
        if cap.width > max_w:
            cap.scale(max_w / cap.width)
        return cap

    def run_code_beat(self, desc, code, outputs, exec_order, skip, filename, voice_text):
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

        # Voiceover for code explanation
        with self.voiceover(text=voice_text) as tracker:
            # Highlight lines in exec_order and print outputs
            for i in exec_order:
                self.highlight_line(i)
                if outputs[i] is not None:
                    self.print_output(outputs[i])

            # Dim skipped lines
            skip_mobs = [self.code_lines[i] for i in skip] + [self.code_numbers[i] for i in skip]
            if skip_mobs:
                self.play(*[m.animate.set_opacity(0.3) for m in skip_mobs], run_time=0.4)

            self.wait(0.3)

    # ==================================================================== outro --
    def section_outro(self):
        with self.voiceover(text=(
            "Thanks for watching! If you enjoyed this lesson, please like, share, and subscribe "
            "for more visual Python tutorials."
        )) as tracker:
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
