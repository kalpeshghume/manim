"""
Python Variables — Full Lesson, Neon Light Theme, single scene with voiceover.
Manim Community v0.20.2
Voiceover uses manim_voiceover with Google Text‑to‑Speech (gTTS).

Install:
    pip install manim-voiceover gTTS

Render:
    manim -pql pv_full_course.py PythonVariablesFullScene
    manim -pqh pv_full_course.py PythonVariablesFullScene

One continuous Scene, topics in this order, screen cleared gracefully
between every single one:
    1. What is a Variable?
    2. Variables & Memory        (name/arrow/object reference diagram)
    3. Variable Declaration      (Python has no separate declare step)
    4. Variable Assignment       (single & multiple)
    5. Variable Reassignment     (same name, new value/type)
    6. Naming Conventions        (valid vs invalid)
    7. Deleting Variables        (del + the NameError it causes)
    8. Outro                    (thanks for watching + like/subscribe/share)

All animations are synchronised with voiceover using tracker.duration.
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
GC_RED = "#ff3860"
TEXT_WHITE = "#f4f4ff"
MUTED = "#7a7a9c"
CODE_MUTED = "#9d9dc9"

# --------------------------------------------------------- code, IDE-style --
GUTTER_W = 0.55
INDENT_W = 0.34
LINE_H = 0.40
CODE_FS = 20
WATCH_ROW_H = 0.42

RIGHT_CENTER_X = 3.55

CODE_LINES_MEMORY = [
    (0, "score = 7"),
    (0, "total = score"),
    (0, "score = 9"),
    (0, "total = 12"),
]
CODE_LINES_ASSIGN = [
    (0, "grade = 88"),
    (0, "score1 = score2 = 250"),
    (0, 'x, y = 3, "Coder"'),
]
CODE_LINES_REASSIGN = [
    (0, "temperature = 72"),
    (0, 'temperature = "hot"'),
]
CODE_LINES_DELETE = [
    (0, "count = 42"),
    (0, "del count"),
    (0, "print(count)"),
]


class PythonVariablesFullScene(VoiceoverScene):
    def construct(self):
        # Set up voiceover service
        self.set_speech_service(GTTSService(lang="en"))

        self.camera.background_color = BG_COLOR
        self.section_mobjects = []
        self.main_title = self.build_main_title()

        self.section_what_is()
        self.clear_section()

        self.section_memory()
        self.clear_section()

        self.section_declaration()
        self.clear_section()

        self.section_assignment()
        self.clear_section()

        self.section_reassignment()
        self.clear_section()

        self.section_naming()
        self.clear_section()

        self.section_delete()
        self.clear_section()

        self.section_outro()

    # ============================================================ shared --
    def track(self, mobj):
        self.section_mobjects.append(mobj)
        return mobj

    def clear_section(self):
        present = [m for m in self.section_mobjects if m in self.mobjects]
        if present:
            self.play(*[FadeOut(m) for m in present], run_time=0.6)
        self.section_mobjects = []

    def build_main_title(self):
        title = Text("Python Variables", weight=BOLD, color=NEON_CYAN).scale(1.15)
        title.to_edge(UP, buff=0.5)
        underline = Underline(title, color=NEON_MAGENTA, buff=0.12)
        with self.voiceover(text="Welcome to this full lesson on Python variables.") as tracker:
            self.play(Write(title), Create(underline), run_time=min(tracker.duration * 0.7, 1.0))
            self.wait(0.2)
        self.play(
            title.animate.scale(0.5).to_corner(UL, buff=0.35),
            FadeOut(underline),
            run_time=0.6,
        )
        return title

    def build_subtitle(self, text_str):
        sub = Text(text_str, font_size=28, color=NEON_MAGENTA, weight=BOLD)
        sub.to_edge(UP, buff=0.55)
        self.play(FadeIn(sub, shift=DOWN * 0.15), run_time=0.5)
        return sub

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

    def build_divider(self):
        divider = Line(UP * 3.2, DOWN * 3.2, stroke_color=NEON_CYAN, stroke_width=1.5)
        divider.set_opacity(0.25)
        return divider

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

        max_w, max_h = 6.3, 6.2
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

    def set_status(self, msg, color=TEXT_WHITE):
        new_text = Text(msg, font_size=22, color=color)
        max_w = 6.3
        if new_text.width > max_w:
            new_text.scale(max_w / new_text.width)
        new_text.move_to(self.status_text)
        self.play(Transform(self.status_text, new_text), run_time=0.3)

    def start_code_section(self, subtitle_text, code_lines, filename, legend_rows):
        """Common setup shared by every code+watch-table topic: subtitle,
        legend, divider, code panel, and a blank status caption."""
        subtitle = self.track(self.build_subtitle(subtitle_text))

        legend = self.build_legend(legend_rows)
        legend.to_corner(UR, buff=0.35)
        self.play(FadeIn(legend, shift=DOWN * 0.2), run_time=0.5)
        self.track(legend)

        divider = self.build_divider()
        self.play(Create(divider), run_time=0.4)
        self.track(divider)

        code_panel, code_lines_m, code_numbers = self.build_code_panel(code_lines, filename=filename)
        code_panel.to_edge(LEFT, buff=0.5)
        code_panel.align_to(subtitle, UP).shift(DOWN * 0.7)
        self.setup_code_geometry(code_lines_m, code_numbers)
        self.play(FadeIn(code_panel, shift=RIGHT * 0.2), run_time=0.6)
        self.track(code_panel)

        self.watch_top_y = legend.get_bottom()[1] - 0.35
        return subtitle

    def start_watch_table(self, num_data_rows):
        self.watch_rows = {}
        self.watch_row_index = {}
        self.watch_row_count = 0

        watch_title = Text("Live Variables", font_size=20, color=NEON_CYAN, weight=BOLD)
        watch_title.next_to(self.watch_point(0.0, 0), RIGHT, buff=0)
        col_name = Text("name", font_size=14, color=CODE_MUTED, weight=BOLD)
        col_value = Text("value", font_size=14, color=CODE_MUTED, weight=BOLD)
        col_type = Text("type", font_size=14, color=CODE_MUTED, weight=BOLD)
        col_name.next_to(self.watch_point(0.0, 1), RIGHT, buff=0)
        col_value.next_to(self.watch_point(1.7, 1), RIGHT, buff=0)
        col_type.next_to(self.watch_point(4.3, 1), RIGHT, buff=0)
        header_group = VGroup(watch_title, col_name, col_value, col_type)
        self.play(FadeIn(header_group), run_time=0.4)
        self.track(header_group)

        status_y = self.watch_top_y - (num_data_rows + 2) * WATCH_ROW_H - 0.5
        self.status_text = Text("", font_size=22, color=MUTED)
        self.status_text.move_to([RIGHT_CENTER_X, status_y, 0])
        self.add(self.status_text)
        self.track(self.status_text)

    def watch_point(self, local_x, slot):
        x = RIGHT_CENTER_X - 2.1 + local_x
        y = self.watch_top_y - slot * WATCH_ROW_H
        return [x, y, 0]

    def build_watch_row(self, name, value_str, type_str, row_index):
        slot = row_index + 2  # 0 = title, 1 = column headers
        name_txt = Text(name, font="Monospace", font_size=18, color=NEON_MAGENTA, weight=BOLD)
        value_txt = Text(value_str, font="Monospace", font_size=18, color=TEXT_WHITE)
        type_txt = Text(type_str, font="Monospace", font_size=14, color=MUTED)
        name_txt.next_to(self.watch_point(0.0, slot), RIGHT, buff=0)
        value_txt.next_to(self.watch_point(1.7, slot), RIGHT, buff=0)
        type_txt.next_to(self.watch_point(4.3, slot), RIGHT, buff=0)
        return VGroup(name_txt, value_txt, type_txt)

    def set_watch(self, name, value_str, type_str):
        if name in self.watch_rows:
            old_row = self.watch_rows[name]
            new_row = self.build_watch_row(name, value_str, type_str, self.watch_row_index[name])
            self.play(
                Transform(old_row, new_row),
                Indicate(old_row, color=NEON_YELLOW, scale_factor=1.05),
                run_time=0.4,
            )
        else:
            idx = self.watch_row_count
            self.watch_row_index[name] = idx
            self.watch_row_count += 1
            row = self.build_watch_row(name, value_str, type_str, idx)
            self.watch_rows[name] = row
            self.track(row)
            self.play(FadeIn(row, shift=LEFT * 0.15), run_time=0.3)
            self.play(Indicate(row, color=NEON_GREEN, scale_factor=1.05), run_time=0.3)

    def remove_watch(self, name):
        row = self.watch_rows.pop(name, None)
        if row is None:
            return
        x_mark = Text("\u2717", color=GC_RED, font_size=20, weight=BOLD)
        x_mark.next_to(row, RIGHT, buff=0.15)
        self.play(row.animate.set_color(GC_RED), FadeIn(x_mark), run_time=0.35)
        self.play(FadeOut(row), FadeOut(x_mark), run_time=0.4)

    # =================================================== 1. WHAT IS A VARIABLE --
    def section_what_is(self):
        subtitle = self.track(self.build_subtitle("1. What is a Variable?"))

        bullets = self.build_bullet_list([
            "A variable is a name you give to a piece of data.",
            "It lets your program store, label, and reuse values.",
            "Think of it as a label attached to a value in memory.",
        ])
        bullets.next_to(subtitle, DOWN, buff=0.6)

        with self.voiceover(text="A variable is a name you give to a piece of data. It lets your program store, label, and reuse values. Think of it as a label attached to a value in memory.") as tracker:
            self.play(
                LaggedStart(*[FadeIn(row, shift=UP * 0.15) for row in bullets], lag_ratio=0.3),
                run_time=min(tracker.duration * 0.7, 1.8),
            )
            self.track(bullets)
            self.wait(0.5)

        example = self.build_mini_example("message", '"Hello"')
        example.next_to(bullets, DOWN, buff=0.7)
        with self.voiceover(text="For example, we can create a variable called message that points to the string Hello.") as tracker:
            self.play(FadeIn(example, shift=UP * 0.1), run_time=min(tracker.duration * 0.6, 0.8))
            self.track(example)
            self.wait(0.8)

    def build_mini_example(self, name, value_str):
        card = RoundedRectangle(corner_radius=0.12, width=2.1, height=0.8,
                                 stroke_color=NEON_GREEN, stroke_width=3.5,
                                 fill_color=CARD_FILL, fill_opacity=1)
        card_label = Text(value_str, font_size=22, color=TEXT_WHITE, weight=BOLD)
        card_label.move_to(card.get_center())
        card_group = VGroup(card, card_label).move_to(DOWN * 0.55)

        tag = RoundedRectangle(corner_radius=0.08, width=1.7, height=0.5,
                                stroke_color=NEON_MAGENTA, stroke_width=3,
                                fill_color=CARD_FILL, fill_opacity=1)
        tag_label = Text(name, font_size=20, color=TEXT_WHITE, weight=BOLD)
        tag_label.move_to(tag.get_center())
        tag_group = VGroup(tag, tag_label).move_to(UP * 0.55)

        arrow = Arrow(
            tag_group.get_bottom(), card_group.get_top(), buff=0.1,
            color=NEON_MAGENTA, stroke_width=3, max_tip_length_to_length_ratio=0.25,
        )
        return VGroup(tag_group, arrow, card_group)

    # =================================================== 2. VARIABLES & MEMORY --
    def section_memory(self):
        subtitle = self.track(self.build_subtitle("2. Variables & Memory"))

        legend = self.build_legend([
            (NEON_GREEN, "Object in memory"),
            (NEON_MAGENTA, "Variable reference"),
            (GC_RED, "Garbage collected"),
        ])
        legend.to_corner(UR, buff=0.35)
        self.play(FadeIn(legend, shift=DOWN * 0.2), run_time=0.5)
        self.track(legend)

        self.names_y = legend.get_bottom()[1] - 0.5
        self.objects_y = self.names_y - 2.3
        self.slot_x = [RIGHT_CENTER_X - 1.8, RIGHT_CENTER_X, RIGHT_CENTER_X + 1.8]
        self.name_x = [RIGHT_CENTER_X - 0.9, RIGHT_CENTER_X + 0.9]

        divider = self.build_divider()
        self.play(Create(divider), run_time=0.4)
        self.track(divider)

        code_panel, code_lines, code_numbers = self.build_code_panel(
            CODE_LINES_MEMORY, filename="memory_demo.py"
        )
        code_panel.to_edge(LEFT, buff=0.5)
        code_panel.align_to(subtitle, UP).shift(DOWN * 0.7)
        self.setup_code_geometry(code_lines, code_numbers)
        self.play(FadeIn(code_panel, shift=RIGHT * 0.2), run_time=0.6)
        self.track(code_panel)

        note = Text(
            "A variable is a name that references an object\nin memory "
            "\u2014 it does not store the value itself.",
            font_size=19, color=MUTED,
        )
        note.next_to(code_panel, DOWN, buff=0.5).align_to(code_panel, LEFT)
        self.play(FadeIn(note), run_time=0.5)
        self.track(note)

        self.status_text = Text("", font_size=22, color=MUTED)
        self.status_text.move_to([RIGHT_CENTER_X, self.objects_y - 1.1, 0])
        self.add(self.status_text)
        self.track(self.status_text)

        self.run_memory_demo()
        self.wait(1.0)

    def make_object_card(self, value_str, x):
        box = RoundedRectangle(
            corner_radius=0.12, width=1.3, height=0.8,
            stroke_color=NEON_GREEN, stroke_width=3.5,
            fill_color=CARD_FILL, fill_opacity=1,
        )
        box.move_to([x, self.objects_y, 0])
        label = Text(value_str, font_size=24, color=TEXT_WHITE, weight=BOLD)
        label.move_to(box.get_center())
        return VGroup(box, label)

    def make_name_tag(self, name, x):
        box = RoundedRectangle(
            corner_radius=0.08, width=1.3, height=0.5,
            stroke_color=NEON_MAGENTA, stroke_width=3,
            fill_color=CARD_FILL, fill_opacity=1,
        )
        box.move_to([x, self.names_y, 0])
        label = Text(name, font_size=20, color=TEXT_WHITE, weight=BOLD)
        label.move_to(box.get_center())
        return VGroup(box, label)

    def make_arrow(self, tag, obj):
        return Arrow(
            tag.get_bottom(), obj.get_top(), buff=0.12,
            color=NEON_MAGENTA, stroke_width=3,
            max_tip_length_to_length_ratio=0.2,
        )

    def run_memory_demo(self):
        self.highlight_line(0)
        object_7 = self.track(self.make_object_card("7", self.slot_x[0]))
        score_tag = self.track(self.make_name_tag("score", self.name_x[0]))
        with self.voiceover(text="First, we assign score equals 7. The variable score now references the integer object 7 in memory.") as tracker:
            self.set_status("score references the object 7")
            self.play(GrowFromCenter(object_7), run_time=min(tracker.duration * 0.3, 0.5))
            self.play(FadeIn(score_tag), run_time=0.3)
            arrow_score = self.track(self.make_arrow(score_tag, object_7))
            self.play(Create(arrow_score), run_time=0.35)

        self.highlight_line(1)
        total_tag = self.track(self.make_name_tag("total", self.name_x[1]))
        with self.voiceover(text="Next, we assign total equals score. This makes total reference the same object, not a copy. Both variables point to the same integer 7.") as tracker:
            self.set_status("total -> same object (shared reference)")
            self.play(FadeIn(total_tag), run_time=0.3)
            arrow_total = self.track(self.make_arrow(total_tag, object_7))
            self.play(
                Create(arrow_total),
                Indicate(object_7, color=NEON_YELLOW, scale_factor=1.1),
                run_time=0.4,
            )

        self.highlight_line(2)
        object_9 = self.track(self.make_object_card("9", self.slot_x[1]))
        with self.voiceover(text="Now we reassign score equals 9. Python creates a new integer object 9, and score now points to it. The old object 7 remains unchanged, and total still references it.") as tracker:
            self.set_status("score -> new object 9; total is unaffected")
            self.play(GrowFromCenter(object_9), run_time=0.35)
            new_arrow_score = self.make_arrow(score_tag, object_9)
            self.play(Transform(arrow_score, new_arrow_score), run_time=0.45)

        self.highlight_line(3)
        object_12 = self.track(self.make_object_card("12", self.slot_x[2]))
        with self.voiceover(text="Finally, we assign total equals 12. total now points to a new object 12. The object 7 no longer has any references, so Python's garbage collector will clean it up.") as tracker:
            self.set_status("total -> new object 12")
            self.play(GrowFromCenter(object_12), run_time=0.35)
            new_arrow_total = self.make_arrow(total_tag, object_12)
            self.play(Transform(arrow_total, new_arrow_total), run_time=0.45)

        gc_label = Text("no references left", font_size=15, color=GC_RED)
        gc_label.next_to(object_7, DOWN, buff=0.15)
        self.set_status("object 7 is now garbage collected")
        self.play(FadeIn(gc_label), run_time=0.3)
        self.play(FadeOut(object_7), FadeOut(gc_label), run_time=0.6)

    # =================================================== 3. VARIABLE DECLARATION --
    def section_declaration(self):
        subtitle = self.track(self.build_subtitle("3. Variable Declaration"))

        bullets = self.build_bullet_list([
            "Some languages need a separate declaration step first.",
            "Python has no such step — assigning a value both",
            "declares AND creates the variable, all in one line.",
        ])
        bullets.next_to(subtitle, DOWN, buff=0.6)
        with self.voiceover(text="In some programming languages, you must declare a variable before you can use it. Python is different: assigning a value both declares and creates the variable, all in one line.") as tracker:
            self.play(
                LaggedStart(*[FadeIn(row, shift=UP * 0.15) for row in bullets], lag_ratio=0.3),
                run_time=min(tracker.duration * 0.7, 1.8),
            )
            self.track(bullets)
            self.wait(0.5)

        comparison = VGroup(
            self.build_lang_card("Other languages", "int age;", MUTED, False),
            self.build_lang_card("Python", "age = 25", NEON_GREEN, True),
        )
        comparison.arrange(RIGHT, buff=1.0)
        comparison.next_to(bullets, DOWN, buff=0.7)
        with self.voiceover(text="For example, in other languages you'd write 'int age;' to declare, then assign separately. In Python, you just write 'age = 25' and the variable is created immediately.") as tracker:
            self.play(
                LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in comparison], lag_ratio=0.3),
                run_time=min(tracker.duration * 0.6, 1.2),
            )
            self.track(comparison)
            self.wait(0.8)

    def build_lang_card(self, header, code_str, color, valid):
        head = Text(header, font_size=18, color=color, weight=BOLD)
        code = Text(code_str, font="Monospace", font_size=20, color=TEXT_WHITE)
        mark = Text("declared" if valid else "not needed in Python", font_size=14, color=color)
        inner = VGroup(head, code, mark).arrange(DOWN, buff=0.18)
        box = SurroundingRectangle(inner, color=color, buff=0.28, stroke_width=2.5)
        box.set_fill(CARD_FILL, opacity=1)
        return VGroup(box, inner)

    # =================================================== 4. VARIABLE ASSIGNMENT --
    def section_assignment(self):
        self.start_code_section(
            "4. Variable Assignment",
            CODE_LINES_ASSIGN,
            "assign_demo.py",
            [(NEON_MAGENTA, "Variable name"), (NEON_GREEN, "New variable")],
        )
        self.start_watch_table(num_data_rows=4)
        self.run_assignment_demo()

    def run_assignment_demo(self):
        self.highlight_line(0)
        with self.voiceover(text="Single assignment: we assign grade equals 88. The variable grade is created and stores the integer 88.") as tracker:
            self.set_status("Single assignment: one name, one value")
            self.set_watch("grade", "88", "int")

        self.highlight_line(1)
        with self.voiceover(text="Multiple assignment: we assign both score1 and score2 to 250. Both variables reference the same integer object.") as tracker:
            self.set_status("Multiple assignment: both names, one value")
            self.set_watch("score1", "250", "int")
            self.set_watch("score2", "250", "int")

        self.highlight_line(2)
        with self.voiceover(text="Tuple unpacking: we assign x to 3 and y to the string 'Coder' in one line. Python matches the left and right sides.") as tracker:
            self.set_status("Multiple assignment: different values, one line")
            self.set_watch("x", "3", "int")
            self.set_watch("y", '"Coder"', "str")
            self.wait(0.6)

    # ================================================= 5. VARIABLE REASSIGNMENT --
    def section_reassignment(self):
        self.start_code_section(
            "5. Variable Reassignment",
            CODE_LINES_REASSIGN,
            "reassign_demo.py",
            [(NEON_MAGENTA, "Variable name"), (NEON_YELLOW, "Value changed")],
        )
        self.start_watch_table(num_data_rows=1)
        self.run_reassignment_demo()

    def run_reassignment_demo(self):
        self.highlight_line(0)
        with self.voiceover(text="First, temperature is assigned the integer 72. So the variable holds an integer.") as tracker:
            self.set_status("temperature holds an integer")
            self.set_watch("temperature", "72", "int")

        self.highlight_line(1)
        with self.voiceover(text="Now we reassign temperature to the string 'hot'. The same variable name now points to a completely different type. Python is dynamically typed, so this is allowed.") as tracker:
            self.set_status("Reassigned: same name, new value AND new type")
            self.set_watch("temperature", '"hot"', "str")
            self.wait(0.8)

    # =================================================== 6. NAMING CONVENTIONS --
    def section_naming(self):
        subtitle = self.track(self.build_subtitle("6. Naming Conventions"))

        panel = self.build_naming_panel()
        panel.next_to(subtitle, DOWN, buff=0.7)
        with self.voiceover(text="Python has rules for variable names. Let's see some valid and invalid examples. Valid names can contain letters, digits, and underscores, but they cannot start with a digit. Also, you cannot use reserved keywords like 'for', and hyphens are not allowed.") as tracker:
            self.play(
                LaggedStart(*[FadeIn(col, shift=UP * 0.15) for col in panel], lag_ratio=0.3),
                run_time=min(tracker.duration * 0.7, 1.8),
            )
            self.track(panel)
            self.wait(1.0)

        with self.voiceover(text="For instance, 'stage2', '_level', and 'max_speed' are all valid. But '2ndTry' is invalid because it starts with a digit, 'for' is a reserved keyword, and 'user-id' contains a hyphen which is not allowed.") as tracker:
            self.play(Indicate(panel, color=NEON_YELLOW), run_time=0.6)
            self.wait(0.5)

    def build_naming_panel(self):
        valid_header = Text("Valid names", color=NEON_GREEN, weight=BOLD, font_size=24)
        invalid_header = Text("Invalid names", color=NEON_MAGENTA, weight=BOLD, font_size=24)

        valid_items = VGroup(*[
            self._name_row(n, NEON_GREEN, "\u2713")
            for n in ["stage2", "_level", "max_speed"]
        ])
        valid_items.arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        invalid_items = VGroup(*[
            self._name_row(n, NEON_MAGENTA, "\u2717", reason)
            for n, reason in [
                ("2ndTry", "starts with a digit"),
                ("for", "reserved keyword"),
                ("user-id", "hyphens aren't allowed"),
            ]
        ])
        invalid_items.arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        valid_col = VGroup(valid_header, valid_items).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        invalid_col = VGroup(invalid_header, invalid_items).arrange(DOWN, aligned_edge=LEFT, buff=0.35)

        columns = VGroup(valid_col, invalid_col).arrange(RIGHT, buff=1.4, aligned_edge=UP)

        max_w = 11.5
        if columns.width > max_w:
            columns.scale(max_w / columns.width)
        return columns

    def _name_row(self, name, color, mark, reason=None):
        m = Text(mark, color=color, weight=BOLD, font_size=22)
        n = Text(name, font="Monospace", color=TEXT_WHITE, font_size=22)
        n.next_to(m, RIGHT, buff=0.25)
        row = VGroup(m, n)
        if reason:
            r = Text(f"({reason})", color=MUTED, font_size=15)
            r.next_to(n, RIGHT, buff=0.3)
            row.add(r)
        return row

    # =================================================== 7. DELETING VARIABLES --
    def section_delete(self):
        self.start_code_section(
            "7. Deleting Variables",
            CODE_LINES_DELETE,
            "delete_demo.py",
            [(NEON_MAGENTA, "Variable name"), (GC_RED, "Deleted")],
        )
        self.start_watch_table(num_data_rows=1)
        self.run_delete_demo()

    def run_delete_demo(self):
        self.highlight_line(0)
        with self.voiceover(text="First, we create the variable count with value 42. It appears in our live variables table.") as tracker:
            self.set_status("count is created and holds 42")
            self.set_watch("count", "42", "int")

        self.highlight_line(1)
        with self.voiceover(text="Now we use the 'del' statement to delete count. This removes the variable name from the namespace. The object may still exist if other references point to it, but this name is gone.") as tracker:
            self.set_status("del removes count's name binding", NEON_YELLOW)
            self.remove_watch("count")

        self.highlight_line(2)
        with self.voiceover(text="If we then try to use count, for example with print, we get a NameError because the name is no longer defined. This is a common error to remember.") as tracker:
            self.set_status("NameError: name 'count' is not defined", GC_RED)
            self.wait(0.8)

    # ==================================================================== outro --
    def section_outro(self):
        thanks = Text("Thanks for Watching!", weight=BOLD, color=NEON_CYAN).scale(1.15)
        thanks.move_to(UP * 1.3)
        self.play(Write(thanks), run_time=1.0)
        self.track(thanks)

        buttons = VGroup(
            self.make_outro_button("LIKE", NEON_MAGENTA),
            self.make_outro_button("SUBSCRIBE", NEON_YELLOW),
            self.make_outro_button("SHARE", NEON_GREEN),
        )
        buttons.arrange(RIGHT, buff=0.6)
        buttons.next_to(thanks, DOWN, buff=0.8)

        with self.voiceover(text="Thanks for watching! If you found this lesson helpful, please like, subscribe, and share this video with your friends. See you in the next lesson.") as tracker:
            self.play(
                LaggedStart(*[GrowFromCenter(b) for b in buttons], lag_ratio=0.25),
                run_time=min(tracker.duration * 0.6, 1.2),
            )
            self.play(*[Indicate(b, scale_factor=1.1, color=NEON_CYAN) for b in buttons], run_time=0.6)
            self.track(buttons)
            self.wait(1.0)

    def make_outro_button(self, label, color):
        box = RoundedRectangle(corner_radius=0.15, width=2.7, height=0.8,
                                stroke_color=color, stroke_width=3,
                                fill_color=CARD_FILL, fill_opacity=1)
        text = Text(label, font_size=22, color=color, weight=BOLD)
        text.move_to(box.get_center())
        return VGroup(box, text)
