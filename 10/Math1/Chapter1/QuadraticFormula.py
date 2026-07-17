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
VERY_TINY_MATH_SIZE = 25

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


class QuadraticFormulaLesson(VoiceoverScene):

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
            # Keeps content inside safe video frame
            if mob.width > SAFE_WIDTH:
                mob.scale_to_fit_width(SAFE_WIDTH)
            if mob.height > SAFE_HEIGHT:
                mob.scale_to_fit_height(SAFE_HEIGHT)
            return mob

        def make_title(text):
            # Creates title at top
            title = Text(
                text,
                font_size=TITLE_SIZE,
                color=NEON_PINK
            )
            title.to_edge(UP)
            return title

        def neon_box(mob, color=NEON_YELLOW, buff=0.12):
            # Creates a neon rectangle around an object
            return SurroundingRectangle(
                mob,
                color=color,
                buff=buff,
                stroke_width=3
            )

        def blink_box(mob, color=NEON_YELLOW, times=2, buff=0.12):
            # Blinking highlight animation
            for index in range(times):
                box = neon_box(mob, color=color, buff=buff)
                self.play(Create(box), run_time=FAST)
                self.play(FadeOut(box), run_time=FAST)

        def clear_scene():
            # Clears complete screen at once
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
            # Waits until voiceover finishes
            remaining = tracker.duration - used_time

            if remaining > 0:
                self.wait(remaining + MIN_WAIT)
            else:
                self.wait(MIN_WAIT)

        def make_step_row(equation_tex, comment_text, equation_color=WHITE_TEXT, comment_color=NEON_BLUE):
            # Creates one derivation row with a supporting comment on right side
            equation = MathTex(
                equation_tex,
                font_size=TINY_MATH_SIZE,
                color=equation_color
            )

            comment = Text(
                comment_text,
                font_size=SMALL_TEXT_SIZE,
                color=comment_color
            )

            row = VGroup(equation, comment)
            row.arrange(RIGHT, buff=MEDIUM_BUFF)
            return row

        # ============================================================
        # SCENE 1: OPENING TITLE
        # ============================================================

        title = Text(
            "Formula for Solving a Quadratic Equation",
            font_size=TITLE_SIZE,
            color=NEON_PINK
        )

        subtitle = Text(
            "Derivation, formula, and solved example",
            font_size=TEXT_SIZE,
            color=NEON_BLUE
        )
        subtitle.next_to(title, DOWN, buff=MEDIUM_BUFF)

        opening_group = VGroup(title, subtitle)
        opening_group.move_to([0, 0, 0])

        with self.voiceover(
            text="Welcome. In this lesson, we will derive the formula for solving a quadratic equation."
        ) as tracker:
            self.play(Write(title), run_time=NORMAL)
            sync_wait(tracker, NORMAL)

        with self.voiceover(
            text="After deriving the formula step by step, we will solve one example using the formula."
        ) as tracker:
            self.play(FadeIn(subtitle, shift=UP), run_time=NORMAL)
            sync_wait(tracker, NORMAL)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 2: WHAT IS THE GENERAL QUADRATIC EQUATION?
        # ============================================================

        header = make_title("General Quadratic Equation")

        eq_general = MathTex(
            r"ax^2 + bx + c = 0",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        )
        eq_general.next_to(header, DOWN, buff=LARGE_BUFF)

        condition = MathTex(
            r"a \ne 0",
            font_size=MATH_SIZE,
            color=NEON_RED
        )
        condition.next_to(eq_general, DOWN, buff=MEDIUM_BUFF)

        meaning = Text(
            "Here a, b, and c are constants, and a must not be zero.",
            font_size=TEXT_SIZE,
            color=WHITE_TEXT
        )
        meaning.next_to(condition, DOWN, buff=MEDIUM_BUFF)

        goal = Text(
            "Our goal is to find the values of x which satisfy this equation.",
            font_size=TEXT_SIZE,
            color=NEON_GREEN
        )
        goal.next_to(meaning, DOWN, buff=MEDIUM_BUFF)

        scene_group = VGroup(header, eq_general, condition, meaning, goal)
        fit_to_screen(scene_group)

        with self.voiceover(
            text="The general quadratic equation is a x squared plus b x plus c equals zero."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(eq_general), run_time=NORMAL)
            blink_box(eq_general, color=NEON_YELLOW, times=1)
            sync_wait(tracker, 2.0)

        with self.voiceover(
            text="Here, a must not be zero. Otherwise the equation will not remain quadratic."
        ) as tracker:
            self.play(Write(condition), run_time=NORMAL)
            blink_box(condition, color=NEON_RED, times=1)
            sync_wait(tracker, 1.9)

        with self.voiceover(
            text="The constants are a, b, and c. Our goal is to find the values of x."
        ) as tracker:
            self.play(FadeIn(meaning), run_time=NORMAL)
            self.play(FadeIn(goal), run_time=NORMAL)
            blink_box(goal, color=NEON_GREEN, times=1)
            sync_wait(tracker, 2.2)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 3: PLAN OF DERIVATION
        # ============================================================

        header = make_title("Plan of Derivation")

        plan1 = Text(
            "1. Divide by a to make coefficient of x squared equal to 1.",
            font_size=SMALL_TEXT_SIZE,
            color=WHITE_TEXT
        )

        plan2 = Text(
            "2. Complete the square using x squared plus bx form.",
            font_size=SMALL_TEXT_SIZE,
            color=WHITE_TEXT
        )

        plan3 = Text(
            "3. Move all constants to the right side.",
            font_size=SMALL_TEXT_SIZE,
            color=WHITE_TEXT
        )

        plan4 = Text(
            "4. Take square root on both sides.",
            font_size=SMALL_TEXT_SIZE,
            color=WHITE_TEXT
        )

        plan5 = Text(
            "5. Simplify to get the quadratic formula.",
            font_size=SMALL_TEXT_SIZE,
            color=NEON_GREEN
        )

        identity = MathTex(
            r"(p+q)^2 = p^2 + 2pq + q^2",
            font_size=SMALL_MATH_SIZE,
            color=NEON_PURPLE
        )

        plan_group = VGroup(plan1, plan2, plan3, plan4, plan5, identity)
        plan_group.arrange(DOWN, aligned_edge=LEFT, buff=MEDIUM_BUFF)
        plan_group.next_to(header, DOWN, buff=LARGE_BUFF)

        all_group = VGroup(header, plan_group)
        fit_to_screen(all_group)

        with self.voiceover(
            text="Before deriving the formula, let us understand the plan."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            sync_wait(tracker, NORMAL)

        with self.voiceover(
            text="First, divide by a, so that the coefficient of x squared becomes one."
        ) as tracker:
            self.play(FadeIn(plan1, shift=RIGHT), run_time=FAST)
            blink_box(plan1, color=NEON_BLUE, times=1)
            sync_wait(tracker, 1.7)

        with self.voiceover(
            text="Second, complete the square. This means we will convert part of the expression into a perfect square."
        ) as tracker:
            self.play(FadeIn(plan2, shift=RIGHT), run_time=FAST)
            blink_box(plan2, color=NEON_GREEN, times=1)
            sync_wait(tracker, 2.0)

        with self.voiceover(
            text="Then we will move constants to the right side, take square root, and simplify."
        ) as tracker:
            self.play(FadeIn(plan3, shift=RIGHT), run_time=FAST)
            self.play(FadeIn(plan4, shift=RIGHT), run_time=FAST)
            self.play(FadeIn(plan5, shift=RIGHT), run_time=FAST)
            sync_wait(tracker, 2.0)

        with self.voiceover(
            text="The supporting identity is p plus q whole square equals p squared plus two p q plus q squared."
        ) as tracker:
            self.play(Write(identity), run_time=NORMAL)
            blink_box(identity, color=NEON_PURPLE, times=1)
            sync_wait(tracker, 2.2)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 4: DERIVATION STEP 1
        # ============================================================

        header = make_title("Derivation: Start with Standard Form")

        row1 = make_step_row(
            r"ax^2 + bx + c = 0",
            ".... standard quadratic equation",
            equation_color=NEON_YELLOW,
            comment_color=NEON_BLUE
        )
        row1.next_to(header, DOWN, buff=LARGE_BUFF)

        row2 = make_step_row(
            r"x^2 + \frac{b}{a}x + \frac{c}{a} = 0",
            ".... divide every term by a",
            equation_color=WHITE_TEXT,
            comment_color=NEON_ORANGE
        )
        row2.next_to(row1, DOWN, buff=MEDIUM_BUFF)

        row3 = make_step_row(
            r"x^2 + \frac{b}{a}x = -\frac{c}{a}",
            ".... move constant term to right side",
            equation_color=WHITE_TEXT,
            comment_color=NEON_GREEN
        )
        row3.next_to(row2, DOWN, buff=MEDIUM_BUFF)

        screen_group = VGroup(header, row1, row2, row3)
        fit_to_screen(screen_group)

        with self.voiceover(
            text="We start with the standard quadratic equation, a x squared plus b x plus c equals zero."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(row1), run_time=NORMAL)
            blink_box(row1, color=NEON_YELLOW, times=1)
            sync_wait(tracker, 2.1)

        with self.voiceover(
            text="Now divide every term by a. This makes the coefficient of x squared equal to one."
        ) as tracker:
            self.play(TransformFromCopy(row1, row2), run_time=SLOW)
            blink_box(row2, color=NEON_ORANGE, times=1)
            sync_wait(tracker, 2.2)

        with self.voiceover(
            text="Now move c by a to the right side. So the left side has only x squared and the x term."
        ) as tracker:
            self.play(TransformFromCopy(row2, row3), run_time=SLOW)
            blink_box(row3, color=NEON_GREEN, times=1)
            sync_wait(tracker, 2.3)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 5: DERIVATION STEP 2 COMPLETE THE SQUARE
        # ============================================================

        header = make_title("Derivation: Complete the Square")

        formula_note = MathTex(
            r"x^2 + 2px + p^2 = (x+p)^2",
            font_size=SMALL_MATH_SIZE,
            color=NEON_PURPLE
        )
        formula_note.next_to(header, DOWN, buff=MEDIUM_BUFF)

        row1 = make_step_row(
            r"x^2 + \frac{b}{a}x = -\frac{c}{a}",
            ".... compare with x squared plus 2px",
            equation_color=WHITE_TEXT,
            comment_color=NEON_BLUE
        )
        row1.next_to(formula_note, DOWN, buff=MEDIUM_BUFF)

        row2 = make_step_row(
            r"2p = \frac{b}{a},\quad p = \frac{b}{2a}",
            ".... half of coefficient of x",
            equation_color=NEON_YELLOW,
            comment_color=NEON_ORANGE
        )
        row2.next_to(row1, DOWN, buff=MEDIUM_BUFF)

        row3 = make_step_row(
            r"p^2 = \left(\frac{b}{2a}\right)^2",
            ".... square the half coefficient",
            equation_color=NEON_GREEN,
            comment_color=NEON_GREEN
        )
        row3.next_to(row2, DOWN, buff=MEDIUM_BUFF)

        row4 = make_step_row(
            r"x^2 + \frac{b}{a}x + \left(\frac{b}{2a}\right)^2 = -\frac{c}{a} + \left(\frac{b}{2a}\right)^2",
            ".... add same square to both sides",
            equation_color=WHITE_TEXT,
            comment_color=NEON_ORANGE
        )
        row4.next_to(row3, DOWN, buff=MEDIUM_BUFF)

        screen_group = VGroup(header, formula_note, row1, row2, row3, row4)
        fit_to_screen(screen_group)

        with self.voiceover(
            text="To complete the square, we use this form: x squared plus two p x plus p squared equals x plus p whole square."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(formula_note), run_time=NORMAL)
            blink_box(formula_note, color=NEON_PURPLE, times=1)
            sync_wait(tracker, 2.3)

        with self.voiceover(
            text="Now compare x squared plus b by a x with x squared plus two p x."
        ) as tracker:
            self.play(Write(row1), run_time=NORMAL)
            blink_box(row1, color=NEON_BLUE, times=1)
            sync_wait(tracker, 2.0)

        with self.voiceover(
            text="So two p is equal to b by a. Therefore p is equal to b by two a."
        ) as tracker:
            self.play(TransformFromCopy(row1, row2), run_time=SLOW)
            blink_box(row2, color=NEON_YELLOW, times=1)
            sync_wait(tracker, 2.2)

        with self.voiceover(
            text="Now square p. So p squared is b by two a whole square."
        ) as tracker:
            self.play(TransformFromCopy(row2, row3), run_time=NORMAL)
            blink_box(row3, color=NEON_GREEN, times=1)
            sync_wait(tracker, 2.0)

        with self.voiceover(
            text="Add this square value to both sides, because we are working with an equation."
        ) as tracker:
            self.play(TransformFromCopy(row3, row4), run_time=SLOW)
            blink_box(row4, color=NEON_ORANGE, times=1)
            sync_wait(tracker, 2.2)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 6: DERIVATION STEP 3 SIMPLIFY LEFT SIDE
        # ============================================================

        header = make_title("Derivation: Convert to Perfect Square")

        identity = MathTex(
            r"x^2 + 2px + p^2 = (x+p)^2",
            font_size=SMALL_MATH_SIZE,
            color=NEON_PURPLE
        )
        identity.next_to(header, DOWN, buff=MEDIUM_BUFF)

        row1 = make_step_row(
            r"x^2 + \frac{b}{a}x + \left(\frac{b}{2a}\right)^2 = -\frac{c}{a} + \left(\frac{b}{2a}\right)^2",
            ".... completed square form",
            equation_color=WHITE_TEXT,
            comment_color=NEON_BLUE
        )
        row1.next_to(identity, DOWN, buff=MEDIUM_BUFF)

        row2 = make_step_row(
            r"\left(x + \frac{b}{2a}\right)^2 = -\frac{c}{a} + \frac{b^2}{4a^2}",
            ".... left side becomes perfect square",
            equation_color=NEON_GREEN,
            comment_color=NEON_GREEN
        )
        row2.next_to(row1, DOWN, buff=MEDIUM_BUFF)

        row3 = make_step_row(
            r"\left(x + \frac{b}{2a}\right)^2 = \frac{-4ac}{4a^2} + \frac{b^2}{4a^2}",
            ".... make common denominator 4a squared",
            equation_color=WHITE_TEXT,
            comment_color=NEON_ORANGE
        )
        row3.next_to(row2, DOWN, buff=MEDIUM_BUFF)

        row4 = make_step_row(
            r"\left(x + \frac{b}{2a}\right)^2 = \frac{b^2 - 4ac}{4a^2}",
            ".... combine fractions",
            equation_color=NEON_YELLOW,
            comment_color=NEON_YELLOW
        )
        row4.next_to(row3, DOWN, buff=MEDIUM_BUFF)

        screen_group = VGroup(header, identity, row1, row2, row3, row4)
        fit_to_screen(screen_group)

        with self.voiceover(
            text="Now we convert the left side into a perfect square using the identity."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(identity), run_time=NORMAL)
            blink_box(identity, color=NEON_PURPLE, times=1)
            sync_wait(tracker, 2.0)

        with self.voiceover(
            text="This completed expression is now ready to become x plus b by two a whole square."
        ) as tracker:
            self.play(Write(row1), run_time=NORMAL)
            blink_box(row1, color=NEON_BLUE, times=1)
            sync_wait(tracker, 2.2)

        with self.voiceover(
            text="The left side becomes x plus b by two a whole square."
        ) as tracker:
            self.play(TransformFromCopy(row1, row2), run_time=SLOW)
            blink_box(row2, color=NEON_GREEN, times=2)
            sync_wait(tracker, 2.1)

        with self.voiceover(
            text="Now simplify the right side using common denominator four a squared."
        ) as tracker:
            self.play(TransformFromCopy(row2, row3), run_time=SLOW)
            blink_box(row3, color=NEON_ORANGE, times=1)
            sync_wait(tracker, 2.2)

        with self.voiceover(
            text="After combining, we get b squared minus four a c divided by four a squared."
        ) as tracker:
            self.play(TransformFromCopy(row3, row4), run_time=NORMAL)
            blink_box(row4, color=NEON_YELLOW, times=2)
            sync_wait(tracker, 2.2)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 7: DERIVATION STEP 4 TAKE SQUARE ROOT
        # ============================================================

        header = make_title("Derivation: Take Square Root")

        root_rule = MathTex(
            r"\text{If } A^2 = B,\text{ then } A = \pm \sqrt{B}",
            font_size=SMALL_MATH_SIZE,
            color=NEON_PURPLE
        )
        root_rule.next_to(header, DOWN, buff=MEDIUM_BUFF)

        row1 = make_step_row(
            r"\left(x + \frac{b}{2a}\right)^2 = \frac{b^2 - 4ac}{4a^2}",
            ".... square form obtained",
            equation_color=NEON_YELLOW,
            comment_color=NEON_BLUE
        )
        row1.next_to(root_rule, DOWN, buff=MEDIUM_BUFF)

        row2 = make_step_row(
            r"x + \frac{b}{2a} = \pm \sqrt{\frac{b^2 - 4ac}{4a^2}}",
            ".... take square root on both sides",
            equation_color=WHITE_TEXT,
            comment_color=NEON_ORANGE
        )
        row2.next_to(row1, DOWN, buff=MEDIUM_BUFF)

        row3 = make_step_row(
            r"x + \frac{b}{2a} = \pm \frac{\sqrt{b^2 - 4ac}}{2a}",
            ".... square root of 4a squared is 2a",
            equation_color=NEON_GREEN,
            comment_color=NEON_GREEN
        )
        row3.next_to(row2, DOWN, buff=MEDIUM_BUFF)

        row4 = make_step_row(
            r"x = -\frac{b}{2a} \pm \frac{\sqrt{b^2 - 4ac}}{2a}",
            ".... subtract b by 2a from both sides",
            equation_color=WHITE_TEXT,
            comment_color=NEON_BLUE
        )
        row4.next_to(row3, DOWN, buff=MEDIUM_BUFF)

        row5 = make_step_row(
            r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
            ".... combine into one fraction",
            equation_color=NEON_YELLOW,
            comment_color=NEON_YELLOW
        )
        row5.next_to(row4, DOWN, buff=MEDIUM_BUFF)

        screen_group = VGroup(header, root_rule, row1, row2, row3, row4, row5)
        fit_to_screen(screen_group)

        with self.voiceover(
            text="Now we take square root on both sides. We use this rule."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(root_rule), run_time=NORMAL)
            blink_box(root_rule, color=NEON_PURPLE, times=1)
            sync_wait(tracker, 2.0)

        with self.voiceover(
            text="Start with the square form obtained in the previous step."
        ) as tracker:
            self.play(Write(row1), run_time=NORMAL)
            blink_box(row1, color=NEON_YELLOW, times=1)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="Taking square root gives plus or minus square root of the right side."
        ) as tracker:
            self.play(TransformFromCopy(row1, row2), run_time=SLOW)
            blink_box(row2, color=NEON_ORANGE, times=1)
            sync_wait(tracker, 2.2)

        with self.voiceover(
            text="Square root of four a squared is two a, so the right side simplifies."
        ) as tracker:
            self.play(TransformFromCopy(row2, row3), run_time=SLOW)
            blink_box(row3, color=NEON_GREEN, times=1)
            sync_wait(tracker, 2.2)

        with self.voiceover(
            text="Now subtract b by two a from both sides."
        ) as tracker:
            self.play(TransformFromCopy(row3, row4), run_time=NORMAL)
            blink_box(row4, color=NEON_BLUE, times=1)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="Finally combine the two fractions. This gives the quadratic formula."
        ) as tracker:
            self.play(TransformFromCopy(row4, row5), run_time=SLOW)
            blink_box(row5, color=NEON_YELLOW, times=2)
            sync_wait(tracker, 2.2)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 8: FINAL FORMULA
        # ============================================================

        header = make_title("Quadratic Formula")

        formula = MathTex(
            r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
            font_size=44,
            color=NEON_YELLOW
        )
        formula.next_to(header, DOWN, buff=LARGE_BUFF)

        note1 = Text(
            "This formula gives the two roots of ax squared plus bx plus c equals 0.",
            font_size=TEXT_SIZE,
            color=NEON_GREEN
        )
        note1.next_to(formula, DOWN, buff=LARGE_BUFF)

        discriminant = MathTex(
            r"D = b^2 - 4ac",
            font_size=MATH_SIZE,
            color=NEON_PURPLE
        )
        discriminant.next_to(note1, DOWN, buff=MEDIUM_BUFF)

        note2 = Text(
            "The expression inside the square root is called the discriminant.",
            font_size=SMALL_TEXT_SIZE,
            color=WHITE_TEXT
        )
        note2.next_to(discriminant, DOWN, buff=MEDIUM_BUFF)

        scene_group = VGroup(header, formula, note1, discriminant, note2)
        fit_to_screen(scene_group)

        with self.voiceover(
            text="Therefore, the formula for solving a quadratic equation is x equals negative b plus or minus square root of b squared minus four a c, divided by two a."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(formula), run_time=SLOW)
            blink_box(formula, color=NEON_YELLOW, times=2)
            sync_wait(tracker, 3.0)

        with self.voiceover(
            text="This formula gives the roots of a x squared plus b x plus c equals zero."
        ) as tracker:
            self.play(FadeIn(note1), run_time=NORMAL)
            blink_box(note1, color=NEON_GREEN, times=1)
            sync_wait(tracker, 2.0)

        with self.voiceover(
            text="The expression b squared minus four a c is called the discriminant."
        ) as tracker:
            self.play(Write(discriminant), run_time=NORMAL)
            self.play(FadeIn(note2), run_time=NORMAL)
            blink_box(discriminant, color=NEON_PURPLE, times=1)
            sync_wait(tracker, 2.2)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 9: ALL FORMULA SIMPLIFICATION STEPS ON SINGLE SCREEN
        # ============================================================

        header = make_title("Formula Derivation on One Screen")

        line1 = MathTex(
            r"ax^2 + bx + c = 0",
            font_size=VERY_TINY_MATH_SIZE,
            color=NEON_YELLOW
        )

        line2 = MathTex(
            r"x^2 + \frac{b}{a}x + \frac{c}{a} = 0",
            font_size=VERY_TINY_MATH_SIZE,
            color=WHITE_TEXT
        )

        line3 = MathTex(
            r"x^2 + \frac{b}{a}x = -\frac{c}{a}",
            font_size=VERY_TINY_MATH_SIZE,
            color=WHITE_TEXT
        )

        line4 = MathTex(
            r"x^2 + \frac{b}{a}x + \left(\frac{b}{2a}\right)^2 = -\frac{c}{a} + \left(\frac{b}{2a}\right)^2",
            font_size=VERY_TINY_MATH_SIZE,
            color=WHITE_TEXT
        )

        line5 = MathTex(
            r"\left(x + \frac{b}{2a}\right)^2 = \frac{b^2 - 4ac}{4a^2}",
            font_size=VERY_TINY_MATH_SIZE,
            color=NEON_GREEN
        )

        line6 = MathTex(
            r"x + \frac{b}{2a} = \pm \frac{\sqrt{b^2 - 4ac}}{2a}",
            font_size=VERY_TINY_MATH_SIZE,
            color=NEON_BLUE
        )

        line7 = MathTex(
            r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
            font_size=SMALL_MATH_SIZE,
            color=NEON_YELLOW
        )

        all_lines = VGroup(line1, line2, line3, line4, line5, line6, line7)
        all_lines.arrange(DOWN, aligned_edge=LEFT, buff=SMALL_BUFF)
        all_lines.next_to(header, DOWN, buff=MEDIUM_BUFF)

        note = Text(
            ".... These are the complete simplification steps used to derive the formula.",
            font_size=SMALL_TEXT_SIZE,
            color=NEON_GREEN
        )
        note.next_to(all_lines, DOWN, buff=MEDIUM_BUFF)

        screen_group = VGroup(header, all_lines, note)
        fit_to_screen(screen_group)

        with self.voiceover(
            text="Now let us see all formula simplification steps together on one screen."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            sync_wait(tracker, NORMAL)

        with self.voiceover(
            text="These are the complete steps, from standard form to the final quadratic formula."
        ) as tracker:
            self.play(FadeIn(all_lines, shift=RIGHT), run_time=SLOW)
            self.play(FadeIn(note), run_time=NORMAL)
            blink_box(line7, color=NEON_YELLOW, times=2)
            sync_wait(tracker, 2.6)

        self.wait(1.0)
        clear_scene()

        # ============================================================
        # SCENE 10: PROBLEM INTRODUCTION
        # ============================================================

        header = make_title("Solved Example")

        problem = MathTex(
            r"m^2 - 14m + 13 = 0",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        )
        problem.next_to(header, DOWN, buff=LARGE_BUFF)

        formula = MathTex(
            r"m = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
            font_size=MATH_SIZE,
            color=NEON_GREEN
        )
        formula.next_to(problem, DOWN, buff=LARGE_BUFF)

        note = Text(
            "We compare the equation with ax squared plus bx plus c equals 0.",
            font_size=TEXT_SIZE,
            color=NEON_BLUE
        )
        note.next_to(formula, DOWN, buff=MEDIUM_BUFF)

        scene_group = VGroup(header, problem, formula, note)
        fit_to_screen(scene_group)

        with self.voiceover(
            text="Now let us solve one example using the quadratic formula."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            sync_wait(tracker, NORMAL)

        with self.voiceover(
            text="Solve m squared minus fourteen m plus thirteen equals zero."
        ) as tracker:
            self.play(Write(problem), run_time=NORMAL)
            blink_box(problem, color=NEON_YELLOW, times=1)
            sync_wait(tracker, 1.9)

        with self.voiceover(
            text="We will use the formula m equals negative b plus or minus square root of b squared minus four a c divided by two a."
        ) as tracker:
            self.play(Write(formula), run_time=NORMAL)
            blink_box(formula, color=NEON_GREEN, times=1)
            sync_wait(tracker, 2.6)

        with self.voiceover(
            text="Now compare the equation with a x squared plus b x plus c equals zero."
        ) as tracker:
            self.play(FadeIn(note), run_time=NORMAL)
            blink_box(note, color=NEON_BLUE, times=1)
            sync_wait(tracker, 2.0)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 11: IDENTIFY a, b, c
        # ============================================================

        header = make_title("Step 1: Identify a, b, and c")

        compare = MathTex(
            r"m^2 - 14m + 13 = 0",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        )
        compare.next_to(header, DOWN, buff=MEDIUM_BUFF)

        standard = MathTex(
            r"ax^2 + bx + c = 0",
            font_size=SMALL_MATH_SIZE,
            color=NEON_PURPLE
        )
        standard.next_to(compare, DOWN, buff=MEDIUM_BUFF)

        values = MathTex(
            r"a = 1,\quad b = -14,\quad c = 13",
            font_size=MATH_SIZE,
            color=NEON_GREEN
        )
        values.next_to(standard, DOWN, buff=LARGE_BUFF)

        note = Text(
            ".... coefficient of m squared is 1, coefficient of m is -14, constant is 13",
            font_size=SMALL_TEXT_SIZE,
            color=WHITE_TEXT
        )
        note.next_to(values, DOWN, buff=MEDIUM_BUFF)

        scene_group = VGroup(header, compare, standard, values, note)
        fit_to_screen(scene_group)

        with self.voiceover(
            text="First identify the values of a, b, and c."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            sync_wait(tracker, NORMAL)

        with self.voiceover(
            text="Compare m squared minus fourteen m plus thirteen equals zero with the standard form."
        ) as tracker:
            self.play(Write(compare), run_time=NORMAL)
            self.play(Write(standard), run_time=NORMAL)
            blink_box(VGroup(compare, standard), color=NEON_PURPLE, times=1)
            sync_wait(tracker, 2.2)

        with self.voiceover(
            text="So a is one, b is negative fourteen, and c is thirteen."
        ) as tracker:
            self.play(Write(values), run_time=NORMAL)
            self.play(FadeIn(note), run_time=NORMAL)
            blink_box(values, color=NEON_GREEN, times=2)
            sync_wait(tracker, 2.2)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 12: FIND DISCRIMINANT
        # ============================================================

        header = make_title("Step 2: Find Discriminant")

        d_formula = MathTex(
            r"D = b^2 - 4ac",
            font_size=MATH_SIZE,
            color=NEON_PURPLE
        )
        d_formula.next_to(header, DOWN, buff=MEDIUM_BUFF)

        d_sub = MathTex(
            r"D = (-14)^2 - 4(1)(13)",
            font_size=MATH_SIZE,
            color=WHITE_TEXT
        )
        d_sub.next_to(d_formula, DOWN, buff=MEDIUM_BUFF)

        d_calc = MathTex(
            r"D = 196 - 52",
            font_size=MATH_SIZE,
            color=WHITE_TEXT
        )
        d_calc.next_to(d_sub, DOWN, buff=MEDIUM_BUFF)

        d_result = MathTex(
            r"D = 144",
            font_size=MATH_SIZE,
            color=NEON_GREEN
        )
        d_result.next_to(d_calc, DOWN, buff=MEDIUM_BUFF)

        note = Text(
            ".... discriminant tells what is inside the square root",
            font_size=SMALL_TEXT_SIZE,
            color=NEON_BLUE
        )
        note.next_to(d_result, DOWN, buff=MEDIUM_BUFF)

        scene_group = VGroup(header, d_formula, d_sub, d_calc, d_result, note)
        fit_to_screen(scene_group)

        with self.voiceover(
            text="Now find the discriminant. The discriminant is b squared minus four a c."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(d_formula), run_time=NORMAL)
            blink_box(d_formula, color=NEON_PURPLE, times=1)
            sync_wait(tracker, 2.1)

        with self.voiceover(
            text="Substitute b equals negative fourteen, a equals one, and c equals thirteen."
        ) as tracker:
            self.play(TransformFromCopy(d_formula, d_sub), run_time=NORMAL)
            blink_box(d_sub, color=NEON_BLUE, times=1)
            sync_wait(tracker, 2.2)

        with self.voiceover(
            text="Negative fourteen squared is one hundred ninety six, and four into one into thirteen is fifty two."
        ) as tracker:
            self.play(TransformFromCopy(d_sub, d_calc), run_time=NORMAL)
            blink_box(d_calc, color=NEON_ORANGE, times=1)
            sync_wait(tracker, 2.4)

        with self.voiceover(
            text="Therefore, the discriminant is one hundred forty four."
        ) as tracker:
            self.play(TransformFromCopy(d_calc, d_result), run_time=NORMAL)
            self.play(FadeIn(note), run_time=NORMAL)
            blink_box(d_result, color=NEON_GREEN, times=2)
            sync_wait(tracker, 2.0)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 13: SUBSTITUTE IN FORMULA
        # ============================================================

        header = make_title("Step 3: Substitute in Formula")

        formula = MathTex(
            r"m = \frac{-b \pm \sqrt{D}}{2a}",
            font_size=MATH_SIZE,
            color=NEON_PURPLE
        )
        formula.next_to(header, DOWN, buff=MEDIUM_BUFF)

        sub1 = MathTex(
            r"m = \frac{-(-14) \pm \sqrt{144}}{2(1)}",
            font_size=MATH_SIZE,
            color=WHITE_TEXT
        )
        sub1.next_to(formula, DOWN, buff=MEDIUM_BUFF)

        sub2 = MathTex(
            r"m = \frac{14 \pm 12}{2}",
            font_size=MATH_SIZE,
            color=NEON_GREEN
        )
        sub2.next_to(sub1, DOWN, buff=MEDIUM_BUFF)

        note1 = Text(
            ".... negative of negative fourteen becomes positive fourteen",
            font_size=SMALL_TEXT_SIZE,
            color=NEON_BLUE
        )
        note1.next_to(sub2, DOWN, buff=SMALL_BUFF)

        note2 = Text(
            ".... square root of 144 is 12",
            font_size=SMALL_TEXT_SIZE,
            color=NEON_ORANGE
        )
        note2.next_to(note1, DOWN, buff=SMALL_BUFF)

        scene_group = VGroup(header, formula, sub1, sub2, note1, note2)
        fit_to_screen(scene_group)

        with self.voiceover(
            text="Now substitute the values in the quadratic formula."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(formula), run_time=NORMAL)
            blink_box(formula, color=NEON_PURPLE, times=1)
            sync_wait(tracker, 2.0)

        with self.voiceover(
            text="Put b equals negative fourteen, discriminant equals one hundred forty four, and a equals one."
        ) as tracker:
            self.play(TransformFromCopy(formula, sub1), run_time=SLOW)
            blink_box(sub1, color=NEON_BLUE, times=1)
            sync_wait(tracker, 2.4)

        with self.voiceover(
            text="Negative of negative fourteen becomes positive fourteen, and square root of one hundred forty four is twelve."
        ) as tracker:
            self.play(TransformFromCopy(sub1, sub2), run_time=SLOW)
            self.play(FadeIn(note1), run_time=NORMAL)
            self.play(FadeIn(note2), run_time=NORMAL)
            blink_box(sub2, color=NEON_GREEN, times=2)
            sync_wait(tracker, 2.8)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 14: SPLIT PLUS AND MINUS ROOTS
        # ============================================================

        header = make_title("Step 4: Get the Two Roots")

        base = MathTex(
            r"m = \frac{14 \pm 12}{2}",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        )
        base.next_to(header, DOWN, buff=LARGE_BUFF)

        plus_case = MathTex(
            r"m = \frac{14 + 12}{2} = \frac{26}{2} = 13",
            font_size=SMALL_MATH_SIZE,
            color=NEON_GREEN
        )
        plus_case.next_to(base, DOWN, buff=LARGE_BUFF)

        minus_case = MathTex(
            r"m = \frac{14 - 12}{2} = \frac{2}{2} = 1",
            font_size=SMALL_MATH_SIZE,
            color=NEON_GREEN
        )
        minus_case.next_to(plus_case, DOWN, buff=MEDIUM_BUFF)

        note = Text(
            ".... plus sign gives one root, minus sign gives the other root",
            font_size=SMALL_TEXT_SIZE,
            color=NEON_BLUE
        )
        note.next_to(minus_case, DOWN, buff=MEDIUM_BUFF)

        scene_group = VGroup(header, base, plus_case, minus_case, note)
        fit_to_screen(scene_group)

        with self.voiceover(
            text="Now we separate the plus and minus cases."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(base), run_time=NORMAL)
            blink_box(base, color=NEON_YELLOW, times=1)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="Using the plus sign, m equals fourteen plus twelve divided by two, which is thirteen."
        ) as tracker:
            self.play(TransformFromCopy(base, plus_case), run_time=SLOW)
            blink_box(plus_case, color=NEON_GREEN, times=2)
            sync_wait(tracker, 2.4)

        with self.voiceover(
            text="Using the minus sign, m equals fourteen minus twelve divided by two, which is one."
        ) as tracker:
            self.play(TransformFromCopy(base, minus_case), run_time=SLOW)
            self.play(FadeIn(note), run_time=NORMAL)
            blink_box(minus_case, color=NEON_GREEN, times=2)
            sync_wait(tracker, 2.4)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 15: COMPLETE SOLUTION ON ONE SCREEN
        # ============================================================

        header = make_title("Complete Solution on One Screen")

        line1 = MathTex(
            r"m^2 - 14m + 13 = 0",
            font_size=VERY_TINY_MATH_SIZE,
            color=NEON_YELLOW
        )

        line2 = MathTex(
            r"a = 1,\quad b = -14,\quad c = 13",
            font_size=VERY_TINY_MATH_SIZE,
            color=WHITE_TEXT
        )

        line3 = MathTex(
            r"D = b^2 - 4ac = (-14)^2 - 4(1)(13)",
            font_size=VERY_TINY_MATH_SIZE,
            color=WHITE_TEXT
        )

        line4 = MathTex(
            r"D = 196 - 52 = 144",
            font_size=VERY_TINY_MATH_SIZE,
            color=NEON_GREEN
        )

        line5 = MathTex(
            r"m = \frac{-b \pm \sqrt{D}}{2a}",
            font_size=VERY_TINY_MATH_SIZE,
            color=NEON_PURPLE
        )

        line6 = MathTex(
            r"m = \frac{-(-14) \pm \sqrt{144}}{2(1)}",
            font_size=VERY_TINY_MATH_SIZE,
            color=WHITE_TEXT
        )

        line7 = MathTex(
            r"m = \frac{14 \pm 12}{2}",
            font_size=VERY_TINY_MATH_SIZE,
            color=WHITE_TEXT
        )

        line8 = MathTex(
            r"m = \frac{14 + 12}{2} = 13,\quad m = \frac{14 - 12}{2} = 1",
            font_size=VERY_TINY_MATH_SIZE,
            color=NEON_GREEN
        )

        line9 = Text(
            "Therefore, 13 and 1 are roots of the equation.",
            font_size=SMALL_TEXT_SIZE,
            color=NEON_YELLOW
        )

        solution_lines = VGroup(line1, line2, line3, line4, line5, line6, line7, line8, line9)
        solution_lines.arrange(DOWN, aligned_edge=LEFT, buff=SMALL_BUFF)
        solution_lines.next_to(header, DOWN, buff=MEDIUM_BUFF)

        screen_group = VGroup(header, solution_lines)
        fit_to_screen(screen_group)

        with self.voiceover(
            text="Now let us see the entire solution on one screen."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            sync_wait(tracker, NORMAL)

        with self.voiceover(
            text="The values of a, b, and c are substituted into the formula and simplified to get the two roots."
        ) as tracker:
            self.play(FadeIn(solution_lines, shift=RIGHT), run_time=SLOW)
            blink_box(line8, color=NEON_GREEN, times=2)
            blink_box(line9, color=NEON_YELLOW, times=1)
            sync_wait(tracker, 3.0)

        self.wait(1.0)
        clear_scene()

        # ============================================================
        # SCENE 16: SUMMARY
        # ============================================================

        header = make_title("Summary")

        s1 = Text(
            "1. Start with ax squared plus bx plus c equals 0.",
            font_size=TEXT_SIZE,
            color=WHITE_TEXT
        )

        s2 = Text(
            "2. Divide by a and complete the square.",
            font_size=TEXT_SIZE,
            color=WHITE_TEXT
        )

        s3 = Text(
            "3. Take square root on both sides.",
            font_size=TEXT_SIZE,
            color=WHITE_TEXT
        )

        s4 = Text(
            "4. Simplify to get the quadratic formula.",
            font_size=TEXT_SIZE,
            color=NEON_GREEN
        )

        s5 = MathTex(
            r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        )

        summary = VGroup(s1, s2, s3, s4, s5)
        summary.arrange(DOWN, aligned_edge=LEFT, buff=MEDIUM_BUFF)
        summary.next_to(header, DOWN, buff=LARGE_BUFF)

        screen_group = VGroup(header, summary)
        fit_to_screen(screen_group)

        with self.voiceover(
            text="Let us summarize."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            sync_wait(tracker, NORMAL)

        with self.voiceover(
            text="Start with the standard quadratic equation."
        ) as tracker:
            self.play(FadeIn(s1, shift=RIGHT), run_time=FAST)
            blink_box(s1, color=NEON_BLUE, times=1)
            sync_wait(tracker, 1.4)

        with self.voiceover(
            text="Divide by a and complete the square."
        ) as tracker:
            self.play(FadeIn(s2, shift=RIGHT), run_time=FAST)
            blink_box(s2, color=NEON_ORANGE, times=1)
            sync_wait(tracker, 1.4)

        with self.voiceover(
            text="Take square root on both sides and simplify."
        ) as tracker:
            self.play(FadeIn(s3, shift=RIGHT), run_time=FAST)
            self.play(FadeIn(s4, shift=RIGHT), run_time=FAST)
            blink_box(VGroup(s3, s4), color=NEON_GREEN, times=1)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="This gives the quadratic formula."
        ) as tracker:
            self.play(Write(s5), run_time=NORMAL)
            blink_box(s5, color=NEON_YELLOW, times=2)
            sync_wait(tracker, 1.8)

        self.wait(0.4)
        clear_scene()

        # ============================================================
        # SCENE 17: END SCREEN
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
