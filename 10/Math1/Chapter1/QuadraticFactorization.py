from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


# ============================================================
# GLOBAL SETTINGS
# ============================================================

# Font sizes
#TITLE_SIZE = 45
#HEADING_SIZE = 30
#TEXT_SIZE = 24
#SMALL_TEXT_SIZE = 20
#MATH_SIZE = 34
#SMALL_MATH_SIZE = 28
#TINY_MATH_SIZE = 24

TITLE_SIZE = 45
HEADING_SIZE = 45
TEXT_SIZE = 30
SMALL_TEXT_SIZE = 30
MATH_SIZE = 40
SMALL_MATH_SIZE = 40
TINY_MATH_SIZE = 35
SMALL_TEXT_SIZE_1 = 20

# Animation speeds
FAST = 0.45
NORMAL = 0.9
SLOW = 1.35
VERY_SLOW = 1.8

# Voice sync wait
MIN_WAIT_AFTER_STEP = 0.15

# Spacing
SMALL_BUFF = 0.18
MEDIUM_BUFF = 0.35
LARGE_BUFF = 0.65

# Neon colors
NEON_PINK = "#FF00FF"
NEON_BLUE = "#00FFFF"
NEON_GREEN = "#39FF14"
NEON_YELLOW = "#FFFF00"
NEON_ORANGE = "#FF8800"
NEON_PURPLE = "#B026FF"
NEON_RED = "#FF3131"
WHITE_TEXT = "#F8F8FF"
BLACK_BG = "#000000"

# Screen safety
SAFE_WIDTH = 12.2
SAFE_HEIGHT = 6.4


class QuadraticFactorizationLessonSynced(VoiceoverScene):

    def construct(self):

        # ========================================================
        # VOICEOVER SETUP
        # ========================================================
        # gTTS needs internet when rendering.
        # If voiceover fails, comment this line.
        self.set_speech_service(GTTSService(lang="en"))

        self.camera.background_color = BLACK_BG

        # ========================================================
        # HELPER FUNCTIONS
        # ========================================================

        def fit_to_screen(mob):
            """Scale down content if it goes outside the safe screen area."""
            if mob.width > SAFE_WIDTH:
                mob.scale_to_fit_width(SAFE_WIDTH)
            if mob.height > SAFE_HEIGHT:
                mob.scale_to_fit_height(SAFE_HEIGHT)
            return mob

        def make_title(text):
            """Create title text at the top."""
            return Text(
                text,
                font_size=TITLE_SIZE,
                color=NEON_YELLOW
            ).to_edge(UP)

        def neon_box(mob, color=NEON_YELLOW, buff=0.12):
            """Create a bright rectangular highlight box."""
            return SurroundingRectangle(
                mob,
                color=color,
                buff=buff,
                stroke_width=3
            )

        def clear_scene():
            """Fade out all visible objects."""
            if len(self.mobjects) > 0:
                self.play(
                    *[FadeOut(m) for m in self.mobjects],
                    run_time=FAST
                )

        def blink_box(mob, color=NEON_YELLOW, times=2, buff=0.12):
            """Blink a rectangle around a mobject."""
            box = neon_box(mob, color=color, buff=buff)
            for _ in range(times):
                self.play(Create(box), run_time=FAST)
                self.play(FadeOut(box), run_time=FAST)

        def voice_wait(tracker, used_time):
            """Wait for remaining voiceover time if animation ended early."""
            remaining = tracker.duration - used_time
            if remaining > 0:
                self.wait(remaining + MIN_WAIT_AFTER_STEP)
            else:
                self.wait(MIN_WAIT_AFTER_STEP)

        # ========================================================
        # SCENE 1: OPENING TITLE
        # ========================================================

        title = Text(
            "Quadratic Equation by Factorization",
            font_size=TITLE_SIZE,
            color=NEON_YELLOW
        )

        subtitle = Text(
            "Concept first, then example step by step",
            font_size=TEXT_SIZE,
            color=NEON_BLUE
        ).next_to(title, DOWN, buff=MEDIUM_BUFF)

        opening = VGroup(title, subtitle).move_to(ORIGIN)

        with self.voiceover(
            text="Welcome. Today we will learn quadratic equations by factorization method."
        ) as tracker:
            self.play(Write(title), run_time=NORMAL)
            voice_wait(tracker, NORMAL)

        with self.voiceover(
            text="First we will understand the concept. Then we will solve one example step by step."
        ) as tracker:
            self.play(FadeIn(subtitle, shift=UP), run_time=NORMAL)
            voice_wait(tracker, NORMAL)

        self.wait(0.4)
        clear_scene()

        # ========================================================
        # SCENE 2: THEORY INTRODUCTION FROM IMAGE 1
        # ========================================================

        header = make_title("Solutions of a Quadratic Equation by Factorization")

        line1 = Text(
            "Substituting random values to find roots is time consuming.",
            font_size=SMALL_TEXT_SIZE,
            color=WHITE_TEXT
        ).next_to(header, DOWN, buff=MEDIUM_BUFF)

        line2 = Text(
            "Factorization helps us find the roots faster.",
            font_size=SMALL_TEXT_SIZE,
            color=NEON_GREEN
        ).next_to(line1, DOWN, buff=SMALL_BUFF)

        expr = MathTex(
            r"x^2 - 4x - 5",
            font_size=MATH_SIZE,
            color=WHITE_TEXT
        ).next_to(line2, DOWN, buff=LARGE_BUFF)

        factorized = MathTex(
            r"x^2 - 4x - 5 = (x - 5)(x + 1)",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        ).next_to(expr, DOWN, buff=MEDIUM_BUFF)

        factor_line = Text(
            "(x - 5) and (x + 1) are two linear factors.",
            font_size=TEXT_SIZE,
            color=NEON_BLUE
        ).next_to(factorized, DOWN, buff=MEDIUM_BUFF)

        full_group = VGroup(header, line1, line2, expr, factorized, factor_line)
        fit_to_screen(full_group)

        with self.voiceover(
            text="By substituting arbitrary values for the variable, finding roots of a quadratic equation becomes time consuming."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(FadeIn(line1), run_time=NORMAL)
            voice_wait(tracker, 2 * NORMAL)

        with self.voiceover(
            text="So, we use the factorization method to find the roots faster."
        ) as tracker:
            self.play(FadeIn(line2), run_time=NORMAL)
            voice_wait(tracker, NORMAL)

        with self.voiceover(
            text="Consider the quadratic expression x squared minus four x minus five."
        ) as tracker:
            self.play(Write(expr), run_time=NORMAL)
            blink_box(expr, color=NEON_PINK, times=1)
            voice_wait(tracker, NORMAL + 2 * FAST)

        with self.voiceover(
            text="This expression can be written as x minus five multiplied by x plus one."
        ) as tracker:
            self.play(TransformFromCopy(expr, factorized), run_time=SLOW)
            blink_box(factorized, color=NEON_YELLOW, times=1)
            voice_wait(tracker, SLOW + 2 * FAST)

        with self.voiceover(
            text="Here, x minus five and x plus one are two linear factors of the quadratic polynomial."
        ) as tracker:
            self.play(FadeIn(factor_line), run_time=NORMAL)
            blink_box(factor_line, color=NEON_BLUE, times=1)
            voice_wait(tracker, NORMAL + 2 * FAST)

        self.wait(0.4)
        clear_scene()

        # ========================================================
        # SCENE 3: WHY x^2 - 4x - 5 FACTORIZES
        # ========================================================

        header = make_title("Why does it become (x - 5)(x + 1)?")

        expr_parts = MathTex(
            r"x^2", r"-4x", r"-5",
            font_size=MATH_SIZE,
            color=WHITE_TEXT
        ).next_to(header, DOWN, buff=LARGE_BUFF)

        expr_parts[1].set_color(NEON_GREEN)
        expr_parts[2].set_color(NEON_ORANGE)

        product_need = MathTex(
            r"\text{Product of numbers} = -5",
            font_size=SMALL_MATH_SIZE,
            color=NEON_ORANGE
        )

        sum_need = MathTex(
            r"\text{Sum of numbers} = -4",
            font_size=SMALL_MATH_SIZE,
            color=NEON_GREEN
        )

        needs = VGroup(product_need, sum_need).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=SMALL_BUFF
        ).next_to(expr_parts, DOWN, buff=MEDIUM_BUFF)

        number_pair = MathTex(
            r"-5", r"\quad \text{and} \quad", r"+1",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        ).next_to(needs, DOWN, buff=MEDIUM_BUFF)

        product_check = MathTex(
            r"(-5)(+1) = -5",
            font_size=SMALL_MATH_SIZE,
            color=NEON_ORANGE
        )

        sum_check = MathTex(
            r"(-5) + (+1) = -4",
            font_size=SMALL_MATH_SIZE,
            color=NEON_GREEN
        )

        checks = VGroup(product_check, sum_check).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=SMALL_BUFF
        ).next_to(number_pair, DOWN, buff=MEDIUM_BUFF)

        final_factor = MathTex(
            r"x^2 - 4x - 5 = (x - 5)(x + 1)",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        ).next_to(checks, DOWN, buff=MEDIUM_BUFF)

        scene_group = VGroup(header, expr_parts, needs, number_pair, checks, final_factor)
        fit_to_screen(scene_group)

        with self.voiceover(
            text="Now let us understand how x squared minus four x minus five is factorized."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(expr_parts), run_time=NORMAL)
            voice_wait(tracker, 2 * NORMAL)

        with self.voiceover(
            text="For factorization, we look at the constant term negative five and the middle term negative four x."
        ) as tracker:
            blink_box(expr_parts[2], color=NEON_ORANGE, times=1)
            blink_box(expr_parts[1], color=NEON_GREEN, times=1)
            voice_wait(tracker, 4 * FAST)

        with self.voiceover(
            text="We need two numbers whose product is negative five."
        ) as tracker:
            self.play(Write(product_need), run_time=NORMAL)
            blink_box(product_need, color=NEON_ORANGE, times=1)
            voice_wait(tracker, NORMAL + 2 * FAST)

        with self.voiceover(
            text="And whose sum is negative four."
        ) as tracker:
            self.play(Write(sum_need), run_time=NORMAL)
            blink_box(sum_need, color=NEON_GREEN, times=1)
            voice_wait(tracker, NORMAL + 2 * FAST)

        with self.voiceover(
            text="The numbers are negative five and positive one."
        ) as tracker:
            self.play(Write(number_pair), run_time=NORMAL)
            blink_box(number_pair, color=NEON_YELLOW, times=2)
            voice_wait(tracker, NORMAL + 4 * FAST)

        with self.voiceover(
            text="Negative five multiplied by positive one gives negative five."
        ) as tracker:
            self.play(Write(product_check), run_time=NORMAL)
            blink_box(product_check, color=NEON_ORANGE, times=1)
            voice_wait(tracker, NORMAL + 2 * FAST)

        with self.voiceover(
            text="Negative five plus positive one gives negative four."
        ) as tracker:
            self.play(Write(sum_check), run_time=NORMAL)
            blink_box(sum_check, color=NEON_GREEN, times=1)
            voice_wait(tracker, NORMAL + 2 * FAST)

        with self.voiceover(
            text="Therefore, x squared minus four x minus five is equal to x minus five multiplied by x plus one."
        ) as tracker:
            self.play(Write(final_factor), run_time=SLOW)
            blink_box(final_factor, color=NEON_YELLOW, times=1)
            voice_wait(tracker, SLOW + 2 * FAST)

        self.wait(0.4)
        clear_scene()

        # ========================================================
        # SCENE 4: ZERO PRODUCT RULE FOR CONCEPT
        # ========================================================

        header = make_title("Zero Product Rule")

        equation = MathTex(
            r"(x - 5)(x + 1) = 0",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        ).next_to(header, DOWN, buff=LARGE_BUFF)

        rule = Text(
            "If product of two numbers is zero, then at least one of them is zero.",
            font_size=TEXT_SIZE,
            color=NEON_GREEN
        ).next_to(equation, DOWN, buff=MEDIUM_BUFF)

        left_eq = MathTex(
            r"x - 5 = 0",
            font_size=SMALL_MATH_SIZE,
            color=NEON_BLUE
        )

        right_eq = MathTex(
            r"x + 1 = 0",
            font_size=SMALL_MATH_SIZE,
            color=NEON_BLUE
        )

        branches = VGroup(left_eq, right_eq).arrange(
            RIGHT,
            buff=1.8
        ).next_to(rule, DOWN, buff=LARGE_BUFF)

        arrow_left = Arrow(
            equation.get_bottom(),
            left_eq.get_top(),
            color=NEON_PINK,
            buff=0.12
        )

        arrow_right = Arrow(
            equation.get_bottom(),
            right_eq.get_top(),
            color=NEON_PINK,
            buff=0.12
        )

        sol_left = MathTex(
            r"x = 5",
            font_size=SMALL_MATH_SIZE,
            color=NEON_GREEN
        ).next_to(left_eq, DOWN, buff=MEDIUM_BUFF)

        sol_right = MathTex(
            r"x = -1",
            font_size=SMALL_MATH_SIZE,
            color=NEON_GREEN
        ).next_to(right_eq, DOWN, buff=MEDIUM_BUFF)

        roots_line = Text(
            "5 and -1 are the roots of the given quadratic equation.",
            font_size=TEXT_SIZE,
            color=NEON_YELLOW
        ).next_to(VGroup(sol_left, sol_right), DOWN, buff=MEDIUM_BUFF)

        method_line1 = Text(
            "While solving the equation, first we obtained the linear factors.",
            font_size=SMALL_TEXT_SIZE,
            color=WHITE_TEXT
        ).next_to(roots_line, DOWN, buff=SMALL_BUFF)

        method_line2 = Text(
            "So, we call this method factorization method of solving quadratic equation.",
            font_size=SMALL_TEXT_SIZE,
            color=WHITE_TEXT
        ).next_to(method_line1, DOWN, buff=SMALL_BUFF)

        scene_group = VGroup(
            header, equation, rule, branches, arrow_left, arrow_right,
            sol_left, sol_right, roots_line, method_line1, method_line2
        )
        fit_to_screen(scene_group)

        with self.voiceover(
            text="Now write the quadratic equation using the factors."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(equation), run_time=NORMAL)
            blink_box(equation, color=NEON_YELLOW, times=1)
            voice_wait(tracker, 2 * NORMAL + 2 * FAST)

        with self.voiceover(
            text="If product of two numbers is zero, then at least one of them is zero."
        ) as tracker:
            self.play(FadeIn(rule), run_time=NORMAL)
            blink_box(rule, color=NEON_GREEN, times=1)
            voice_wait(tracker, NORMAL + 2 * FAST)

        with self.voiceover(
            text="So, either x minus five is zero, or x plus one is zero."
        ) as tracker:
            self.play(Create(arrow_left), Create(arrow_right), run_time=NORMAL)
            self.play(Write(left_eq), Write(right_eq), run_time=NORMAL)
            blink_box(branches, color=NEON_BLUE, times=1)
            voice_wait(tracker, 2 * NORMAL + 2 * FAST)

        with self.voiceover(
            text="From x minus five equals zero, we get x equals five."
        ) as tracker:
            self.play(Write(sol_left), run_time=NORMAL)
            blink_box(sol_left, color=NEON_GREEN, times=1)
            voice_wait(tracker, NORMAL + 2 * FAST)

        with self.voiceover(
            text="From x plus one equals zero, we get x equals negative one."
        ) as tracker:
            self.play(Write(sol_right), run_time=NORMAL)
            blink_box(sol_right, color=NEON_GREEN, times=1)
            voice_wait(tracker, NORMAL + 2 * FAST)

        with self.voiceover(
            text="Therefore, five and negative one are the roots of the given quadratic equation."
        ) as tracker:
            self.play(FadeIn(roots_line), run_time=NORMAL)
            blink_box(roots_line, color=NEON_YELLOW, times=1)
            voice_wait(tracker, NORMAL + 2 * FAST)

        with self.voiceover(
            text="While solving the equation, first we obtained the linear factors."
        ) as tracker:
            self.play(FadeIn(method_line1), run_time=NORMAL)
            voice_wait(tracker, NORMAL)

        with self.voiceover(
            text="So, we call this method factorization method of solving quadratic equation."
        ) as tracker:
            self.play(FadeIn(method_line2), run_time=NORMAL)
            blink_box(VGroup(method_line1, method_line2), color=NEON_PINK, times=1)
            voice_wait(tracker, NORMAL + 2 * FAST)

        self.wait(0.4)
        clear_scene()

        # ========================================================
        # SCENE 5: EXAMPLE START
        # ========================================================

        header = make_title("Example")

        example = MathTex(
            r"m^2 - 14m + 13 = 0",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        ).next_to(header, DOWN, buff=LARGE_BUFF)

        with self.voiceover(
            text="Now let us solve the example."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            voice_wait(tracker, NORMAL)

        with self.voiceover(
            text="m squared minus fourteen m plus thirteen equals zero."
        ) as tracker:
            self.play(Write(example), run_time=NORMAL)
            blink_box(example, color=NEON_PINK, times=1)
            voice_wait(tracker, NORMAL + 2 * FAST)

        self.wait(0.4)
        clear_scene()

        # ========================================================
        # SCENE 6: SPLIT THE MIDDLE TERM WITH ARROWS
        # ========================================================

        header = make_title("Split the Middle Term")

        original = MathTex(
            r"m^2", r"-14m", r"+13", r"=0",
            font_size=MATH_SIZE,
            color=WHITE_TEXT
        ).next_to(header, DOWN, buff=MEDIUM_BUFF)

        original[1].set_color(NEON_RED)

        middle = MathTex(
            r"-14m",
            font_size=MATH_SIZE,
            color=NEON_RED
        ).next_to(original, DOWN, buff=MEDIUM_BUFF)

        brace = Brace(middle, DOWN, color=NEON_ORANGE)

        split1 = MathTex(
            r"-13m",
            font_size=SMALL_MATH_SIZE,
            color=NEON_GREEN
        )

        split2 = MathTex(
            r"-1m",
            font_size=SMALL_MATH_SIZE,
            color=NEON_GREEN
        )

        split_terms = VGroup(split1, split2).arrange(
            RIGHT,
            buff=1.2
        ).next_to(brace, DOWN, buff=MEDIUM_BUFF)

        arrow1 = Arrow(
            middle.get_bottom(),
            split1.get_top(),
            color=NEON_PINK,
            buff=0.1
        )

        arrow2 = Arrow(
            middle.get_bottom(),
            split2.get_top(),
            color=NEON_PINK,
            buff=0.1
        )

        product_check = MathTex(
            r"(-13)(-1) = 13",
            font_size=SMALL_MATH_SIZE,
            color=NEON_ORANGE
        )

        sum_check = MathTex(
            r"(-13)+(-1) = -14",
            font_size=SMALL_MATH_SIZE,
            color=NEON_GREEN
        )

        checks = VGroup(product_check, sum_check).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=SMALL_BUFF
        ).next_to(split_terms, DOWN, buff=MEDIUM_BUFF)

        rewritten = MathTex(
            r"m^2 - 13m - 1m + 13 = 0",
            font_size=SMALL_MATH_SIZE,
            color=NEON_YELLOW
        ).next_to(checks, DOWN, buff=MEDIUM_BUFF)

        scene_group = VGroup(
            header, original, middle, brace, split_terms,
            arrow1, arrow2, checks, rewritten
        )
        fit_to_screen(scene_group)

        with self.voiceover(
            text="First, identify the middle term."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(original), run_time=NORMAL)
            blink_box(original[1], color=NEON_RED, times=3)
            voice_wait(tracker, 2 * NORMAL + 6 * FAST)

        with self.voiceover(
            text="The middle term is negative fourteen m."
        ) as tracker:
            self.play(TransformFromCopy(original[1], middle), run_time=NORMAL)
            self.play(Create(brace), run_time=FAST)
            blink_box(middle, color=NEON_RED, times=1)
            voice_wait(tracker, NORMAL + FAST + 2 * FAST)

        with self.voiceover(
            text="We need two numbers whose product is positive thirteen."
        ) as tracker:
            self.play(Write(product_check), run_time=NORMAL)
            blink_box(product_check, color=NEON_ORANGE, times=1)
            voice_wait(tracker, NORMAL + 2 * FAST)

        with self.voiceover(
            text="And whose sum is negative fourteen."
        ) as tracker:
            self.play(Write(sum_check), run_time=NORMAL)
            blink_box(sum_check, color=NEON_GREEN, times=1)
            voice_wait(tracker, NORMAL + 2 * FAST)

        with self.voiceover(
            text="The numbers are negative thirteen and negative one."
        ) as tracker:
            self.play(Create(arrow1), Create(arrow2), run_time=NORMAL)
            self.play(Write(split1), Write(split2), run_time=NORMAL)
            blink_box(split_terms, color=NEON_GREEN, times=2)
            voice_wait(tracker, 2 * NORMAL + 4 * FAST)

        with self.voiceover(
            text="So, negative fourteen m becomes negative thirteen m and minus one m."
        ) as tracker:
            self.play(Write(rewritten), run_time=NORMAL)
            blink_box(rewritten, color=NEON_YELLOW, times=1)
            voice_wait(tracker, NORMAL + 2 * FAST)

        self.wait(0.4)
        clear_scene()

        # ========================================================
        # SCENE 7: ALIGNED EQUATION STEPS WITH GROUPING
        # ========================================================

        header = make_title("Solution Steps")

        # Create rows with separated parts so equal signs stay aligned
        eq_x = 1.45
        y_start = 2.0
        y_gap = 0.75

        def make_aligned_row(left_tex, right_tex, y_value, left_color=WHITE_TEXT):
            left = MathTex(
                left_tex,
                font_size=SMALL_MATH_SIZE,
                color=left_color
            )
            equal = MathTex(
                r"=",
                font_size=SMALL_MATH_SIZE,
                color=NEON_BLUE
            )
            right = MathTex(
                right_tex,
                font_size=SMALL_MATH_SIZE,
                color=WHITE_TEXT
            )
            equal.move_to([eq_x, y_value, 0])
            left.next_to(equal, LEFT, buff=MEDIUM_BUFF)
            right.next_to(equal, RIGHT, buff=MEDIUM_BUFF)
            return VGroup(left, equal, right)

        row1 = make_aligned_row(
            r"m^2 - 14m + 13",
            r"0",
            y_start
        )

        row2 = make_aligned_row(
            r"m^2 - 13m - 1m + 13",
            r"0",
            y_start - y_gap
        )

        row3 = make_aligned_row(
            r"(m^2 - 13m) + (-1m + 13)",
            r"0",
            y_start - 2 * y_gap
        )

        row4 = make_aligned_row(
            r"m(m - 13) - 1(m - 13)",
            r"0",
            y_start - 3 * y_gap
        )

        row5 = make_aligned_row(
            r"(m - 13)(m - 1)",
            r"0",
            y_start - 4 * y_gap,
            left_color=NEON_YELLOW
        )

        rows = VGroup(row1, row2, row3, row4, row5)
        rows.next_to(header, DOWN, buff=LARGE_BUFF)

        note_grouping = Text(
            "Group the terms",
            font_size=SMALL_TEXT_SIZE_1,
            color=NEON_GREEN
        ).next_to(row3, DOWN, buff=0.04)

        note_common = Text(
            "Common binomial factor is (m - 13)",
            font_size=SMALL_TEXT_SIZE_1,
            color=NEON_PURPLE
        ).next_to(row4, DOWN, buff=0.04)

        scene_group = VGroup(header, rows, note_grouping, note_common)
        fit_to_screen(scene_group)

        with self.voiceover(
            text="Now we solve the equation step by step."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            voice_wait(tracker, NORMAL)

        with self.voiceover(
            text="Start with m squared minus fourteen m plus thirteen equals zero."
        ) as tracker:
            self.play(Write(row1), run_time=NORMAL)
            blink_box(row1, color=NEON_PINK, times=1)
            voice_wait(tracker, NORMAL + 2 * FAST)

        with self.voiceover(
            text="Replace negative fourteen m by negative thirteen m and minus one m."
        ) as tracker:
            self.play(TransformFromCopy(row1, row2), run_time=SLOW)
            blink_box(row2[0], color=NEON_RED, times=2)
            voice_wait(tracker, SLOW + 4 * FAST)

        with self.voiceover(
            text="Now group the first two terms, and group the last two terms."
        ) as tracker:
            self.play(TransformFromCopy(row2, row3), run_time=SLOW)

            group_box1 = SurroundingRectangle(
                row3[0],
                color=NEON_GREEN,
                buff=0.12,
                stroke_width=3
            )

            self.play(Create(group_box1), run_time=FAST)
            self.play(FadeIn(note_grouping), run_time=FAST)
            blink_box(row3[0], color=NEON_GREEN, times=1)
            self.play(FadeOut(group_box1), run_time=FAST)

            voice_wait(tracker, SLOW + 4 * FAST)

        with self.voiceover(
            text="From the first group, take m common. From the second group, take negative one common."
        ) as tracker:
            self.play(TransformFromCopy(row3, row4), run_time=SLOW)
            blink_box(row4[0], color=NEON_ORANGE, times=1)
            voice_wait(tracker, SLOW + 2 * FAST)

        with self.voiceover(
            text="Notice carefully. The common binomial factor is m minus thirteen."
        ) as tracker:
            self.play(FadeIn(note_common), run_time=FAST)

            common_text = MathTex(
                r"(m - 13)",
                font_size=SMALL_MATH_SIZE,
                color=NEON_PURPLE
            ).next_to(row4, RIGHT, buff=0.5)

            arrow_common = Arrow(
                row4.get_right(),
                common_text.get_left(),
                color=NEON_PURPLE,
                buff=0.1
            )

            self.play(Create(arrow_common), Write(common_text), run_time=NORMAL)
            blink_box(common_text, color=NEON_PURPLE, times=3)
            self.play(FadeOut(arrow_common), FadeOut(common_text), run_time=FAST)

            voice_wait(tracker, NORMAL + 6 * FAST + FAST)

        with self.voiceover(
            text="Therefore, the factorized form is m minus thirteen multiplied by m minus one equals zero."
        ) as tracker:
            self.play(TransformFromCopy(row4, row5), run_time=SLOW)
            blink_box(row5, color=NEON_YELLOW, times=2)
            voice_wait(tracker, SLOW + 4 * FAST)

        self.wait(0.4)
        clear_scene()

        # ========================================================
        # SCENE 8: MORE DETAILED COMMON FACTOR ANIMATION
        # ========================================================

        header = make_title("Understanding the Common Factor")

        grouped = MathTex(
            r"m(m - 13)", r"-", r"1(m - 13)", r"= 0",
            font_size=MATH_SIZE,
            color=WHITE_TEXT
        ).next_to(header, DOWN, buff=LARGE_BUFF)

        grouped[0].set_color(NEON_GREEN)
        grouped[2].set_color(NEON_GREEN)

        first_common = MathTex(
            r"(m - 13)",
            font_size=SMALL_MATH_SIZE,
            color=NEON_PURPLE
        ).next_to(grouped, DOWN, buff=MEDIUM_BUFF)

        remaining = MathTex(
            r"\text{Remaining terms are } m \text{ and } -1",
            font_size=SMALL_MATH_SIZE,
            color=NEON_BLUE
        ).next_to(first_common, DOWN, buff=MEDIUM_BUFF)

        final = MathTex(
            r"(m - 13)(m - 1) = 0",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        ).next_to(remaining, DOWN, buff=MEDIUM_BUFF)

        scene_group = VGroup(header, grouped, first_common, remaining, final)
        fit_to_screen(scene_group)

        with self.voiceover(
            text="Let us understand this important simplification more clearly."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(grouped), run_time=NORMAL)
            voice_wait(tracker, 2 * NORMAL)

        with self.voiceover(
            text="In both terms, the same factor m minus thirteen is present."
        ) as tracker:
            blink_box(grouped[0], color=NEON_GREEN, times=1)
            blink_box(grouped[2], color=NEON_GREEN, times=1)
            voice_wait(tracker, 4 * FAST)

        with self.voiceover(
            text="So, we take m minus thirteen as a common factor."
        ) as tracker:
            self.play(Write(first_common), run_time=NORMAL)
            blink_box(first_common, color=NEON_PURPLE, times=2)
            voice_wait(tracker, NORMAL + 4 * FAST)

        with self.voiceover(
            text="After taking the common factor out, the remaining terms are m and negative one."
        ) as tracker:
            self.play(FadeIn(remaining), run_time=NORMAL if False else NORMAL)
            blink_box(remaining, color=NEON_BLUE, times=1)
            voice_wait(tracker, NORMAL + 2 * FAST)

        with self.voiceover(
            text="So the equation becomes m minus thirteen multiplied by m minus one equals zero."
        ) as tracker:
            self.play(TransformFromCopy(grouped, final), run_time=SLOW)
            blink_box(final, color=NEON_YELLOW, times=2)
            voice_wait(tracker, SLOW + 4 * FAST)

        self.wait(0.4)
        clear_scene()

        # ========================================================
        # SCENE 9: APPLY ZERO PRODUCT RULE TO EXAMPLE
        # ========================================================

        header = make_title("Apply Zero Product Rule")

        factorized_example = MathTex(
            r"(m - 13)(m - 1) = 0",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        ).next_to(header, DOWN, buff=LARGE_BUFF)

        rule = Text(
            "If product of two numbers is zero, then at least one of them is zero.",
            font_size=TEXT_SIZE,
            color=NEON_GREEN
        ).next_to(factorized_example, DOWN, buff=MEDIUM_BUFF)

        left_eq = MathTex(
            r"m - 13 = 0",
            font_size=SMALL_MATH_SIZE,
            color=NEON_BLUE
        )

        right_eq = MathTex(
            r"m - 1 = 0",
            font_size=SMALL_MATH_SIZE,
            color=NEON_BLUE
        )

        branch = VGroup(left_eq, right_eq).arrange(
            RIGHT,
            buff=1.8
        ).next_to(rule, DOWN, buff=LARGE_BUFF)

        arrow_left = Arrow(
            factorized_example.get_bottom(),
            left_eq.get_top(),
            color=NEON_PINK,
            buff=0.12
        )

        arrow_right = Arrow(
            factorized_example.get_bottom(),
            right_eq.get_top(),
            color=NEON_PINK,
            buff=0.12
        )

        sol_left = MathTex(
            r"m = 13",
            font_size=SMALL_MATH_SIZE,
            color=NEON_GREEN
        ).next_to(left_eq, DOWN, buff=MEDIUM_BUFF)

        sol_right = MathTex(
            r"m = 1",
            font_size=SMALL_MATH_SIZE,
            color=NEON_GREEN
        ).next_to(right_eq, DOWN, buff=MEDIUM_BUFF)

        roots = Text(
            "13 and 1 are the roots of the given quadratic equation.",
            font_size=TEXT_SIZE,
            color=NEON_YELLOW
        ).next_to(VGroup(sol_left, sol_right), DOWN, buff=LARGE_BUFF)

        scene_group = VGroup(
            header, factorized_example, rule, branch,
            arrow_left, arrow_right, sol_left, sol_right, roots
        )
        fit_to_screen(scene_group)

        with self.voiceover(
            text="Now apply the zero product rule to the factorized equation."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(factorized_example), run_time=NORMAL)
            blink_box(factorized_example, color=NEON_YELLOW, times=1)
            voice_wait(tracker, 2 * NORMAL + 2 * FAST)

        with self.voiceover(
            text="If product of two numbers is zero, then at least one of them is zero."
        ) as tracker:
            self.play(FadeIn(rule), run_time=NORMAL)
            blink_box(rule, color=NEON_GREEN, times=1)
            voice_wait(tracker, NORMAL + 2 * FAST)

        with self.voiceover(
            text="Therefore, m minus thirteen is zero, or m minus one is zero."
        ) as tracker:
            self.play(Create(arrow_left), Create(arrow_right), run_time=NORMAL)
            self.play(Write(left_eq), Write(right_eq), run_time=NORMAL)
            blink_box(branch, color=NEON_BLUE, times=1)
            voice_wait(tracker, 2 * NORMAL + 2 * FAST)

        with self.voiceover(
            text="Solving m minus thirteen equals zero gives m equals thirteen."
        ) as tracker:
            self.play(Write(sol_left), run_time=NORMAL)
            blink_box(sol_left, color=NEON_GREEN, times=1)
            voice_wait(tracker, NORMAL + 2 * FAST)

        with self.voiceover(
            text="Solving m minus one equals zero gives m equals one."
        ) as tracker:
            self.play(Write(sol_right), run_time=NORMAL)
            blink_box(sol_right, color=NEON_GREEN, times=1)
            voice_wait(tracker, NORMAL + 2 * FAST)

        with self.voiceover(
            text="Therefore, thirteen and one are the roots of the given quadratic equation."
        ) as tracker:
            self.play(FadeIn(roots), run_time=NORMAL)
            blink_box(roots, color=NEON_YELLOW, times=2)
            voice_wait(tracker, NORMAL + 4 * FAST)

        self.wait(0.4)
        clear_scene()

        # ========================================================
        # SCENE 10: FINAL SUMMARY
        # ========================================================

        header = make_title("Summary")

        s1 = Text(
            "Step 1: Write the quadratic equation.",
            font_size=TEXT_SIZE,
            color=WHITE_TEXT
        )

        s2 = Text(
            "Step 2: Split the middle term.",
            font_size=TEXT_SIZE,
            color=WHITE_TEXT
        )

        s3 = Text(
            "Step 3: Group the terms.",
            font_size=TEXT_SIZE,
            color=WHITE_TEXT
        )

        s4 = Text(
            "Step 4: Take common factors.",
            font_size=TEXT_SIZE,
            color=WHITE_TEXT
        )

        s5 = Text(
            "Step 5: Apply zero product rule.",
            font_size=TEXT_SIZE,
            color=WHITE_TEXT
        )

        s6 = Text(
            "Step 6: Solve the linear equations to get roots.",
            font_size=TEXT_SIZE,
            color=WHITE_TEXT
        )

        summary = VGroup(s1, s2, s3, s4, s5, s6).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=MEDIUM_BUFF
        ).next_to(header, DOWN, buff=LARGE_BUFF)

        scene_group = VGroup(header, summary)
        fit_to_screen(scene_group)

        with self.voiceover(
            text="Let us quickly revise the steps."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            voice_wait(tracker, NORMAL)

        with self.voiceover(
            text="Step one. Write the quadratic equation."
        ) as tracker:
            self.play(FadeIn(s1, shift=RIGHT), run_time=FAST)
            blink_box(s1, color=NEON_BLUE, times=1)
            voice_wait(tracker, FAST + 2 * FAST)

        with self.voiceover(
            text="Step two. Split the middle term using product and sum."
        ) as tracker:
            self.play(FadeIn(s2, shift=RIGHT), run_time=FAST)
            blink_box(s2, color=NEON_RED, times=1)
            voice_wait(tracker, FAST + 2 * FAST)

        with self.voiceover(
            text="Step three. Group the terms."
        ) as tracker:
            self.play(FadeIn(s3, shift=RIGHT), run_time=FAST)
            blink_box(s3, color=NEON_GREEN, times=1)
            voice_wait(tracker, FAST + 2 * FAST)

        with self.voiceover(
            text="Step four. Take common factors."
        ) as tracker:
            self.play(FadeIn(s4, shift=RIGHT), run_time=FAST)
            blink_box(s4, color=NEON_ORANGE, times=1)
            voice_wait(tracker, FAST + 2 * FAST)

        with self.voiceover(
            text="Step five. Apply the zero product rule."
        ) as tracker:
            self.play(FadeIn(s5, shift=RIGHT), run_time=FAST)
            blink_box(s5, color=NEON_PURPLE, times=1)
            voice_wait(tracker, FAST + 2 * FAST)

        with self.voiceover(
            text="Step six. Solve the linear equations. The answers are called the roots."
        ) as tracker:
            self.play(FadeIn(s6, shift=RIGHT), run_time=FAST)
            blink_box(s6, color=NEON_YELLOW, times=1)
            voice_wait(tracker, FAST + 2 * FAST)

        self.wait(0.4)
        clear_scene()

        # ========================================================
        # SCENE 11: END SCREEN
        # ========================================================

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

        end_group = VGroup(thanks, like, share, subscribe).arrange(
            DOWN,
            buff=MEDIUM_BUFF
        ).move_to(ORIGIN)

        subscribe_box = neon_box(subscribe, color=NEON_PINK, buff=0.18)

        with self.voiceover(
            text="Thanks for watching."
        ) as tracker:
            self.play(Write(thanks), run_time=NORMAL)
            voice_wait(tracker, NORMAL)

        with self.voiceover(
            text="Please like and share this video."
        ) as tracker:
            self.play(FadeIn(like, shift=LEFT), run_time=FAST)
            self.play(FadeIn(share, shift=RIGHT), run_time=FAST)
            voice_wait(tracker, 2 * FAST)

        with self.voiceover(
            text="Subscribe for more mathematical videos."
        ) as tracker:
            self.play(Write(subscribe), run_time=NORMAL)
            self.play(Create(subscribe_box), run_time=FAST)

            self.play(
                subscribe.animate.scale(1.12),
                subscribe_box.animate.scale(1.12),
                run_time=FAST
            )

            self.play(
                subscribe.animate.scale(1 / 1.12),
                subscribe_box.animate.scale(1 / 1.12),
                run_time=FAST
            )

            voice_wait(tracker, NORMAL + 3 * FAST)

        self.wait(2)
