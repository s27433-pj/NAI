"""Command-line interface for the Dots & Boxes (3×3) game.

This program allows the user to play either against another human
or against a simple AI opponent using minimax with alpha–beta pruning.

Game modes:
    1. Human vs Human
    2. Human vs AI

Move input formats (any of the following):
    - Orientation form:
        "h r c" → draws a horizontal edge from (r, c) to (r, c+1)
        "v r c" → draws a vertical edge from (r, c) to (r+1, c)
    - Two-point form:
        "r1 c1 r2 c2"  or  "r1,c1 r2,c2"
    - Quit:
        "q", "quit", or "exit"

Dependencies:
    - colorama (for colored terminal output)
    - game.py   (core game logic and rendering)
    - ai.py     (minimax AI with alpha–beta pruning)
"""

from __future__ import annotations
from typing import Optional, Tuple
from colorama import init as colorama_init, Fore, Style

colorama_init(autoreset=True)

from game import GameState, IllegalMove, DOTS, normalize_edge
from ai import best_move



def parse_move(text: str) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """Parse a user move into two grid points.

    Supported forms:
        - "h r c"  -> ((r,c), (r, c+1))
        - "v r c"  -> ((r,c), (r+1, c))
        - "r1 c1 r2 c2"
        - "r1,c1 r2,c2"
    Returns None on failure; caller shows an error and retries.
    """
    s = text.strip().lower()
    if not s:
        return None


    parts = s.split()
    if parts[0] in {"h", "v"}:
        if len(parts) != 3:
            return None
        try:
            r, c = int(parts[1]), int(parts[2])
        except ValueError:
            return None
        if parts[0] == "h":
            return (r, c), (r, c + 1)
        else:
            return (r, c), (r + 1, c)


    s = s.replace("(", " ").replace(")", " ").replace(",", " ")
    parts = s.split()
    if len(parts) == 4:
        try:
            r1, c1, r2, c2 = map(int, parts)
        except ValueError:
            return None
        return (r1, c1), (r2, c2)

    return None


def ask_human_move(state: GameState) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Prompt the user until a legal move is given; returns canonical edge."""
    while True:
        raw = input(Fore.YELLOW + "Twój ruch (np. 'h 0 0' lub '0 0 0 1', q=wyjście): " + Style.RESET_ALL).strip()
        if not raw:
            continue
        lr = raw.lower()
        if lr in {"q", "quit", "exit"}:
            raise SystemExit

        parsed = parse_move(lr)
        if parsed is None:
            print(Fore.RED + "Nie rozumiem. Użyj: 'h r c' | 'v r c' | 'r1 c1 r2 c2' | q" + Style.RESET_ALL)
            continue

        a, b = parsed

        r1, c1 = a
        r2, c2 = b
        if not (0 <= r1 < DOTS and 0 <= c1 < DOTS and 0 <= r2 < DOTS and 0 <= c2 < DOTS):
            print(Fore.RED + f"Punkt poza planszą (0..{DOTS - 1})." + Style.RESET_ALL);
            continue
        if a == b:
            print(Fore.RED + "Punkty nie mogą być identyczne." + Style.RESET_ALL);
            continue
        dr, dc = abs(r1 - r2), abs(c1 - c2)
        if (dr, dc) not in [(0, 1), (1, 0)]:
            print(Fore.RED + "Dozwolone tylko sąsiedztwo ortogonalne." + Style.RESET_ALL);
            continue
        if not state.is_edge_valid(a, b):
            print(Fore.RED + "Krawędź już istnieje lub jest nielegalna." + Style.RESET_ALL);
            continue


        if r1 == r2 and c1 > c2:
            a, b = b, a  # left->right
        if c1 == c2 and r1 < r2:
            a, b = b, a  # bottom->top

        return normalize_edge(a, b)



def play_human_vs_human() -> None:
    """Play Human vs Human until terminal state; prints board after each move."""
    state = GameState()
    print("Dots & Boxes (3x3) — Człowiek (P0) vs Człowiek (P1)\n")
    print(state.board_ascii())

    while not state.is_terminal():
        try:
            a, b = ask_human_move(state)
            state.play(a, b)
        except IllegalMove as e:
            print("Błąd:", e);
            continue
        except SystemExit:
            print("Do zobaczenia!");
            return
        print(state.board_ascii())

    _print_result(state)


def play_human_vs_ai(ai_player: int = 1, depth: int = 7) -> None:
    """Play Human vs AI. `ai_player` is 0 or 1 indicating AI's side."""
    state = GameState()
    print(f"Dots & Boxes (3x3) — Człowiek (P{1 - ai_player}) vs AI (P{ai_player})\n")
    print(state.board_ascii())


    _maybe_ai_turn(state, ai_player, depth)

    while not state.is_terminal():
        if state.player != ai_player:
            try:
                a, b = ask_human_move(state)
                state.play(a, b)
            except IllegalMove as e:
                print("Błąd:", e);
                continue
            except SystemExit:
                print("Do zobaczenia!");
                return
            print(state.board_ascii())
        _maybe_ai_turn(state, ai_player, depth)

    _print_result(state)


def _maybe_ai_turn(state: GameState, ai_player: int, depth: int) -> None:
    """While it's AI's turn, keep moving (extra moves after boxes continue)."""
    while not state.is_terminal() and state.player == ai_player:
        mv = best_move(state, depth=depth)
        print(f"\nRuch AI: {mv}")
        state.play(*mv)
        print(state.board_ascii())


def _print_result(state: GameState) -> None:
    """Print match result summary."""
    s0, s1 = state.scores
    print("\nKONIEC GRY!")
    if s0 > s1:
        print("Wygrał P0!")
    elif s1 > s0:
        print("Wygrał P1!")
    else:
        print("Remis.")



def main() -> None:
    """Ask for opponent type and start the selected mode."""
    print("Wybierz tryb:")
    print("  1) Człowiek vs Człowiek")
    print("  2) Człowiek vs AI")
    choice = input("Twój wybór [1/2]: ").strip()

    if choice == "1":
        play_human_vs_human()
        return


    who = input("Kto ma być AI? (0 / 1) [domyślnie 1]: ").strip() or "1"
    try:
        ai_player = 1 if who not in {"0", "1"} else int(who)
    except ValueError:
        ai_player = 1

    depth_in = input("Głębokość przeszukiwania AI [7]: ").strip()
    try:
        depth = int(depth_in) if depth_in else 7
    except ValueError:
        depth = 7

    play_human_vs_ai(ai_player=ai_player, depth=depth)


if __name__ == "__main__":
    main()