# Researcher mindset

The operating philosophy of this project. Read this first. It defines what
counts as progress.

## The problem is a target, not a monument

P vs NP has been open since 1971 and is one of the seven Clay Millennium Prize
Problems. It is easy to treat such a problem as a monument: something to admire,
circle, and leave untouched. This project does the opposite. We treat it as a
target. We are trying to solve it. The odds against any single program are long,
and that is the honest baseline, but long odds are a reason to be precise, not a
reason to stop.

## We advance a front

Progress is not "solved / unsolved." Progress is moving a front: pushing the
boundary of what is known about which techniques can work and what a winning
technique must look like. The three barrier theorems are the clearest example.
Each one did not solve P vs NP, but each one permanently changed the map by
ruling out a whole class of attacks. Williams's 2011 result moved the front the
other way, by exhibiting a technique that threads all three barriers. Both kinds
of move are progress.

## Negative results are coordinates

When a barrier rules out a class of techniques, that is not a defeat. It is a
coordinate. Relativization tells us the proof must open up the machine. Natural
proofs tells us the lower-bound property must be non-constructive or
function-specific. Algebrization tells us the technique must fail under
low-degree oracle extensions. Three coordinates pin a point: the proof must be
non-relativizing, non-natural, and non-algebrizing at once. That is a far sharper
target than "prove P is not NP."

Avoid fatalism. "Stuck," "hopeless," "can never" are not the vocabulary of this
project. A barrier is a wall only if you insist on walking into it; read as a
compass, it points away from the wall toward where the proof can live.

## Honesty is the engine

The single most important discipline is honest accounting. A barrier that is
proved is proved. An open problem (does MCSP have an efficient algorithm? can the
Williams template reach P/poly?) is open, and we say so. A technique that hits a
barrier is flagged by the checker, and we do not pursue it unless we can say
exactly how it evades that barrier. Overclaiming is the failure mode that wastes
the most time, because it sends the program down branches that a moment of
honesty would have pruned.

This is why the repo has a mechanical wrong-approach detector
(`experiments/_shared/barriers.py`) and why every experiment writeup states what
it does NOT show. The detector does not replace judgment; it mechanizes the
bookkeeping so judgment can focus on the hard part.

## The marginal lesson, translated

The companion Riemann Hypothesis repo found that RH appears true "only at the
margin," so any proof must engage the exact structure of the zeta function rather
than generic positivity. P vs NP has the same shape of lesson in a different key:
the barriers show that generic, soft, or black-box arguments cannot separate the
classes. The separation, if it exists, must come from a technique that engages
the exact combinatorial or algebraic structure of an NP-complete problem in a way
that is simultaneously non-relativizing, non-natural, and non-algebrizing. The
soft routes are ruled out so that effort concentrates on the structural one.
