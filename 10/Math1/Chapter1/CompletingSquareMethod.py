from manim import Text
from manim import MathTex
from manim import VGroup
from manim import Group
from manim import FadeIn
from manim import FadeOut
from manim import Write
from manim import Create
from manim import TransformFromCopy
from manim import SurroundingRectangle
from manim import UP
from manim import DOWN
from manim import LEFT
from manim import RIGHT

from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


# ============================================================
# GLOBAL SETTINGS
# ============================================================

TITLE_SIZE = 45
TEXT_SIZE = 30
SMALL_TEXT_SIZE = 30
MATH_SIZE = 40
SMALL_MATH_SIZE = 40
TINY_MATH_SIZE = 25

FAST = 0.45
NORMAL = 0.9
SLOW = 1.35

SMALL_BUFF = 0.18
MEDIUM_BUFF = 0.35
LARGE_BUFF = 0.65

NEON_PINK = "#FF00FF"
NEON_BLUE = "#00FFFF"
NEON_GREEN = "#39FF14"
NEON_YELLOW = "#FFFF00"
NEON_ORANGE = "#FF8800"
NEON_PURPLE = "#B026FF"
NEON_RED = "#FF3131"
WHITE_TEXT = "#F8F8FF"
BLACK_BG = "#050505"

SAFE_WIDTH = 12.3
SAFE_HEIGHT = 6.5
MIN_WAIT = 0.15


class CompletingSquareQuadraticLessonDetailed(VoiceoverScene):

    def construct(self):

        # ------------------------------------------------------------
        # Voiceover setup
        # ------------------------------------------------------------
        # gTTS requires internet while rendering.
        # If voiceover fails, comment the next line.
        self.set_speech_service(GTTSService(lang="en"))

        # Dark background for neon style
        self.camera.background_color = BLACK_BG

        # ============================================================
        # HELPER FUNCTIONS
        # ============================================================

        def fit_to_screen(mob):
            # Keep content inside screen
            if mob.width > SAFE_WIDTH:
                mob.scale_to_fit_width(SAFE_WIDTH)
            if mob.height > SAFE_HEIGHT:
                mob.scale_to_fit_height(SAFE_HEIGHT)
            return mob

        def make_title(text):
            # Create a standard title at top
            title = Text(
                text,
                font_size=TITLE_SIZE,
                color=NEON_PINK
            )
            title.to_edge(UP)
            return title

        def neon_box(mob, color=NEON_YELLOW, buff=0.12):
            # Create neon highlight rectangle
            return SurroundingRectangle(
                mob,
                color=color,
                buff=buff,
                stroke_width=3
            )

        def blink_box(mob, color=NEON_YELLOW, times=2, buff=0.12):
            # Blink the highlight box to attract student attention
            for index in range(times):
                box = neon_box(mob, color=color, buff=buff)
                self.play(Create(box), run_time=FAST)
                self.play(FadeOut(box), run_time=FAST)

        def clear_scene():
            # Clear whole screen at once
            current_objects = list(self.mobjects)

            if len(current_objects) > 0:
                all_objects = Group()

                for mob in current_objects:
                    all_objects.add(mob)

                self.play(
                    FadeOut(all_objects),
                    run_time=FAST
                )

        def sync_wait(tracker, used_time):
            # Wait till voiceover finishes if animations end early
            remaining = tracker.duration - used_time

            if remaining > 0:
                self.wait(remaining + MIN_WAIT)
            else:
                self.wait(MIN_WAIT)

        # ============================================================
        # SCENE 1: OPENING TITLE
        # ============================================================

        title1 = Text(
                    "Solving quadratic equation",
                    font_size=TITLE_SIZE,
                    color=NEON_YELLOW
                )

        title = Text(
            "Completing the Square Method",
            font_size=TITLE_SIZE,
            color=NEON_PINK
        )
        title.next_to(title1, DOWN, buff=MEDIUM_BUFF)

        subtitle = Text(
            "Concept, formula, approach, and solved example",
            font_size=TEXT_SIZE,
            color=NEON_BLUE
        )
        subtitle.next_to(title, DOWN, buff=MEDIUM_BUFF)

        opening_group = VGroup(title1,title, subtitle)
        opening_group.move_to([0, 0, 0])

        with self.voiceover(
            text="Welcome. In this lesson, we will learn how to solve quadratic equations by completing the square."
        ) as tracker:
            self.play(Write(title1), run_time=NORMAL)
            self.play(Write(title), run_time=NORMAL)
            sync_wait(tracker, NORMAL)

        with self.voiceover(
            text="We will first understand the concept clearly, then see a small example, and finally solve a complete equation step by step."
        ) as tracker:
            self.play(FadeIn(subtitle, shift=UP), run_time=NORMAL)
            sync_wait(tracker, NORMAL)

        self.wait(0.1)
        clear_scene()

        # ============================================================
        # SCENE 2: WHY COMPLETING THE SQUARE IS NEEDED
        # ============================================================

        header = make_title("Why Completing the Square?")

        line1 = Text(
            "Some quadratic equations are not easy to factorize directly.",
            font_size=TEXT_SIZE,
            color=WHITE_TEXT
        )
        line1.next_to(header, DOWN, buff=MEDIUM_BUFF)

        equation = MathTex(
            r"x^2 + 10x + 2 = 0",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        )
        equation.next_to(line1, DOWN, buff=LARGE_BUFF)

        factor_note = Text(
            "Here, factors of 2 do not give sum 10.",
            font_size=TEXT_SIZE,
            color=NEON_RED
        )
        factor_note.next_to(equation, DOWN, buff=MEDIUM_BUFF)

        method_note = Text(
            "So we use another method: completing the square.",
            font_size=TEXT_SIZE,
            color=NEON_GREEN
        )
        method_note.next_to(factor_note, DOWN, buff=MEDIUM_BUFF)

        need_group = VGroup(header, line1, equation, factor_note, method_note)
        fit_to_screen(need_group)

        with self.voiceover(
            text="Some quadratic equations are not easy to factorize directly."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(FadeIn(line1), run_time=NORMAL)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="For example, consider x-squared plus ten-x plus two equals zero."
        ) as tracker:
            self.play(Write(equation), run_time=NORMAL)
            blink_box(equation, color=NEON_YELLOW, times=1)
            #sync_wait(tracker, 1.8)
            self.wait_for_voiceover()

        with self.voiceover(
            text="Here, it is not convenient to find factors of two whose sum is ten."
        ) as tracker:
            self.play(FadeIn(factor_note), run_time=NORMAL)
            blink_box(factor_note, color=NEON_RED, times=1)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="So we use another method called completing the square."
        ) as tracker:
            self.play(FadeIn(method_note), run_time=NORMAL)
            blink_box(method_note, color=NEON_GREEN, times=1)
            sync_wait(tracker, 1.8)

        self.wait(0.1)
        clear_scene()

        # ============================================================
        # SCENE 3: FORMULA USED
        # ============================================================

        header = make_title("Formula Used")

        formula_plus = MathTex(
            r"(a + b)^2 = a^2 + 2ab + b^2",
            font_size=MATH_SIZE,
            color=NEON_GREEN
        )
        formula_plus.next_to(header, DOWN, buff=LARGE_BUFF)

        formula_minus = MathTex(
            r"(a - b)^2 = a^2 - 2ab + b^2",
            font_size=MATH_SIZE,
            color=NEON_ORANGE
        )
        formula_minus.next_to(formula_plus, DOWN, buff=MEDIUM_BUFF)

        explanation = Text(
            "A perfect square trinomial has three parts:",
            font_size=TEXT_SIZE,
            color=WHITE_TEXT
        )
        explanation.next_to(formula_minus, DOWN, buff=LARGE_BUFF)

        parts = MathTex(
            r"a^2,\quad 2ab,\quad b^2",
            font_size=MATH_SIZE,
            color=NEON_BLUE
        )
        parts.next_to(explanation, DOWN, buff=MEDIUM_BUFF)

        formula_group = VGroup(header, formula_plus, formula_minus, explanation, parts)
        fit_to_screen(formula_group)

        with self.voiceover(
            text="The main identity used in completing the square is a-plus-b whole square equals a-squared plus two ab plus b-squared."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(formula_plus), run_time=NORMAL)
            blink_box(formula_plus, color=NEON_GREEN, times=1)
            sync_wait(tracker, 2.2)

        with self.voiceover(
            text="If the sign is negative, then a-minus-b whole square equals a-squared minus two ab plus b_squared."
        ) as tracker:
            self.play(Write(formula_minus), run_time=NORMAL)
            blink_box(formula_minus, color=NEON_ORANGE, times=1)
            sync_wait(tracker, 2.2)

        with self.voiceover(
            text="So a perfect square trinomial has three parts: first square, middle term, and last square."
        ) as tracker:
            self.play(FadeIn(explanation), run_time=NORMAL)
            self.play(Write(parts), run_time=NORMAL)
            blink_box(parts, color=NEON_BLUE, times=1)
            sync_wait(tracker, 2.2)

        self.wait(0.1)
        clear_scene()

        # ============================================================
        # SCENE 4: FULL EQUATION CONCEPT
        # ============================================================

        header = make_title("How Completing the Square Works")

        full_equation = MathTex(
            r"x^2 + bx + c = 0",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        )
        full_equation.next_to(header, DOWN, buff=MEDIUM_BUFF)

        move_c = MathTex(
            r"x^2 + bx = -c",
            font_size=MATH_SIZE,
            color=WHITE_TEXT
        )
        move_c.next_to(full_equation, DOWN, buff=MEDIUM_BUFF)

        focus_note = Text(
            "Now we focus on ledt hand equation.",
            font_size=TEXT_SIZE,
            color=NEON_BLUE
        )
        focus_note.next_to(move_c, DOWN, buff=MEDIUM_BUFF)

        reason_note = Text(
            "These two terms will become part of a perfect square.",
            font_size=SMALL_TEXT_SIZE,
            color=WHITE_TEXT
        )
        reason_note.next_to(focus_note, DOWN, buff=SMALL_BUFF)

        add_square = MathTex(
            r"x^2 + bx + \left(\frac{b}{2}\right)^2 = -c + \left(\frac{b}{2}\right)^2",
            font_size=SMALL_MATH_SIZE,
            color=NEON_ORANGE
        )
        add_square.next_to(reason_note, DOWN, buff=MEDIUM_BUFF)

        perfect_square = MathTex(
            r"\left(x + \frac{b}{2}\right)^2 = \left(\frac{b}{2}\right)^2 - c",
            font_size=SMALL_MATH_SIZE,
            color=NEON_GREEN
        )
        perfect_square.next_to(add_square, DOWN, buff=MEDIUM_BUFF)

        concept_group = VGroup(
            header,
            full_equation,
            move_c,
            focus_note,
            reason_note,
            add_square,
            perfect_square
        )
        fit_to_screen(concept_group)

        with self.voiceover(
            text="We always start with the full quadratic equation, x squared plus b x plus c equals zero."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(full_equation), run_time=NORMAL)
            blink_box(full_equation, color=NEON_YELLOW, times=1)
           # sync_wait(tracker, 2.0)
            self.wait_for_voiceover()

        with self.voiceover(
            text="First, move the constant term c to the right side. So we get x squared plus b x equals negative c."
        ) as tracker:
            self.play(TransformFromCopy(full_equation, move_c), run_time=SLOW)
            blink_box(move_c, color=NEON_BLUE, times=1)
            #sync_wait(tracker, 2.4)
            self.wait_for_voiceover()
        with self.voiceover(
            text="Now we focus on x squared plus bx. These two terms will become part of a perfect square."
        ) as tracker:
            self.play(FadeIn(focus_note), run_time=NORMAL)
            self.play(FadeIn(reason_note), run_time=NORMAL)
            blink_box(VGroup(focus_note, reason_note), color=NEON_BLUE, times=1)
            sync_wait(tracker, 2.2)

        with self.voiceover(
            text="To complete the square, add b by two whole square to both sides. We add to both sides because this is an equation."
        ) as tracker:
            self.play(Write(add_square), run_time=SLOW)
            blink_box(add_square, color=NEON_ORANGE, times=1)
            sync_wait(tracker, 2.4)

        with self.voiceover(
            text="Now the left side becomes x-plus-b by two whole square."
        ) as tracker:
            self.play(TransformFromCopy(add_square, perfect_square), run_time=SLOW)
            blink_box(perfect_square, color=NEON_GREEN, times=2)
            sync_wait(tracker, 2.2)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 5: EQUATION VS EXPRESSION
        # ============================================================

        header = make_title("Equation vs Expression")

        eq_title = Text(
            "Equation:",
            font_size=TEXT_SIZE,
            color=NEON_GREEN
        )
        eq_title.move_to([-3.5, 2.0, 0])

        expr_title = Text(
            "Expression:",
            font_size=TEXT_SIZE,
            color=NEON_ORANGE
        )
        expr_title.move_to([3.2, 2.0, 0])

        left_line1 = MathTex(
            r"x^2 + bx = -c",
            font_size=SMALL_MATH_SIZE,
            color=WHITE_TEXT
        )
        left_line1.next_to(eq_title, DOWN, buff=MEDIUM_BUFF)

        left_line2 = MathTex(
            r"x^2 + bx + \left(\frac{b}{2}\right)^2 = -c + \left(\frac{b}{2}\right)^2",
            font_size=TINY_MATH_SIZE,
            color=NEON_GREEN
        )
        left_line2.next_to(left_line1, DOWN, buff=MEDIUM_BUFF)

        left_note = Text(
            "Add same value to both sides.",
            font_size=SMALL_TEXT_SIZE,
            color=NEON_GREEN
        )
        left_note.next_to(left_line2, DOWN, buff=MEDIUM_BUFF)

        right_line1 = MathTex(
            r"x^2 + bx + c",
            font_size=SMALL_MATH_SIZE,
            color=WHITE_TEXT
        )
        right_line1.next_to(expr_title, DOWN, buff=MEDIUM_BUFF)

        right_line2 = MathTex(
            r"x^2 + bx + \left(\frac{b}{2}\right)^2 + c - \left(\frac{b}{2}\right)^2",
            font_size=TINY_MATH_SIZE,
            color=NEON_ORANGE
        )
        right_line2.next_to(right_line1, DOWN, buff=MEDIUM_BUFF)

        right_note = Text(
            "Add and subtract same value.",
            font_size=SMALL_TEXT_SIZE,
            color=NEON_ORANGE
        )
        right_note.next_to(right_line2, DOWN, buff=MEDIUM_BUFF)

        comparison_group = VGroup(
            header,
            eq_title,
            expr_title,
            left_line1,
            left_line2,
            left_note,
            right_line1,
            right_line2,
            right_note
        )
        fit_to_screen(comparison_group)

        with self.voiceover(
            text="There is one important difference. If we have an equation, we add the same value to both sides."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(FadeIn(eq_title), run_time=NORMAL)
            self.play(Write(left_line1), run_time=NORMAL)
            self.play(Write(left_line2), run_time=NORMAL)
            self.play(FadeIn(left_note), run_time=NORMAL)
            blink_box(left_note, color=NEON_GREEN, times=1)
            sync_wait(tracker, 2.6)

        with self.voiceover(
            text="But if we have only an expression, we add and subtract the same value inside the expression, so the value does not change."
        ) as tracker:
            self.play(FadeIn(expr_title), run_time=NORMAL)
            self.play(Write(right_line1), run_time=NORMAL)
            self.play(Write(right_line2), run_time=NORMAL)
            self.play(FadeIn(right_note), run_time=NORMAL)
            blink_box(right_note, color=NEON_ORANGE, times=1)
            sync_wait(tracker, 2.8)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 6: SMALL EXAMPLE
        # ============================================================

        header = make_title("Small Example")

        small_intro = Text(
            "Solve using completing the square:",
            font_size=TEXT_SIZE,
            color=NEON_BLUE
        )
        small_intro.next_to(header, DOWN, buff=MEDIUM_BUFF)

        eq1 = MathTex(
            r"x^2 + 10x + 2 = 0",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        )
        eq1.next_to(small_intro, DOWN, buff=MEDIUM_BUFF)

        step1 = MathTex(
            r"x^2 + 10x = -2",
            font_size=SMALL_MATH_SIZE,
            color=WHITE_TEXT
        )
        step1.next_to(eq1, DOWN, buff=MEDIUM_BUFF)

        step2 = MathTex(
            r"\text{Half of } 10 \text{ is } 5",
            font_size=SMALL_MATH_SIZE,
            color=NEON_BLUE
        )
        step2.next_to(step1, DOWN, buff=MEDIUM_BUFF)

        step3 = MathTex(
            r"5^2 = 25",
            font_size=SMALL_MATH_SIZE,
            color=NEON_ORANGE
        )
        step3.next_to(step2, DOWN, buff=MEDIUM_BUFF)

        step4 = MathTex(
            r"x^2 + 10x + 25 = -2 + 25",
            font_size=SMALL_MATH_SIZE,
            color=WHITE_TEXT
        )
        step4.next_to(step3, DOWN, buff=MEDIUM_BUFF)

        identity_note = MathTex(
            r"(a+b)^2 = a^2 + 2ab + b^2",
            font_size=SMALL_MATH_SIZE,
            color=NEON_PURPLE
        )
        identity_note.next_to(step4, DOWN, buff=SMALL_BUFF)

        step5 = MathTex(
            r"(x + 5)^2 = 23",
            font_size=SMALL_MATH_SIZE,
            color=NEON_GREEN
        )
        step5.next_to(identity_note, DOWN, buff=MEDIUM_BUFF)

        step6 = MathTex(
            r"x = -5 \pm \sqrt{23}",
            font_size=SMALL_MATH_SIZE,
            color=NEON_YELLOW
        )
        step6.next_to(step5, DOWN, buff=MEDIUM_BUFF)

        small_group = VGroup(
            header,
            small_intro,
            eq1,
            step1,
            step2,
            step3,
            step4,
            identity_note,
            step5,
            step6
        )
        fit_to_screen(small_group)

        with self.voiceover(
            text="Let us understand the method with a small example."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(FadeIn(small_intro), run_time=NORMAL)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="Consider x squared plus ten x plus two equals zero."
        ) as tracker:
            self.play(Write(eq1), run_time=NORMAL)
            blink_box(eq1, color=NEON_YELLOW, times=1)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="Move two to the right side. Then we focus on x squared plus ten x."
        ) as tracker:
            self.play(TransformFromCopy(eq1, step1), run_time=NORMAL)
            blink_box(step1, color=NEON_BLUE, times=1)
            sync_wait(tracker, 2.0)

        with self.voiceover(
            text="The coefficient of x is ten. Half of ten is five."
        ) as tracker:
            self.play(Write(step2), run_time=NORMAL)
            blink_box(step2, color=NEON_BLUE, times=1)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="Now square five. Five squared is twenty five."
        ) as tracker:
            self.play(Write(step3), run_time=NORMAL)
            blink_box(step3, color=NEON_ORANGE, times=1)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="Add twenty five to both sides, because we must keep the equation balanced."
        ) as tracker:
            self.play(Write(step4), run_time=NORMAL)
            blink_box(step4, color=NEON_ORANGE, times=1)
            sync_wait(tracker, 2.0)

        with self.voiceover(
            text="Now use the formula a plus b whole square equals a squared plus two a b plus b squared."
        ) as tracker:
            self.play(Write(identity_note), run_time=NORMAL)
            blink_box(identity_note, color=NEON_PURPLE, times=1)
            sync_wait(tracker, 2.2)

        with self.voiceover(
            text="Here, x squared plus ten x plus twenty five becomes x plus five whole square."
        ) as tracker:
            self.play(TransformFromCopy(step4, step5), run_time=SLOW)
            blink_box(step5, color=NEON_GREEN, times=2)
            sync_wait(tracker, 2.4)

        with self.voiceover(
            text="Taking square root gives x equals negative five plus or minus root twenty three."
        ) as tracker:
            self.play(Write(step6), run_time=NORMAL)
            blink_box(step6, color=NEON_YELLOW, times=2)
            sync_wait(tracker, 2.2)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 7: START SOLVING GIVEN EQUATION
        # ============================================================

        header = make_title("Solve the Equation")

        q1 = MathTex(
            r"5x^2 - 4x - 3 = 0",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        )
        q1.next_to(header, DOWN, buff=LARGE_BUFF)

        note1 = Text(
            "Make coefficient of x squared equal to 1.",
            font_size=TEXT_SIZE,
            color=NEON_BLUE
        )
        note1.next_to(q1, DOWN, buff=MEDIUM_BUFF)

        q2 = MathTex(
            r"x^2 - \frac{4}{5}x - \frac{3}{5} = 0",
            font_size=MATH_SIZE,
            color=WHITE_TEXT
        )
        q2.next_to(note1, DOWN, buff=MEDIUM_BUFF)

        solve_start_group = VGroup(header, q1, note1, q2)
        fit_to_screen(solve_start_group)

        with self.voiceover(
            text="Now let us solve five x squared minus four x minus three equals zero."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(q1), run_time=NORMAL)
            blink_box(q1, color=NEON_YELLOW, times=1)
            sync_wait(tracker, 2.0)

        with self.voiceover(
            text="First, make the coefficient of x squared equal to one. So divide the whole equation by five."
        ) as tracker:
            self.play(FadeIn(note1), run_time=NORMAL)
            self.play(TransformFromCopy(q1, q2), run_time=SLOW)
            blink_box(q2, color=NEON_BLUE, times=1)
            sync_wait(tracker, 2.4)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 8: FIND COMPLETING SQUARE TERM
        # ============================================================

        header = make_title("Find the Square Term")

        e1 = MathTex(
            r"x^2 - \frac{4}{5}x - \frac{3}{5} = 0",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        )
        e1.next_to(header, DOWN, buff=MEDIUM_BUFF)

        e2 = MathTex(
            r"x^2 - \frac{4}{5}x = \frac{3}{5}",
            font_size=SMALL_MATH_SIZE,
            color=WHITE_TEXT
        )
        e2.next_to(e1, DOWN, buff=MEDIUM_BUFF)

        b_value = MathTex(
            r"b = -\frac{4}{5}",
            font_size=SMALL_MATH_SIZE,
            color=NEON_BLUE
        )
        b_value.next_to(e2, DOWN, buff=MEDIUM_BUFF)

        half_value = MathTex(
            r"\frac{b}{2} = -\frac{2}{5}",
            font_size=SMALL_MATH_SIZE,
            color=NEON_ORANGE
        )
        half_value.next_to(b_value, DOWN, buff=MEDIUM_BUFF)

        square_value = MathTex(
            r"\left(-\frac{2}{5}\right)^2 = \frac{4}{25}",
            font_size=SMALL_MATH_SIZE,
            color=NEON_GREEN
        )
        square_value.next_to(half_value, DOWN, buff=MEDIUM_BUFF)

        find_group = VGroup(header, e1, e2, b_value, half_value, square_value)
        fit_to_screen(find_group)

        with self.voiceover(
            text="Move negative three by five to the right side."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(e1), run_time=NORMAL)
            self.play(TransformFromCopy(e1, e2), run_time=NORMAL)
            blink_box(e2, color=NEON_BLUE, times=1)
            sync_wait(tracker, 2.0)

        with self.voiceover(
            text="Here the coefficient of x is negative four by five."
        ) as tracker:
            self.play(Write(b_value), run_time=NORMAL)
            blink_box(b_value, color=NEON_BLUE, times=1)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="Half of negative four by five is negative two by five."
        ) as tracker:
            self.play(Write(half_value), run_time=NORMAL)
            blink_box(half_value, color=NEON_ORANGE, times=1)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="Now square negative two by five. The square is four by twenty five."
        ) as tracker:
            self.play(Write(square_value), run_time=NORMAL)
            blink_box(square_value, color=NEON_GREEN, times=2)
            sync_wait(tracker, 2.2)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 9: COMPLETE THE SQUARE
        # ============================================================

        header = make_title("Complete the Square")

        formula_used = MathTex(
            r"(a-b)^2 = a^2 - 2ab + b^2",
            font_size=SMALL_MATH_SIZE,
            color=NEON_PURPLE
        )
        formula_used.next_to(header, DOWN, buff=MEDIUM_BUFF)

        s1 = MathTex(
            r"x^2 - \frac{4}{5}x = \frac{3}{5}",
            font_size=SMALL_MATH_SIZE,
            color=WHITE_TEXT
        )
        s1.next_to(formula_used, DOWN, buff=MEDIUM_BUFF)

        s2 = MathTex(
            r"x^2 - \frac{4}{5}x + \frac{4}{25} = \frac{3}{5} + \frac{4}{25}",
            font_size=TINY_MATH_SIZE,
            color=WHITE_TEXT
        )
        s2.next_to(s1, DOWN, buff=MEDIUM_BUFF)

        s3 = MathTex(
            r"\left(x - \frac{2}{5}\right)^2 = \frac{3}{5} + \frac{4}{25}",
            font_size=SMALL_MATH_SIZE,
            color=NEON_GREEN
        )
        s3.next_to(s2, DOWN, buff=MEDIUM_BUFF)

        s4 = MathTex(
            r"\left(x - \frac{2}{5}\right)^2 = \frac{15}{25} + \frac{4}{25}",
            font_size=SMALL_MATH_SIZE,
            color=NEON_BLUE
        )
        s4.next_to(s3, DOWN, buff=MEDIUM_BUFF)

        s5 = MathTex(
            r"\left(x - \frac{2}{5}\right)^2 = \frac{19}{25}",
            font_size=SMALL_MATH_SIZE,
            color=NEON_YELLOW
        )
        s5.next_to(s4, DOWN, buff=MEDIUM_BUFF)

        complete_group = VGroup(header, formula_used, s1, s2, s3, s4, s5)
        fit_to_screen(complete_group)

        with self.voiceover(
            text="Now we use the identity a minus b whole square equals a squared minus two a b plus b squared."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(formula_used), run_time=NORMAL)
            blink_box(formula_used, color=NEON_PURPLE, times=1)
            sync_wait(tracker, 2.2)

        with self.voiceover(
            text="Start from x squared minus four by five x equals three by five."
        ) as tracker:
            self.play(Write(s1), run_time=NORMAL)
            blink_box(s1, color=NEON_BLUE, times=1)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="Add four by twenty five to both sides of the equation."
        ) as tracker:
            self.play(TransformFromCopy(s1, s2), run_time=SLOW)
            blink_box(s2, color=NEON_ORANGE, times=1)
            sync_wait(tracker, 2.0)

        with self.voiceover(
            text="Now the left side becomes x minus two by five whole square."
        ) as tracker:
            self.play(TransformFromCopy(s2, s3), run_time=SLOW)
            blink_box(s3, color=NEON_GREEN, times=2)
            sync_wait(tracker, 2.2)

        with self.voiceover(
            text="On the right side, convert three by five into denominator twenty five."
        ) as tracker:
            self.play(TransformFromCopy(s3, s4), run_time=NORMAL)
            blink_box(s4, color=NEON_BLUE, times=1)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="Fifteen by twenty five plus four by twenty five becomes nineteen by twenty five."
        ) as tracker:
            self.play(TransformFromCopy(s4, s5), run_time=NORMAL)
            blink_box(s5, color=NEON_YELLOW, times=2)
            sync_wait(tracker, 2.2)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 10: TAKE SQUARE ROOT
        # ============================================================

        header = make_title("Take Square Root")

        r1 = MathTex(
            r"\left(x - \frac{2}{5}\right)^2 = \frac{19}{25}",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        )
        r1.next_to(header, DOWN, buff=MEDIUM_BUFF)

        root_rule = MathTex(
            r"\text{If } A^2 = B,\text{ then } A = \pm \sqrt{B}",
            font_size=SMALL_MATH_SIZE,
            color=NEON_PURPLE
        )
        root_rule.next_to(r1, DOWN, buff=MEDIUM_BUFF)

        r2 = MathTex(
            r"x - \frac{2}{5} = \pm \sqrt{\frac{19}{25}}",
            font_size=SMALL_MATH_SIZE,
            color=WHITE_TEXT
        )
        r2.next_to(root_rule, DOWN, buff=MEDIUM_BUFF)

        r3 = MathTex(
            r"x - \frac{2}{5} = \pm \frac{\sqrt{19}}{5}",
            font_size=SMALL_MATH_SIZE,
            color=NEON_GREEN
        )
        r3.next_to(r2, DOWN, buff=MEDIUM_BUFF)

        r4 = MathTex(
            r"x = \frac{2}{5} \pm \frac{\sqrt{19}}{5}",
            font_size=SMALL_MATH_SIZE,
            color=NEON_BLUE
        )
        r4.next_to(r3, DOWN, buff=MEDIUM_BUFF)

        r5 = MathTex(
            r"x = \frac{2 + \sqrt{19}}{5}",
            font_size=SMALL_MATH_SIZE,
            color=NEON_GREEN
        )

        r6 = MathTex(
            r"x = \frac{2 - \sqrt{19}}{5}",
            font_size=SMALL_MATH_SIZE,
            color=NEON_GREEN
        )

        roots_pair = VGroup(r5, r6)
        roots_pair.arrange(RIGHT, buff=LARGE_BUFF)
        roots_pair.next_to(r4, DOWN, buff=MEDIUM_BUFF)

        root_group = VGroup(header, r1, root_rule, r2, r3, r4, roots_pair)
        fit_to_screen(root_group)

        with self.voiceover(
            text="Now we take square root on both sides."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(r1), run_time=NORMAL)
            blink_box(r1, color=NEON_YELLOW, times=1)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="We use this rule. If A squared equals B, then A equals plus or minus square root of B."
        ) as tracker:
            self.play(Write(root_rule), run_time=NORMAL)
            blink_box(root_rule, color=NEON_PURPLE, times=1)
            sync_wait(tracker, 2.2)

        with self.voiceover(
            text="Here, A is x minus two by five, and B is nineteen by twenty five."
        ) as tracker:
            self.play(TransformFromCopy(r1, r2), run_time=SLOW)
            blink_box(r2, color=NEON_ORANGE, times=1)
            sync_wait(tracker, 2.2)

        with self.voiceover(
            text="Square root of nineteen by twenty five is root nineteen by five."
        ) as tracker:
            self.play(TransformFromCopy(r2, r3), run_time=NORMAL)
            blink_box(r3, color=NEON_GREEN, times=2)
            sync_wait(tracker, 2.0)

        with self.voiceover(
            text="Now add two by five to both sides."
        ) as tracker:
            self.play(TransformFromCopy(r3, r4), run_time=NORMAL)
            blink_box(r4, color=NEON_BLUE, times=1)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="Therefore, the two roots are two plus root nineteen by five, and two minus root nineteen by five."
        ) as tracker:
            self.play(Write(r5), run_time=NORMAL)
            self.play(Write(r6), run_time=NORMAL)
            blink_box(roots_pair, color=NEON_GREEN, times=2)
            sync_wait(tracker, 2)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 11: FINAL ANSWER
        # ============================================================

        header = make_title("Final Answer")

        final_eq = MathTex(
            r"5x^2 - 4x - 3 = 0",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        )
        final_eq.next_to(header, DOWN, buff=LARGE_BUFF)

        ans1 = MathTex(
            r"x = \frac{2 + \sqrt{19}}{5}",
            font_size=MATH_SIZE,
            color=NEON_GREEN
        )

        ans2 = MathTex(
            r"x = \frac{2 - \sqrt{19}}{5}",
            font_size=MATH_SIZE,
            color=NEON_GREEN
        )

        answers = VGroup(ans1, ans2)
        answers.arrange(DOWN, buff=MEDIUM_BUFF)
        answers.next_to(final_eq, DOWN, buff=LARGE_BUFF)

        final_line = Text(
            "These are the roots of the given quadratic equation.",
            font_size=TEXT_SIZE,
            color=NEON_BLUE
        )
        final_line.next_to(answers, DOWN, buff=LARGE_BUFF)

        final_group = VGroup(header, final_eq, answers, final_line)
        fit_to_screen(final_group)

        with self.voiceover(
            text="So, for the equation five x squared minus four x minus three equals zero, these are the final roots."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(final_eq), run_time=NORMAL)
            self.play(Write(ans1), run_time=NORMAL)
            self.play(Write(ans2), run_time=NORMAL)
            blink_box(answers, color=NEON_GREEN, times=2)
            sync_wait(tracker, 2.5)

        with self.voiceover(
            text="These two values are the roots of the given quadratic equation."
        ) as tracker:
            self.play(FadeIn(final_line, shift=RIGHT), run_time=NORMAL)
            blink_box(final_line, color=NEON_BLUE, times=1)
            sync_wait(tracker, 1.8)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 12: SUMMARY
        # ============================================================

        header = make_title("Summary")

        p1 = Text(
            "1. Start with ax squared plus bx plus c equals 0.",
            font_size=TEXT_SIZE,
            color=WHITE_TEXT
        )

        p2 = Text(
            "2. Make coefficient of x squared equal to 1.",
            font_size=TEXT_SIZE,
            color=WHITE_TEXT
        )

        p3 = Text(
            "3. Move the constant term to the other side.",
            font_size=TEXT_SIZE,
            color=WHITE_TEXT
        )

        p4 = Text(
            "4. Add half of coefficient of x, squared, to both sides.",
            font_size=TEXT_SIZE,
            color=WHITE_TEXT
        )

        p5 = Text(
            "5. Use square identity to form a perfect square.",
            font_size=TEXT_SIZE,
            color=NEON_GREEN
        )

        p6 = Text(
            "6. Take square root and solve for x.",
            font_size=TEXT_SIZE,
            color=NEON_YELLOW
        )

        summary = VGroup(p1, p2, p3, p4, p5, p6)
        summary.arrange(DOWN, aligned_edge=LEFT, buff=MEDIUM_BUFF)
        summary.next_to(header, DOWN, buff=LARGE_BUFF)

        summary_group = VGroup(header, summary)
        fit_to_screen(summary_group)

        with self.voiceover(
            text="Let us summarize the completing square method."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            sync_wait(tracker, NORMAL)

        with self.voiceover(
            text="First, start with a quadratic equation."
        ) as tracker:
            self.play(FadeIn(p1, shift=RIGHT), run_time=FAST)
            blink_box(p1, color=NEON_BLUE, times=1)
            sync_wait(tracker, 1.3)

        with self.voiceover(
            text="Second, make the coefficient of x squared equal to one."
        ) as tracker:
            self.play(FadeIn(p2, shift=RIGHT), run_time=FAST)
            blink_box(p2, color=NEON_BLUE, times=1)
            sync_wait(tracker, 1.4)

        with self.voiceover(
            text="Third, move the constant term to the other side."
        ) as tracker:
            self.play(FadeIn(p3, shift=RIGHT), run_time=FAST)
            blink_box(p3, color=NEON_ORANGE, times=1)
            sync_wait(tracker, 1.4)

        with self.voiceover(
            text="Fourth, add half of the coefficient of x, squared, to both sides."
        ) as tracker:
            self.play(FadeIn(p4, shift=RIGHT), run_time=FAST)
            blink_box(p4, color=NEON_ORANGE, times=1)
            sync_wait(tracker, 1.6)

        with self.voiceover(
            text="Fifth, use the square identity to form a perfect square."
        ) as tracker:
            self.play(FadeIn(p5, shift=RIGHT), run_time=FAST)
            blink_box(p5, color=NEON_GREEN, times=1)
            sync_wait(tracker, 1.5)

        with self.voiceover(
            text="Finally, take square root and solve for x."
        ) as tracker:
            self.play(FadeIn(p6, shift=RIGHT), run_time=FAST)
            blink_box(p6, color=NEON_YELLOW, times=1)
            sync_wait(tracker, 1.5)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 13: END SCREEN
        # ============================================================

        thanks = Text(
            "Thanks for Watching",
            font_size=44,
            color=NEON_YELLOW
        )

        like = Text(
            "Like",
            font_size=34,
            color=NEON_GREEN
        )

        share = Text(
            "Share",
            font_size=34,
            color=NEON_BLUE
        )

        subscribe = Text(
            "Subscribe",
            font_size=44,
            color=NEON_PINK
        )

        end_group = VGroup(thanks, like, share, subscribe)
        end_group.arrange(DOWN, buff=MEDIUM_BUFF)
        end_group.move_to([0, 0, 0])

        subscribe_box = neon_box(subscribe, color=NEON_PINK, buff=0.18)

        with self.voiceover(
            text="Thanks for watching."
        ) as tracker:
            self.play(Write(thanks), run_time=NORMAL)
            sync_wait(tracker, NORMAL)

        with self.voiceover(
            text="Please like and share this video."
        ) as tracker:
            self.play(FadeIn(like, shift=LEFT), run_time=FAST)
            self.play(FadeIn(share, shift=RIGHT), run_time=FAST)
            sync_wait(tracker, NORMAL)

        with self.voiceover(
            text="And subscribe for more mathematics animations."
        ) as tracker:
            self.play(Write(subscribe), run_time=NORMAL)
            self.play(Create(subscribe_box), run_time=FAST)

            self.play(
                subscribe.animate.scale(1.12),
                subscribe_box.animate.scale(1.12),
                run_time=FAST
            )

            self.play(
                subscribe.animate.scale(0.89),
                subscribe_box.animate.scale(0.89),
                run_time=FAST
            )

            sync_wait(tracker, 1.8)

        self.wait(2)
