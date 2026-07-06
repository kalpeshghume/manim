from manim import *

class TrigIdentity(Scene):
    def construct(self):
        # Title
        title = Text("Pythagorean Trigonometric Identity", font_size=42)
        title.to_edge(UP)

        # Equation
        equation = MathTex(
            r"\sin^2(x)",
            r"+",
            r"\cos^2(x)",
            r"=",
            r"1"
        ).scale(1.5)

        self.play(Write(title))
        self.wait(0.5)

        # Write equation
        self.play(Write(equation))
        self.wait(1)

        # Highlight sin²(x)
        self.play(
            equation[0].animate.set_color(BLUE)
        )
        self.wait(0.5)

        # Highlight cos²(x)
        self.play(
            equation[2].animate.set_color(GREEN)
        )
        self.wait(0.5)

        # Restore colors
        self.play(
            equation[0].animate.set_color(WHITE),
            equation[2].animate.set_color(WHITE)
        )

        self.wait(0.5)

        # Emphasize result
        box = SurroundingRectangle(
            equation[4],
            color=YELLOW,
            buff=0.15
        )

        self.play(Create(box))
        self.play(
            equation[4].animate.set_color(YELLOW).scale(1.3)
        )

        self.wait(2)
