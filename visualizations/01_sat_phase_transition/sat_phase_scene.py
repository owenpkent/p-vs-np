"""Manim scene: the random 3-SAT phase transition and the hardness peak.

Visual companion to experiments/sat_phase_transition/. It draws two curves on a
shared horizontal axis (the clause/variable ratio alpha): the probability that a
random 3-SAT instance is satisfiable (dropping from 1 to 0), and the running-time
hardness of a complete solver (peaking). Both cross near the threshold
alpha_c ~ 4.267, the visual statement of the easy-hard-easy pattern.

The data here are illustrative shapes (a logistic drop for satisfiability and a
bump for hardness), chosen to match the qualitative curves the experiment
produces. The point of the animation is the COINCIDENCE of the crossing and the
peak, which is the structurally important fact for complexity theory.

Render:
    manim -ql visualizations/01_sat_phase_transition/sat_phase_scene.py SatPhaseTransition
"""

from __future__ import annotations

import math

try:
    from manim import (
        Scene, Axes, Create, Write, Text, MathTex, DashedLine,
        VGroup, BLUE, RED, GRAY, YELLOW, UP, DOWN, LEFT, RIGHT,
    )
    _HAS_MANIM = True
except Exception:  # pragma: no cover - manim is optional at lint time
    _HAS_MANIM = False


ALPHA_C = 4.267


def _sat_prob(alpha: float) -> float:
    """Illustrative satisfiability probability: a sharp logistic drop at alpha_c."""
    return 1.0 / (1.0 + math.exp(6.0 * (alpha - ALPHA_C)))


def _hardness(alpha: float) -> float:
    """Illustrative solver hardness: a bump centered at alpha_c (normalized to 1)."""
    return math.exp(-((alpha - ALPHA_C) ** 2) / 0.5)


if _HAS_MANIM:

    class SatPhaseTransition(Scene):
        def construct(self):
            title = Text("Random 3-SAT phase transition", font_size=36).to_edge(UP)
            self.play(Write(title))

            axes = Axes(
                x_range=[3.0, 6.0, 0.5],
                y_range=[0.0, 1.1, 0.5],
                x_length=9,
                y_length=4.5,
                axis_config={"include_numbers": True},
            ).shift(DOWN * 0.3)
            x_label = axes.get_x_axis_label(MathTex(r"\alpha = m/n"))
            self.play(Create(axes), Write(x_label))

            sat_curve = axes.plot(_sat_prob, x_range=[3.0, 6.0], color=BLUE)
            hard_curve = axes.plot(_hardness, x_range=[3.0, 6.0], color=RED)

            sat_label = Text("P(satisfiable)", font_size=24, color=BLUE).to_corner(LEFT + DOWN)
            hard_label = Text("solver hardness", font_size=24, color=RED).next_to(sat_label, RIGHT, buff=1.0)

            self.play(Create(sat_curve), Write(sat_label))
            self.play(Create(hard_curve), Write(hard_label))

            # The threshold line where the crossing and the peak coincide.
            xc = axes.c2p(ALPHA_C, 0.0)
            xc_top = axes.c2p(ALPHA_C, 1.1)
            thresh = DashedLine(xc, xc_top, color=GRAY)
            thresh_label = MathTex(r"\alpha_c \approx 4.267", color=YELLOW).scale(0.7)
            thresh_label.next_to(xc_top, UP, buff=0.1)
            self.play(Create(thresh), Write(thresh_label))

            caption = Text(
                "The SAT/UNSAT crossing and the hardness peak coincide.",
                font_size=24,
            ).to_edge(DOWN)
            self.play(Write(caption))
            self.wait(2)
