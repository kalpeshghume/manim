from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class PythonInterpreterE2EVisual(MovingCameraScene, VoiceoverScene):
    def construct(self):
        # ============================================================
        # GLOBAL SETTINGS
        # ============================================================
        SHOW_COORDINATE_GRID = False
        SHOW_OUTRO = True

        TITLE_SIZE = 50
        SUBTITLE_SIZE = 23
        SECTION_SIZE = 34
        CARD_TITLE = 18
        CARD_BODY = 12
        CODE_SCALE = 0.65

        SPEED_FAST = 0.35
        SPEED_MED = 0.70
        SPEED_SLOW = 1.10

        # ============================================================
        # SETUP
        # ============================================================
        self.set_speech_service(GTTSService(lang="en"))
        self.camera.frame.save_state()

        NEON_BLUE = "#00E5FF"
        NEON_GREEN = "#39FF14"
        NEON_RED = "#FF1744"
        NEON_YELLOW = "#FFF700"
        NEON_ORANGE = "#FF9100"
        NEON_PURPLE = "#D500F9"
        NEON_PINK = "#FF00CC"
        DARK = "#101014"
        CARD_DARK = "#080B12"

        # ============================================================
        # HELPERS
        # ============================================================
        def voice(text, animation_function=None):
            with self.voiceover(text=text) as tracker:
                if animation_function is not None:
                    animation_function(tracker)

        def safe_camera_fit(mobject, margin=1.10, run_time=0.8):
            width_needed = mobject.width * margin
            height_needed = mobject.height * margin
            width_from_height = height_needed * 16 / 9
            final_width = max(width_needed, width_from_height, 11.5)
            self.play(
                self.camera.frame.animate.set_width(final_width).move_to(mobject.get_center()),
                run_time=run_time,
            )

        def add_coordinate_grid():
            grid = VGroup()
            for x in range(-8, 9):
                line = Line([x, -4.5, 0], [x, 4.5, 0], color=GRAY, stroke_width=1).set_opacity(0.2)
                label = Text(str(x), font_size=14, color=GRAY).set_opacity(0.2)
                label.move_to([x, -4.25, 0])
                grid.add(line, label)
            for y in range(-4, 5):
                line = Line([-8, y, 0], [8, y, 0], color=GRAY, stroke_width=1).set_opacity(0.2)
                label = Text(str(y), font_size=14, color=GRAY).set_opacity(0.2)
                label.move_to([-7.75, y, 0])
                grid.add(line, label)
            x_axis = Line([-8, 0, 0], [8, 0, 0], color=NEON_BLUE, stroke_width=2).set_opacity(0.25)
            y_axis = Line([0, -4.5, 0], [0, 4.5, 0], color=NEON_BLUE, stroke_width=2).set_opacity(0.25)
            grid.add(x_axis, y_axis)
            grid.set_z_index(-20)
            self.add(grid)

        if SHOW_COORDINATE_GRID:
            add_coordinate_grid()

        def section_heading(text, color=NEON_YELLOW):
            return Text(text, font_size=SECTION_SIZE, color=color).to_edge(UP, buff=0.35)

        def card(title, body, color, width=2.50, height=1.08, title_size=CARD_TITLE, body_size=CARD_BODY):
            box = RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.18,
                color=color,
                stroke_width=3,
                fill_color=CARD_DARK,
                fill_opacity=0.94,
            )
            title_text = Text(title, font_size=title_size, color=color)
            body_text = Text(body, font_size=body_size, color=WHITE)
            content = VGroup(title_text, body_text).arrange(DOWN, buff=0.12)
            content.move_to(box.get_center())
            return VGroup(box, content)

        def make_code(raw_code, scale_value=CODE_SCALE):
            return Code(
                code_string=raw_code.strip(),
                tab_width=4,
                background="rectangle",
                background_config={
                    "fill_opacity": 0.95,
                    "color": DARK,
                    "stroke_color": NEON_BLUE,
                    "stroke_width": 2,
                },
                language="Python",
                formatter_style="monokai",
            ).scale(scale_value)

        def type_code(code_object, tracker, portion=0.62):
            line_count = len(code_object.code_lines)
            total_time = max(tracker.duration * portion, 1.8)
            line_time = max(total_time / (line_count + 1), 0.18)
            self.play(Create(code_object.background), run_time=line_time)
            for line in code_object.code_lines:
                self.play(Write(line), run_time=line_time)

        def chip(text, color, width=1.15):
            box = RoundedRectangle(
                width=width,
                height=0.45,
                corner_radius=0.12,
                color=color,
                stroke_width=2,
                fill_color=DARK,
                fill_opacity=0.95,
            )
            label = Text(text, font_size=16, color=WHITE).move_to(box)
            return VGroup(box, label)

        def terminal(lines, width=5.3, height=1.50, color=NEON_GREEN):
            box = RoundedRectangle(width=width, height=height, corner_radius=0.14, color=color, stroke_width=3, fill_color=BLACK, fill_opacity=0.95)
            title = Text("Terminal Output", font_size=16, color=color).next_to(box, UP, buff=0.10, aligned_edge=LEFT)
            text_lines = VGroup(*[Text(line, font_size=17, color=WHITE) for line in lines])
            text_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
            text_lines.move_to(box.get_center()).shift(LEFT * 0.10)
            return VGroup(title, box, text_lines)

        def show_terminal(term, tracker, portion=0.35):
            self.play(FadeIn(term[0]), Create(term[1]), run_time=tracker.duration * 0.15)
            line_time = max((tracker.duration * portion) / max(len(term[2]), 1), 0.15)
            for line in term[2]:
                self.play(Write(line), run_time=line_time)

        def fade_items(*items):
            self.play(*[FadeOut(item) for item in items], run_time=SPEED_MED)

        def pulse(obj, color=NEON_YELLOW):
            self.play(Circumscribe(obj, color=color, time_width=0.55), run_time=SPEED_MED)

        def path_blink(arrow):
            dashed = DashedVMobject(arrow.copy(), num_dashes=18, color=NEON_YELLOW).set_stroke(width=5)
            self.play(Create(dashed), run_time=0.28)
            self.play(FadeOut(dashed), run_time=0.28)

        # ============================================================
        # 1. INTRO
        # ============================================================
        title = Text("How Python Interpreter Works", font_size=TITLE_SIZE, color=NEON_BLUE)
        subtitle = Text("Lexing -> Parsing -> Bytecode -> PVM -> Output", font_size=SUBTITLE_SIZE, color=GRAY_B)
        subtitle.next_to(title, DOWN, buff=0.30)

        def intro_anim(tracker):
            self.play(Write(title), run_time=tracker.duration * 0.55)
            self.play(FadeIn(subtitle, shift=UP * 0.20), run_time=tracker.duration * 0.25)

        voice(
            "In this lesson, we will understand how the Python interpreter works from source code to final terminal output.",
            intro_anim,
        )
        self.play(FadeOut(title, shift=UP * 0.35), FadeOut(subtitle, shift=UP * 0.20), run_time=SPEED_FAST)

        # ============================================================
        # 2. END TO END FLOW FIRST
        # ============================================================
        h1 = section_heading("End-to-End Flow")
        stages = VGroup(
            card("Python Code", ".py source", NEON_BLUE),
            card("Lexing", "code to tokens", NEON_GREEN),
            card("Parsing", "tokens to AST", NEON_PURPLE),
            card("Compile", "AST to bytecode", NEON_ORANGE),
            card("PVM", "execute bytecode", NEON_PINK),
            card("Output", "result or error", NEON_YELLOW),
        ).arrange(RIGHT, buff=0.30).move_to(UP * 0.60)

        arrows = VGroup()
        for i in range(len(stages) - 1):
            arrows.add(Arrow(stages[i].get_right(), stages[i + 1].get_left(), color=NEON_YELLOW, stroke_width=4, buff=0.10, max_tip_length_to_length_ratio=0.16))

        sample_code = make_code(
            """
result = 8 * 3 + 2
print(result)
""",
            scale_value=0.72,
        ).move_to(DOWN * 1.95 + LEFT * 2.55)
        sample_terminal = terminal(["26"], width=2.6, height=1.05, color=NEON_GREEN).move_to(DOWN * 1.95 + RIGHT * 3.65)
        e2e_group = VGroup(h1, stages, arrows, sample_code, sample_terminal)

        def e2e_anim(tracker):
            safe_camera_fit(e2e_group, margin=1.08, run_time=SPEED_MED)
            self.play(Write(h1), run_time=tracker.duration * 0.08)
            self.play(LaggedStart(*[GrowFromCenter(stage) for stage in stages], lag_ratio=0.08), run_time=tracker.duration * 0.42)
            self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.08), run_time=tracker.duration * 0.20)
            type_code(sample_code, tracker, portion=0.18)
            show_terminal(sample_terminal, tracker, portion=0.12)

        voice(
            "First, here is the whole journey. Python source code is broken into tokens, tokens are parsed into a syntax tree, the tree is compiled into bytecode, the Python virtual machine executes the bytecode, and the terminal shows output or errors.",
            e2e_anim,
        )

        def e2e_focus(tracker):
            for i in range(len(stages)):
                self.play(stages[i].animate.scale(1.07), rate_func=there_and_back, run_time=tracker.duration * 0.10)
                if i < len(arrows):
                    path_blink(arrows[i])

        voice(
            "Keep this flow in mind. Now we will zoom into each block one by one, without losing the big picture.",
            e2e_focus,
        )
        fade_items(e2e_group)

        # ============================================================
        # 3. LEXING / TOKENIZATION
        # ============================================================
        h2 = section_heading("Step 1: Lexing or Tokenization")
        code_lex = make_code("result = 8 * 3 + 2", scale_value=0.92).move_to(UP * 1.30)
        token_labels = ["result", "=", "8", "*", "3", "+", "2"]
        token_types = ["IDENTIFIER", "OPERATOR", "NUMBER", "OPERATOR", "NUMBER", "OPERATOR", "NUMBER"]
        token_colors = [NEON_BLUE, NEON_YELLOW, NEON_GREEN, NEON_YELLOW, NEON_GREEN, NEON_YELLOW, NEON_GREEN]
        tokens = VGroup()
        token_type_texts = VGroup()
        for label, kind, color in zip(token_labels, token_types, token_colors):
            width = max(0.72, 0.18 * len(label) + 0.55)
            c = chip(label, color, width=width)
            tokens.add(c)
            token_type_texts.add(Text(kind, font_size=11, color=color))
        tokens.arrange(RIGHT, buff=0.18).move_to(DOWN * 0.30)
        for t, c in zip(token_type_texts, tokens):
            t.next_to(c, DOWN, buff=0.08)
        token_group = VGroup(tokens, token_type_texts)
        lexer_box = card("Lexer", "scans characters\nand creates tokens", NEON_GREEN, width=3.35, height=1.15).move_to(DOWN * 2.20)
        lex_scene = VGroup(h2, code_lex, token_group, lexer_box)

        def lex_anim(tracker):
            safe_camera_fit(lex_scene, margin=1.10, run_time=SPEED_MED)
            self.play(Write(h2), run_time=tracker.duration * 0.08)
            type_code(code_lex, tracker, portion=0.22)
            self.play(GrowFromCenter(lexer_box), run_time=tracker.duration * 0.12)
            self.play(LaggedStart(*[FadeIn(tok, shift=DOWN * 0.15) for tok in tokens], lag_ratio=0.08), run_time=tracker.duration * 0.35)
            self.play(LaggedStart(*[Write(t) for t in token_type_texts], lag_ratio=0.08), run_time=tracker.duration * 0.18)

        voice(
            "Lexing is the first step. The lexer scans the characters in the code and turns them into meaningful tokens like identifiers, operators, and numbers.",
            lex_anim,
        )
        voice(
            "Here, result is an identifier, the equals sign and arithmetic symbols are operators, and eight, three, and two are number tokens.",
            lambda tracker: pulse(token_group, NEON_YELLOW),
        )
        fade_items(lex_scene)

        # ============================================================
        # 4. PARSING / AST
        # ============================================================
        h3 = section_heading("Step 2: Parsing into an AST")
        tokens_top = tokens.copy().arrange(RIGHT, buff=0.15).move_to(UP * 1.95)
        parser_box = card("Parser", "checks grammar\nbuilds syntax tree", NEON_PURPLE, width=3.25, height=1.15).move_to(LEFT * 4.35 + UP * 0.45)

        root = chip("Assign", NEON_PURPLE, width=1.28).move_to(UP * 0.55 + RIGHT * 0.80)
        target = chip("Name(result)", NEON_BLUE, width=1.95).move_to(LEFT * 1.00 + DOWN * 0.35)
        expr = chip("BinOp(+)", NEON_ORANGE, width=1.45).move_to(RIGHT * 2.25 + DOWN * 0.35)
        left_mul = chip("BinOp(*)", NEON_ORANGE, width=1.45).move_to(RIGHT * 1.10 + DOWN * 1.35)
        two_node = chip("2", NEON_GREEN, width=0.70).move_to(RIGHT * 3.35 + DOWN * 1.35)
        eight_node = chip("8", NEON_GREEN, width=0.70).move_to(RIGHT * 0.40 + DOWN * 2.25)
        three_node = chip("3", NEON_GREEN, width=0.70).move_to(RIGHT * 1.80 + DOWN * 2.25)
        ast_nodes = VGroup(root, target, expr, left_mul, two_node, eight_node, three_node)
        tree_edges = VGroup(
            Line(root.get_bottom(), target.get_top(), color=NEON_YELLOW, stroke_width=3),
            Line(root.get_bottom(), expr.get_top(), color=NEON_YELLOW, stroke_width=3),
            Line(expr.get_bottom(), left_mul.get_top(), color=NEON_YELLOW, stroke_width=3),
            Line(expr.get_bottom(), two_node.get_top(), color=NEON_YELLOW, stroke_width=3),
            Line(left_mul.get_bottom(), eight_node.get_top(), color=NEON_YELLOW, stroke_width=3),
            Line(left_mul.get_bottom(), three_node.get_top(), color=NEON_YELLOW, stroke_width=3),
        )
        parse_scene = VGroup(h3, tokens_top, parser_box, ast_nodes, tree_edges)

        def parse_anim(tracker):
            safe_camera_fit(parse_scene, margin=1.10, run_time=SPEED_MED)
            self.play(Write(h3), run_time=tracker.duration * 0.08)
            self.play(FadeIn(tokens_top, shift=DOWN * 0.10), GrowFromCenter(parser_box), run_time=tracker.duration * 0.22)
            self.play(LaggedStart(*[GrowFromCenter(n) for n in ast_nodes], lag_ratio=0.09), run_time=tracker.duration * 0.40)
            self.play(LaggedStart(*[Create(e) for e in tree_edges], lag_ratio=0.08), run_time=tracker.duration * 0.20)

        voice(
            "Parsing uses the token stream to check grammar and build an abstract syntax tree, or AST. The AST represents the structure of the program.",
            parse_anim,
        )
        voice(
            "In this tree, the assignment is the root. The target is result, and the value is an expression where multiplication is evaluated before addition.",
            lambda tracker: (pulse(root, NEON_PURPLE), pulse(expr, NEON_ORANGE), pulse(left_mul, NEON_ORANGE)),
        )
        fade_items(parse_scene)

        # ============================================================
        # 5. COMPILATION TO BYTECODE
        # ============================================================
        h4 = section_heading("Step 3: Compilation to Bytecode")
        ast_card = card("AST", "structured program", NEON_PURPLE, width=2.75, height=1.05).move_to(LEFT * 4.35 + UP * 0.70)
        compiler_card = card("Compiler", "AST to bytecode", NEON_ORANGE, width=2.75, height=1.05).move_to(LEFT * 1.45 + UP * 0.70)
        byte_panel = RoundedRectangle(width=4.20, height=2.55, corner_radius=0.15, color=NEON_GREEN, stroke_width=3, fill_color=DARK, fill_opacity=0.95).move_to(RIGHT * 2.90 + UP * 0.20)
        byte_title = Text("Bytecode Instructions", font_size=22, color=NEON_GREEN).next_to(byte_panel, UP, buff=0.12)
        byte_lines = VGroup(
            Text("LOAD_CONST 8", font_size=18, color=WHITE),
            Text("LOAD_CONST 3", font_size=18, color=WHITE),
            Text("BINARY_MULTIPLY", font_size=18, color=NEON_YELLOW),
            Text("LOAD_CONST 2", font_size=18, color=WHITE),
            Text("BINARY_ADD", font_size=18, color=NEON_YELLOW),
            Text("STORE_NAME result", font_size=18, color=NEON_BLUE),
            Text("CALL print", font_size=18, color=NEON_PURPLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10).move_to(byte_panel.get_center())
        arrow_ast_comp = Arrow(ast_card.get_right(), compiler_card.get_left(), color=NEON_YELLOW, stroke_width=4, buff=0.15)
        arrow_comp_byte = Arrow(compiler_card.get_right(), byte_panel.get_left(), color=NEON_YELLOW, stroke_width=4, buff=0.15)
        compile_scene = VGroup(h4, ast_card, compiler_card, byte_panel, byte_title, byte_lines, arrow_ast_comp, arrow_comp_byte)

        def compile_anim(tracker):
            safe_camera_fit(compile_scene, margin=1.10, run_time=SPEED_MED)
            self.play(Write(h4), run_time=tracker.duration * 0.08)
            self.play(GrowFromCenter(ast_card), GrowFromCenter(compiler_card), Create(arrow_ast_comp), run_time=tracker.duration * 0.22)
            self.play(Create(arrow_comp_byte), Create(byte_panel), Write(byte_title), run_time=tracker.duration * 0.20)
            self.play(LaggedStart(*[Write(line) for line in byte_lines], lag_ratio=0.08), run_time=tracker.duration * 0.42)

        voice(
            "Next, Python compiles the AST into bytecode. Bytecode is an intermediate instruction format that the Python virtual machine can execute.",
            compile_anim,
        )
        voice(
            "Bytecode is not normal Python text, and it is not the final machine code. It is a compact instruction list for the Python runtime.",
            lambda tracker: pulse(byte_panel, NEON_GREEN),
        )
        fade_items(compile_scene)

        # ============================================================
        # 6. PVM EXECUTION WITH STACK AND MEMORY
        # ============================================================
        h5 = section_heading("Step 4: PVM Execution with Stack and Memory")
        byte_panel2 = byte_panel.copy().scale(0.85).move_to(LEFT * 4.55 + UP * 0.15)
        byte_title2 = Text("Bytecode", font_size=22, color=NEON_GREEN).next_to(byte_panel2, UP, buff=0.12)
        byte_lines2 = byte_lines.copy().scale(0.85).move_to(byte_panel2.get_center())
        code_bytes = VGroup(byte_panel2, byte_title2, byte_lines2)

        stack_box = RoundedRectangle(width=2.00, height=3.20, corner_radius=0.15, color=NEON_PURPLE, stroke_width=3, fill_color=DARK, fill_opacity=0.95).move_to(ORIGIN + UP * 0.25)
        stack_title = Text("Stack", font_size=22, color=NEON_PURPLE).next_to(stack_box, UP, buff=0.12)
        stack_slots = VGroup()
        for i in range(4):
            slot = Rectangle(width=1.55, height=0.52, color=GRAY, stroke_width=1).set_opacity(0.55)
            stack_slots.add(slot)
        stack_slots.arrange(DOWN, buff=0.14).move_to(stack_box.get_center() + DOWN * 0.20)
        stack_group = VGroup(stack_box, stack_title, stack_slots)

        memory_box = RoundedRectangle(width=2.65, height=1.40, corner_radius=0.15, color=NEON_BLUE, stroke_width=3, fill_color=DARK, fill_opacity=0.95).move_to(RIGHT * 3.65 + UP * 1.05)
        memory_title = Text("Memory", font_size=22, color=NEON_BLUE).next_to(memory_box, UP, buff=0.12)
        memory_text = Text("result = ?", font_size=23, color=WHITE).move_to(memory_box)
        memory_group = VGroup(memory_box, memory_title, memory_text)

        term = terminal(["26"], width=2.75, height=1.10, color=NEON_GREEN).move_to(RIGHT * 3.65 + DOWN * 1.45)
        pvm_card = card("Python VM", "reads bytecode\nupdates stack memory", NEON_PINK, width=3.20, height=1.10).move_to(DOWN * 2.75)
        pvm_scene = VGroup(h5, code_bytes, stack_group, memory_group, term, pvm_card)

        def pvm_build(tracker):
            safe_camera_fit(pvm_scene, margin=1.10, run_time=SPEED_MED)
            self.play(Write(h5), run_time=tracker.duration * 0.08)
            self.play(FadeIn(code_bytes, shift=RIGHT * 0.10), GrowFromCenter(stack_group), GrowFromCenter(memory_group), GrowFromCenter(pvm_card), run_time=tracker.duration * 0.32)
            self.play(FadeIn(term[0]), Create(term[1]), run_time=tracker.duration * 0.12)

        voice(
            "The Python virtual machine now executes bytecode instructions. A stack is used to temporarily hold values, and memory stores named variables.",
            pvm_build,
        )

        stack_values = []
        def push_value(value, color=WHITE):
            text = Text(str(value), font_size=22, color=color)
            slot_index = len(stack_values)
            target_slot = stack_slots[-1 - slot_index]
            text.move_to(target_slot.get_center())
            stack_values.append(text)
            self.play(FadeIn(text, shift=UP * 0.15), run_time=SPEED_SLOW)
            return text

        def pop_value():
            text = stack_values.pop()
            self.play(FadeOut(text, shift=UP * 0.15), run_time=SPEED_SLOW)
            return text

        def highlight_instruction(index, color=NEON_YELLOW):
            rect = SurroundingRectangle(byte_lines2[index], color=color, buff=0.04)
            self.play(Create(rect), run_time=0.25)
            return rect

        def pvm_execute(tracker):
            # LOAD_CONST 8
            r = highlight_instruction(0)
            push_value(8, NEON_GREEN)
            self.play(FadeOut(r), run_time=0.15)
            # LOAD_CONST 3
            r = highlight_instruction(1)
            push_value(3, NEON_GREEN)
            self.play(FadeOut(r), run_time=0.15)
            # MULTIPLY
            r = highlight_instruction(2)
            pop_value()
            pop_value()
            push_value(24, NEON_YELLOW)
            self.play(FadeOut(r), run_time=0.15)
            # LOAD_CONST 2
            r = highlight_instruction(3)
            push_value(2, NEON_GREEN)
            self.play(FadeOut(r), run_time=0.15)
            # ADD
            r = highlight_instruction(4)
            pop_value()
            pop_value()
            push_value(26, NEON_YELLOW)
            self.play(FadeOut(r), run_time=0.15)
            # STORE_NAME result
            r = highlight_instruction(5, NEON_BLUE)
            top = pop_value()
            self.play(Transform(memory_text, Text("result = 26", font_size=23, color=NEON_GREEN).move_to(memory_box)), run_time=0.45)
            self.play(FadeOut(r), run_time=0.15)
            # CALL print
            r = highlight_instruction(6, NEON_PURPLE)
            self.play(Write(term[2][0]), run_time=0.45)
            self.play(FadeOut(r), run_time=0.15)
            pulse(term[1], NEON_GREEN)

        voice(
            "Now watch the stack carefully. The virtual machine loads eight, loads three, multiplies them into twenty four, loads two, adds it, stores twenty six in result, and finally prints the result.",
            pvm_execute,
        )
        fade_items(pvm_scene)

        # ============================================================
        # 7. INTERPRETER VS COMPILER
        # ============================================================
        h6 = section_heading("Interpreter vs Compiler")
        inter_title = Text("Python Interpreter", font_size=30, color=NEON_GREEN).move_to(LEFT * 3.55 + UP * 2.20)
        comp_title = Text("Traditional Compiler", font_size=30, color=NEON_ORANGE).move_to(RIGHT * 3.55 + UP * 2.20)
        divider = DashedLine(UP * 2.75, DOWN * 2.55, color=GRAY, stroke_width=2).set_opacity(0.60)

        inter_code = make_code("""
line 1 -> run
line 2 -> run
line 3 -> run
""", scale_value=0.65).move_to(LEFT * 3.55 + UP * 0.45)
        comp_code = make_code("""
check whole program
compile executable
then run
""", scale_value=0.65).move_to(RIGHT * 3.55 + UP * 0.45)
        inter_card = card("Line by Line", "runs step by step\neasier debugging", NEON_GREEN, width=3.35, height=1.05).move_to(LEFT * 3.55 + DOWN * 1.55)
        comp_card = card("Whole Program", "compile first\nthen execute", NEON_ORANGE, width=3.35, height=1.05).move_to(RIGHT * 3.55 + DOWN * 1.55)
        compare = VGroup(h6, inter_title, comp_title, divider, inter_code, comp_code, inter_card, comp_card)

        def compare_anim(tracker):
            safe_camera_fit(compare, margin=1.10, run_time=SPEED_MED)
            self.play(Write(h6), Create(divider), run_time=tracker.duration * 0.12)
            self.play(Write(inter_title), Write(comp_title), run_time=tracker.duration * 0.12)
            type_code(inter_code, tracker, portion=0.28)
            type_code(comp_code, tracker, portion=0.28)
            self.play(GrowFromCenter(inter_card), GrowFromCenter(comp_card), run_time=tracker.duration * 0.16)

        voice(
            "Compared with a traditional compiler, Python behaves like an interpreter. It can process and execute instructions step by step, while a compiler usually translates the full program before running.",
            compare_anim,
        )

        def compare_focus(tracker):
            pulse(inter_card[0], NEON_GREEN)
            pulse(comp_card[0], NEON_ORANGE)

        voice(
            "This line by line behavior helps beginners test quickly and debug easily, while compiled programs often run faster after compilation.",
            compare_focus,
        )
        fade_items(compare)

        # ============================================================
        # 8. SUMMARY
        # ============================================================
        h7 = Text("Quick Summary", font_size=42, color=NEON_BLUE).shift(UP * 1.75)
        s1 = Text("1. Lexing turns characters into tokens", font_size=28, color=NEON_GREEN)
        s2 = Text("2. Parsing turns tokens into an AST", font_size=28, color=NEON_PURPLE).next_to(s1, DOWN, buff=0.32)
        s3 = Text("3. Compilation turns AST into bytecode", font_size=28, color=NEON_ORANGE).next_to(s2, DOWN, buff=0.32)
        s4 = Text("4. PVM executes bytecode using stack and memory", font_size=28, color=NEON_PINK).next_to(s3, DOWN, buff=0.32)
        s5 = Text("5. Terminal shows output or error", font_size=28, color=NEON_YELLOW).next_to(s4, DOWN, buff=0.32)
        summary = VGroup(h7, s1, s2, s3, s4, s5).move_to(ORIGIN)

        def summary_anim(tracker):
            safe_camera_fit(summary, margin=1.12, run_time=SPEED_MED)
            self.play(Write(h7), run_time=tracker.duration * 0.15)
            for line in [s1, s2, s3, s4, s5]:
                self.play(Write(line), run_time=tracker.duration * 0.14)

        voice(
            "Let us summarize. Python code is tokenized by the lexer, parsed into an AST, compiled into bytecode, executed by the Python virtual machine using stack and memory, and finally displayed in the terminal.",
            summary_anim,
        )
        self.play(FadeOut(summary), run_time=SPEED_MED)

        # ============================================================
        # 9. OUTRO
        # ============================================================
        if SHOW_OUTRO:
            outro_title = Text("Thanks for Watching!", font_size=50, color=NEON_BLUE).shift(UP * 2.35)
            outro_subtitle = Text("Learn Python Visually", font_size=26, color=GRAY_B).next_to(outro_title, DOWN, buff=0.25)
            subscribe_box = RoundedRectangle(width=4.3, height=0.9, corner_radius=0.25, color=NEON_RED, fill_color=NEON_RED, fill_opacity=0.85, stroke_width=4)
            subscribe_text = Text("SUBSCRIBE", font_size=32, color=WHITE).move_to(subscribe_box)
            play_triangle = Triangle(color=WHITE, fill_color=WHITE, fill_opacity=1).scale(0.18)
            play_triangle.rotate(-PI / 2)
            play_triangle.next_to(subscribe_text, LEFT, buff=0.25)
            subscribe = VGroup(subscribe_box, play_triangle, subscribe_text).move_to(UP * 0.35)
            like = card("LIKE", "support the video", NEON_GREEN, width=2.7, height=1.15).move_to(LEFT * 2.9 + DOWN * 1.20)
            share = card("SHARE", "help others learn", NEON_PURPLE, width=2.7, height=1.15).move_to(RIGHT * 2.9 + DOWN * 1.20)
            final = Text("See you in the next animation!", font_size=30, color=NEON_BLUE).to_edge(DOWN, buff=0.35)

            def outro_one(tracker):
                self.play(Write(outro_title), FadeIn(outro_subtitle, shift=UP * 0.20), GrowFromCenter(subscribe), run_time=tracker.duration * 0.75)
                self.play(Circumscribe(subscribe, color=NEON_YELLOW, time_width=0.6), run_time=tracker.duration * 0.20)

            voice("Thanks for watching. Subscribe for more visual Python lessons.", outro_one)

            def outro_two(tracker):
                self.play(FadeIn(like, shift=RIGHT), FadeIn(share, shift=LEFT), run_time=tracker.duration * 0.40)
                self.play(like.animate.scale(1.08), share.animate.scale(1.08), rate_func=there_and_back, run_time=tracker.duration * 0.25)
                self.play(Write(final), run_time=tracker.duration * 0.25)

            voice("Like and share this video with your friends. See you in the next video.", outro_two)

        self.wait(2)
