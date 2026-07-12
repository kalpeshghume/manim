import os
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import numpy as np

# ==========================================================
# GLOBAL SETTINGS & STYLING
# ==========================================================
TITLE_FONT_SIZE = 40
ACTIVE_HEADING_SIZE = 28
ACTIVE_TEXT_SIZE = 22
ACTIVE_MATH_SIZE = 29
COMPACT_HEADING_SIZE = 17
COMPACT_TEXT_SIZE = 14
COMPACT_MATH_SIZE = 16
LABEL_FONT_SIZE = 18

WRITE_SPEED = 0.65
CREATE_SPEED = 0.65
MOVE_SPEED = 0.8
FADE_SPEED = 0.45
INDICATE_SPEED = 0.7
READ_STEP_WAIT_TIME = 0.8

MIDDLE_CENTER_X = 0.00
RIGHT_CENTER_X = 4.35
LEFT_NOTE_LEFT_X = -6.55
MIDDLE_NOTE_LEFT_X = -2.10
COMPACT_MAX_WIDTH = 4.90

ACTIVE_CENTER = np.array([MIDDLE_CENTER_X, 1.35, 0])
ACTIVE_CARD_WIDTH = 4.35
ACTIVE_CARD_HEIGHT = 2.50
DIAGRAM_SHIFT = RIGHT * RIGHT_CENTER_X + UP * 0.5

TRACE_WIDTH = 6
TITLE_COLOR = PINK
THEOREM_COLOR = PINK
GIVEN_COLOR = BLUE
PROVE_COLOR = GREEN
STEP1_COLOR = BLUE
STEP2_COLOR = GREEN
STEP3_COLOR = TEAL
FINAL_COLOR = YELLOW
MAIN_TRIANGLE_COLOR = WHITE
ALTITUDE_COLOR = ORANGE

NEON_GREEN = "#39FF14"
NEON_PINK = "#FF10F0"
NEON_TEAL = "#00F5FF"
NEON_YELLOW = "#FFF700"

# ==========================================================
# HELPER FUNCTIONS & OVERLAYS
# ==========================================================
def readable_label(mob):
    mob.add_background_rectangle(color=BLACK, opacity=0.88, buff=0.05)
    mob.set_z_index(90)
    return mob

def fit_to_box(mob, max_width, max_height):
    if mob.width > max_width: mob.scale(max_width / mob.width)
    if mob.height > max_height: mob.scale(max_height / mob.height)
    return mob

def trace_segment(p1, p2, color=NEON_YELLOW, width=TRACE_WIDTH):
    seg = Line(p1, p2, color=color, stroke_width=width)
    seg.set_z_index(70)
    return seg

def show_triangle_focus(scene, p1, p2, p3, color, text_prompt, opacity=0.24):
    trace = VGroup(trace_segment(p1, p2, color=color), trace_segment(p2, p3, color=color), trace_segment(p3, p1, color=color))
    fill = Polygon(p1, p2, p3, color=color, fill_color=color, fill_opacity=opacity, stroke_width=3).set_z_index(3)
    with scene.voiceover(text=text_prompt) as tracker:
        scene.play(Create(trace), run_time=CREATE_SPEED)
        scene.play(FadeIn(fill), run_time=FADE_SPEED)
        scene.play(Indicate(fill), run_time=INDICATE_SPEED)
    return VGroup(trace, fill)

def show_segment_focus(scene, p1, p2, text_prompt, color=NEON_YELLOW):
    seg = trace_segment(p1, p2, color=color)
    with scene.voiceover(text=text_prompt) as tracker:
        scene.play(Create(seg), run_time=CREATE_SPEED)
        scene.play(Indicate(seg), run_time=INDICATE_SPEED)
    return seg

def clear_focus(scene, focus_group):
    scene.play(FadeOut(focus_group), run_time=FADE_SPEED)

def arrow_from_card_to_point(active_card, line_idx, target_point, color=NEON_TEAL):
    content = active_card[1]
    source = content[line_idx].get_right() + RIGHT * 0.15
    arrow = Arrow(source, target_point, color=color, buff=0.15, stroke_width=4, max_tip_length_to_length_ratio=0.1)
    arrow.set_z_index(85)
    return arrow

def animate_cross_multiplication(scene, math_mobject, color=NEON_PINK):
    c1 = Line(math_mobject.get_left() + UP*0.25, math_mobject.get_right() + DOWN*0.25, color=color, stroke_width=4)
    c2 = Line(math_mobject.get_left() + DOWN*0.25, math_mobject.get_right() + UP*0.25, color=color, stroke_width=4)
    scene.play(Create(c1), Create(c2), run_time=0.4)
    scene.play(Flash(math_mobject, color=color, flash_radius=0.6))
    scene.play(FadeOut(c1), FadeOut(c2), run_time=0.3)

class SmartColumnLayout:
    def __init__(self, left_x, top_y, bottom_y, gap=0.12):
        self.left_x = left_x
        self.top_y = top_y
        self.bottom_y = bottom_y
        self.gap = gap
        self.next_top = top_y
    def can_fit(self, mob): return mob.height <= (self.next_top - self.bottom_y)
    def place(self, mob):
        center_x = self.left_x + mob.width / 2
        center_y = self.next_top - mob.height / 2
        mob.move_to([center_x, center_y, 0])
        self.next_top = mob.get_bottom()[1] - self.gap
        return mob

def make_line(kind, content, mode):
    text_size = ACTIVE_TEXT_SIZE if mode == "active" else COMPACT_TEXT_SIZE
    math_size = ACTIVE_MATH_SIZE if mode == "active" else COMPACT_MATH_SIZE
    if kind == "text": return Text(content, font_size=text_size)
    if kind == "math": return MathTex(content, font_size=math_size)
    return Text(content, font_size=text_size)

def make_active_card(title, color, lines):
    heading = Text(title, font_size=ACTIVE_HEADING_SIZE, color=color)
    items = [heading]
    for kind, content in lines:
        items.append(make_line(kind, content, mode="active"))
    content_group = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    fit_to_box(content_group, ACTIVE_CARD_WIDTH - 0.45, ACTIVE_CARD_HEIGHT - 0.40)
    box = RoundedRectangle(width=ACTIVE_CARD_WIDTH, height=max(1.25, content_group.height + 0.42), corner_radius=0.13, color=color, stroke_width=1.7)
    content_group.move_to(box.get_center()).align_to(box.get_left() + RIGHT * 0.20, LEFT)
    return VGroup(box, content_group).move_to(ACTIVE_CENTER)

def make_compact_note(title, color, lines):
    heading = Text(title, font_size=COMPACT_HEADING_SIZE, color=color)
    items = [heading]
    for kind, content in lines:
        items.append(make_line(kind, content, mode="compact"))
    note = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.03)
    if note.width > COMPACT_MAX_WIDTH: note.scale(COMPACT_MAX_WIDTH / note.width)
    return note

def show_active_card(scene, title, color, lines):
    card = make_active_card(title, color, lines)
    scene.play(Create(card[0]), run_time=CREATE_SPEED)
    scene.play(Write(card[1][0]), run_time=WRITE_SPEED)
    return card

def write_next_line(scene, active_card, line_index):
    scene.play(Write(active_card[1][line_index]), run_time=WRITE_SPEED)

def move_to_smart_location(scene, active_card, title, color, compact_lines, left_layout, middle_layout):
    compact_note = make_compact_note(title, color, compact_lines)
    if left_layout.can_fit(compact_note): left_layout.place(compact_note)
    else: middle_layout.place(compact_note)
    scene.wait(READ_STEP_WAIT_TIME)
    scene.play(ReplacementTransform(active_card, compact_note), run_time=MOVE_SPEED)
    return compact_note

# ==========================================================
# MAIN ANIMATION SCENE
# ==========================================================
class PythagorasTheorem(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        # --- TITLE SETUP ---
        title = Text("Pythagoras Theorem Complete Proof", font_size=TITLE_FONT_SIZE, color=TITLE_COLOR)
        title.to_edge(UP, buff=0.18)
        with self.voiceover(text="Hello everyone and welcome. Today we are going to learn how to prove the famous Pythagoras Theorem step by step.") as tracker:
            self.play(Write(title), run_time=tracker.duration)

        left_layout = SmartColumnLayout(left_x=LEFT_NOTE_LEFT_X, top_y=2.55, bottom_y=-3.58, gap=0.12)
        middle_bottom_layout = SmartColumnLayout(left_x=MIDDLE_NOTE_LEFT_X, top_y=-0.75, bottom_y=-3.50, gap=0.16)

        steps_label = Text("Steps Panel", font_size=22, color=GREY_A).move_to([MIDDLE_CENTER_X, 2.78, 0])
        self.play(Write(steps_label), run_time=WRITE_SPEED)

        # --- GEOMETRY CO-ORDINATES ---
        B_pos = np.array([-1.5, -1.0, 0]) + DIAGRAM_SHIFT
        C_pos = np.array([2.0, -1.0, 0]) + DIAGRAM_SHIFT
        A_pos = np.array([-1.5, 1.5, 0]) + DIAGRAM_SHIFT
        
        v_AC = C_pos - A_pos
        u_AC = v_AC / np.linalg.norm(v_AC)
        v_AB = B_pos - A_pos
        D_pos = A_pos + np.dot(v_AB, u_AC) * u_AC

        triangle_ABC = Polygon(A_pos, B_pos, C_pos, color=MAIN_TRIANGLE_COLOR, stroke_width=3)
        BD = Line(B_pos, D_pos, color=ALTITUDE_COLOR, stroke_width=3)
        right_angle_B = RightAngle(Line(B_pos, A_pos), Line(B_pos, C_pos), length=0.2, color=WHITE, stroke_width=2)
        right_angle_D = RightAngle(Line(D_pos, B_pos), Line(D_pos, C_pos), length=0.18, color=WHITE, stroke_width=2)

        lbl_A = readable_label(MathTex("A", font_size=LABEL_FONT_SIZE).next_to(A_pos, UP+LEFT, buff=0.1))
        lbl_B = readable_label(MathTex("B", font_size=LABEL_FONT_SIZE).next_to(B_pos, DOWN+LEFT, buff=0.1))
        lbl_C = readable_label(MathTex("C", font_size=LABEL_FONT_SIZE).next_to(C_pos, DOWN+RIGHT, buff=0.1))
        lbl_D = readable_label(MathTex("D", font_size=LABEL_FONT_SIZE).next_to(D_pos, UP+RIGHT, buff=0.1))

        # --- INITIAL CONSTRUCTION ---
        with self.voiceover(text="First let us look at our main right angled triangle ABC where the corner angle B is exactly ninety degrees.") as tracker:
            self.play(Create(triangle_ABC), run_time=tracker.duration)
            self.play(FadeIn(lbl_A), FadeIn(lbl_B), FadeIn(lbl_C), Create(right_angle_B))

        with self.voiceover(text="Next for our construction let us draw a straight perpendicular line from vertex B down to the hypotenuse and label this new point D.") as tracker:
            self.play(Create(BD), FadeIn(lbl_D), Create(right_angle_D), run_time=tracker.duration)

        # --- THEOREM STATEMENTS ---
        theorem_lines = [("text", "In a right-angled triangle,"), ("text", "square of hypotenuse equals"), ("text", "sum of squares of other sides.")]
        with self.voiceover(text="The core theorem states that in any right angled triangle the square of the hypotenuse is equal to the sum of the squares of the other two sides.") as tracker:
            t_card = show_active_card(self, "Theorem", THEOREM_COLOR, theorem_lines)
            for i in range(3): write_next_line(self, t_card, i+1)
        move_to_smart_location(self, t_card, "Theorem", THEOREM_COLOR, theorem_lines, left_layout, middle_bottom_layout)

        # --- GIVEN CARD & DIAGRAM SYNC ---
        given_lines = [("math", r"\text{In }\triangle ABC,\;\angle ABC = 90^\circ"), ("math", r"BD \perp AC")]
        with self.voiceover(text="So what is given to us initially is triangle ABC where angle ABC is ninety degrees.") as tracker:
            g_card = show_active_card(self, "Given", GIVEN_COLOR, given_lines)
            write_next_line(self, g_card, 1)
        
        arrow_g1 = arrow_from_card_to_point(g_card, 1, B_pos + UP*0.15 + RIGHT*0.15)
        self.play(Create(arrow_g1))
        self.play(Indicate(right_angle_B, color=NEON_YELLOW), run_time=INDICATE_SPEED)
        self.play(FadeOut(arrow_g1))

        with self.voiceover(text="And remember our construction made line BD perpendicular to the hypotenuse side AC.") as tracker:
            write_next_line(self, g_card, 2)
        
        arrow_g2 = arrow_from_card_to_point(g_card, 2, (B_pos + D_pos)/2)
        self.play(Create(arrow_g2))
        self.play(Indicate(BD, color=NEON_YELLOW), Indicate(right_angle_D, color=NEON_PINK), run_time=INDICATE_SPEED)
        self.play(FadeOut(arrow_g2))
        move_to_smart_location(self, g_card, "Given", GIVEN_COLOR, given_lines, left_layout, middle_bottom_layout)

        # --- TO PROVE CARD ---
        prove_lines = [("math", r"AC^2 = AB^2 + BC^2")]
        with self.voiceover(text="We need to prove that AC squared equals AB squared plus BC squared.") as tracker:
            p_card = show_active_card(self, "To Prove", PROVE_COLOR, prove_lines)
            write_next_line(self, p_card, 1)

        arrow_p = arrow_from_card_to_point(p_card, 1, (A_pos + C_pos)/2)
        self.play(Create(arrow_p))
        focus_ac_prove = show_segment_focus(self, A_pos, C_pos, "Let us highlight the big master hypotenuse side AC right here on the diagram.", color=NEON_GREEN)
        self.play(FadeOut(arrow_p)); clear_focus(self, focus_ac_prove)
        move_to_smart_location(self, p_card, "To Prove", PROVE_COLOR, prove_lines, left_layout, middle_bottom_layout)

        # --- STEP 1: TRIANGLE SIMILARITY ---
        step1_active = [
            ("text", "By Similarity of Right Triangles:"),
            ("math", r"\triangle ABC \sim \triangle ADB \sim \triangle BDC")
        ]
        step1_compact = [("math", r"\triangle ABC \sim \triangle ADB \sim \triangle BDC")]
        with self.voiceover(text="Now for Step one by the property of similarity our main big triangle is similar to both of the smaller inner triangles.") as tracker:
            s1_card = show_active_card(self, "Step 1: Similarity", STEP1_COLOR, step1_active)
            write_next_line(self, s1_card, 1)
            write_next_line(self, s1_card, 2)

        arrow_s1_1 = arrow_from_card_to_point(s1_card, 2, (A_pos + B_pos + C_pos)/3)
        self.play(Create(arrow_s1_1))
        focus_abc = show_triangle_focus(self, A_pos, B_pos, C_pos, NEON_GREEN, "Let us look at the huge master triangle ABC.")
        self.play(FadeOut(arrow_s1_1)); clear_focus(self, focus_abc)

        arrow_s1_2 = arrow_from_card_to_point(s1_card, 2, (A_pos + D_pos + B_pos)/3)
        self.play(Create(arrow_s1_2))
        focus_adb = show_triangle_focus(self, A_pos, D_pos, B_pos, NEON_PINK, "Now check out the top inner split triangle ADB.")
        self.play(FadeOut(arrow_s1_2)); clear_focus(self, focus_adb)

        arrow_s1_3 = arrow_from_card_to_point(s1_card, 2, (B_pos + D_pos + C_pos)/3)
        self.play(Create(arrow_s1_3))
        focus_bdc = show_triangle_focus(self, B_pos, D_pos, C_pos, NEON_TEAL, "And lastly let us see the bottom inner triangle BDC.")
        self.play(FadeOut(arrow_s1_3)); clear_focus(self, focus_bdc)
        move_to_smart_location(self, s1_card, "Step 1: Similarity", STEP1_COLOR, step1_compact, left_layout, middle_bottom_layout)

        # --- STEP 2: PAIR 1 WITH COMPONENT HIGHLIGHTS ---
        step2_active = [
            ("math", r"\triangle ABC \sim \triangle ADB"),
            ("math", r"\frac{AB}{AD} = \frac{AC}{AB}"),
            ("math", r"AB^2 = AD \times AC\quad (I)")
        ]
        step2_compact = [("math", r"AB^2 = AD \times AC\quad (I)")]
        with self.voiceover(text="Step two let us compare the master triangle ABC with the top small triangle ADB.") as tracker:
            s2_card = show_active_card(self, "Step 2: Proving AB^2", STEP2_COLOR, step2_active)
            write_next_line(self, s2_card, 1)

        with self.voiceover(text="Since they are similar the ratios of their corresponding sides must be equal so let us trace each part.") as tracker:
            write_next_line(self, s2_card, 2)

        # Highlight 1: AB (Numerator Left)
        arrow_s2_ab = arrow_from_card_to_point(s2_card, 2, (A_pos + B_pos)/2)
        self.play(Create(arrow_s2_ab))
        f_ab = show_segment_focus(self, A_pos, B_pos, "Let us look at side AB of the large triangle.", color=NEON_GREEN)
        self.play(FadeOut(arrow_s2_ab)); clear_focus(self, f_ab)

        # Highlight 2: AD (Denominator Left)
        arrow_s2_ad = arrow_from_card_to_point(s2_card, 2, (A_pos + D_pos)/2)
        self.play(Create(arrow_s2_ad))
        f_ad = show_segment_focus(self, A_pos, D_pos, "Compare it to side AD of the smaller triangle.", color=NEON_PINK)
        self.play(FadeOut(arrow_s2_ad)); clear_focus(self, f_ad)

        # Highlight 3: AC (Numerator Right)
        arrow_s2_ac = arrow_from_card_to_point(s2_card, 2, (A_pos + C_pos)/2)
        self.play(Create(arrow_s2_ac))
        f_ac = show_segment_focus(self, A_pos, C_pos, "Now see the primary master hypotenuse side AC.", color=NEON_YELLOW)
        self.play(FadeOut(arrow_s2_ac)); clear_focus(self, f_ac)

        # Highlight 4: AB (Denominator Right)
        arrow_s2_ab2 = arrow_from_card_to_point(s2_card, 2, (A_pos + B_pos)/2)
        self.play(Create(arrow_s2_ab2))
        f_ab2 = show_segment_focus(self, A_pos, B_pos, "And match it against the smaller triangle hypotenuse side AB again.", color=NEON_GREEN)
        self.play(FadeOut(arrow_s2_ab2)); clear_focus(self, f_ab2)

        with self.voiceover(text="Now if we cross multiply diagonally across these fractions") as tracker:
            animate_cross_multiplication(self, s2_card[1][2], color=NEON_PINK)

        with self.voiceover(text="We get our first equation stating that AB squared equals AD times AC which we will label as equation one.") as tracker:
            write_next_line(self, s2_card, 3)
        move_to_smart_location(self, s2_card, "Step 2: Eq (I)", STEP2_COLOR, step2_compact, left_layout, middle_bottom_layout)

        # --- STEP 3: PAIR 2 WITH COMPONENT HIGHLIGHTS ---
        step3_active = [
            ("math", r"\triangle ABC \sim \triangle BDC"),
            ("math", r"\frac{BC}{DC} = \frac{AC}{BC}"),
            ("math", r"BC^2 = DC \times AC\quad (II)")
        ]
        step3_compact = [("math", r"BC^2 = DC \times AC\quad (II)")]
        with self.voiceover(text="Step three let us do the exact same thing with the master triangle ABC and the lower small triangle BDC.") as tracker:
            s3_card = show_active_card(self, "Step 3: Proving BC^2", STEP3_COLOR, step3_active)
            write_next_line(self, s3_card, 1)

        with self.voiceover(text="Let us set up the matching side ratios for these two shapes and trace each corresponding segment.") as tracker:
            write_next_line(self, s3_card, 2)

        # Highlight 1: BC (Numerator Left)
        arrow_s3_bc = arrow_from_card_to_point(s3_card, 2, (B_pos + C_pos)/2)
        self.play(Create(arrow_s3_bc))
        f_bc = show_segment_focus(self, B_pos, C_pos, "Let us highlight side line segment BC on the main diagram.", color=NEON_GREEN)
        self.play(FadeOut(arrow_s3_bc)); clear_focus(self, f_bc)

        # Highlight 2: DC (Denominator Left)
        arrow_s3_dc = arrow_from_card_to_point(s3_card, 2, (D_pos + C_pos)/2)
        self.play(Create(arrow_s3_dc))
        f_dc = show_segment_focus(self, D_pos, C_pos, "Compare that with the lower base segment piece DC.", color=NEON_TEAL)
        self.play(FadeOut(arrow_s3_dc)); clear_focus(self, f_dc)

        # Highlight 3: AC (Numerator Right)
        arrow_s3_ac = arrow_from_card_to_point(s3_card, 2, (A_pos + C_pos)/2)
        self.play(Create(arrow_s3_ac))
        f_ac3 = show_segment_focus(self, A_pos, C_pos, "Bring back our attention to the full master hypotenuse side AC.", color=NEON_YELLOW)
        self.play(FadeOut(arrow_s3_ac)); clear_focus(self, f_ac3)

        # Highlight 4: BC (Denominator Right)
        arrow_s3_bc2 = arrow_from_card_to_point(s3_card, 2, (B_pos + C_pos)/2)
        self.play(Create(arrow_s3_bc2))
        f_bc2 = show_segment_focus(self, B_pos, C_pos, "And finish the ratio with side BC of the lower inner triangle.", color=NEON_GREEN)
        self.play(FadeOut(arrow_s3_bc2)); clear_focus(self, f_bc2)

        with self.voiceover(text="Just like step two let us execute another diagonal cross multiplication on these terms.") as tracker:
            animate_cross_multiplication(self, s3_card[1][2], color=NEON_TEAL)

        with self.voiceover(text="This gives us our second equation stating that BC squared equals DC times AC which we will label as equation two.") as tracker:
            write_next_line(self, s3_card, 3)
        move_to_smart_location(self, s3_card, "Step 3: Eq (II)", STEP3_COLOR, step3_compact, left_layout, middle_bottom_layout)

        # --- FINAL RESULTS & ALGEBRAIC MERGER ---
        final_active = [
            ("text", "Adding Equations (I) and (II):"),
            ("math", r"AB^2 + BC^2 = (AD \times AC) + (DC \times AC)"),
            ("math", r"= AC(AD + DC)"),
            ("math", r"= AC \times AC \quad \because AD+DC = AC"),
            ("math", r"= AC^2")
        ]
        final_compact = [("math", r"AB^2 + BC^2 = AC^2")]
        with self.voiceover(text="We are almost there, now let us add equation one and equation two together to combine our results.") as tracker:
            f_card = show_active_card(self, "Final Step: Solution", FINAL_COLOR, final_active)
            write_next_line(self, f_card, 1)
            write_next_line(self, f_card, 2)

        with self.voiceover(text="Notice that side AC is present in both terms so let us factor out that common side AC.") as tracker:
            write_next_line(self, f_card, 3)
            self.play(Indicate(f_card[1][3], color=NEON_YELLOW), run_time=1.0)

        with self.voiceover(text="Look inside the parentheses where we have segment AD plus segment DC and let us see what that looks like on our diagram.") as tracker:
            write_next_line(self, f_card, 4)
            text_box = SurroundingRectangle(f_card[1][4], color=RED, buff=0.1)
            self.play(Create(text_box))
            self.play(Flash(f_card[1][4], color=NEON_GREEN, flash_radius=0.5))
            self.play(FadeOut(text_box))

        arrow_final = arrow_from_card_to_point(f_card, 4, (A_pos + C_pos)/2)
        self.play(Create(arrow_final))
        focus_combined = show_segment_focus(self, A_pos, C_pos, "See that segment AD plus segment DC merges perfectly to form the entire master line AC.")
        self.play(FadeOut(arrow_final)); clear_focus(self, focus_combined)

        with self.voiceover(text="And finally multiplying side AC by itself simplifies directly into AC squared.") as tracker:
            write_next_line(self, f_card, 5)
            self.play(Indicate(f_card[1][5], color=NEON_GREEN), run_time=1.0)
        move_to_smart_location(self, f_card, "Final Proof", FINAL_COLOR, final_compact, left_layout, middle_bottom_layout)

        # --- FINAL MASTER ACCENT BOX ---
        final_box = RoundedRectangle(width=4.5, height=1.5, corner_radius=0.18, color=YELLOW, stroke_width=2.5).move_to([RIGHT_CENTER_X, -2.5, 0])
        final_formula = MathTex(r"AC^2 = AB^2 + BC^2", font_size=26, color=YELLOW).move_to(final_box.get_center())
        
        with self.voiceover(text="The derivation is complete and we have successfully proven the theorem of Pythagoras.") as tracker:
            self.play(Create(final_box), run_time=CREATE_SPEED)
            self.play(Write(final_formula), run_time=WRITE_SPEED)
            self.play(Circumscribe(final_formula, color=RED, buff=0.25))

        self.wait(1)
        self.play(FadeOut(*self.mobjects), run_time=1.0)

        # ==========================================================
        # OUTRO SCREEN WITH VOICEOVER
        # ==========================================================
        subscribe_text = Text("SUBSCRIBE", font_size=74, weight=BOLD, color=RED)
        like_text = Text("LIKE  👍", font_size=42, color=YELLOW, font="Segoe UI Emoji")
        share_text = Text("SHARE  ✨", font_size=42, weight=BOLD, color=NEON_TEAL)
        thanks_text = Text("Thank you for watching!", font_size=28, color=WHITE)
        outro_group = VGroup(subscribe_text, like_text, share_text, thanks_text).arrange(DOWN, buff=0.35).move_to(ORIGIN)

        with self.voiceover(text="If this math animation made geometry clear and easy to understand please remember to hit that subscribe button give this video a big thumbs up and share it with your friends. Thank you so much for watching and I will see you in our next lesson.") as tracker:
            self.play(GrowFromCenter(subscribe_text), run_time=0.6)
            self.play(Write(like_text), run_time=0.5)
            self.play(Write(share_text), run_time=0.5)
            self.play(FadeIn(thanks_text), run_time=0.5)
            self.play(Indicate(subscribe_text, color=YELLOW, scale_factor=1.12))
            self.play(Flash(subscribe_text, color=YELLOW, flash_radius=1.3, line_length=0.25))
        
        self.wait(2)
