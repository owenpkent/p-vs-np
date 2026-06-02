# Visualizations, manim Scenes

Built with [manim Community Edition](https://docs.manim.community/) (v0.18+).

## Setup

| Dependency | Purpose | Install |
|---|---|---|
| Python 3.10+ | Runtime | python.org |
| manim | Animation engine | `pip install manim` |
| FFmpeg | Video encoding | `winget install Gyan.FFmpeg` |
| LaTeX (MiKTeX or TeX Live) | Math typesetting | miktex.org / tug.org/texlive |

```powershell
pip install manim
```

## Rendering

```powershell
# Low quality, fast preview (480p)
manim -ql visualizations/<folder>/<script>.py <SceneName>

# High quality (1080p)
manim -qh visualizations/<folder>/<script>.py <SceneName>
```

## Scenes

| Folder | Scene | What it shows |
|---|---|---|
| `01_sat_phase_transition/` | `SatPhaseTransition` | The random 3-SAT satisfiability curve and the running-time hardness peak both crossing the threshold near $\alpha_c \approx 4.267$. The visual companion to [`experiments/sat_phase_transition/`](../experiments/sat_phase_transition/). |

## Planned scenes

- The BGS diagonalization: a poly-time oracle machine querying a sub-$2^n$ set of
  strings, and the free string flipping the answer.
- The switching lemma: a width-$w$ term collapsing under a random restriction
  while parity stays robust.
