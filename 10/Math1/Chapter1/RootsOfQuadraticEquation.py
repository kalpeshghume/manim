from manim import Text
from manim import MathTex
from manim import VGroup
from manim import FadeIn
from manim import FadeOut
from manim import Write
from manim import Create
from manim import TransformFromCopy
from manim import SurroundingRectangle
from manim import DashedLine
from manim import Dot
from manim import NumberLine
from manim import UP
from manim import DOWN
from manim import LEFT
from manim import RIGHT
from manim import Group

from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


TITLE_SIZE = 45
TEXT_SIZE = 30
SMALL_TEXT_SIZE = 30
MATH_SIZE = 40
SMALL_MATH_SIZE = 35

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
NEON_RED = "#FF3131"
WHITE_TEXT = "#F8F8FF"
BLACK_BG = "#050505"

SAFE_WIDTH = 12.3
SAFE_HEIGHT = 6.5
MIN_WAIT = 0.15


class RootsOfQuadraticEquation(VoiceoverScene):

    def construct(self):

        self.set_speech_service(GTTSService(lang="en"))
        self.camera.background_color = BLACK_BG

        def fit_to_screen(mob):
            if mob.width > SAFE_WIDTH:
                mob.scale_to_fit_width(SAFE_WIDTH)
            if mob.height > SAFE_HEIGHT:
                mob.scale_to_fit_height(SAFE_HEIGHT)
            return mob

        def make_title(text):
            title = Text(
                text,
                font_size=TITLE_SIZE,
                color=NEON_PINK
            )
            title.to_edge(UP)
            return title

        def neon_box(mob, color=NEON_YELLOW, buff=0.12):
            return SurroundingRectangle(
                mob,
                color=color,
                buff=buff,
                stroke_width=3
            )

        def blink_box(mob, color=NEON_YELLOW, times=2, buff=0.12):
            for index in range(times):
                box = neon_box(mob, color=color, buff=buff)
                self.play(Create(box), run_time=FAST)
                self.play(FadeOut(box), run_time=FAST)


        def clear_scene():
            current_objects = list(self.mobjects)

            if len(current_objects) > 0:
                all_objects = Group()

                for mob in current_objects:
                    all_objects.add(mob)

                self.play(
                    FadeOut(all_objects),
                    run_time=0.1
                )
           

        def sync_wait(tracker, used_time):
            remaining = tracker.duration - used_time
            if remaining > 0:
                self.wait(remaining + MIN_WAIT)
            else:
                self.wait(MIN_WAIT)

        title = Text(
            "Roots of a Quadratic Equation",
            font_size=TITLE_SIZE,
            color=NEON_PINK
        )

        
     

        opening_group = VGroup(title)
        opening_group.move_to([0, 0, 0])

        with self.voiceover(
            text="Welcome. In this lesson, we will understand the meaning of roots of a quadratic equation."
        ) as tracker:
            self.play(Write(title), run_time=NORMAL)
            sync_wait(tracker, NORMAL)

        
        self.wait(0.1)
        clear_scene()

        header = make_title("Concept of Root")

        line1 = Text(
            "If a value of x makes a polynomial equal to zero,",
            font_size=SMALL_TEXT_SIZE,
            color=WHITE_TEXT
        )
        line1.next_to(header, DOWN, buff=MEDIUM_BUFF)

        line2 = Text(
            "then that value is called a root or solution.",
            font_size=SMALL_TEXT_SIZE,
            color=NEON_GREEN
        )
        line2.next_to(line1, DOWN, buff=SMALL_BUFF)

        polynomial = MathTex(
            r"p(x) = x^2 + 5x - 6",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        )
        polynomial.next_to(line2, DOWN, buff=MEDIUM_BUFF)

        rule1 = MathTex(
            r"\text{If } p(a) = 0,\text{ then } x = a \text{ is a root.}",
            font_size=SMALL_MATH_SIZE,
            color=NEON_BLUE
        )
        rule1.next_to(polynomial, DOWN, buff=MEDIUM_BUFF)

        rule2 = MathTex(
            r"\text{If } p(a) = 0,\text{ then } (x-a) \text{ is a factor of } p(x).",
            font_size=SMALL_MATH_SIZE,
            color=NEON_ORANGE
        )
        rule2.next_to(rule1, DOWN, buff=MEDIUM_BUFF)

        concept_group = VGroup(header, line1, line2, polynomial, rule1, rule2)
        fit_to_screen(concept_group)

        with self.voiceover(
            text="In algebra, a root is a value of x that makes the polynomial equal to zero."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(FadeIn(line1), run_time=NORMAL)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="That value is also called a solution of the equation."
        ) as tracker:
            self.play(FadeIn(line2), run_time=NORMAL)
            blink_box(line2, color=NEON_GREEN, times=1)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="Let the polynomial be p of x equals x squared plus five x minus six."
        ) as tracker:
            self.play(Write(polynomial), run_time=NORMAL)
            blink_box(polynomial, color=NEON_YELLOW, times=1)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="If p of a is equal to zero, then x equals a is a root."
        ) as tracker:
            self.play(Write(rule1), run_time=NORMAL)
            blink_box(rule1, color=NEON_BLUE, times=1)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="Also, if p of a is zero, then x minus a is a factor of p of x."
        ) as tracker:
            self.play(Write(rule2), run_time=NORMAL)
            blink_box(rule2, color=NEON_ORANGE, times=1)
            sync_wait(tracker, 1.8)

        self.wait(0.1)
        clear_scene()

        header = make_title("Example")

        example_poly = MathTex(
            r"p(x) = x^2 + 5x - 6",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        )
        example_poly.next_to(header, DOWN, buff=LARGE_BUFF)

        check_line = Text(
            "Check whether x = -6 and x = 2 are roots.",
            font_size=TEXT_SIZE,
            color=NEON_BLUE
        )
        check_line.next_to(example_poly, DOWN, buff=MEDIUM_BUFF)

        value_left = MathTex(
            r"x = -6",
            font_size=MATH_SIZE,
            color=NEON_GREEN
        )

        value_right = MathTex(
            r"x = 2",
            font_size=MATH_SIZE,
            color=NEON_RED
        )

        values = VGroup(value_left, value_right)
        values.arrange(RIGHT, buff=2.4)
        values.next_to(check_line, DOWN, buff=LARGE_BUFF)

        intro_group = VGroup(header, example_poly, check_line, values)
        fit_to_screen(intro_group)

        with self.voiceover(
            text="Now let us take the polynomial x squared plus five x minus six."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(example_poly), run_time=NORMAL)
            blink_box(example_poly, color=NEON_YELLOW, times=1)
            sync_wait(tracker, 2.0)

        with self.voiceover(
            text="We will check whether x equals negative six and x equals two are roots."
        ) as tracker:
            self.play(FadeIn(check_line), run_time=NORMAL)
            self.play(Write(value_left), Write(value_right), run_time=NORMAL)
            blink_box(values, color=NEON_BLUE, times=1)
            sync_wait(tracker, 2.2)

        self.wait(0.1)
        clear_scene()

        header = make_title("Side-by-Side Comparison")

        divider = DashedLine(
            start=[0, 2.45, 0],
            end=[0, -2.85, 0],
            color=NEON_PINK,
            dash_length=0.18
        )

        left_title = Text(
            "Let x = -6",
            font_size=TEXT_SIZE,
            color=NEON_GREEN
        )
        left_title.move_to([-3.5, 2.35, 0])

        right_title = Text(
            "Let x = 2",
            font_size=TEXT_SIZE,
            color=NEON_RED
        )
        right_title.move_to([3.5, 2.35, 0])

        left_step1 = MathTex(
            r"x^2 + 5x - 6",
            font_size=SMALL_MATH_SIZE,
            color=WHITE_TEXT
        )

        left_step2 = MathTex(
            r"= (-6)^2 + 5(-6) - 6",
            font_size=SMALL_MATH_SIZE,
            color=WHITE_TEXT
        )

        left_step3 = MathTex(
            r"= 36 - 30 - 6",
            font_size=SMALL_MATH_SIZE,
            color=WHITE_TEXT
        )

        left_step4 = MathTex(
            r"= 0",
            font_size=SMALL_MATH_SIZE,
            color=NEON_GREEN
        )

        left_result = Text(
            "x = -6 is a solution.",
            font_size=SMALL_TEXT_SIZE,
            color=NEON_GREEN
        )

        left_root = Text(
            "Hence, -6 is one root.",
            font_size=SMALL_TEXT_SIZE,
            color=NEON_YELLOW
        )

        left_steps = VGroup(
            left_step1,
            left_step2,
            left_step3,
            left_step4,
            left_result,
            left_root
        )
        left_steps.arrange(DOWN, aligned_edge=LEFT, buff=SMALL_BUFF)
        left_steps.move_to([-3.4, -0.35, 0])

        right_step1 = MathTex(
            r"x^2 + 5x - 6",
            font_size=SMALL_MATH_SIZE,
            color=WHITE_TEXT
        )

        right_step2 = MathTex(
            r"= 2^2 + 5(2) - 6",
            font_size=SMALL_MATH_SIZE,
            color=WHITE_TEXT
        )

        right_step3 = MathTex(
            r"= 4 + 10 - 6",
            font_size=SMALL_MATH_SIZE,
            color=WHITE_TEXT
        )

        right_step4 = MathTex(
            r"= 8 \ne 0",
            font_size=SMALL_MATH_SIZE,
            color=NEON_RED
        )

        right_result = Text(
            "x = 2 is not a solution.",
            font_size=SMALL_TEXT_SIZE,
            color=NEON_RED
        )

        right_root = Text(
            "Hence, 2 is not a root.",
            font_size=SMALL_TEXT_SIZE,
            color=NEON_YELLOW
        )

        right_steps = VGroup(
            right_step1,
            right_step2,
            right_step3,
            right_step4,
            right_result,
            right_root
        )
        right_steps.arrange(DOWN, aligned_edge=LEFT, buff=SMALL_BUFF)
        right_steps.move_to([3.35, -0.35, 0])

        side_group = VGroup(
            header,
            divider,
            left_title,
            right_title,
            left_steps,
            right_steps
        )
        fit_to_screen(side_group)

        with self.voiceover(
            text="Now we will compare both values side by side."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Create(divider), run_time=NORMAL)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="On the left side, we check x equals negative six."
        ) as tracker:
            self.play(Write(left_title), run_time=NORMAL)
            blink_box(left_title, color=NEON_GREEN, times=1)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="On the right side, we check x equals two."
        ) as tracker:
            self.play(Write(right_title), run_time=NORMAL)
            blink_box(right_title, color=NEON_RED, times=1)
            sync_wait(tracker, 1.8)

        same_expression = VGroup(left_step1, right_step1)

        with self.voiceover(
            text="In both cases, we start with the same expression, x squared plus five x minus six."
        ) as tracker:
            self.play(Write(left_step1), Write(right_step1), run_time=NORMAL)
            blink_box(same_expression, color=NEON_BLUE, times=1)
            sync_wait(tracker, 2.0)

        with self.voiceover(
            text="Now substitute negative six on the left, and substitute two on the right."
        ) as tracker:
            self.play(TransformFromCopy(left_step1, left_step2), run_time=NORMAL)
            self.play(TransformFromCopy(right_step1, right_step2), run_time=NORMAL)
            blink_box(left_step2, color=NEON_GREEN, times=1)
            blink_box(right_step2, color=NEON_RED, times=1)
            sync_wait(tracker, 2.4)

        with self.voiceover(
            text="Now simplify the powers and multiplication."
        ) as tracker:
            self.play(TransformFromCopy(left_step2, left_step3), run_time=NORMAL)
            self.play(TransformFromCopy(right_step2, right_step3), run_time=NORMAL)
            blink_box(left_step3, color=NEON_ORANGE, times=1)
            blink_box(right_step3, color=NEON_ORANGE, times=1)
            sync_wait(tracker, 2.2)

        with self.voiceover(
            text="On the left side, thirty six minus thirty minus six becomes zero."
        ) as tracker:
            self.play(TransformFromCopy(left_step3, left_step4), run_time=NORMAL)
            blink_box(left_step4, color=NEON_GREEN, times=2)
            sync_wait(tracker, 2.0)

        with self.voiceover(
            text="On the right side, four plus ten minus six becomes eight, which is not zero."
        ) as tracker:
            self.play(TransformFromCopy(right_step3, right_step4), run_time=NORMAL)
            blink_box(right_step4, color=NEON_RED, times=2)
            sync_wait(tracker, 2.2)

        with self.voiceover(
            text="Since the value becomes zero when x equals negative six, x equals negative six is a solution."
        ) as tracker:
            self.play(FadeIn(left_result, shift=RIGHT), run_time=NORMAL)
            blink_box(left_result, color=NEON_GREEN, times=1)
            sync_wait(tracker, 2.0)

        with self.voiceover(
            text="Since the value does not become zero when x equals two, x equals two is not a solution."
        ) as tracker:
            self.play(FadeIn(right_result, shift=RIGHT), run_time=NORMAL)
            blink_box(right_result, color=NEON_RED, times=1)
            sync_wait(tracker, 2.0)

        with self.voiceover(
            text="Therefore, negative six is one root of the equation, but two is not a root."
        ) as tracker:
            self.play(FadeIn(left_root, shift=RIGHT), run_time=NORMAL)
            self.play(FadeIn(right_root, shift=RIGHT), run_time=NORMAL)
            blink_box(left_root, color=NEON_YELLOW, times=1)
            blink_box(right_root, color=NEON_YELLOW, times=1)
            sync_wait(tracker, 2.5)

        self.wait(0.2)
        clear_scene()

        header = make_title("Meaning of Root")

        equation = MathTex(
            r"x^2 + 5x - 6 = 0",
            font_size=MATH_SIZE,
            color=NEON_YELLOW
        )
        equation.next_to(header, DOWN, buff=LARGE_BUFF)

        number_line = NumberLine(
            x_range=[-8, 4, 1],
            length=9,
            color=WHITE_TEXT,
            include_numbers=True,
            font_size=20
        )
        number_line.next_to(equation, DOWN, buff=LARGE_BUFF)

        root_dot = Dot(
            number_line.n2p(-6),
            color=NEON_GREEN,
            radius=0.09
        )

        root_label = MathTex(
            r"x=-6",
            font_size=SMALL_MATH_SIZE,
            color=NEON_GREEN
        )
        root_label.next_to(root_dot, UP, buff=SMALL_BUFF)

        not_root_dot = Dot(
            number_line.n2p(2),
            color=NEON_RED,
            radius=0.09
        )

        not_root_label = MathTex(
            r"x=2",
            font_size=SMALL_MATH_SIZE,
            color=NEON_RED
        )
        not_root_label.next_to(not_root_dot, UP, buff=SMALL_BUFF)

        final_meaning = Text(
            "Root means the value that makes the equation equal to zero.",
            font_size=TEXT_SIZE,
            color=NEON_GREEN
        )
        final_meaning.next_to(number_line, DOWN, buff=MEDIUM_BUFF)

        number_group = VGroup(
            header,
            equation,
            number_line,
            root_dot,
            root_label,
            not_root_dot,
            not_root_label,
            final_meaning
        )
        fit_to_screen(number_group)

        with self.voiceover(
            text="The equation is x squared plus five x minus six equals zero."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            self.play(Write(equation), run_time=NORMAL)
            sync_wait(tracker, 1.8)

        with self.voiceover(
            text="On the number line, negative six gives zero, so negative six is a root."
        ) as tracker:
            self.play(Create(number_line), run_time=NORMAL)
            self.play(FadeIn(root_dot), Write(root_label), run_time=NORMAL)
            blink_box(root_label, color=NEON_GREEN, times=2)
            sync_wait(tracker, 2.4)

        with self.voiceover(
            text="But two gives eight, not zero. So two is not a root."
        ) as tracker:
            self.play(FadeIn(not_root_dot), Write(not_root_label), run_time=NORMAL)
            blink_box(not_root_label, color=NEON_RED, times=2)
            sync_wait(tracker, 2.2)

        with self.voiceover(
            text="So remember, root means the value that makes the equation equal to zero."
        ) as tracker:
            self.play(FadeIn(final_meaning), run_time=NORMAL)
            blink_box(final_meaning, color=NEON_GREEN, times=1)
            sync_wait(tracker, 2.0)

        self.wait(0.1)
        clear_scene()

        header = make_title("Summary")

        s1 = Text(
            "1. Put the given value in the polynomial.",
            font_size=TEXT_SIZE,
            color=WHITE_TEXT
        )

        s2 = Text(
            "2. Simplify the expression carefully.",
            font_size=TEXT_SIZE,
            color=WHITE_TEXT
        )

        s3 = Text(
            "3. If the answer is 0, the value is a root.",
            font_size=TEXT_SIZE,
            color=NEON_GREEN
        )

        s4 = Text(
            "4. If the answer is not 0, the value is not a root.",
            font_size=TEXT_SIZE,
            color=NEON_RED
        )



        summary = VGroup(s1, s2, s3, s4)
        summary.arrange(DOWN, aligned_edge=LEFT, buff=MEDIUM_BUFF)
        summary.next_to(header, DOWN, buff=LARGE_BUFF)

        summary_group = VGroup(header, summary)
        fit_to_screen(summary_group)

        with self.voiceover(
            text="Let us summarize."
        ) as tracker:
            self.play(Write(header), run_time=NORMAL)
            sync_wait(tracker, NORMAL)

        with self.voiceover(
            text="First, put the given value in the polynomial."
        ) as tracker:
            self.play(FadeIn(s1, shift=RIGHT), run_time=FAST)
            blink_box(s1, color=NEON_BLUE, times=1)
            sync_wait(tracker, 1.2)

        with self.voiceover(
            text="Second, simplify the expression carefully."
        ) as tracker:
            self.play(FadeIn(s2, shift=RIGHT), run_time=FAST)
            blink_box(s2, color=NEON_ORANGE, times=1)
            sync_wait(tracker, 1.2)

        with self.voiceover(
            text="If the answer is zero, the value is a root."
        ) as tracker:
            self.play(FadeIn(s3, shift=RIGHT), run_time=FAST)
            blink_box(s3, color=NEON_GREEN, times=1)
            sync_wait(tracker, 1.2)

        with self.voiceover(
            text="If the answer is not zero, the value is not a root."
        ) as tracker:
            self.play(FadeIn(s4, shift=RIGHT), run_time=FAST)
            blink_box(s4, color=NEON_RED, times=1)
            sync_wait(tracker, 1.2)


        self.wait(0.1)
        clear_scene()

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
            text="And subscribe for more mathematics lessons."
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
