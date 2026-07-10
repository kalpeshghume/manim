from manim import *
import numpy as np

# ==========================================================
# GLOBAL SETTINGS
# ==========================================================

TITLE_FONT_SIZE = 28

ACTIVE_HEADING_SIZE = 28
ACTIVE_TEXT_SIZE = 22
ACTIVE_MATH_SIZE = 29

COMPACT_HEADING_SIZE = 17
COMPACT_TEXT_SIZE = 14
COMPACT_MATH_SIZE = 16

LABEL_FONT_SIZE = 18

WRITE_SPEED = 0.75
CREATE_SPEED = 0.75
MOVE_SPEED = 0.9
FADE_SPEED = 0.55
INDICATE_SPEED = 0.8
READ_STEP_WAIT_TIME = 1.7

MIDDLE_CENTER_X = 0.00
RIGHT_CENTER_X = 4.75

LEFT_NOTE_LEFT_X = -7.05
MIDDLE_NOTE_LEFT_X = -2.10

COMPACT_MAX_WIDTH = 4.90

ACTIVE_CENTER = np.array([MIDDLE_CENTER_X, 1.35, 0])
ACTIVE_CARD_WIDTH = 4.35
ACTIVE_CARD_HEIGHT = 2.50

DIAGRAM_SHIFT = RIGHT * RIGHT_CENTER_X + UP * 0.22

SEGMENT_WIDTH = 7
TRACE_WIDTH = 6
TRIANGLE_FILL_OPACITY = 0.22
ANGLE_RADIUS = 0.28

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

# Neon colors for black background
NEON_GREEN = "#39FF14"
NEON_PINK = "#FF10F0"
NEON_YELLOW = "#FFF700"
NEON_TEAL = "#00F5FF"
NEON_ORANGE = "#FF9D00"
NEON_BLUE = "#00A2FF"


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def readable_label(mob):
    mob.add_background_rectangle(
        color=BLACK,
        opacity=0.88,
        buff=0.05
    )
    mob.set_z_index(90)
    return mob


def fit_to_box(mob, max_width, max_height):
    if mob.width > max_width:
        mob.scale(max_width / mob.width)

    if mob.height > max_height:
        mob.scale(max_height / mob.height)

    return mob


def trace_segment(p1, p2, color=NEON_YELLOW, width=TRACE_WIDTH):
    seg = Line(
        p1,
        p2,
        color=color,
        stroke_width=width
    )
    seg.set_z_index(70)
    return seg


def trace_triangle_sides(p1, p2, p3, color=NEON_GREEN):
    side1 = trace_segment(p1, p2, color=color)
    side2 = trace_segment(p2, p3, color=color)
    side3 = trace_segment(p3, p1, color=color)

    return VGroup(side1, side2, side3)


def smart_triangle_fill(p1, p2, p3, color, opacity=TRIANGLE_FILL_OPACITY):
    tri = Polygon(
        p1,
        p2,
        p3,
        color=color,
        fill_color=color,
        fill_opacity=opacity,
        stroke_width=3
    )
    tri.set_z_index(3)
    return tri


def show_triangle_focus(scene, p1, p2, p3, color, opacity=0.24):
    """
    One-triangle focus:
    1. Trace all three sides using one neon color
    2. Fill same triangle
    3. Indicate triangle
    """
    trace = trace_triangle_sides(
        p1,
        p2,
        p3,
        color=color
    )

    fill = smart_triangle_fill(
        p1,
        p2,
        p3,
        color=color,
        opacity=opacity
    )

    scene.play(
        Create(trace),
        run_time=CREATE_SPEED
    )

    scene.play(
        FadeIn(fill),
        run_time=FADE_SPEED
    )

    scene.play(
        Indicate(fill),
        run_time=INDICATE_SPEED
    )

    return VGroup(trace, fill)


def show_segment_focus(scene, p1, p2, color=NEON_YELLOW):
    """
    One-segment focus:
    trace and indicate a single segment.
    """
    seg = trace_segment(
        p1,
        p2,
        color=color
    )

    scene.play(
        Create(seg),
        run_time=CREATE_SPEED
    )

    scene.play(
        Indicate(seg),
        run_time=INDICATE_SPEED
    )

    return seg


def clear_focus(scene, focus_group):
    scene.play(
        FadeOut(focus_group),
        run_time=FADE_SPEED
    )


def angle_side_traces(vertex, p1, p2, color=NEON_YELLOW):
    s1 = trace_segment(
        vertex,
        p1,
        color=color
    )

    s2 = trace_segment(
        vertex,
        p2,
        color=color
    )

    return VGroup(s1, s2)


def interior_angle_arc(vertex, p1, p2, color=NEON_YELLOW, radius=ANGLE_RADIUS):
    """
    Draws smaller interior angle arc between rays vertex->p1 and vertex->p2.
    This avoids most exterior angle issues.
    """
    v1 = p1 - vertex
    v2 = p2 - vertex

    a1 = np.arctan2(v1[1], v1[0])
    a2 = np.arctan2(v2[1], v2[0])

    diff = a2 - a1

    while diff <= -PI:
        diff += TAU

    while diff > PI:
        diff -= TAU

    arc = Arc(
        radius=radius,
        start_angle=a1,
        angle=diff,
        color=color,
        stroke_width=5
    )

    arc.move_arc_center_to(vertex)
    arc.set_z_index(80)

    return arc


def show_angle_focus(scene, vertex, p1, p2, color=NEON_YELLOW, radius=0.28):
    """
    Angle focus:
    1. Trace the two sides forming the angle
    2. Show interior angle arc
    3. Indicate angle
    """
    side_traces = angle_side_traces(
        vertex,
        p1,
        p2,
        color=color
    )

    angle_arc = interior_angle_arc(
        vertex,
        p1,
        p2,
        color=color,
        radius=radius
    )

    scene.play(
        Create(side_traces),
        run_time=CREATE_SPEED
    )

    scene.play(
        Create(angle_arc),
        run_time=CREATE_SPEED
    )

    scene.play(
        Indicate(angle_arc),
        run_time=INDICATE_SPEED
    )

    return VGroup(side_traces, angle_arc)


def show_right_angle_focus(scene, vertex, p1, p2, color=NEON_YELLOW, size=0.17):
    """
    Right angle focus:
    1. Trace two perpendicular rays
    2. Show right-angle square
    3. Indicate square
    """
    side_traces = angle_side_traces(
        vertex,
        p1,
        p2,
        color=color
    )

    right_square = RightAngle(
        Line(vertex, p1),
        Line(vertex, p2),
        length=size,
        color=color,
        stroke_width=4
    )

    right_square.set_z_index(85)

    scene.play(
        Create(side_traces),
        run_time=CREATE_SPEED
    )

    scene.play(
        Create(right_square),
        run_time=CREATE_SPEED
    )

    scene.play(
        Indicate(right_square),
        run_time=INDICATE_SPEED
    )

    return VGroup(side_traces, right_square)


def arrow_from_text_to_point(active_card, line_index, target_point, color=NEON_TEAL):
    content = active_card[1]
    source = content[line_index].get_right() + RIGHT * 0.12

    arrow = Arrow(
        source,
        target_point,
        color=color,
        buff=0.15,
        stroke_width=4,
        max_tip_length_to_length_ratio=0.08
    )

    arrow.set_z_index(85)

    return arrow


class SmartColumnLayout:
    def __init__(self, left_x, top_y, bottom_y, gap=0.12):
        self.left_x = left_x
        self.top_y = top_y
        self.bottom_y = bottom_y
        self.gap = gap
        self.next_top = top_y

    def available_height(self):
        return self.next_top - self.bottom_y

    def can_fit(self, mob):
        return mob.height <= self.available_height()

    def place(self, mob):
        center_x = self.left_x + mob.width / 2
        center_y = self.next_top - mob.height / 2

        mob.move_to([center_x, center_y, 0])

        self.next_top = mob.get_bottom()[1] - self.gap

        return mob


def make_line(kind, content, mode):
    if mode == "active":
        text_size = ACTIVE_TEXT_SIZE
        math_size = ACTIVE_MATH_SIZE
    else:
        text_size = COMPACT_TEXT_SIZE
        math_size = COMPACT_MATH_SIZE

    if kind == "text":
        return Text(
            content,
            font_size=text_size
        )

    if kind == "tex":
        return Tex(
            content,
            font_size=text_size
        )

    if kind == "math":
        return MathTex(
            content,
            font_size=math_size
        )

    return Text(
        content,
        font_size=text_size
    )


def make_active_card(title, color, lines):
    heading = Text(
        title,
        font_size=ACTIVE_HEADING_SIZE,
        color=color
    )

    items = [heading]

    for kind, content in lines:
        items.append(
            make_line(kind, content, mode="active")
        )

    content_group = VGroup(*items).arrange(
        DOWN,
        aligned_edge=LEFT,
        buff=0.055
    )

    fit_to_box(
        content_group,
        ACTIVE_CARD_WIDTH - 0.45,
        ACTIVE_CARD_HEIGHT - 0.40
    )

    box_height = max(
        1.25,
        content_group.height + 0.42
    )

    box = RoundedRectangle(
        width=ACTIVE_CARD_WIDTH,
        height=box_height,
        corner_radius=0.13,
        color=color,
        stroke_width=1.7
    )

    box.set_fill(
        BLACK,
        opacity=0.10
    )

    content_group.move_to(
        box.get_center()
    )

    content_group.align_to(
        box.get_left() + RIGHT * 0.20,
        LEFT
    )

    card = VGroup(
        box,
        content_group
    )

    card.move_to(
        ACTIVE_CENTER
    )

    return card


def make_compact_note(title, color, lines):
    heading = Text(
        title,
        font_size=COMPACT_HEADING_SIZE,
        color=color
    )

    items = [heading]

    for kind, content in lines:
        items.append(
            make_line(kind, content, mode="compact")
        )

    note = VGroup(*items).arrange(
        DOWN,
        aligned_edge=LEFT,
        buff=0.03
    )

    if note.width > COMPACT_MAX_WIDTH:
        note.scale(
            COMPACT_MAX_WIDTH / note.width
        )

    return note


def show_active_card(scene, title, color, lines):
    card = make_active_card(
        title,
        color,
        lines
    )

    box = card[0]
    content = card[1]

    scene.play(
        Create(box),
        run_time=CREATE_SPEED
    )

    scene.play(
        Write(content[0]),
        run_time=WRITE_SPEED
    )

    return card


def write_next_line(scene, active_card, line_index):
    content = active_card[1]

    scene.play(
        Write(content[line_index]),
        run_time=WRITE_SPEED
    )


def move_to_smart_location(
    scene,
    active_card,
    title,
    color,
    compact_lines,
    left_layout,
    middle_layout
):
    compact_note = make_compact_note(
        title,
        color,
        compact_lines
    )

    if left_layout.can_fit(compact_note):
        left_layout.place(compact_note)
    else:
        middle_layout.place(compact_note)

    scene.wait(
        READ_STEP_WAIT_TIME
    )

    scene.play(
        ReplacementTransform(
            active_card,
            compact_note
        ),
        run_time=MOVE_SPEED
    )

    return compact_note


def blink_box(scene, box, blink_color=RED, base_color=YELLOW):
    for _ in range(3):
        scene.play(
            box.animate.set_stroke(
                color=blink_color,
                width=5
            ),
            run_time=0.22
        )

        scene.play(
            box.animate.set_stroke(
                color=base_color,
                width=2.5
            ),
            run_time=0.22
        )


# ==========================================================
# MAIN SCENE
# ==========================================================

class AreasOfSimilarTriangles(Scene):

    def construct(self):

        # ==================================================
        # TITLE
        # ==================================================

        title = Text(
            "Theorem of Areas of Similar Triangles",
            font_size=TITLE_FONT_SIZE,
            color=TITLE_COLOR
        )

        title.to_edge(
            UP,
            buff=0.18
        )

        self.play(
            Write(title),
            run_time=WRITE_SPEED
        )

        # ==================================================
        # SMART LAYOUTS
        # ==================================================

        left_layout = SmartColumnLayout(
            left_x=LEFT_NOTE_LEFT_X,
            top_y=2.55,
            bottom_y=-3.58,
            gap=0.12
        )

        middle_bottom_layout = SmartColumnLayout(
            left_x=MIDDLE_NOTE_LEFT_X,
            top_y=-0.75,
            bottom_y=-3.50,
            gap=0.16
        )

        steps_label = Text(
            "Steps",
            font_size=22,
            color=GREY_A
        )

        steps_label.move_to(
            [MIDDLE_CENTER_X, 2.78, 0]
        )

        self.play(
            Write(steps_label),
            run_time=WRITE_SPEED
        )

        # ==================================================
        # RIGHT SIDE GEOMETRY
        # ==================================================

        # Triangle ABC
        B_pos = np.array([-1.55, 0.10, 0]) + DIAGRAM_SHIFT
        C_pos = np.array([0.05, 0.10, 0]) + DIAGRAM_SHIFT
        D_pos = np.array([-0.35, 0.10, 0]) + DIAGRAM_SHIFT
        A_pos = np.array([-0.35, 1.55, 0]) + DIAGRAM_SHIFT

        # Triangle PQR
        Q_pos = np.array([0.45, 0.10, 0]) + DIAGRAM_SHIFT
        R_pos = np.array([1.85, 0.10, 0]) + DIAGRAM_SHIFT
        S_pos = np.array([1.15, 0.10, 0]) + DIAGRAM_SHIFT
        P_pos = np.array([1.15, 1.28, 0]) + DIAGRAM_SHIFT

        triangle_ABC = Polygon(
            A_pos,
            B_pos,
            C_pos,
            color=MAIN_TRIANGLE_COLOR,
            stroke_width=3
        )

        triangle_PQR = Polygon(
            P_pos,
            Q_pos,
            R_pos,
            color=MAIN_TRIANGLE_COLOR,
            stroke_width=3
        )

        AD = Line(
            A_pos,
            D_pos,
            color=ALTITUDE_COLOR,
            stroke_width=3
        )

        PS = Line(
            P_pos,
            S_pos,
            color=ALTITUDE_COLOR,
            stroke_width=3
        )

        right_angle_D = RightAngle(
            Line(D_pos, A_pos),
            Line(D_pos, C_pos),
            length=0.15,
            color=WHITE,
            stroke_width=2
        )

        right_angle_S = RightAngle(
            Line(S_pos, P_pos),
            Line(S_pos, R_pos),
            length=0.15,
            color=WHITE,
            stroke_width=2
        )

        self.play(
            Create(triangle_ABC),
            Create(triangle_PQR),
            run_time=CREATE_SPEED
        )

        self.play(
            Create(AD),
            Create(PS),
            Create(right_angle_D),
            Create(right_angle_S),
            run_time=CREATE_SPEED
        )

        A = Dot(A_pos, radius=0.04)
        B = Dot(B_pos, radius=0.04)
        C = Dot(C_pos, radius=0.04)
        D = Dot(D_pos, radius=0.04)

        P = Dot(P_pos, radius=0.04)
        Q = Dot(Q_pos, radius=0.04)
        R = Dot(R_pos, radius=0.04)
        S = Dot(S_pos, radius=0.04)

        points = VGroup(A, B, C, D, P, Q, R, S)
        points.set_z_index(60)

        self.play(
            FadeIn(points),
            run_time=FADE_SPEED
        )

        labels = VGroup(
            readable_label(
                MathTex("A", font_size=LABEL_FONT_SIZE).move_to(
                    A_pos + UP * 0.25
                )
            ),
            readable_label(
                MathTex("B", font_size=LABEL_FONT_SIZE).move_to(
                    B_pos + LEFT * 0.22 + DOWN * 0.18
                )
            ),
            readable_label(
                MathTex("C", font_size=LABEL_FONT_SIZE).move_to(
                    C_pos + RIGHT * 0.20 + DOWN * 0.18
                )
            ),
            readable_label(
                MathTex("D", font_size=LABEL_FONT_SIZE).move_to(
                    D_pos + DOWN * 0.25
                )
            ),
            readable_label(
                MathTex("P", font_size=LABEL_FONT_SIZE).move_to(
                    P_pos + UP * 0.25
                )
            ),
            readable_label(
                MathTex("Q", font_size=LABEL_FONT_SIZE).move_to(
                    Q_pos + LEFT * 0.18 + DOWN * 0.18
                )
            ),
            readable_label(
                MathTex("R", font_size=LABEL_FONT_SIZE).move_to(
                    R_pos + RIGHT * 0.18 + DOWN * 0.18
                )
            ),
            readable_label(
                MathTex("S", font_size=LABEL_FONT_SIZE).move_to(
                    S_pos + DOWN * 0.25
                )
            ),
        )

        self.play(
            Write(labels),
            run_time=WRITE_SPEED
        )

        # ==================================================
        # THEOREM
        # ==================================================

        theorem_active_lines = [
            ("text", "For two similar triangles,"),
            ("text", "area ratio equals square of side ratio.")
        ]

        theorem_compact_lines = [
            ("text", "For two similar triangles,"),
            ("text", "area ratio equals square of side ratio.")
        ]

        theorem_active = show_active_card(
            self,
            "Theorem",
            THEOREM_COLOR,
            theorem_active_lines
        )

        write_next_line(self, theorem_active, 1)
        write_next_line(self, theorem_active, 2)

        theorem_note = move_to_smart_location(
            self,
            theorem_active,
            "Theorem",
            THEOREM_COLOR,
            theorem_compact_lines,
            left_layout,
            middle_bottom_layout
        )

        # ==================================================
        # GIVEN
        # ==================================================

        given_active_lines = [
            ("math", r"\triangle ABC \sim \triangle PQR"),
            ("math", r"AD \perp BC,\quad PS \perp QR")
        ]

        given_compact_lines = [
            ("math", r"\triangle ABC \sim \triangle PQR,\quad AD\perp BC,\quad PS\perp QR")
        ]

        given_active = show_active_card(
            self,
            "Given",
            GIVEN_COLOR,
            given_active_lines
        )

        write_next_line(self, given_active, 1)

        arrow_given_tri_1 = arrow_from_text_to_point(
            given_active,
            1,
            (A_pos + B_pos + C_pos) / 3,
            color=NEON_TEAL
        )

        self.play(Create(arrow_given_tri_1), run_time=CREATE_SPEED)

        focus_given_abc = show_triangle_focus(
            self,
            A_pos,
            B_pos,
            C_pos,
            color=NEON_GREEN,
            opacity=0.18
        )

        self.play(FadeOut(arrow_given_tri_1), run_time=FADE_SPEED)

        clear_focus(self, focus_given_abc)

        arrow_given_tri_2 = arrow_from_text_to_point(
            given_active,
            1,
            (P_pos + Q_pos + R_pos) / 3,
            color=NEON_TEAL
        )

        self.play(Create(arrow_given_tri_2), run_time=CREATE_SPEED)

        focus_given_pqr = show_triangle_focus(
            self,
            P_pos,
            Q_pos,
            R_pos,
            color=NEON_PINK,
            opacity=0.18
        )

        self.play(FadeOut(arrow_given_tri_2), run_time=FADE_SPEED)

        clear_focus(self, focus_given_pqr)

        write_next_line(self, given_active, 2)

        arrow_given_height_1 = arrow_from_text_to_point(
            given_active,
            2,
            D_pos,
            color=NEON_TEAL
        )

        self.play(Create(arrow_given_height_1), run_time=CREATE_SPEED)

        focus_AD = show_segment_focus(
            self,
            A_pos,
            D_pos,
            color=NEON_ORANGE
        )

        focus_BC = show_segment_focus(
            self,
            B_pos,
            C_pos,
            color=NEON_YELLOW
        )

        self.play(
            Indicate(right_angle_D),
            run_time=INDICATE_SPEED
        )

        self.play(FadeOut(arrow_given_height_1), run_time=FADE_SPEED)

        clear_focus(self, focus_AD)
        clear_focus(self, focus_BC)

        arrow_given_height_2 = arrow_from_text_to_point(
            given_active,
            2,
            S_pos,
            color=NEON_TEAL
        )

        self.play(Create(arrow_given_height_2), run_time=CREATE_SPEED)

        focus_PS = show_segment_focus(
            self,
            P_pos,
            S_pos,
            color=NEON_ORANGE
        )

        focus_QR = show_segment_focus(
            self,
            Q_pos,
            R_pos,
            color=NEON_YELLOW
        )

        self.play(
            Indicate(right_angle_S),
            run_time=INDICATE_SPEED
        )

        self.play(FadeOut(arrow_given_height_2), run_time=FADE_SPEED)

        clear_focus(self, focus_PS)
        clear_focus(self, focus_QR)

        given_note = move_to_smart_location(
            self,
            given_active,
            "Given",
            GIVEN_COLOR,
            given_compact_lines,
            left_layout,
            middle_bottom_layout
        )

        # ==================================================
        # TO PROVE
        # ==================================================

        prove_active_lines = [
            ("math", r"\frac{A(\triangle ABC)}{A(\triangle PQR)}"),
            ("math", r"=\frac{AB^2}{PQ^2}=\frac{BC^2}{QR^2}=\frac{AC^2}{PR^2}")
        ]

        prove_compact_lines = [
            ("math", r"\frac{A(\triangle ABC)}{A(\triangle PQR)}=\frac{AB^2}{PQ^2}=\frac{BC^2}{QR^2}=\frac{AC^2}{PR^2}")
        ]

        prove_active = show_active_card(
            self,
            "To Prove",
            PROVE_COLOR,
            prove_active_lines
        )

        write_next_line(self, prove_active, 1)

        arrow_prove_1 = arrow_from_text_to_point(
            prove_active,
            1,
            (A_pos + B_pos + C_pos) / 3,
            color=NEON_TEAL
        )

        self.play(Create(arrow_prove_1), run_time=CREATE_SPEED)

        focus_prove_abc = show_triangle_focus(
            self,
            A_pos,
            B_pos,
            C_pos,
            color=NEON_GREEN,
            opacity=0.18
        )

        self.play(FadeOut(arrow_prove_1), run_time=FADE_SPEED)

        clear_focus(self, focus_prove_abc)

        arrow_prove_2 = arrow_from_text_to_point(
            prove_active,
            1,
            (P_pos + Q_pos + R_pos) / 3,
            color=NEON_TEAL
        )

        self.play(Create(arrow_prove_2), run_time=CREATE_SPEED)

        focus_prove_pqr = show_triangle_focus(
            self,
            P_pos,
            Q_pos,
            R_pos,
            color=NEON_PINK,
            opacity=0.18
        )

        self.play(FadeOut(arrow_prove_2), run_time=FADE_SPEED)

        clear_focus(self, focus_prove_pqr)

        write_next_line(self, prove_active, 2)

        prove_note = move_to_smart_location(
            self,
            prove_active,
            "To Prove",
            PROVE_COLOR,
            prove_compact_lines,
            left_layout,
            middle_bottom_layout
        )

        # ==================================================
        # STEP 1: AREA RATIO
        # ==================================================

        step1_active_lines = [
            ("text", "Using area formula of triangle,"),
            ("math", r"\frac{A(\triangle ABC)}{A(\triangle PQR)}"),
            ("math", r"=\frac{BC\times AD}{QR\times PS}"),
            ("math", r"=\frac{BC}{QR}\times\frac{AD}{PS}\quad (I)")
        ]

        step1_compact_lines = [
            ("text", "Using area formula,"),
            ("math", r"\frac{A(\triangle ABC)}{A(\triangle PQR)}=\frac{BC\times AD}{QR\times PS}=\frac{BC}{QR}\times\frac{AD}{PS}\;(I)")
        ]

        step1_active = show_active_card(
            self,
            "Step 1: Area Ratio",
            STEP1_COLOR,
            step1_active_lines
        )

        write_next_line(self, step1_active, 1)

        arrow_area_abc = arrow_from_text_to_point(
            step1_active,
            1,
            (A_pos + B_pos + C_pos) / 3,
            color=NEON_TEAL
        )

        self.play(Create(arrow_area_abc), run_time=CREATE_SPEED)

        focus_area_abc = show_triangle_focus(
            self,
            A_pos,
            B_pos,
            C_pos,
            color=NEON_GREEN,
            opacity=0.18
        )

        self.play(FadeOut(arrow_area_abc), run_time=FADE_SPEED)

        clear_focus(self, focus_area_abc)

        arrow_area_pqr = arrow_from_text_to_point(
            step1_active,
            1,
            (P_pos + Q_pos + R_pos) / 3,
            color=NEON_TEAL
        )

        self.play(Create(arrow_area_pqr), run_time=CREATE_SPEED)

        focus_area_pqr = show_triangle_focus(
            self,
            P_pos,
            Q_pos,
            R_pos,
            color=NEON_PINK,
            opacity=0.18
        )

        self.play(FadeOut(arrow_area_pqr), run_time=FADE_SPEED)

        clear_focus(self, focus_area_pqr)

        write_next_line(self, step1_active, 2)

        arrow_area_formula_1 = arrow_from_text_to_point(
            step1_active,
            2,
            (A_pos + B_pos + C_pos) / 3,
            color=NEON_TEAL
        )

        self.play(Create(arrow_area_formula_1), run_time=CREATE_SPEED)

        focus_abc_area_again = show_triangle_focus(
            self,
            A_pos,
            B_pos,
            C_pos,
            color=NEON_GREEN,
            opacity=0.18
        )

        self.play(FadeOut(arrow_area_formula_1), run_time=FADE_SPEED)

        clear_focus(self, focus_abc_area_again)

        arrow_area_formula_2 = arrow_from_text_to_point(
            step1_active,
            2,
            (P_pos + Q_pos + R_pos) / 3,
            color=NEON_TEAL
        )

        self.play(Create(arrow_area_formula_2), run_time=CREATE_SPEED)

        focus_pqr_area_again = show_triangle_focus(
            self,
            P_pos,
            Q_pos,
            R_pos,
            color=NEON_PINK,
            opacity=0.18
        )

        self.play(FadeOut(arrow_area_formula_2), run_time=FADE_SPEED)

        clear_focus(self, focus_pqr_area_again)

        write_next_line(self, step1_active, 3)

        arrow_bc = arrow_from_text_to_point(
            step1_active,
            3,
            (B_pos + C_pos) / 2,
            color=NEON_TEAL
        )

        self.play(Create(arrow_bc), run_time=CREATE_SPEED)

        focus_BC = show_segment_focus(
            self,
            B_pos,
            C_pos,
            color=NEON_YELLOW
        )

        self.play(FadeOut(arrow_bc), run_time=FADE_SPEED)

        clear_focus(self, focus_BC)

        arrow_ad = arrow_from_text_to_point(
            step1_active,
            3,
            (A_pos + D_pos) / 2,
            color=NEON_TEAL
        )

        self.play(Create(arrow_ad), run_time=CREATE_SPEED)

        focus_AD = show_segment_focus(
            self,
            A_pos,
            D_pos,
            color=NEON_ORANGE
        )

        self.play(FadeOut(arrow_ad), run_time=FADE_SPEED)

        clear_focus(self, focus_AD)

        arrow_qr = arrow_from_text_to_point(
            step1_active,
            3,
            (Q_pos + R_pos) / 2,
            color=NEON_TEAL
        )

        self.play(Create(arrow_qr), run_time=CREATE_SPEED)

        focus_QR = show_segment_focus(
            self,
            Q_pos,
            R_pos,
            color=NEON_YELLOW
        )

        self.play(FadeOut(arrow_qr), run_time=FADE_SPEED)

        clear_focus(self, focus_QR)

        arrow_ps = arrow_from_text_to_point(
            step1_active,
            3,
            (P_pos + S_pos) / 2,
            color=NEON_TEAL
        )

        self.play(Create(arrow_ps), run_time=CREATE_SPEED)

        focus_PS = show_segment_focus(
            self,
            P_pos,
            S_pos,
            color=NEON_ORANGE
        )

        self.play(FadeOut(arrow_ps), run_time=FADE_SPEED)

        clear_focus(self, focus_PS)

        write_next_line(self, step1_active, 4)

        step1_note = move_to_smart_location(
            self,
            step1_active,
            "Step 1: Area Ratio",
            STEP1_COLOR,
            step1_compact_lines,
            left_layout,
            middle_bottom_layout
        )

        # ==================================================
        # STEP 2: COMPARE HEIGHTS
        # ==================================================

        step2_active_lines = [
            ("tex", r"In $\triangle ABD$ and $\triangle PQS$,"),
            ("math", r"\angle B \cong \angle Q\quad \text{(corresponding angles)}"),
            ("math", r"\angle ADB \cong \angle PSQ\quad \text{(each }90^\circ\text{)}"),
            ("math", r"\therefore\;\triangle ABD \sim \triangle PQS\quad \text{(AA test)}"),
            ("math", r"\frac{AD}{PS}=\frac{AB}{PQ}\quad (II)")
        ]

        step2_compact_lines = [
            ("tex", r"In $\triangle ABD$ and $\triangle PQS$,"),
            ("math", r"\angle B \cong \angle Q,\quad \angle ADB \cong \angle PSQ"),
            ("math", r"\triangle ABD \sim \triangle PQS,\quad \frac{AD}{PS}=\frac{AB}{PQ}\;(II)")
        ]

        step2_active = show_active_card(
            self,
            "Step 2: Compare Heights",
            STEP2_COLOR,
            step2_active_lines
        )

        write_next_line(self, step2_active, 1)

        arrow_abd = arrow_from_text_to_point(
            step2_active,
            1,
            (A_pos + B_pos + D_pos) / 3,
            color=NEON_TEAL
        )

        self.play(Create(arrow_abd), run_time=CREATE_SPEED)

        focus_ABD = show_triangle_focus(
            self,
            A_pos,
            B_pos,
            D_pos,
            color=NEON_GREEN,
            opacity=0.24
        )

        self.play(FadeOut(arrow_abd), run_time=FADE_SPEED)

        clear_focus(self, focus_ABD)

        arrow_pqs = arrow_from_text_to_point(
            step2_active,
            1,
            (P_pos + Q_pos + S_pos) / 3,
            color=NEON_TEAL
        )

        self.play(Create(arrow_pqs), run_time=CREATE_SPEED)

        focus_PQS = show_triangle_focus(
            self,
            P_pos,
            Q_pos,
            S_pos,
            color=NEON_PINK,
            opacity=0.24
        )

        self.play(FadeOut(arrow_pqs), run_time=FADE_SPEED)

        clear_focus(self, focus_PQS)

        write_next_line(self, step2_active, 2)

        arrow_angle_b = arrow_from_text_to_point(
            step2_active,
            2,
            B_pos,
            color=NEON_TEAL
        )

        self.play(Create(arrow_angle_b), run_time=CREATE_SPEED)

        focus_angle_B = show_angle_focus(
            self,
            B_pos,
            A_pos,
            C_pos,
            color=NEON_YELLOW,
            radius=0.28
        )

        self.play(FadeOut(arrow_angle_b), run_time=FADE_SPEED)

        clear_focus(self, focus_angle_B)

        arrow_angle_q = arrow_from_text_to_point(
            step2_active,
            2,
            Q_pos,
            color=NEON_TEAL
        )

        self.play(Create(arrow_angle_q), run_time=CREATE_SPEED)

        focus_angle_Q = show_angle_focus(
            self,
            Q_pos,
            P_pos,
            R_pos,
            color=NEON_YELLOW,
            radius=0.28
        )

        self.play(FadeOut(arrow_angle_q), run_time=FADE_SPEED)

        clear_focus(self, focus_angle_Q)

        write_next_line(self, step2_active, 3)

        arrow_right_d = arrow_from_text_to_point(
            step2_active,
            3,
            D_pos,
            color=NEON_TEAL
        )

        self.play(Create(arrow_right_d), run_time=CREATE_SPEED)

        focus_right_D = show_right_angle_focus(
            self,
            D_pos,
            A_pos,
            B_pos,
            color=NEON_YELLOW,
            size=0.15
        )

        self.play(FadeOut(arrow_right_d), run_time=FADE_SPEED)

        clear_focus(self, focus_right_D)

        arrow_right_s = arrow_from_text_to_point(
            step2_active,
            3,
            S_pos,
            color=NEON_TEAL
        )

        self.play(Create(arrow_right_s), run_time=CREATE_SPEED)

        focus_right_S = show_right_angle_focus(
            self,
            S_pos,
            P_pos,
            Q_pos,
            color=NEON_YELLOW,
            size=0.15
        )

        self.play(FadeOut(arrow_right_s), run_time=FADE_SPEED)

        clear_focus(self, focus_right_S)

        write_next_line(self, step2_active, 4)

        focus_ABD_again = show_triangle_focus(
            self,
            A_pos,
            B_pos,
            D_pos,
            color=NEON_GREEN,
            opacity=0.24
        )

        clear_focus(self, focus_ABD_again)

        focus_PQS_again = show_triangle_focus(
            self,
            P_pos,
            Q_pos,
            S_pos,
            color=NEON_PINK,
            opacity=0.24
        )

        clear_focus(self, focus_PQS_again)

        write_next_line(self, step2_active, 5)

        arrow_ad_ratio = arrow_from_text_to_point(
            step2_active,
            5,
            (A_pos + D_pos) / 2,
            color=NEON_TEAL
        )

        self.play(Create(arrow_ad_ratio), run_time=CREATE_SPEED)

        focus_AD_ratio = show_segment_focus(
            self,
            A_pos,
            D_pos,
            color=NEON_ORANGE
        )

        self.play(FadeOut(arrow_ad_ratio), run_time=FADE_SPEED)

        clear_focus(self, focus_AD_ratio)

        arrow_ps_ratio = arrow_from_text_to_point(
            step2_active,
            5,
            (P_pos + S_pos) / 2,
            color=NEON_TEAL
        )

        self.play(Create(arrow_ps_ratio), run_time=CREATE_SPEED)

        focus_PS_ratio = show_segment_focus(
            self,
            P_pos,
            S_pos,
            color=NEON_ORANGE
        )

        self.play(FadeOut(arrow_ps_ratio), run_time=FADE_SPEED)

        clear_focus(self, focus_PS_ratio)

        arrow_ab_ratio = arrow_from_text_to_point(
            step2_active,
            5,
            (A_pos + B_pos) / 2,
            color=NEON_TEAL
        )

        self.play(Create(arrow_ab_ratio), run_time=CREATE_SPEED)

        focus_AB_ratio = show_segment_focus(
            self,
            A_pos,
            B_pos,
            color=NEON_GREEN
        )

        self.play(FadeOut(arrow_ab_ratio), run_time=FADE_SPEED)

        clear_focus(self, focus_AB_ratio)

        arrow_pq_ratio = arrow_from_text_to_point(
            step2_active,
            5,
            (P_pos + Q_pos) / 2,
            color=NEON_TEAL
        )

        self.play(Create(arrow_pq_ratio), run_time=CREATE_SPEED)

        focus_PQ_ratio = show_segment_focus(
            self,
            P_pos,
            Q_pos,
            color=NEON_PINK
        )

        self.play(FadeOut(arrow_pq_ratio), run_time=FADE_SPEED)

        clear_focus(self, focus_PQ_ratio)

        step2_note = move_to_smart_location(
            self,
            step2_active,
            "Step 2: Compare Heights",
            STEP2_COLOR,
            step2_compact_lines,
            left_layout,
            middle_bottom_layout
        )

        # ==================================================
        # STEP 3: SIMILARITY RATIO
        # ==================================================

        step3_active_lines = [
            ("text", "Since original triangles are similar,"),
            ("math", r"\frac{AB}{PQ}=\frac{BC}{QR}=\frac{AC}{PR}\quad (III)")
        ]

        step3_compact_lines = [
            ("text", "Since original triangles are similar,"),
            ("math", r"\frac{AB}{PQ}=\frac{BC}{QR}=\frac{AC}{PR}\;(III)")
        ]

        step3_active = show_active_card(
            self,
            "Step 3: Similarity Ratio",
            STEP3_COLOR,
            step3_active_lines
        )

        write_next_line(self, step3_active, 1)

        arrow_sim_abc = arrow_from_text_to_point(
            step3_active,
            1,
            (A_pos + B_pos + C_pos) / 3,
            color=NEON_TEAL
        )

        self.play(Create(arrow_sim_abc), run_time=CREATE_SPEED)

        focus_sim_abc = show_triangle_focus(
            self,
            A_pos,
            B_pos,
            C_pos,
            color=NEON_GREEN,
            opacity=0.18
        )

        self.play(FadeOut(arrow_sim_abc), run_time=FADE_SPEED)

        clear_focus(self, focus_sim_abc)

        arrow_sim_pqr = arrow_from_text_to_point(
            step3_active,
            1,
            (P_pos + Q_pos + R_pos) / 3,
            color=NEON_TEAL
        )

        self.play(Create(arrow_sim_pqr), run_time=CREATE_SPEED)

        focus_sim_pqr = show_triangle_focus(
            self,
            P_pos,
            Q_pos,
            R_pos,
            color=NEON_PINK,
            opacity=0.18
        )

        self.play(FadeOut(arrow_sim_pqr), run_time=FADE_SPEED)

        clear_focus(self, focus_sim_pqr)

        write_next_line(self, step3_active, 2)

        segment_pairs = [
            (A_pos, B_pos, NEON_GREEN),
            (P_pos, Q_pos, NEON_PINK),
            (B_pos, C_pos, NEON_GREEN),
            (Q_pos, R_pos, NEON_PINK),
            (A_pos, C_pos, NEON_GREEN),
            (P_pos, R_pos, NEON_PINK),
        ]

        for p1, p2, col in segment_pairs:
            focus_side = show_segment_focus(
                self,
                p1,
                p2,
                color=col
            )
            clear_focus(
                self,
                focus_side
            )

        step3_note = move_to_smart_location(
            self,
            step3_active,
            "Step 3: Similarity Ratio",
            STEP3_COLOR,
            step3_compact_lines,
            left_layout,
            middle_bottom_layout
        )

        # ==================================================
        # FINAL RESULT
        # ==================================================

        final_active_lines = [
            ("text", "From (I), (II), and (III),"),
            ("math", r"\frac{A(\triangle ABC)}{A(\triangle PQR)}"),
            ("math", r"=\frac{AB^2}{PQ^2}=\frac{BC^2}{QR^2}=\frac{AC^2}{PR^2}")
        ]

        final_compact_lines = [
            ("text", "From (I), (II), and (III),"),
            ("math", r"\frac{A(\triangle ABC)}{A(\triangle PQR)}=\frac{AB^2}{PQ^2}=\frac{BC^2}{QR^2}=\frac{AC^2}{PR^2}")
        ]

        final_active = show_active_card(
            self,
            "Final Result",
            FINAL_COLOR,
            final_active_lines
        )

        write_next_line(self, final_active, 1)
        write_next_line(self, final_active, 2)

        focus_final_abc = show_triangle_focus(
            self,
            A_pos,
            B_pos,
            C_pos,
            color=NEON_GREEN,
            opacity=0.18
        )

        clear_focus(self, focus_final_abc)

        focus_final_pqr = show_triangle_focus(
            self,
            P_pos,
            Q_pos,
            R_pos,
            color=NEON_PINK,
            opacity=0.18
        )

        clear_focus(self, focus_final_pqr)

        write_next_line(self, final_active, 3)

        final_note = move_to_smart_location(
            self,
            final_active,
            "Final Result",
            FINAL_COLOR,
            final_compact_lines,
            left_layout,
            middle_bottom_layout
        )

        # ==================================================
        # FINAL RESULT BOX
        # ==================================================

        final_box = RoundedRectangle(
            width=4.65,
            height=1.78,
            corner_radius=0.18,
            color=YELLOW,
            stroke_width=2.5
        )

        final_box.move_to(
            [RIGHT_CENTER_X, -2.78, 0]
        )

        final_box.set_fill(
            BLACK,
            opacity=0.12
        )

        final_heading = Text(
            "Result",
            font_size=23,
            color=YELLOW
        )

        final_formula = MathTex(
            r"\frac{A(\triangle ABC)}{A(\triangle PQR)}"
            r"="
            r"\frac{AB^2}{PQ^2}"
            r"="
            r"\frac{BC^2}{QR^2}"
            r"="
            r"\frac{AC^2}{PR^2}",
            font_size=22,
            color=YELLOW
        )

        if final_formula.width > final_box.width - 0.45:
            final_formula.scale(
                (final_box.width - 0.45) / final_formula.width
            )

        final_group = VGroup(
            final_heading,
            final_formula
        ).arrange(
            DOWN,
            buff=0.30
        )

        final_group.move_to(
            final_box.get_center()
        )

        self.play(
            Create(final_box),
            run_time=CREATE_SPEED
        )

        self.play(
            Write(final_group),
            run_time=WRITE_SPEED
        )

        blink_box(
            self,
            final_box,
            blink_color=RED,
            base_color=YELLOW
        )

        self.play(
            Circumscribe(
                final_group,
                color=RED,
                time_width=1.2,
                buff=0.28
            ),
            run_time=1.4
        )

        self.wait(2)

        # ==================================================
        # CLEAR CANVAS
        # ==================================================

        self.play(
            FadeOut(*self.mobjects),
            run_time=1.2
        )

        # ==================================================
        # SUBSCRIBE END SCREEN
        # ==================================================

        subscribe_text = Text(
            "SUBSCRIBE",
            font_size=78,
            weight=BOLD,
            color=RED
        )

        like_text = Text(
            "LIKE  👍  😊",
            font_size=44,
            color=YELLOW,
            font="Segoe UI Emoji"
        )

        share_text = Text(
            "SHARE",
            font_size=44,
            weight=BOLD,
            color=NEON_TEAL
        )

        thanks_text = Text(
            "Thank you for watching!",
            font_size=30,
            color=WHITE
        )

        end_group = VGroup(
            subscribe_text,
            like_text,
            share_text,
            thanks_text
        ).arrange(
            DOWN,
            buff=0.32
        )

        end_group.move_to(ORIGIN)

        self.play(
            GrowFromCenter(subscribe_text),
            run_time=1.0
        )

        self.play(
            Write(like_text),
            run_time=0.9
        )

        self.play(
            Write(share_text),
            run_time=0.9
        )

        self.play(
            FadeIn(thanks_text),
            run_time=0.8
        )

        self.play(
            Indicate(
                subscribe_text,
                color=YELLOW,
                scale_factor=1.12
            ),
            run_time=1.2
        )

        self.play(
            Indicate(
                share_text,
                color=NEON_YELLOW,
                scale_factor=1.12
            ),
            run_time=1.0
        )

        self.play(
            Flash(
                subscribe_text,
                color=YELLOW,
                flash_radius=1.3,
                line_length=0.25
            ),
            run_time=1.2
        )

        self.wait(3)
