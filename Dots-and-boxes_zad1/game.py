"""Dots & Boxes core game model (3x3 by default).

This module defines the immutable board constants, lightweight typing aliases,
and the `GameState` engine for validating and applying moves, computing scoring,
and rendering an ANSI-colored ASCII view.

Design notes
------------
- Coordinates use (row, col) zero-based indexing; `r=0` is the top row.
- A move is an edge between two *orthogonally adjacent* dots.
- When a move completes one or more cells (boxes), the same player moves again.
- Terminal condition is reached when **all edges** on the board are drawn.

The engine is intentionally simple and side-effect free beyond mutating the
`GameState` instance. All rule checks go through `is_edge_valid` and `play`.
"""

from __future__ import annotations

from typing import Dict, List, Tuple


BOARD_SIZE: int = 3
DOTS: int = BOARD_SIZE + 1

# Typing aliases
Point = tuple[int, int]
Edge = tuple[Point, Point]

from colorama import Fore, Style



def pcolor(player: int | None) -> str:
    """ANSI color for a given player id.

    Args:
        player: Player id (0 or 1). If ``None``, returns empty color code.

    Returns:
        str: Color escape sequence for Colorama.
    """
    if player is None:
        return ""
    return Fore.CYAN if player == 0 else Fore.MAGENTA


def normalize_edge(a: Point, b: Point) -> Edge:
    """Return a canonical ordering of an edge endpoints.

    The smaller endpoint goes first using tuple ordering, which makes
    comparisons and set/dict usage reliable.

    Args:
        a: First endpoint as (row, col).
        b: Second endpoint as (row, col).

    Returns:
        Edge: A 2-tuple with endpoints ordered increasingly.
    """
    return (a, b) if a <= b else (b, a)


def cell_edges(r: int, c: int) -> tuple[Edge, Edge, Edge, Edge]:
    """Edges surrounding the cell (r, c) in order: top, right, bottom, left.

    Args:
        r: Cell row (0..BOARD_SIZE-1).
        c: Cell column (0..BOARD_SIZE-1).

    Returns:
        Tuple of four canonical edges: (top, right, bottom, left).
    """
    top = normalize_edge((r, c), (r, c + 1))
    right = normalize_edge((r, c + 1), (r + 1, c + 1))
    bottom = normalize_edge((r + 1, c), (r + 1, c + 1))
    left = normalize_edge((r, c), (r + 1, c))
    return top, right, bottom, left


class IllegalMove(ValueError):
    """Raised when attempting to apply an invalid move."""
    pass


class GameState:
    """Mutable state of a Dots & Boxes match.

    Attributes:
        edges: Set of drawn edges (undirected, canonicalized).
        edge_owner: Mapping from edge to the player id who drew it (0 or 1).
        owner: Mapping from completed cell (r, c) to its owner player id.
        scores: Two-element list with scores for P0 and P1 respectively.
        player: Id of the player to move next (0 or 1).
    """

    def __init__(self) -> None:

        self.edges: set[Edge] = set()
        self.edge_owner: Dict[Edge, int] = {}
        self.owner: Dict[tuple[int, int], int] = {}
        self.scores: List[int] = [0, 0]
        self.player: int = 0


    def is_inside(self, a: Point) -> bool:
        """Check if a point lies within the DOTS x DOTS grid."""
        r, c = a
        return 0 <= r < DOTS and 0 <= c < DOTS

    def is_edge_valid(self, a: Point, b: Point) -> bool:
        """Validate whether the edge (a, b) is a legal move.

        A legal edge connects two distinct, orthogonally adjacent points that
        are both inside the board and has not been drawn yet.

        Args:
            a: First endpoint.
            b: Second endpoint.

        Returns:
            True if the edge is legal given the current state; False otherwise.
        """
        if not (self.is_inside(a) and self.is_inside(b)):
            return False
        if a == b:
            return False
        (r1, c1), (r2, c2) = a, b
        dr, dc = abs(r1 - r2), abs(c1 - c2)
        if (dr, dc) not in [(0, 1), (1, 0)]:
            return False
        e = normalize_edge(a, b)
        return e not in self.edges

    def _cells_completed_by_adding(self, e: Edge) -> List[tuple[int, int]]:
        """Compute the list of cells that would be completed by adding `e`.

        At most two cells are adjacent to any edge. For each candidate cell, if
        it currently has exactly three edges drawn, the new edge would complete it.

        Args:
            e: Candidate edge (canonical).

        Returns:
            List of cell coordinates (r, c) completed by adding `e` (length 0..2).
        """
        completed: List[tuple[int, int]] = []
        (r1, c1), (r2, c2) = e
        if r1 == r2:  # horizontal edge
            r = r1
            c = min(c1, c2)
            cand = []
            if r > 0:
                cand.append((r - 1, c))
            if r < BOARD_SIZE:
                cand.append((r, c))
        else:  # vertical edge
            c = c1
            r = min(r1, r2)
            cand = []
            if c > 0:
                cand.append((r, c - 1))
            if c < BOARD_SIZE:
                cand.append((r, c))
        for (rr, cc) in cand:
            top, right, bottom, left = cell_edges(rr, cc)
            have = (
                int(top in self.edges)
                + int(right in self.edges)
                + int(bottom in self.edges)
                + int(left in self.edges)
            )
            if have == 3:
                completed.append((rr, cc))
        return completed

    def play(self, a: Point, b: Point) -> None:
        """Apply a legal move (draw an edge) and update game state.

        Side effects:
        - Adds the edge and records its owner.
        - If one or more cells are completed by this move, the current player
          receives that many points and **keeps the turn**.
        - Otherwise, the turn passes to the opponent.

        Args:
            a: First endpoint of the edge.
            b: Second endpoint of the edge.

        Raises:
            IllegalMove: If (a, b) is not a legal edge in the current state.
        """
        if not self.is_edge_valid(a, b):
            raise IllegalMove("Nielegalny ruch.")
        e = normalize_edge(a, b)
        completed_cells = self._cells_completed_by_adding(e)

        self.edges.add(e)
        self.edge_owner[e] = self.player

        if completed_cells:
            self.scores[self.player] += len(completed_cells)
            for cell in completed_cells:
                self.owner[cell] = self.player
        else:
            self.player = 1 - self.player

    def is_terminal(self) -> bool:
        """Return True when all possible edges on the board are drawn.

        For an N×N cells board (DOTS=N+1), the number of edges equals:
            E = 2 * DOTS * (DOTS - 1)

        Returns:
            bool: ``True`` if the match is over.
        """
        total_edges = 2 * DOTS * (DOTS - 1)
        return len(self.edges) == total_edges

    def board_ascii(self) -> str:
        """Render the board as ANSI-colored ASCII art.

        - Columns and rows are annotated with indices.
        - Edges are colored by the player who drew them.
        - Completed cells display ``P0``/``P1`` in the owner's color.
        - Footer prints current scores and the player to move.

        Returns:
            str: Multiline string representation suitable for printing.
        """
        rows: List[str] = []


        header = ["   "]
        for c in range(DOTS):
            header.append(str(c))
            if c < DOTS - 1:
                header.append("  ")
        rows.append("".join(header))

        def h_edge_str(e: Edge) -> str:
            owner = self.edge_owner.get(e)
            return f"{pcolor(owner)}──{Style.RESET_ALL}" if owner is not None else "──"

        def v_edge_str(e: Edge) -> str:
            owner = self.edge_owner.get(e)
            return f"{pcolor(owner)}│{Style.RESET_ALL}" if owner is not None else "│"

        def cell_repr(r: int, c: int) -> str:
            top, right, bottom, left = cell_edges(r, c)
            have = int(top in self.edges) + int(right in self.edges) + int(bottom in self.edges) + int(left in self.edges)
            if have == 4:
                owner = self.owner.get((r, c))
                if owner is not None:
                    return f"{pcolor(owner)}P{owner}{Style.RESET_ALL}"
                return "[]"
            return "  "

        for r in range(DOTS):

            dot_row: List[str] = [f"{r}  "]
            for c in range(DOTS):
                dot_row.append("·")
                if c < DOTS - 1:
                    e = normalize_edge((r, c), (r, c + 1))
                    dot_row.append(h_edge_str(e) if e in self.edges else "  ")
            rows.append("".join(dot_row))


            if r < DOTS - 1:
                vert_row: List[str] = ["   "]
                for c in range(DOTS):
                    e = normalize_edge((r, c), (r + 1, c))
                    vert_row.append(v_edge_str(e) if e in self.edges else " ")
                    if c < DOTS - 1:
                        vert_row.append(cell_repr(r, c))
                rows.append("".join(vert_row))

        who = self.player
        rows.append(
            f"\nPunkty  {Fore.CYAN}P0:{self.scores[0]}{Style.RESET_ALL}  "
            f"{Fore.MAGENTA}P1:{self.scores[1]}{Style.RESET_ALL}   |   "
            f"Ruch: {pcolor(who)}P{who}{Style.RESET_ALL}"
        )
        return "\n".join(rows)