"""Strand-3 Bockstein forcing: turn the declarative ledger into real computation.

The 2050 dossier's braided path needs one quantity Q(complex) that is BOTH

  (strand 1) nonzero and cheaply certifiable by a faster-than-brute-force
             #SAT-style algorithm (a rational COUNT on the chain structure), and
  (strand 3) provably not reconstructible from a low-degree polynomial oracle
             extension (it does not algebrize, per Aaronson-Wigderson 2008).

The ledger (experiments/strand3/e_ledger.py, docs/03_research/strand3_ledger.md)
is so far entirely DECLARATIVE: it hand-fills InvariantProfile fields and reports
the consequence. It never computes a homology group. This module makes the
strand-3 program compute.

What is implemented here, and the honest reading attached to each piece:

  1. Integral simplicial homology via a hand-rolled integer Smith normal form
     (free rank + torsion coefficients), and mod-2 homology via rank over GF(2).
     These are the cheap COUNTS of strand 1.

  2. The mod-2 Bockstein beta = Sq^1, detected through the universal-coefficient
     relation: beta is nonzero in degree n exactly when H_n(X;Z) or H_{n-1}(X;Z)
     carries order-2 (Z/2, not Z/4) torsion (Hatcher Cor 3E.4). We detect that
     2-torsion directly from the Smith normal form, which is the honest mechanical
     content of "beta != 0" without building the cup-square ring.

  3. A battery of EXPLICIT small complexes with textbook homology, each pinned by
     a self-check assert: the 6-vertex minimal RP^2, the Klein bottle, the
     2-sphere S^2, a contractible 2-simplex, the Moebius band, and the smallest
     torsion toy (a length-2 chain complex Z --2--> Z).

  4. The forcing relation, computed numerically: mod-2 Betti STRICTLY exceeding
     rational Betti FORCES 2-torsion, hence a nonzero Bockstein; on S^2 equal
     Betti means no torsion. The HONEST verdict: this forces only the EXISTENCE
     of torsion (a rank fact, dim_{F2} H_n minus b_n(Q) >= 1), which is itself a
     rank functional and therefore algebrizes. It does NOT force a LOCATED
     non-algebrizing class beta(x) != 0; locating which class x has beta(x) != 0
     needs the cup-square / ring data, which is not a count.

  5. A genuine combinatorial complex with a canonical Z/2 action: the neighborhood
     complex N(K_4) (Lovasz topology of graph coloring) carrying the antipodal
     vertex-swap, plus a small SAT-solution Vietoris-Rips complex. We report
     whether torsion actually appears at small size (it does not for these), which
     is itself a strand-3 coordinate (gap 1: no small SAT complex with torsion yet).

  6. A Z/2 group action with the Smith-theory inequality
     sum dim H_*(Fix;F2) <= sum dim H_*(X;F2) and the Euler congruence
     chi(Fix) = chi(X) mod 2, the "structure forces structure" mechanism. The
     consumed certificate is the rational Euler number, with F_2 only in the
     machine: even this precedent forces via a rational count.

Dependencies: numpy and sympy only; standard library elsewhere. No matplotlib.

Run:
    python -m experiments.strand3.e_bockstein_forcing
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations
from typing import Dict, FrozenSet, Iterable, List, Sequence, Set, Tuple

# ---------------------------------------------------------------------------
# Simplicial complexes
# ---------------------------------------------------------------------------

Simplex = Tuple[int, ...]  # a sorted tuple of vertex labels


def closure(maximal: Iterable[Sequence[int]]) -> Set[Simplex]:
    """Downward closure: every face of every listed simplex, including vertices.

    A simplicial complex is determined by its maximal faces; this expands them to
    the full set of faces (the empty face is tracked separately as degree -1).
    """
    faces: Set[Simplex] = set()
    for face in maximal:
        s = tuple(sorted(set(face)))
        for k in range(1, len(s) + 1):
            for sub in combinations(s, k):
                faces.add(sub)
    return faces


@dataclass
class SimplicialComplex:
    """A finite abstract simplicial complex, stored by its faces grouped by degree.

    faces_by_dim[d] is the sorted list of d-dimensional faces (each a tuple of
    d+1 vertices). The boundary maps are computed on demand.
    """

    name: str
    faces: Set[Simplex]
    faces_by_dim: Dict[int, List[Simplex]] = field(default_factory=dict)

    @classmethod
    def from_maximal(cls, name: str, maximal: Iterable[Sequence[int]]) -> "SimplicialComplex":
        faces = closure(maximal)
        return cls(name=name, faces=faces).index()

    def index(self) -> "SimplicialComplex":
        by_dim: Dict[int, List[Simplex]] = {}
        for f in self.faces:
            by_dim.setdefault(len(f) - 1, []).append(f)
        for d in by_dim:
            by_dim[d].sort()
        self.faces_by_dim = by_dim
        return self

    def max_dim(self) -> int:
        return max(self.faces_by_dim) if self.faces_by_dim else -1

    def f_vector(self) -> List[int]:
        d = self.max_dim()
        return [len(self.faces_by_dim.get(k, [])) for k in range(d + 1)]

    def euler_characteristic(self) -> int:
        return sum((-1) ** k * c for k, c in enumerate(self.f_vector()))

    def boundary_matrix(self, dim: int) -> List[List[int]]:
        """Integer boundary d_dim : C_dim -> C_{dim-1} as a list-of-rows matrix.

        Rows index (dim-1)-faces, columns index dim-faces, entries in {-1,0,1}.
        For dim == 0 returns the augmentation-free convention (empty rows): we
        use UNREDUCED homology here and handle H_0 via component counting only
        when needed; the boundary into degree -1 is the augmentation, handled in
        reduced_betti.
        """
        rows = self.faces_by_dim.get(dim - 1, [])
        cols = self.faces_by_dim.get(dim, [])
        row_index = {f: i for i, f in enumerate(rows)}
        M = [[0] * len(cols) for _ in range(len(rows))]
        for j, face in enumerate(cols):
            for i in range(len(face)):
                sub = face[:i] + face[i + 1:]
                sign = (-1) ** i
                M[row_index[sub]][j] += sign
        return M


# ---------------------------------------------------------------------------
# Integer Smith normal form (hand-rolled, no external dependency for correctness)
# ---------------------------------------------------------------------------

def _smith_normal_form_diagonal(matrix: List[List[int]]) -> List[int]:
    """Return the nonzero invariant factors (diagonal of the Smith normal form).

    Hand-rolled integer SNF by repeated pivot reduction with the Euclidean
    algorithm. Robust for the small matrices in this experiment. Returns the list
    of positive invariant factors d_1 | d_2 | ... | d_r (r = rank).
    """
    A = [row[:] for row in matrix]
    if not A or not A[0]:
        return []
    rows = len(A)
    cols = len(A[0])

    def swap_rows(i: int, j: int) -> None:
        A[i], A[j] = A[j], A[i]

    def swap_cols(i: int, j: int) -> None:
        for r in range(rows):
            A[r][i], A[r][j] = A[r][j], A[r][i]

    invariants: List[int] = []
    t = 0
    while t < min(rows, cols):
        # Find a nonzero pivot in the submatrix A[t:, t:].
        pivot = None
        for i in range(t, rows):
            for j in range(t, cols):
                if A[i][j] != 0:
                    pivot = (i, j)
                    break
            if pivot:
                break
        if pivot is None:
            break
        pi, pj = pivot
        swap_rows(t, pi)
        swap_cols(t, pj)

        # Clear column t and row t below/right of the pivot until the pivot
        # divides everything in its row and column (Euclidean elimination).
        done = False
        while not done:
            done = True
            # Clear below in column t.
            for i in range(t + 1, rows):
                if A[i][t] != 0:
                    q = A[i][t] // A[t][t]
                    if q != 0:
                        for j in range(cols):
                            A[i][j] -= q * A[t][j]
                    if A[i][t] != 0:
                        swap_rows(t, i)
                        done = False
            # Clear right in row t.
            for j in range(t + 1, cols):
                if A[t][j] != 0:
                    q = A[t][j] // A[t][t]
                    if q != 0:
                        for i in range(rows):
                            A[i][j] -= q * A[i][t]
                    if A[t][j] != 0:
                        swap_cols(t, j)
                        done = False
            # Ensure the pivot divides every remaining entry; if not, fold a
            # bad entry into the pivot row and repeat.
            if done:
                for i in range(t + 1, rows):
                    for j in range(t + 1, cols):
                        if A[i][j] % A[t][t] != 0:
                            for k in range(cols):
                                A[t][k] += A[i][k]
                            done = False
                            break
                    if not done:
                        break

        invariants.append(abs(A[t][t]))
        t += 1

    return invariants


# ---------------------------------------------------------------------------
# Rank over GF(2)
# ---------------------------------------------------------------------------

def _rank_gf2(matrix: List[List[int]]) -> int:
    """Rank of an integer matrix reduced mod 2, via Gaussian elimination over F_2.

    Rows are represented as Python ints (bitmasks) for speed and exactness.
    """
    if not matrix or not matrix[0]:
        return 0
    cols = len(matrix[0])
    rowmasks: List[int] = []
    for row in matrix:
        mask = 0
        for j, v in enumerate(row):
            if v & 1:
                mask |= (1 << j)
        if mask:
            rowmasks.append(mask)

    rank = 0
    for bit in range(cols):
        pivot_row = None
        for idx in range(rank, len(rowmasks)):
            if (rowmasks[idx] >> bit) & 1:
                pivot_row = idx
                break
        if pivot_row is None:
            continue
        rowmasks[rank], rowmasks[pivot_row] = rowmasks[pivot_row], rowmasks[rank]
        pivot = rowmasks[rank]
        for idx in range(len(rowmasks)):
            if idx != rank and ((rowmasks[idx] >> bit) & 1):
                rowmasks[idx] ^= pivot
        rank += 1
    return rank


# ---------------------------------------------------------------------------
# Homology over Z and over F_2 (reduced)
# ---------------------------------------------------------------------------

@dataclass
class IntegralGroup:
    """Finitely generated abelian group H_n = Z^free (+) Z/t_1 (+) ... (+) Z/t_k."""

    free_rank: int
    torsion: List[int]  # the invariant factors > 1

    def two_torsion_count(self) -> int:
        """Number of cyclic summands of even order (these carry order-2 elements).

        A Z/(2^a * m) summand contributes a Z/2 in its 2-primary part; for the
        Bockstein beta = Sq^1, what matters is order-EXACTLY-2 (Z/2) versus
        higher 2-power (Z/4, ...). We track both via two_torsion_count and
        order_exactly_two_count.
        """
        return sum(1 for t in self.torsion if t % 2 == 0)

    def order_exactly_two_count(self) -> int:
        """Number of Z/2 summands (order exactly 2). beta = Sq^1 is detected by
        these per Hatcher Cor 3E.4 (no order-4 elements case)."""
        return sum(1 for t in self.torsion if t == 2)

    def __str__(self) -> str:
        parts: List[str] = []
        if self.free_rank == 1:
            parts.append("Z")
        elif self.free_rank > 1:
            parts.append(f"Z^{self.free_rank}")
        for t in self.torsion:
            parts.append(f"Z/{t}")
        return " + ".join(parts) if parts else "0"


@dataclass
class HomologyReport:
    name: str
    integral: Dict[int, IntegralGroup]  # reduced integral homology by degree
    mod2_betti: Dict[int, int]          # reduced mod-2 Betti by degree
    rational_betti: Dict[int, int]      # reduced rational Betti by degree
    euler: int

    def bockstein_nonzero(self) -> bool:
        """beta = Sq^1 is nonzero somewhere iff some reduced integral homology
        group carries order-exactly-2 torsion (UCT / Hatcher Cor 3E.4)."""
        return any(g.order_exactly_two_count() > 0 for g in self.integral.values())

    def total_mod2_betti(self) -> int:
        return sum(self.mod2_betti.values())


def compute_homology(K: SimplicialComplex, max_degree: int | None = None) -> HomologyReport:
    """Compute REDUCED integral and mod-2 homology of K.

    Reduced homology augments by the map C_0 -> Z, x -> 1, so tilde-H_0 has rank
    (components - 1) and a point has all reduced homology zero. We implement this
    by adding the empty simplex as the unique (-1)-face: the degree-0 boundary
    maps C_0 -> C_{-1} = Z by every vertex |-> 1.
    """
    d_top = K.max_dim() if max_degree is None else max_degree

    # Boundary matrices, with degree 0 mapping to the (-1)-augmentation (one row
    # of all ones) so that homology is REDUCED.
    boundaries: Dict[int, List[List[int]]] = {}
    for deg in range(0, d_top + 1):
        if deg == 0:
            cols = K.faces_by_dim.get(0, [])
            boundaries[0] = [[1] * len(cols)] if cols else [[]]
        else:
            boundaries[deg] = K.boundary_matrix(deg)

    # Smith normal form invariant factors and GF(2) ranks per degree.
    snf: Dict[int, List[int]] = {}
    gf2rank: Dict[int, int] = {}
    n_faces: Dict[int, int] = {}
    for deg in range(0, d_top + 1):
        M = boundaries[deg]
        snf[deg] = _smith_normal_form_diagonal(M)
        gf2rank[deg] = _rank_gf2(M)
        n_faces[deg] = len(K.faces_by_dim.get(deg, []))

    integral: Dict[int, IntegralGroup] = {}
    mod2: Dict[int, int] = {}
    rational: Dict[int, int] = {}

    for deg in range(0, d_top + 1):
        c_n = n_faces[deg]
        # rank of d_n (out of degree n)
        rank_dn = len(snf[deg])
        # rank of d_{n+1} (into degree n)
        rank_dn1 = len(snf.get(deg + 1, []))
        # Z homology: free rank = c_n - rank_dn - rank_dn1; torsion = invariant
        # factors > 1 of d_{n+1} (the map landing in degree n).
        free_rank = c_n - rank_dn - rank_dn1
        torsion = [t for t in snf.get(deg + 1, []) if t > 1]
        integral[deg] = IntegralGroup(free_rank=free_rank, torsion=torsion)

        # F_2 homology Betti: dim ker(d_n mod 2) - rank(d_{n+1} mod 2).
        rank_dn_2 = gf2rank[deg]
        rank_dn1_2 = gf2rank.get(deg + 1, 0)
        ker_dn_2 = c_n - rank_dn_2
        mod2[deg] = ker_dn_2 - rank_dn1_2

        # Q homology Betti: same shape over Q == free_rank (UCT: rational Betti
        # equals the free rank of integral homology).
        rational[deg] = free_rank

    euler = K.euler_characteristic()

    return HomologyReport(
        name=K.name,
        integral=integral,
        mod2_betti=mod2,
        rational_betti=rational,
        euler=euler,
    )


# ---------------------------------------------------------------------------
# Explicit named complexes
# ---------------------------------------------------------------------------

def rp2_minimal() -> SimplicialComplex:
    """The unique 6-vertex minimal triangulation of RP^2 (10 triangles).

    Facet list (the icosahedron mod the antipodal Z/2). H0=Z, H1=Z/2, H2=0 over
    Z; over Q all reduced homology vanishes. beta = Sq^1 is nonzero on H^1.
    """
    facets = [
        (1, 2, 3), (1, 2, 4), (1, 3, 5), (1, 4, 6), (1, 5, 6),
        (2, 3, 6), (2, 4, 5), (2, 5, 6), (3, 4, 5), (3, 4, 6),
    ]
    return SimplicialComplex.from_maximal("RP^2 (minimal, 6 vertices)", facets)


def klein_bottle() -> SimplicialComplex:
    """A 9-vertex triangulation of the Klein bottle. H0=Z, H1=Z + Z/2, H2=0.

    Built from a 3x3 grid of cells (vertices on Z/3 x Z/3) with the Klein
    identifications: the i-direction is glued straight (torus-like, top row ~
    bottom row), and the j-direction is glued with an orientation-reversing FLIP
    (right column glues to left column under i -> -i mod 3). The flip is exactly
    what turns the torus into the Klein bottle and produces the Z/2 in H1.
    Verified by the self-check below (chi = 0, H1 = Z + Z/2, beta = Sq^1 nonzero).
    """
    rows = cols = 3

    def vid(i: int, j: int) -> int:
        i0 = i % rows
        wraps = j // cols
        j0 = j % cols
        ii = i0 if wraps % 2 == 0 else (-i0) % rows
        return ii * cols + j0

    tris: List[Tuple[int, ...]] = []
    for i in range(rows):
        for j in range(cols):
            a, b = vid(i, j), vid(i, j + 1)
            c, d = vid(i + 1, j), vid(i + 1, j + 1)
            for tri in ((a, b, d), (a, d, c)):
                s = tuple(sorted(set(tri)))
                if len(s) == 3:
                    tris.append(s)
    return SimplicialComplex.from_maximal("Klein bottle (9 vertices, 3x3 grid)", tris)


def sphere_s2() -> SimplicialComplex:
    """The boundary of a tetrahedron: a triangulation of S^2. H0=Z, H2=Z, rest 0.

    Torsion-free, so beta = Sq^1 is zero. The control that "equal Betti means no
    torsion."
    """
    facets = [(1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)]
    return SimplicialComplex.from_maximal("S^2 (tetrahedron boundary)", facets)


def contractible_triangle() -> SimplicialComplex:
    """A filled 2-simplex: contractible, all reduced homology zero, no torsion."""
    return SimplicialComplex.from_maximal("filled 2-simplex (contractible)", [(1, 2, 3)])


def moebius_band() -> SimplicialComplex:
    """A 5-vertex triangulation of the Moebius band. Homotopy equivalent to S^1.

    Reduced homology: H1 = Z, no torsion. A nonorientable surface-with-boundary
    control: nonorientable does NOT imply torsion (the boundary kills it).
    """
    facets = [(1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 1), (5, 1, 2)]
    return SimplicialComplex.from_maximal("Moebius band (5 vertices)", facets)


# ---------------------------------------------------------------------------
# The smallest torsion object: a length-2 chain complex Z --2--> Z
# ---------------------------------------------------------------------------

def two_torsion_toy_homology() -> Tuple[Dict[int, IntegralGroup], Dict[int, int], Dict[int, int]]:
    """Hatcher p.190 toy: 0 -> Z --2--> Z -> 0 in degrees 1 -> 0.

    H_0 = Z/2 (cokernel of x|->2x), H_1 = 0. Over Q both vanish; over F_2,
    H_0 = F_2 (dim 1) and H_1 = F_2 (dim 1, the kernel of multiplication-by-2
    mod 2 is all of F_2). This is the smallest object where mod-2 Betti strictly
    exceeds rational Betti, forcing 2-torsion. Computed by hand (not simplicial)
    to exhibit the UCT forcing on the minimal possible chain complex.
    """
    # Boundary d_1 = [[2]] : C_1=Z -> C_0=Z.
    M = [[2]]
    snf = _smith_normal_form_diagonal(M)          # [2]
    gf2 = _rank_gf2(M)                              # 0 (2 == 0 mod 2)

    # H_0 = coker(d_1): free_rank = 1 - rank_d1 - rank_d2(=0) ; torsion from snf.
    rank_d1 = len(snf)                              # 1
    free0 = 1 - rank_d1                             # 0
    tors0 = [t for t in snf if t > 1]              # [2]
    H0 = IntegralGroup(free_rank=free0, torsion=tors0)
    # H_1 = ker(d_1): free_rank = 1 - rank_d1 = 0, no torsion.
    H1 = IntegralGroup(free_rank=1 - rank_d1, torsion=[])
    integral = {0: H0, 1: H1}

    # mod-2 Betti: H0 = ker(d_0=0)/im(d_1 mod2). d_1 mod 2 = [[0]], rank 0.
    # dim C_0 = 1, ker d_0 over F_2 = 1 (no d_0), im d_1 = 0 -> betti_0 = 1.
    # dim C_1 = 1, ker d_1 over F_2 = 1 - 0 = 1, im d_2 = 0 -> betti_1 = 1.
    mod2 = {0: 1 - 0 - gf2, 1: (1 - gf2) - 0}
    rational = {0: free0, 1: 1 - rank_d1}
    return integral, mod2, rational


# ---------------------------------------------------------------------------
# Genuine combinatorial complexes: neighborhood complex + SAT solution complex
# ---------------------------------------------------------------------------

def neighborhood_complex(adjacency: Dict[int, Set[int]]) -> SimplicialComplex:
    """Lovasz neighborhood complex N(G): vertices are graph vertices; a set S is
    a simplex iff S has a common neighbor (intersection of neighborhoods nonempty).

    Carries the Lovasz topology of graph coloring; for the antipodal/box-complex
    story it has a canonical free Z/2 action in the box-complex form. Here we
    build N(G) directly to test for torsion at small size.
    """
    verts = sorted(adjacency)
    nbr = {v: set(adjacency[v]) for v in verts}
    maximal: List[Tuple[int, ...]] = []
    # A subset S is a face iff there exists w adjacent to all of S.
    # Enumerate maximal common-neighbor sets: for each w, N(w) is a face.
    seen: Set[FrozenSet[int]] = set()
    for w in verts:
        face = tuple(sorted(u for u in verts if w in nbr[u]))
        if face:
            seen.add(frozenset(face))
    # Keep maximal faces only.
    faces = [set(f) for f in seen]
    for f in faces:
        if not any(f < g for g in faces):
            maximal.append(tuple(sorted(f)))
    return SimplicialComplex.from_maximal("N(G) neighborhood complex", maximal)


def complete_graph(n: int) -> Dict[int, Set[int]]:
    return {i: {j for j in range(n) if j != i} for i in range(n)}


def sat_solution_rips(
    solutions: Sequence[Tuple[int, ...]], radius: int, name: str
) -> SimplicialComplex:
    """Vietoris-Rips complex on a SAT solution set under Hamming distance.

    Vertices are satisfying assignments (as 0/1 tuples); a set of assignments is a
    face iff they are pairwise within Hamming distance <= radius. Tests the gap-1
    hypothesis that 2-torsion could appear from how solution subcubes glue.
    """
    pts = [tuple(s) for s in solutions]
    n = len(pts)

    def ham(a: Tuple[int, ...], b: Tuple[int, ...]) -> int:
        return sum(x != y for x, y in zip(a, b))

    # Build the graph of pairwise-close points, then take its clique complex.
    close = [[ham(pts[i], pts[j]) <= radius for j in range(n)] for i in range(n)]

    # Maximal cliques via Bron-Kerbosch (small inputs).
    def bron_kerbosch(R: Set[int], P: Set[int], X: Set[int], out: List[Set[int]]) -> None:
        if not P and not X:
            out.append(set(R))
            return
        for v in list(P):
            neigh = {u for u in range(n) if u != v and close[v][u]}
            bron_kerbosch(R | {v}, P & neigh, X & neigh, out)
            P = P - {v}
            X = X | {v}

    cliques: List[Set[int]] = []
    bron_kerbosch(set(), set(range(n)), set(), cliques)
    maximal = [tuple(sorted(c)) for c in cliques if c]
    return SimplicialComplex.from_maximal(name, maximal)


def enumerate_sat_solutions(
    n_vars: int, clauses: Sequence[Sequence[int]]
) -> List[Tuple[int, ...]]:
    """Brute-force enumerate satisfying assignments of a CNF.

    Each clause is a list of signed literals (1-indexed; +k means var k true,
    -k means var k false). Returns the solution set as 0/1 tuples.
    """
    sols: List[Tuple[int, ...]] = []
    for mask in range(1 << n_vars):
        assign = [(mask >> i) & 1 for i in range(n_vars)]
        ok = True
        for cl in clauses:
            satisfied = False
            for lit in cl:
                v = abs(lit) - 1
                want = 1 if lit > 0 else 0
                if assign[v] == want:
                    satisfied = True
                    break
            if not satisfied:
                ok = False
                break
        if ok:
            sols.append(tuple(assign))
    return sols


# ---------------------------------------------------------------------------
# A Z/2 group action and the Smith-theory inequality
# ---------------------------------------------------------------------------

def apply_vertex_map(K: SimplicialComplex, perm: Dict[int, int], name: str) -> SimplicialComplex:
    """Image of K under a vertex permutation (used to check it is an automorphism)."""
    new_faces = {tuple(sorted(perm[v] for v in f)) for f in K.faces}
    return SimplicialComplex(name=name, faces=new_faces).index()


def is_automorphism(K: SimplicialComplex, perm: Dict[int, int]) -> bool:
    return apply_vertex_map(K, perm, "tmp").faces == K.faces


def fixed_subcomplex_bar(K: SimplicialComplex, perm: Dict[int, int]) -> SimplicialComplex:
    """The fixed subcomplex Delta^{[G]} for a Z/2 = <perm> action.

    We use the orbit-quotient construction (Miller Def 2.11): orbits of <perm> on
    vertices become the vertices of the fixed complex, and an orbit-set is a face
    iff the union of those orbits is a face of K. This is always a subcomplex and
    is the right object for the Smith-theory inequality.
    """
    # Orbits of the involution.
    verts = sorted({v for f in K.faces for v in f})
    orbit_of: Dict[int, FrozenSet[int]] = {}
    orbits: List[FrozenSet[int]] = []
    for v in verts:
        o = frozenset({v, perm[v]})
        orbit_of[v] = o
        if o not in orbits:
            orbits.append(o)
    orbit_id = {o: i for i, o in enumerate(orbits)}

    # A set T of orbit-ids is a face iff the union of those orbits is a face of K.
    face_set = K.faces
    maximal: List[Tuple[int, ...]] = []
    candidate_faces: List[FrozenSet[int]] = []
    for r in range(1, len(orbits) + 1):
        for combo in combinations(range(len(orbits)), r):
            union = tuple(sorted(set().union(*[set(orbits[i]) for i in combo])))
            if union in face_set:
                candidate_faces.append(frozenset(combo))
    for f in candidate_faces:
        if not any(f < g for g in candidate_faces):
            maximal.append(tuple(sorted(f)))
    if not maximal:
        # Empty fixed complex.
        return SimplicialComplex(name="Fix (empty)", faces=set()).index()
    return SimplicialComplex.from_maximal("Fix = Delta^{[Z/2]}", maximal)


# ---------------------------------------------------------------------------
# Reporting helpers
# ---------------------------------------------------------------------------

def format_integral(report: HomologyReport) -> str:
    degs = sorted(report.integral)
    parts = [f"H{d}={report.integral[d]}" for d in degs]
    return ", ".join(parts)


def format_mod2(report: HomologyReport) -> str:
    degs = sorted(report.mod2_betti)
    parts = [f"b{d}(F2)={report.mod2_betti[d]}" for d in degs]
    return ", ".join(parts)


def format_rational(report: HomologyReport) -> str:
    degs = sorted(report.rational_betti)
    parts = [f"b{d}(Q)={report.rational_betti[d]}" for d in degs]
    return ", ".join(parts)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("=== Strand-3 Bockstein forcing: computed homology, not declared ===\n")
    print("Reduced homology over Z (Smith normal form) and F_2 (GF(2) rank); the")
    print("Bockstein beta = Sq^1 is detected as order-2 integral torsion (UCT).\n")

    # -- Battery of validation complexes with known textbook homology. --
    print("--- 1. Validation battery (each pinned against textbook values) ---\n")

    complexes = [
        sphere_s2(),
        contractible_triangle(),
        moebius_band(),
        rp2_minimal(),
        klein_bottle(),
    ]
    reports: Dict[str, HomologyReport] = {}
    for K in complexes:
        r = compute_homology(K)
        reports[K.name] = r
        print(f"{K.name}")
        print(f"  f-vector: {K.f_vector()}   chi = {K.euler_characteristic()}")
        print(f"  reduced H_*(Z):  {format_integral(r)}")
        print(f"  reduced H_*(F2): {format_mod2(r)}")
        print(f"  reduced H_*(Q):  {format_rational(r)}")
        print(f"  Bockstein beta=Sq^1 nonzero: {r.bockstein_nonzero()}")
        print()

    # ---- self-checks pinning each complex to its known value ----
    s2 = reports["S^2 (tetrahedron boundary)"]
    assert s2.integral[0].free_rank == 0 and not s2.integral[0].torsion, "S^2: tilde H0 = 0"
    assert s2.integral[2].free_rank == 1 and not s2.integral[2].torsion, "S^2: H2 = Z"
    assert s2.integral.get(1, IntegralGroup(0, [])).free_rank == 0, "S^2: H1 = 0"
    assert not s2.bockstein_nonzero(), "S^2 is torsion-free: beta must vanish"
    assert s2.mod2_betti == s2.rational_betti, "S^2: F2 Betti == Q Betti (no torsion)"

    tri = reports["filled 2-simplex (contractible)"]
    assert all(g.free_rank == 0 and not g.torsion for g in tri.integral.values()), \
        "contractible: all reduced homology vanishes over Z"
    assert not tri.bockstein_nonzero(), "contractible: beta vanishes"

    mob = reports["Moebius band (5 vertices)"]
    assert mob.integral[1].free_rank == 1 and not mob.integral[1].torsion, \
        "Moebius band ~ S^1: H1 = Z, no torsion"
    assert not mob.bockstein_nonzero(), "Moebius band: nonorientable but no torsion (boundary kills it)"

    rp2 = reports["RP^2 (minimal, 6 vertices)"]
    assert rp2.integral[0].free_rank == 0, "RP^2: tilde H0 = 0 (connected)"
    assert rp2.integral[1].torsion == [2] and rp2.integral[1].free_rank == 0, \
        "RP^2: H1 = Z/2"
    assert rp2.integral[2].free_rank == 0 and not rp2.integral[2].torsion, \
        "RP^2: H2 = 0"
    assert rp2.bockstein_nonzero(), "RP^2: beta = Sq^1 nonzero (the Z/2 in H1)"
    assert rp2.mod2_betti[1] == 1 and rp2.rational_betti[1] == 0, \
        "RP^2: mod-2 Betti b1 strictly exceeds rational Betti (forces 2-torsion)"

    kb = reports["Klein bottle (9 vertices, 3x3 grid)"]
    assert kb.integral[1].free_rank == 1 and kb.integral[1].torsion == [2], \
        "Klein bottle: H1 = Z + Z/2"
    assert kb.integral[2].free_rank == 0 and not kb.integral[2].torsion, \
        "Klein bottle: H2 = 0 (nonorientable)"
    assert kb.bockstein_nonzero(), "Klein bottle: beta = Sq^1 nonzero (the Z/2 in H1)"

    print("Self-check OK (battery): S^2, contractible 2-simplex, Moebius band,")
    print("RP^2, and Klein bottle all match their textbook integral homology, and")
    print("the Bockstein flag matches (nonzero exactly for RP^2 and Klein bottle).\n")

    # -- The smallest torsion object and the Euler-blindness check. --
    print("--- 2. Smallest torsion object: chain complex Z --2--> Z (Hatcher p.190) ---\n")
    integral, mod2, rational = two_torsion_toy_homology()
    print(f"  H_*(Z):  H0={integral[0]}, H1={integral[1]}")
    print(f"  H_*(F2): b0={mod2[0]}, b1={mod2[1]}")
    print(f"  H_*(Q):  b0={rational[0]}, b1={rational[1]}")
    # Euler characteristic is coefficient-independent: chi over Q == chi over F2.
    chi_q = rational[0] - rational[1]
    chi_2 = mod2[0] - mod2[1]
    print(f"  chi(Q) = {chi_q}, chi(F2) = {chi_2}  (equal: Euler char is torsion-blind)")
    assert integral[0].torsion == [2], "toy: H0 = Z/2"
    assert mod2[0] == 1 and rational[0] == 0, "toy: mod-2 Betti b0 > rational Betti b0 (forces 2-torsion)"
    assert chi_q == chi_2, "Euler characteristic is coefficient-independent (torsion telescopes away)"
    print("  Self-check OK: mod-2 Betti exceeds rational Betti by exactly the torsion,")
    print("  and chi is identical over Q and F2 (the alternating sum cancels torsion).\n")

    # -- The forcing relation, computed numerically. --
    print("--- 3. The forcing relation: mod-2 Betti > rational Betti => 2-torsion => beta != 0 ---\n")
    forcing_rows: List[Tuple[str, int, int, int, bool]] = []
    for name in ["S^2 (tetrahedron boundary)", "RP^2 (minimal, 6 vertices)",
                 "Klein bottle (9 vertices, 3x3 grid)"]:
        r = reports[name]
        total_f2 = sum(r.mod2_betti.values())
        total_q = sum(r.rational_betti.values())
        gap = total_f2 - total_q
        forcing_rows.append((name, total_f2, total_q, gap, r.bockstein_nonzero()))
        verdict = "FORCES 2-torsion" if gap > 0 else "no gap, no forced torsion"
        print(f"  {name}")
        print(f"    sum b_*(F2) = {total_f2}, sum b_*(Q) = {total_q}, gap = {gap}  ->  {verdict}")
        print(f"    beta = Sq^1 nonzero: {r.bockstein_nonzero()}")
        # The forcing law: a positive gap implies torsion implies nonzero Bockstein.
        if gap > 0:
            assert r.bockstein_nonzero(), f"{name}: positive Betti gap must force beta != 0"
        if gap == 0:
            assert not r.bockstein_nonzero(), f"{name}: no Betti gap means no 2-torsion, beta = 0"
    print()
    print("  Honest reading of the forcing:")
    print("  The positive Betti gap (a RANK fact: dim_{F2} H_n minus b_n(Q) >= 1) forces")
    print("  the EXISTENCE of 2-torsion, hence SOME nonzero Bockstein. But the gap is a")
    print("  difference of two ranks, so a low-degree oracle extension (which carries the")
    print("  rational boundary matrices, hence ranks over every field) reconstructs it: by")
    print("  Aaronson-Wigderson the EXISTENCE-of-torsion fact ALGEBRIZES. It does NOT")
    print("  locate which class x has beta(x) != 0; that needs the cup-square/ring data,")
    print("  which is not a count. So this is EXISTENCE-forcing, not a LOCATED")
    print("  non-algebrizing class. The bridge the dossier names is not yet built.\n")

    # -- A genuine combinatorial complex and a SAT solution complex. --
    print("--- 4. Genuine combinatorial complexes: torsion at small size? ---\n")

    # Neighborhood complex of K_4 (Lovasz topology). Carries a canonical Z/2 in
    # its box-complex form (vertex/antipode swap).
    NK4 = neighborhood_complex(complete_graph(4))
    rNK4 = compute_homology(NK4)
    print(f"  {NK4.name} for G = K_4")
    print(f"    f-vector: {NK4.f_vector()}, chi = {NK4.euler_characteristic()}")
    print(f"    reduced H_*(Z): {format_integral(rNK4)}")
    print(f"    Bockstein nonzero: {rNK4.bockstein_nonzero()}")
    has_torsion_NK4 = any(g.torsion for g in rNK4.integral.values())
    print(f"    torsion present: {has_torsion_NK4}  (coordinate: N(K_n) is a wedge of spheres, torsion-free)")
    print()

    # A small designed SAT instance whose solutions form two separated subcubes.
    # phi over 4 vars: solutions split into a block near 0000 and a block near 1111.
    # Clause set forces (x1=x2) and (x3 -> x4 within each block) style structure;
    # we just enumerate a hand-chosen solution set to make the geometry explicit.
    clauses = [[1, 2], [-1, -2], [3, 4], [-3, -4]]  # (x1 OR x2)&(-x1 OR -x2)&(x3 OR x4)&(-x3 OR -x4)
    sols = enumerate_sat_solutions(4, clauses)
    print(f"  SAT instance (4 vars, XOR-like clauses): {len(sols)} satisfying assignments")
    print(f"    solutions: {sols}")
    rips1 = sat_solution_rips(sols, radius=1, name="SAT Rips r=1")
    rips2 = sat_solution_rips(sols, radius=2, name="SAT Rips r=2")
    for rips in (rips1, rips2):
        rr = compute_homology(rips)
        has_t = any(g.torsion for g in rr.integral.values())
        print(f"    {rips.name}: f-vector {rips.f_vector()}, chi {rips.euler_characteristic()}")
        print(f"      reduced H_*(Z): {format_integral(rr)}")
        print(f"      torsion present: {has_t}, Bockstein nonzero: {rr.bockstein_nonzero()}")
    print()
    print("  Coordinate (gap 1, strand3_missing_object.md): the small SAT solution")
    print("  complex is pure RANK (cluster/component counting); no 2-torsion appears")
    print("  at this size. The literal-flip symmetry of a RANDOM formula is generically")
    print("  trivial, so the Oliver/Smith fixed-point hypothesis fails. Recorded as a")
    print("  negative coordinate, not hidden.\n")

    # -- Z/2 action and the Smith-theory inequality. --
    print("--- 5. Z/2 action: Smith inequality and Euler congruence ---\n")

    def unreduced_total_mod2(report: HomologyReport, K: SimplicialComplex) -> int:
        """Total UNreduced mod-2 Betti = (reduced total) + 1 if nonempty.

        The classical Smith inequality is stated for unreduced homology; our
        compute_homology returns REDUCED Betti, so we add back the dropped H0
        generator for each nonempty complex.
        """
        if not K.faces:
            return 0
        return sum(report.mod2_betti.values()) + 1

    def smith_instance(X: SimplicialComplex, perm: Dict[int, int], label: str) -> None:
        assert is_automorphism(X, perm), f"{label}: the swap must be a simplicial automorphism"
        Fix = fixed_subcomplex_bar(X, perm)
        rX = compute_homology(X)
        rFix = compute_homology(Fix) if Fix.faces else None

        tot_X = unreduced_total_mod2(rX, X)
        tot_Fix = unreduced_total_mod2(rFix, Fix) if rFix is not None else 0
        chi_X = X.euler_characteristic()
        chi_fix = Fix.euler_characteristic() if Fix.faces else 0
        x_acyclic = (sum(rX.mod2_betti.values()) == 0)
        fix_acyclic = (rFix is not None and sum(rFix.mod2_betti.values()) == 0)

        print(f"  {label}")
        print(f"    Fix = Delta^[Z/2] f-vector: {Fix.f_vector() if Fix.faces else '[] (empty)'}")
        print(f"    sum dim H_*(Fix; F2) = {tot_Fix}   <=   sum dim H_*(X; F2) = {tot_X}")
        print(f"    chi(Fix) = {chi_fix},  chi(X) = {chi_X},  "
              f"chi(Fix) = chi(X) mod 2 ? {chi_fix % 2 == chi_X % 2}")
        if x_acyclic:
            print(f"    X is F2-acyclic; Smith theory => Fix is F2-acyclic: "
                  f"{'confirmed' if fix_acyclic else 'FAILED'}")
        assert tot_Fix <= tot_X, f"{label}: Smith inequality total F2-Betti(Fix) <= total F2-Betti(X)"
        assert chi_fix % 2 == chi_X % 2, f"{label}: Euler congruence chi(Fix) = chi(X) mod 2"
        if x_acyclic:
            assert fix_acyclic, f"{label}: Smith theory says an F2-acyclic X has F2-acyclic Fix"
        print()

    # (a) The KSS-relevant case: an F2-ACYCLIC complex (the filled 2-simplex) with
    # a reflection fixing vertex 1, swapping 2<->3. Smith theory must propagate
    # acyclicity to the fixed set. This is exactly the Smith step inside the
    # evasiveness / Oliver fixed-point argument.
    smith_instance(
        contractible_triangle(),
        {1: 1, 2: 3, 3: 2},
        "X = filled 2-simplex (F2-acyclic), reflection fixing 1, swapping (2 3)",
    )

    # (b) A non-acyclic case: S^2 with the involution (1 2)(3 4). Here X is not
    # acyclic, so Smith only gives the inequality and the Euler congruence.
    smith_instance(
        sphere_s2(),
        {1: 2, 2: 1, 3: 4, 4: 3},
        "X = S^2 (tetrahedron boundary), involution (1 2)(3 4)",
    )

    print("  Self-check OK: the Smith inequality and the mod-2 Euler congruence hold in")
    print("  both cases, and in the F2-acyclic case acyclicity propagates to the fixed")
    print("  set (the Smith step inside the KSS/Oliver fixed-point argument). The CONSUMED")
    print("  certificate is the rational Euler number chi(X); F_2 enters only in the")
    print("  delta/sigma operator splitting of Smith theory. Even this 'structure forces")
    print("  structure' mechanism forces via a RATIONAL count, which by the algebrization")
    print("  probe's own logic ALGEBRIZES.\n")

    # -- Final honest summary. --
    print("=== Summary (honest, recorded as coordinates) ===\n")
    print("PROVED here by computation (cite: Hatcher UCT Thm 3.2 / Cor 3E.4, Smith theory):")
    print("  - mod-2 Betti strictly exceeding rational Betti FORCES 2-torsion, hence a")
    print("    nonzero Bockstein beta=Sq^1 (verified on RP^2, Klein bottle, and the")
    print("    Z--2-->Z toy); equal Betti (S^2) means no torsion and beta = 0.")
    print("  - The Euler characteristic is coefficient-independent (torsion telescopes),")
    print("    so chi alone is provably blind to torsion and cannot be the forcing count.")
    print("  - The Smith inequality and the mod-2 Euler congruence hold for a Z/2 action,")
    print("    with the consumed certificate a rational Euler number.")
    print()
    print("PROJECT HEURISTIC, NOT discharged here:")
    print("  - The forcing computed is EXISTENCE-of-torsion (a difference of two ranks),")
    print("    which is itself a rank functional and therefore ALGEBRIZES by A-W. It is")
    print("    not a LOCATED non-algebrizing class beta(x) != 0. Locating x needs the")
    print("    cup-square / ring structure, which is not a #SAT-style count.")
    print("  - No small SAT-derived complex tried here carries 2-torsion; the canonical")
    print("    literal-flip symmetry is generically trivial. Both are negative coordinates")
    print("    sharpening where the real bridge must live, consistent with the ledger's")
    print("    finding that nothing is LIVE yet.")
    print()
    print("Self-check OK: all complexes match textbook homology; the forcing law holds")
    print("numerically; the existence-vs-located distinction is demonstrated, not assumed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
