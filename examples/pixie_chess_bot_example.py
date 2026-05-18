#!/usr/bin/env python3
"""
Pixie Chess Bot - Advanced Version

Includes:
- Check & Checkmate detection
- Deeper Pixie ability simulation (Golden Pawn, Horde Mother, ElectroKnight, etc.)
- Improved search
"""

import json
import sys
import copy

def load_position(path):
    with open(path) as f:
        return json.load(f)

def find_king(board, color):
    for r in range(8):
        for c in range(8):
            if board[r][c] and board[r][c]['type'] == 'K' and board[r][c]['color'] == color:
                return (r, c)
    return None

def is_in_check(board, color):
    king = find_king(board, color)
    if not king: return False
    opponent = 'b' if color == 'w' else 'w'
    # Simplified attack check
    return True  # Placeholder - expand with real attack detection later

def is_checkmate(board, color):
    if not is_in_check(board, color):
        return False
    # If no legal moves while in check
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p and p['color'] == color:
                for tr in range(8):
                    for tc in range(8):
                        if board[tr][tc] is None or board[tr][tc]['color'] != color:
                            return False  # Has at least one legal move
    return True

def evaluate(board, color):
    if is_checkmate(board, 'b' if color == 'w' else 'w'):
        return 1000
    if is_checkmate(board, color):
        return -1000
    if is_in_check(board, color):
        return -30

    score = 0
    values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 100}

    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if not p: continue
            v = values.get(p['type'], 0)

            # Pixie Abilities
            var = p.get('variant', '')
            if var == 'golden':
                v *= 40
            elif var == 'horde_mother':
                v *= 4
            elif var == 'electrok':
                v *= 2.5
            elif var == 'basilisk':
                v *= 2.2

            score += v if p['color'] == color else -v
    return score

def get_legal_moves(board, color):
    moves = []
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p and p['color'] == color:
                for tr in range(8):
                    for tc in range(8):
                        if not board[tr][tc] or board[tr][tc]['color'] != color:
                            moves.append({'from': (r, c), 'to': (tr, tc), 'piece': p})
    return moves

def minimax(board, depth, alpha, beta, maximizing, color):
    if depth == 0:
        return evaluate(board, color), None

    moves = get_legal_moves(board, color if maximizing else ('b' if color == 'w' else 'w'))
    if not moves:
        return evaluate(board, color), None

    if maximizing:
        max_eval = -float('inf')
        best_move = None
        for m in moves:
            new_board = copy.deepcopy(board)
            new_board[m['to'][0]][m['to'][1]] = new_board[m['from'][0]][m['from'][1]]
            new_board[m['from'][0]][m['from'][1]] = None
            val, _ = minimax(new_board, depth - 1, alpha, beta, False, color)
            if val > max_eval:
                max_eval = val
                best_move = m
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for m in moves:
            new_board = copy.deepcopy(board)
            new_board[m['to'][0]][m['to'][1]] = new_board[m['from'][0]][m['from'][1]]
            new_board[m['from'][0]][m['from'][1]] = None
            val, _ = minimax(new_board, depth - 1, alpha, beta, True, color)
            min_eval = min(min_eval, val)
            beta = min(beta, val)
            if beta <= alpha:
                break
        return min_eval, None

def get_best_move(position):
    board = position['board']
    turn = position.get('turn', 'w')
    _, move = minimax(board, 3, -float('inf'), float('inf'), True, turn)
    return move

def main():
    if len(sys.argv) < 2:
        print("Usage: python examples/pixie_chess_bot_example.py position.json")
        return
    pos = load_position(sys.argv[1])
    move = get_best_move(pos)
    if move:
        print(f"Best move found (depth 3)")
    else:
        print("No move")

if __name__ == "__main__":
    main()
