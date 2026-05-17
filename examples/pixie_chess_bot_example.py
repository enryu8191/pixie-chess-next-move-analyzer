#!/usr/bin/env python3
"""
Pixie Chess Bot Integration Example (Enhanced)

Features:
- Load exported positions from the web analyzer
- Heuristic move generation with Pixie ability awareness
- Basic minimax search (depth 2-3) for better suggestions
- Extensible ability framework

This is a stepping stone toward a full production bot.

Usage:
    python examples/pixie_chess_bot_example.py path/to/position.json
"""

import json
import sys
import copy
from typing import Dict, List, Any, Optional, Tuple


def load_position(json_path: str) -> Dict[str, Any]:
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_piece_symbol(piece: Optional[Dict]) -> str:
    if not piece:
        return '.'
    symbols = {'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔'}
    base = symbols.get(piece.get('type', '?'), '?')
    if piece.get('variant'):
        return f"{base}({piece['variant']})"
    return base


def is_valid_position(row: int, col: int) -> bool:
    return 0 <= row < 8 and 0 <= col < 8


def generate_pseudo_legal_moves(board: List[List[Optional[Dict]]], color: str) -> List[Dict]:
    """
    Generate pseudo-legal moves. Includes basic Pixie variant awareness.
    This is intentionally simplified but extensible.
    """
    moves = []
    files = ['a','b','c','d','e','f','g','h']
    ranks = [8,7,6,5,4,3,2,1]

    directions = {
        'P': [(-1,0)] if color == 'w' else [(1,0)],
        'N': [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)],
        'B': [(-1,-1),(-1,1),(1,-1),(1,1)],
        'R': [(-1,0),(1,0),(0,-1),(0,1)],
        'Q': [(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)],
        'K': [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    }

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if not piece or piece.get('color') != color:
                continue

            ptype = piece['type']
            variant = piece.get('variant')

            # Long Knight variant
            if ptype == 'N' and variant == 'long':
                knight_deltas = [(-3,-1),(-3,1),(-1,-3),(-1,3),(1,-3),(1,3),(3,-1),(3,1)]
            else:
                knight_deltas = directions.get(ptype, [])

            if ptype in ['N', 'K'] or (ptype == 'N' and variant == 'long'):
                deltas = knight_deltas if ptype == 'N' else directions['K']
                for dr, dc in deltas:
                    nr, nc = r + dr, c + dc
                    if is_valid_position(nr, nc):
                        target = board[nr][nc]
                        if not target or target.get('color') != color:
                            moves.append({
                                'from': (r, c), 'to': (nr, nc),
                                'san': f"{files[c]}{ranks[r]}{files[nc]}{ranks[nr]}",
                                'piece': piece, 'variant': variant
                            })
            else:
                # Sliding pieces + Pawn
                dirs = directions.get(ptype, [])
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    while is_valid_position(nr, nc):
                        target = board[nr][nc]
                        if target:
                            if target.get('color') != color:
                                moves.append({'from': (r, c), 'to': (nr, nc), 'san': f"{files[c]}{ranks[r]}{files[nc]}{ranks[nr]}", 'piece': piece, 'variant': variant})
                            break
                        else:
                            moves.append({'from': (r, c), 'to': (nr, nc), 'san': f"{files[c]}{ranks[r]}{files[nc]}{ranks[nr]}", 'piece': piece, 'variant': variant})
                        if ptype == 'P':  # Pawns only move one square forward
                            break
                        nr += dr
                        nc += dc

    return moves


def evaluate_position(board: List[List[Optional[Dict]]], color: str) -> float:
    """Simple material + position evaluation with Pixie ability bonuses."""
    score = 0.0
    values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 100}

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if not piece:
                continue
            val = values.get(piece['type'], 0)
            if piece['color'] == color:
                score += val
            else:
                score -= val

            # Pixie ability positional bonuses
            if piece.get('variant') == 'freeze':
                score += 0.5 if piece['color'] == color else -0.5
            if piece.get('variant') == 'push':
                score += 0.4 if piece['color'] == color else -0.4

    return score


def apply_move(board: List[List[Optional[Dict]]], move: Dict) -> List[List[Optional[Dict]]]:
    new_board = copy.deepcopy(board)
    fr, fc = move['from']
    tr, tc = move['to']
    new_board[tr][tc] = new_board[fr][fc]
    new_board[fr][fc] = None
    return new_board


def minimax(board: List[List[Optional[Dict]]], depth: int, maximizing: bool, color: str, alpha: float = -float('inf'), beta: float = float('inf')) -> Tuple[float, Optional[Dict]]:
    """Basic minimax with alpha-beta pruning. Depth 2-3 is practical for demo."""
    if depth == 0:
        return evaluate_position(board, color), None

    current_color = color if maximizing else ('b' if color == 'w' else 'w')
    moves = generate_pseudo_legal_moves(board, current_color)

    if not moves:
        return evaluate_position(board, color), None

    best_move = None
    if maximizing:
        max_eval = -float('inf')
        for move in moves:
            new_board = apply_move(board, move)
            eval_score, _ = minimax(new_board, depth-1, False, color, alpha, beta)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            new_board = apply_move(board, move)
            eval_score, _ = minimax(new_board, depth-1, True, color, alpha, beta)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move


def suggest_best_move_with_minimax(position: Dict[str, Any], depth: int = 2) -> Optional[Dict]:
    board = position.get('board', [])
    turn = position.get('turn', 'w')

    _, best_move = minimax(board, depth, True, turn)

    if not best_move:
        # Fallback to heuristic
        moves = generate_pseudo_legal_moves(board, turn)
        if not moves:
            return None
        best_move = max(moves, key=lambda m: 10 if m.get('variant') else 1)

    reasoning = "Minimax search (depth " + str(depth) + ")"
    if best_move.get('variant'):
        reasoning += f" | Considering {best_move['variant']} ability"

    return {
        'recommended_move': best_move['san'],
        'reasoning': reasoning,
        'variant_used': best_move.get('variant'),
        'depth_searched': depth
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python examples/pixie_chess_bot_example.py <position.json>")
        sys.exit(1)

    position = load_position(sys.argv[1])
    print("=== Pixie Chess Position Loaded ===")
    print(f"Turn: {position.get('turn', 'w').upper()}")

    suggestion = suggest_best_move_with_minimax(position, depth=2)
    if suggestion:
        print(f"\nBest move (minimax): {suggestion['recommended_move']}")
        print(f"Reasoning: {suggestion['reasoning']}")
        if suggestion.get('variant_used'):
            print(f"Pixie ability involved: {suggestion['variant_used']}")
    else:
        print("No moves found.")

if __name__ == "__main__":
    main()
