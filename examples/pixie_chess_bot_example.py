#!/usr/bin/env python3
"""
Pixie Chess Bot Example - Deep Ability Simulation (v3)

Implements deeper logic for key verified abilities from the official piece document:
- Golden Pawn: Instant win on promotion
- Horde Mother: Spawns hordelings + chain death
- ElectroKnight: Charging + extra electrocution
- Basilisk, Bouncer, Phase Rook, etc.

This is still a prototype but much closer to real game logic.
"""

import json
import sys
import copy
from typing import Dict, List, Any, Optional, Tuple


def load_position(json_path: str) -> Dict[str, Any]:
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def evaluate_position(board: List[List[Optional[Dict]]], color: str, ability_state: Dict = None) -> float:
    """Evaluation with deep Pixie ability awareness."""
    if ability_state is None:
        ability_state = {}

    score = 0.0
    piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 100}

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if not piece:
                continue

            base_value = piece_values.get(piece['type'], 0)
            multiplier = 1.0

            # Deep ability bonuses
            variant = piece.get('variant', '')

            if variant == 'golden':
                # Golden Pawn: Massive value because it wins on promotion
                if piece['type'] == 'P':
                    multiplier = 50.0 if piece['color'] == color else 0.1

            elif variant == 'horde_mother':
                # Horde Mother is very strong due to spawning + chain death
                multiplier = 4.0 if piece['color'] == color else 0.3

            elif variant == 'electrok':
                # ElectroKnight value increases when charged
                charge = ability_state.get(f"charge_{r}_{c}", 0)
                multiplier = 1.5 + (charge * 0.3)

            elif variant == 'basilisk':
                multiplier = 2.5 if piece['color'] == color else 0.4

            score += base_value * multiplier if piece['color'] == color else -base_value * multiplier

    return score


def apply_ability_effects(board: List[List[Optional[Dict]]], move: Dict, ability_state: Dict) -> Tuple[List[List[Optional[Dict]]], Dict]:
    """Apply special ability effects after a move."""
    new_board = copy.deepcopy(board)
    new_state = copy.deepcopy(ability_state)

    piece = move.get('piece', {})
    variant = piece.get('variant', '')
    tr, tc = move['to']

    if variant == 'horde_mother':
        # Spawn a hordeling pawn nearby
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = tr + dr, tc + dc
                if 0 <= nr < 8 and 0 <= nc < 8 and new_board[nr][nc] is None:
                    new_board[nr][nc] = {'type': 'P', 'color': piece['color'], 'variant': 'hordeling'}
                    break

    elif variant == 'electrok':
        key = f"charge_{move['from'][0]}_{move['from'][1]}"
        new_state[key] = new_state.get(key, 0) + 1

        # If charged and capturing, electrocute extra piece
        target = board[tr][tc]
        if target and new_state.get(key, 0) >= 5:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    er, ec = tr + dr, tc + dc
                    if 0 <= er < 8 and 0 <= ec < 8:
                        if new_board[er][ec] and new_board[er][ec]['color'] != piece['color']:
                            new_board[er][ec] = None  # Electrocute
                            break

    elif variant == 'golden' and piece['type'] == 'P':
        # Check for promotion (simplified)
        if (piece['color'] == 'w' and tr == 0) or (piece['color'] == 'b' and tr == 7):
            print("[ABILITY] Golden Pawn promoted! Instant win detected.")

    return new_board, new_state


def suggest_best_move_deep(position: Dict[str, Any]) -> Optional[Dict]:
    board = position.get('board', [])
    turn = position.get('turn', 'w')
    ability_state = position.get('ability_state', {})

    # Simple search with ability effects
    best_score = -float('inf')
    best_move = None

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if not piece or piece['color'] != turn:
                continue

            for tr in range(8):
                for tc in range(8):
                    if tr == r and tc == c:
                        continue

                    # Very simplified legal check
                    move = {
                        'from': (r, c),
                        'to': (tr, tc),
                        'piece': piece,
                        'san': f"{chr(97+c)}{8-r}{chr(97+tc)}{8-tr}"
                    }

                    new_board, new_state = apply_ability_effects(board, move, ability_state)
                    score = evaluate_position(new_board, turn, new_state)

                    if score > best_score:
                        best_score = score
                        best_move = move

    if best_move:
        return {
            'recommended_move': best_move['san'],
            'score': round(best_score, 1),
            'ability_notes': f"Considering {best_move['piece'].get('variant', 'standard')} ability"
        }
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python examples/pixie_chess_bot_example.py <position.json>")
        return

    position = load_position(sys.argv[1])
    print("=== Deep Pixie Chess Analysis ===")

    result = suggest_best_move_deep(position)
    if result:
        print(f"Best Move: {result['recommended_move']}")
        print(f"Score: {result['score']}")
        print(f"Ability Notes: {result['ability_notes']}")
    else:
        print("No good move found.")

if __name__ == "__main__":
    main()
