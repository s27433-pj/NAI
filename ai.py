"""Simple alpha–beta AI for Dots & Boxes (3×3 default).

Overview
--------
- Search: depth-limited **minimax with alpha–beta pruning**.
- Move ordering: prioritize moves that complete cells (0..2) to improve pruning.
- Heuristic: score difference from the reference player's perspective.

This implementation is optimized for small boards (3×3). It relies on the
`GameState` engine to handle the "free extra move after completing a cell"
rule by leaving the `player` unchanged when appropriate.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from game import GameState, Edge, DOTS, normalize_edge, cell_edges



def all_moves(state: GameState) -> List[Edge]:
    """List all legal, yet-undrawn edges on the board.

    Args:
        state: Current game state.

    Returns:
        List of canonical edges (may be up to 24 on 3×3).
    """
    moves: List[Edge] = []
    # horizontal
    for r in range(DOTS):
        for c in range(DOTS - 1):
            e = normalize_edge((r, c), (r, c + 1))
            if e not in state.edges:
                moves.append(e)
    # vertical
    for r in range(DOTS - 1):
        for c in range(DOTS):
            e = normalize_edge((r, c), (r + 1, c))
            if e not in state.edges:
                moves.append(e)
    return moves


def closes_cells_count(state: GameState, e: Edge) -> int:
    """How many cells would be completed by drawing edge `e`?

    Args:
        state: Current state.
        e: Candidate edge.

    Returns:
        int: Number of cells that would be completed (0..2).
    """
    (r1, c1), (r2, c2) = e
    cnt = 0
    if r1 == r2:  # horizontal
        r = r1
        c = min(c1, c2)
        candidates = []
        if r > 0:
            candidates.append((r - 1, c))
        if r < DOTS - 1:
            candidates.append((r, c))
    else:  # vertical
        c = c1
        r = min(r1, r2)
        candidates = []
        if c > 0:
            candidates.append((r, c - 1))
        if c < DOTS - 1:
            candidates.append((r, c))
    for rr, cc in candidates:
        top, right, bottom, left = cell_edges(rr, cc)
        have = int(top in state.edges) + int(right in state.edges) + int(bottom in state.edges) + int(left in state.edges)
        if have == 3:
            cnt += 1
    return cnt


def ordered_moves(state: GameState) -> List[Edge]:
    """Return moves ordered by descending ``closes_cells_count``.

    This dramatically improves alpha–beta pruning on 3×3.
    """
    ms = all_moves(state)
    ms.sort(key=lambda e: closes_cells_count(state, e), reverse=True)
    return ms



def clone(state: GameState) -> GameState:
    """Shallow clone of a `GameState` suitable for search.

    All internal containers are copied so subsequent mutations are isolated.
    """
    c = GameState()
    c.edges = set(state.edges)
    c.edge_owner = dict(state.edge_owner)
    c.owner = dict(state.owner)
    c.scores = [state.scores[0], state.scores[1]]
    c.player = state.player
    return c


def apply_move(state: GameState, move: Edge) -> GameState:
    """Return a new state obtained by playing `move` in `state`."""
    ns = clone(state)
    a, b = move
    ns.play(a, b)
    return ns


def evaluate(state: GameState, ref_player: int) -> int:
    """Heuristic evaluation: score difference for `ref_player`.

    Args:
        state: Position to evaluate.
        ref_player: Player id for whom the value is computed.

    Returns:
        Signed integer: positive = good for `ref_player`.
    """
    me = ref_player
    opp = 1 - me
    return state.scores[me] - state.scores[opp]



def alphabeta(state: GameState, depth: int, alpha: int, beta: int, ref_player: int) -> Tuple[int, Optional[Edge]]:
    """Depth-limited alpha–beta minimax.

    Important: When a move completes a cell, `GameState.play` keeps the
    current player to move. This naturally yields consecutive MAX or MIN
    layers without special handling.

    Args:
        state: Current position.
        depth: Remaining depth (plies). Decrements by 1 for each edge drawn.
        alpha: Best value guaranteed for MAX so far.
        beta: Best value guaranteed for MIN so far.
        ref_player: The maximizing player id (root player).

    Returns:
        Tuple[value, best_move]: evaluation and a best move at this node.
    """
    if depth == 0 or state.is_terminal():
        return evaluate(state, ref_player), None

    best_move: Optional[Edge] = None
    moves = ordered_moves(state)

    if state.player == ref_player:
        value = -10**9
        for m in moves:
            child = apply_move(state, m)
            score, _ = alphabeta(child, depth - 1, alpha, beta, ref_player)
            if score > value:
                value = score
                best_move = m
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, best_move
    else:
        value = 10**9
        for m in moves:
            child = apply_move(state, m)
            score, _ = alphabeta(child, depth - 1, alpha, beta, ref_player)
            if score < value:
                value = score
                best_move = m
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value, best_move


def best_move(state: GameState, depth: int = 7) -> Edge:
    """Choose the best move for the current player in `state`.

    Args:
        state: Current position (whose `player` is to move).
        depth: Search depth in plies; 6–8 is sufficient for 3×3.

    Returns:
        Edge: Selected move.

    Notes:
        If `depth` is 0 or the position is terminal, a fallback legal move
        (if any) is returned.
    """
    value, mv = alphabeta(state, depth, -10**9, 10**9, ref_player=state.player)
    if mv is None:
        ms = all_moves(state)
        if not ms:
            raise RuntimeError("No legal moves available")
        return ms[0]
    return mv